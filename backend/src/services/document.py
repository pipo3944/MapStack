"""
ドキュメントリビジョン管理サービス

このモジュールは、ドキュメントおよびそのリビジョン管理に関連する機能を提供します。
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
from uuid import UUID, uuid4

from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from ..db.models.document import Document, DocumentRevision, NodeDocumentLink
from ..db.models.roadmap import RoadmapNode
from ..api.v1.schemas.document import DocumentContentBase, DocumentSectionBase, DocumentRevisionDiff

logger = logging.getLogger(__name__)


class VersionUtility:
    """セマンティックバージョン管理のユーティリティクラス"""

    @staticmethod
    def parse_version(version: str) -> Tuple[int, int, int]:
        """
        バージョン文字列をメジャー、マイナー、パッチに分解する

        Args:
            version: "1.2.3" 形式のバージョン文字列

        Returns:
            (メジャー, マイナー, パッチ)のタプル
        """
        # バージョン形式確認（x.y.z）
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            raise ValueError(f"バージョン文字列の形式が無効です: {version}")

        parts = version.split('.')
        return int(parts[0]), int(parts[1]), int(parts[2])

    @staticmethod
    def format_version(major: int, minor: int, patch: int) -> str:
        """
        メジャー、マイナー、パッチからバージョン文字列を生成する

        Args:
            major: メジャーバージョン
            minor: マイナーバージョン
            patch: パッチバージョン

        Returns:
            "x.y.z" 形式のバージョン文字列
        """
        return f"{major}.{minor}.{patch}"

    @staticmethod
    def increment_version(current_version: str, version_type: str = "minor") -> str:
        """
        現在のバージョンをインクリメントする

        Args:
            current_version: 現在のバージョン文字列
            version_type: インクリメントのタイプ ("major", "minor", "patch")

        Returns:
            インクリメントされたバージョン文字列
        """
        major, minor, patch = VersionUtility.parse_version(current_version)

        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            raise ValueError(f"無効なバージョンタイプ: {version_type}")

        return VersionUtility.format_version(major, minor, patch)

    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """
        2つのバージョンを比較する

        Args:
            version1: 比較する最初のバージョン
            version2: 比較する2番目のバージョン

        Returns:
            -1 (version1 < version2), 0 (version1 == version2), 1 (version1 > version2)
        """
        v1_parts = VersionUtility.parse_version(version1)
        v2_parts = VersionUtility.parse_version(version2)

        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1
        else:
            return 0

    @staticmethod
    def is_valid_version(version: str) -> bool:
        """
        バージョン文字列が有効なセマンティックバージョンかどうかを確認する

        Args:
            version: 確認するバージョン文字列

        Returns:
            有効な場合はTrue、そうでない場合はFalse
        """
        try:
            VersionUtility.parse_version(version)
            return True
        except ValueError:
            return False


class DocumentDiffUtility:
    """ドキュメントリビジョン間の差分計算ユーティリティ"""

    @staticmethod
    def compute_section_diff(old_sections: List[Dict], new_sections: List[Dict]) -> Dict[str, List]:
        """
        2つのセクションリストの差分を計算する

        Args:
            old_sections: 古いバージョンのセクションリスト
            new_sections: 新しいバージョンのセクションリスト

        Returns:
            追加/削除/変更されたセクションを含む辞書
        """
        # タイトルでセクションをマップ化
        old_map = {section['title']: section for section in old_sections}
        new_map = {section['title']: section for section in new_sections}

        # 追加されたセクション
        added = [section for title, section in new_map.items() if title not in old_map]

        # 削除されたセクション
        removed = [section for title, section in old_map.items() if title not in new_map]

        # 変更されたセクション
        modified = []
        for title in set(old_map.keys()) & set(new_map.keys()):
            if old_map[title]['content'] != new_map[title]['content']:
                modified.append({
                    'title': title,
                    'old_content': old_map[title]['content'],
                    'new_content': new_map[title]['content']
                })

        return {
            'added': added,
            'removed': removed,
            'modified': modified
        }

    @staticmethod
    def create_revision_diff(old_content: Dict, new_content: Dict) -> DocumentRevisionDiff:
        """
        2つのリビジョン間の差分をDocumentRevisionDiffとして生成する

        Args:
            old_content: 古いバージョンのコンテンツ
            new_content: 新しいバージョンのコンテンツ

        Returns:
            リビジョン差分オブジェクト
        """
        # 両方のセクションを取得
        old_sections = old_content.get('sections', [])
        new_sections = new_content.get('sections', [])

        # 差分計算
        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        # Pydanticモデルに変換
        sections_added = [DocumentSectionBase(**section) for section in diff['added']]
        sections_removed = [DocumentSectionBase(**section) for section in diff['removed']]

        return DocumentRevisionDiff(
            from_version="",  # 呼び出し側で設定
            to_version="",    # 呼び出し側で設定
            sections_added=sections_added,
            sections_removed=sections_removed,
            sections_modified=diff['modified']
        )


class DocumentStorageService:
    """ドキュメントコンテンツのストレージサービス"""

    def __init__(self, base_storage_path: str = "storage"):
        """
        Args:
            base_storage_path: ストレージのベースディレクトリ
        """
        self.base_path = base_storage_path

    def get_document_path(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージパスを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージパス
        """
        return os.path.join(self.base_path, "documents", str(document_id), f"{version}.json")

    def get_storage_key(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージキーを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        return os.path.join("documents", str(document_id), f"{version}.json")

    def save_content(self, content: Dict, document_id: Union[UUID, str], version: str) -> str:
        """
        コンテンツをファイルに保存する

        Args:
            content: 保存するコンテンツデータ
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        # ドキュメント保存ディレクトリ
        doc_dir = os.path.dirname(self.get_document_path(document_id, version))

        # ディレクトリが存在しない場合は作成
        os.makedirs(doc_dir, exist_ok=True)

        # ファイルパス
        file_path = self.get_document_path(document_id, version)

        # JSONとして保存
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        # ストレージキーを返す
        return self.get_storage_key(document_id, version)

    def load_content(self, storage_key: str) -> Dict:
        """
        ストレージキーからコンテンツを読み込む

        Args:
            storage_key: コンテンツのストレージキー

        Returns:
            読み込まれたコンテンツデータ
        """
        file_path = os.path.join(self.base_path, storage_key)

        # ファイルが存在しない場合はエラー
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"コンテンツファイルが見つかりません: {file_path}")

        # JSONとして読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def delete_content(self, storage_key: str) -> bool:
        """
        ストレージキーのコンテンツを削除する

        Args:
            storage_key: 削除するコンテンツのストレージキー

        Returns:
            削除に成功した場合はTrue
        """
        file_path = os.path.join(self.base_path, storage_key)

        # ファイルが存在する場合は削除
        if os.path.exists(file_path):
            os.remove(file_path)
            return True

        return False

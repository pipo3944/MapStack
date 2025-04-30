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
from ..config.settings import get_settings
from .storage import get_storage_service, StorageService

logger = logging.getLogger(__name__)
settings = get_settings()


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


class DocumentService:
    """ドキュメントコンテンツの管理サービス"""

    def __init__(self):
        """
        ストレージサービスを初期化する
        """
        self.storage = get_storage_service()

    async def save_content(self, content: Dict, document_id: Union[UUID, str], version: str) -> str:
        """
        コンテンツを保存する

        Args:
            content: 保存するコンテンツデータ
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        return await self.storage.save_content(content, document_id, version)

    async def load_content(self, storage_key: str) -> Dict:
        """
        コンテンツを読み込む

        Args:
            storage_key: ストレージキー

        Returns:
            読み込んだコンテンツデータ

        Raises:
            FileNotFoundError: 指定されたキーのコンテンツが見つからない場合
        """
        return await self.storage.load_content(storage_key)

    async def delete_content(self, storage_key: str) -> bool:
        """
        コンテンツを削除する

        Args:
            storage_key: ストレージキー

        Returns:
            削除が成功した場合はTrue、それ以外はFalse
        """
        return await self.storage.delete_content(storage_key)

    async def list_document_versions(self, document_id: Union[UUID, str]) -> List[str]:
        """
        ドキュメントの全バージョンのストレージキーを取得する

        Args:
            document_id: ドキュメントID

        Returns:
            ストレージキーのリスト
        """
        prefix = f"documents/{document_id}"
        keys = await self.storage.list_contents(prefix)
        return keys

    def get_storage_key(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージキーを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        return self.storage.get_storage_key(document_id, version)


# 後方互換性のためのエイリアス
DocumentStorageService = DocumentService

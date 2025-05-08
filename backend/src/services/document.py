"""
ドキュメントリビジョン管理サービス

このモジュールは、ドキュメントリビジョン管理に関する主要なビジネスロジックを提供します。
"""

import os
import json
import re
import logging
from datetime import datetime, UTC
from typing import List, Dict, Any, Optional, Tuple, Union
from uuid import UUID, uuid4

from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload, selectinload

from ..db.models.document import Document, DocumentRevision, NodeDocumentLink
from ..db.models.roadmap import RoadmapNode
from ..api.v1.schemas.document import DocumentContentBase, DocumentSectionBase, DocumentRevisionDiff, SectionDiff, ModifiedSection, DocumentSearchParams
from ..config.settings import get_settings
from .storage import get_storage_service, StorageService

logger = logging.getLogger(__name__)
settings = get_settings()


class VersionUtility:
    """バージョン番号管理ユーティリティ"""

    @staticmethod
    def parse_version(version: str) -> Tuple[int, int, int]:
        """
        バージョン文字列をパースして、メジャー、マイナー、パッチバージョンに分割する

        例: "1.2.3" -> (1, 2, 3)
        """
        parts = version.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version}. Expected format: X.Y.Z")

        try:
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])
            return major, minor, patch
        except ValueError:
            raise ValueError(f"Version parts must be integers: {version}")

    @staticmethod
    def format_version(major: int, minor: int, patch: int) -> str:
        """
        メジャー、マイナー、パッチバージョンをバージョン文字列にフォーマットする

        例: (1, 2, 3) -> "1.2.3"
        """
        return f"{major}.{minor}.{patch}"

    @staticmethod
    def increment_version(version: str, version_type: str) -> str:
        """
        指定されたバージョンタイプに基づいてバージョンをインクリメントする

        Args:
            version: 現在のバージョン（例: "1.2.3"）
            version_type: バージョンタイプ（"major", "minor", "patch"）

        Returns:
            インクリメントされたバージョン
        """
        major, minor, patch = VersionUtility.parse_version(version)

        if version_type == "major":
            return VersionUtility.format_version(major + 1, 0, 0)
        elif version_type == "minor":
            return VersionUtility.format_version(major, minor + 1, 0)
        elif version_type == "patch":
            return VersionUtility.format_version(major, minor, patch + 1)
        else:
            raise ValueError(f"Invalid version type: {version_type}. Expected: major, minor, or patch")

    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """
        2つのバージョンを比較する

        Returns:
            -1: version1 < version2
            0: version1 == version2
            1: version1 > version2
        """
        major1, minor1, patch1 = VersionUtility.parse_version(version1)
        major2, minor2, patch2 = VersionUtility.parse_version(version2)

        if major1 < major2:
            return -1
        elif major1 > major2:
            return 1

        if minor1 < minor2:
            return -1
        elif minor1 > minor2:
            return 1

        if patch1 < patch2:
            return -1
        elif patch1 > patch2:
            return 1

        return 0

    @staticmethod
    def is_valid_version(version: str) -> bool:
        """バージョン文字列が有効かチェックする"""
        try:
            VersionUtility.parse_version(version)
            return True
        except ValueError:
            return False

    @staticmethod
    def determine_version_type(old_content: Dict[str, Any], new_content: Dict[str, Any]) -> str:
        """
        コンテンツの変更に基づいて適切なバージョンタイプ（major/minor/patch）を決定する

        基本ルール:
        - タイトルの変更: minor
        - セクションの追加/削除: minor
        - 既存セクションの内容変更 (50文字以上): minor
        - 既存セクションの内容変更 (50文字未満): patch
        - その他の小さな変更: patch

        Returns:
            "major", "minor", "patch" のいずれか
        """
        # タイトルの変更をチェック
        if old_content.get("title") != new_content.get("title"):
            return "minor"

        # セクション構成の変更を計算
        old_sections = old_content.get("sections", [])
        new_sections = new_content.get("sections", [])

        # セクション数の変化があれば minor
        if len(old_sections) != len(new_sections):
            return "minor"

        # セクションの変更を詳細に分析
        old_section_map = {s.get("title"): s.get("content", "") for s in old_sections}
        new_section_map = {s.get("title"): s.get("content", "") for s in new_sections}

        # タイトルの異なるセクションがあれば minor
        if set(old_section_map.keys()) != set(new_section_map.keys()):
            return "minor"

        # 内容変更の規模を評価
        significant_changes = False
        for title, old_content in old_section_map.items():
            new_content = new_section_map.get(title, "")
            # 内容が変わっている場合
            if old_content != new_content:
                # コンテンツの差が大きい場合
                content_diff = abs(len(old_content) - len(new_content))
                if content_diff > 50:
                    return "minor"
                significant_changes = True

        # 小さな変更が1つ以上あれば patch
        if significant_changes:
            return "patch"

        # 実質的な変更がない場合はパッチとして処理
        return "patch"


class DocumentDiffUtility:
    """ドキュメントバージョン間の差分計算ユーティリティ"""

    @staticmethod
    def compute_section_diff(old_sections: List[Dict[str, Any]], new_sections: List[Dict[str, Any]]) -> Dict[str, List]:
        """
        2つのセクションリスト間の差分を計算する

        Returns:
            {
                "added": [追加されたセクション, ...],
                "removed": [削除されたセクション, ...],
                "modified": [変更されたセクション, ...]
            }
        """
        old_section_map = {s["title"]: s["content"] for s in old_sections}
        new_section_map = {s["title"]: s["content"] for s in new_sections}

        # 追加されたセクション
        added = [
            {"title": title, "content": content}
            for title, content in new_section_map.items()
            if title not in old_section_map
        ]

        # 削除されたセクション
        removed = [
            {"title": title, "content": content}
            for title, content in old_section_map.items()
            if title not in new_section_map
        ]

        # 変更されたセクション
        modified = [
            {
                "title": title,
                "old_content": old_section_map[title],
                "new_content": new_section_map[title]
            }
            for title in set(old_section_map.keys()) & set(new_section_map.keys())
            if old_section_map[title] != new_section_map[title]
        ]

        return {
            "added": added,
            "removed": removed,
            "modified": modified
        }

    @staticmethod
    def create_revision_diff(old_content: Dict[str, Any], new_content: Dict[str, Any]) -> DocumentRevisionDiff:
        """
        2つのコンテンツバージョン間の差分を計算してPydanticモデルとして返す
        """
        old_sections = old_content.get("sections", [])
        new_sections = new_content.get("sections", [])

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        # Pydanticモデルに変換
        sections_added = [
            SectionDiff(title=section["title"], content=section["content"])
            for section in diff["added"]
        ]

        sections_removed = [
            SectionDiff(title=section["title"], content=section["content"])
            for section in diff["removed"]
        ]

        sections_modified = [
            ModifiedSection(
                title=section["title"],
                old_content=section["old_content"],
                new_content=section["new_content"]
            ).model_dump()
            for section in diff["modified"]
        ]

        return DocumentRevisionDiff(
            from_version="",  # 呼び出し側で設定
            to_version="",  # 呼び出し側で設定
            sections_added=sections_added,
            sections_removed=sections_removed,
            sections_modified=sections_modified
        )


class DocumentService:
    """ドキュメントとリビジョン管理サービス"""

    def __init__(self):
        """初期化"""
        self.storage_service = get_storage_service()

    # ストレージ関連のメソッド
    async def save_content(self, content: Dict[str, Any], document_id: Union[str, UUID], version: str) -> str:
        """コンテンツをストレージに保存する"""
        storage_key = await self.storage_service.save_content(content, str(document_id), version)
        return storage_key

    async def load_content(self, storage_key: str) -> Dict[str, Any]:
        """ストレージからコンテンツを読み込む"""
        content = await self.storage_service.load_content(storage_key)
        return content

    async def delete_content(self, storage_key: str) -> bool:
        """ストレージからコンテンツを削除する"""
        result = await self.storage_service.delete_content(storage_key)
        return result

    async def list_document_versions(self, document_id: Union[str, UUID]) -> List[str]:
        """ドキュメントの全バージョンのストレージキーをリストアップする"""
        prefix = f"documents/{document_id}"
        storage_keys = await self.storage_service.list_contents(prefix)
        return storage_keys

    def get_storage_key(self, document_id: Union[str, UUID], version: str) -> str:
        """ストレージキーを生成する"""
        return self.storage_service.get_storage_key(str(document_id), version)

    # ドキュメント操作メソッド
    async def get_document(self, db: AsyncSession, document_id: UUID) -> Optional[Document]:
        """ドキュメントを取得する（リビジョンも事前ロード）"""
        query = select(Document).where(Document.id == document_id).options(selectinload(Document.revisions))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_document_with_revisions(self, db: AsyncSession, document_id: UUID) -> Optional[Document]:
        """リビジョン情報付きでドキュメントを取得する"""
        query = (
            select(Document)
            .where(Document.id == document_id)
            .options(selectinload(Document.revisions))
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_latest_revision(self, db: AsyncSession, document_id: UUID) -> Optional[DocumentRevision]:
        """最新のリビジョンを取得する"""
        query = (
            select(DocumentRevision)
            .where(DocumentRevision.document_id == document_id)
            .order_by(desc(DocumentRevision.created_at))
            .limit(1)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_revision_by_version(self, db: AsyncSession, document_id: UUID, version: str) -> Optional[DocumentRevision]:
        """指定バージョンのリビジョンを取得する"""
        query = (
            select(DocumentRevision)
            .where(
                DocumentRevision.document_id == document_id,
                DocumentRevision.version == version
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def search_documents(
        self,
        db: AsyncSession,
        params: DocumentSearchParams
    ) -> Tuple[List[Document], int]:
        """ドキュメントを検索する"""
        # 基本クエリ
        query = select(Document)
        count_query = select(func.count(Document.id))

        # 検索条件の適用
        if params.title_contains:
            title_filter = Document.title.ilike(f"%{params.title_contains}%")
            query = query.where(title_filter)
            count_query = count_query.where(title_filter)

        if params.node_id:
            # ノードにリンクされたドキュメントのみを取得
            node_filter = Document.id.in_(
                select(NodeDocumentLink.document_id)
                .where(NodeDocumentLink.node_id == params.node_id)
            )
            query = query.where(node_filter)
            count_query = count_query.where(node_filter)

        # 合計件数を取得
        count_result = await db.execute(count_query)
        total = count_result.scalar_one()

        # ソートの適用
        if params.sort_by == "title":
            sort_column = Document.title
        elif params.sort_by == "created_at":
            sort_column = Document.created_at
        else:  # デフォルトはupdated_at
            sort_column = Document.updated_at

        if params.sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # ページネーション
        query = query.offset((params.page - 1) * params.per_page).limit(params.per_page)

        # クエリ実行
        result = await db.execute(query)
        documents = result.scalars().all()

        return documents, total

    async def get_node_documents(self, db: AsyncSession, node_id: UUID) -> Tuple[Optional[RoadmapNode], List[Document]]:
        """指定されたノードに関連付けられたドキュメント一覧を取得する"""
        # ノードの取得
        node_query = select(RoadmapNode).where(RoadmapNode.id == node_id)
        node_result = await db.execute(node_query)
        node = node_result.scalar_one_or_none()

        if not node:
            return None, []

        # 関連ドキュメントの取得
        docs_query = (
            select(Document)
            .join(NodeDocumentLink, NodeDocumentLink.document_id == Document.id)
            .where(NodeDocumentLink.node_id == node_id)
            .order_by(NodeDocumentLink.order_position)
        )
        docs_result = await db.execute(docs_query)
        documents = docs_result.scalars().all()

        return node, documents

    async def create_document(
        self,
        db: AsyncSession,
        title: str,
        description: Optional[str],
        content: Dict[str, Any],
        created_by: Optional[UUID] = None
    ) -> Document:
        """新規ドキュメントを作成する"""
        now = datetime.now(UTC)

        # ドキュメントレコードの作成
        document = Document(
            id=uuid4(),
            title=title,
            description=description,
            created_at=now,
            updated_at=now
        )
        db.add(document)

        # 初期リビジョンの作成
        initial_version = "1.0.0"
        storage_key = self.get_storage_key(document.id, initial_version)

        revision = DocumentRevision(
            id=uuid4(),
            document_id=document.id,
            version=initial_version,
            storage_key=storage_key,
            created_by=created_by,
            created_at=now
        )
        db.add(revision)

        # DBに保存
        await db.flush()

        # コンテンツをストレージに保存
        await self.save_content(content, document.id, initial_version)

        return document

    async def update_document(
        self,
        db: AsyncSession,
        document_id: UUID,
        content: Dict[str, Any],
        version_type: str = "minor",
        change_summary: Optional[str] = None,
        created_by: Optional[UUID] = None
    ) -> Tuple[Document, DocumentRevision]:
        """ドキュメントを更新して新しいリビジョンを作成する"""
        # ドキュメントとその最新リビジョンを取得
        document = await self.get_document(db, document_id)
        if not document:
            raise ValueError(f"Document with ID {document_id} not found")

        latest_revision = await self.get_latest_revision(db, document_id)
        if not latest_revision:
            raise ValueError(f"No revisions found for document {document_id}")

        # 最新のコンテンツを取得
        latest_content = await self.load_content(latest_revision.storage_key)

        # 内容に基づいてバージョンタイプを自動決定（明示的に指定されていない場合）
        if version_type == "auto":
            version_type = VersionUtility.determine_version_type(latest_content, content)

        # 新しいバージョン番号の生成
        new_version = VersionUtility.increment_version(latest_revision.version, version_type)

        # 新しいストレージキーの生成
        storage_key = self.get_storage_key(document_id, new_version)

        # 新しいリビジョンレコードの作成
        now = datetime.now(UTC)
        new_revision = DocumentRevision(
            id=uuid4(),
            document_id=document_id,
            version=new_version,
            storage_key=storage_key,
            change_summary=change_summary,
            created_by=created_by,
            created_at=now
        )
        db.add(new_revision)

        # ドキュメントの更新日時を更新
        document.updated_at = now
        if "title" in content:
            document.title = content["title"]

        await db.flush()

        # コンテンツをストレージに保存
        await self.save_content(content, document_id, new_version)

        return document, new_revision

    async def link_node_document(
        self,
        db: AsyncSession,
        node_id: UUID,
        document_id: UUID,
        relation_type: str = "primary",
        order_position: Optional[int] = None
    ) -> NodeDocumentLink:
        """ノードとドキュメントを関連付ける"""
        # ノードとドキュメントの存在確認
        node_query = select(RoadmapNode).where(RoadmapNode.id == node_id)
        node_result = await db.execute(node_query)
        node = node_result.scalar_one_or_none()

        if not node:
            raise ValueError(f"Node with ID {node_id} not found")

        doc_query = select(Document).where(Document.id == document_id)
        doc_result = await db.execute(doc_query)
        document = doc_result.scalar_one_or_none()

        if not document:
            raise ValueError(f"Document with ID {document_id} not found")

        # 既存の関連付けをチェック
        existing_query = select(NodeDocumentLink).where(
            NodeDocumentLink.node_id == node_id,
            NodeDocumentLink.document_id == document_id
        )
        existing_result = await db.execute(existing_query)
        existing_link = existing_result.scalar_one_or_none()

        if existing_link:
            # 既存の関連付けを更新
            if relation_type:
                existing_link.relation_type = relation_type
            if order_position is not None:
                existing_link.order_position = order_position

            await db.flush()
            return existing_link

        # 新しい関連付けを作成
        if order_position is None:
            # 最大の順序位置を取得
            max_order_query = select(func.max(NodeDocumentLink.order_position)).where(NodeDocumentLink.node_id == node_id)
            max_order_result = await db.execute(max_order_query)
            max_order = max_order_result.scalar_one_or_none() or 0
            order_position = max_order + 100  # 100単位で余裕を持たせる

        link = NodeDocumentLink(
            id=uuid4(),
            node_id=node_id,
            document_id=document_id,
            relation_type=relation_type,
            order_position=order_position,
            created_at=datetime.now(UTC)
        )
        db.add(link)
        await db.flush()

        return link

    async def unlink_node_document(self, db: AsyncSession, node_id: UUID, document_id: UUID) -> bool:
        """ノードとドキュメントの関連付けを解除する"""
        # 関連付けを検索
        query = select(NodeDocumentLink).where(
            NodeDocumentLink.node_id == node_id,
            NodeDocumentLink.document_id == document_id
        )
        result = await db.execute(query)
        link = result.scalar_one_or_none()

        if not link:
            return False

        # 関連付けを削除
        await db.delete(link)
        await db.flush()

        return True


# 後方互換性のためのエイリアス
DocumentStorageService = DocumentService

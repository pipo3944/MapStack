"""
ドキュメントリビジョン管理のAPIスキーマ定義

このモジュールは、ドキュメントとリビジョン関連のAPIリクエスト・レスポンスのスキーマを定義します。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator

from .common import PaginationParams, PaginatedResponse
import json


# コンテンツ関連のスキーマ
class DocumentSectionBase(BaseModel):
    """ドキュメントセクション基本クラス"""
    title: str
    content: str


class DocumentContentBase(BaseModel):
    """ドキュメントコンテンツの基本構造"""
    title: str
    sections: List[DocumentSectionBase]


# リクエスト・レスポンススキーマ
class DocumentBase(BaseModel):
    """ドキュメント基本情報"""
    title: str
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    """ドキュメント作成リクエスト"""
    content: DocumentContentBase  # 初期リビジョンのコンテンツ


class DocumentResponse(DocumentBase):
    """ドキュメント情報レスポンス"""
    id: UUID
    created_at: datetime
    updated_at: datetime


class DocumentRevisionBase(BaseModel):
    """リビジョン基本情報"""
    version: str
    change_summary: Optional[str] = None
    created_at: datetime


class DocumentRevisionCreate(BaseModel):
    """リビジョン作成リクエスト"""
    content: DocumentContentBase
    change_summary: Optional[str] = None
    version_type: str = "minor"  # "major", "minor", "patch"


class DocumentRevisionResponse(DocumentRevisionBase):
    """リビジョン情報レスポンス"""
    id: UUID
    document_id: UUID
    created_by: Optional[UUID] = None


class DocumentRevisionContentResponse(DocumentRevisionResponse):
    """リビジョンコンテンツ付きレスポンス"""
    content: DocumentContentBase


class DocumentWithRevisionsResponse(DocumentResponse):
    """リビジョン履歴付きドキュメント情報レスポンス"""
    revisions: List[DocumentRevisionResponse]


class DocumentDetailResponse(DocumentResponse):
    """最新リビジョン情報付きドキュメント詳細レスポンス"""
    latest_revision: DocumentRevisionResponse


class NodeDocumentLinkBase(BaseModel):
    """ノードとドキュメントのリンク基本情報"""
    relation_type: str = "primary"
    order_position: Optional[int] = None


class NodeDocumentLinkCreate(NodeDocumentLinkBase):
    """ノードとドキュメントのリンク作成リクエスト"""
    document_id: UUID


class NodeDocumentLinkResponse(NodeDocumentLinkBase):
    """ノードとドキュメントのリンク情報レスポンス"""
    id: UUID
    node_id: UUID
    document_id: UUID
    created_at: datetime


class NodeDocumentsResponse(BaseModel):
    """ノードに関連するドキュメント一覧レスポンス"""
    node_id: UUID
    node_title: str
    documents: List[DocumentResponse]


# ドキュメント一覧取得用
class DocumentSearchParams(PaginationParams):
    """ドキュメント検索パラメータ"""
    title_contains: Optional[str] = None
    node_id: Optional[UUID] = None
    sort_by: str = "updated_at"
    sort_order: str = "desc"


class PaginatedDocumentResponse(PaginatedResponse):
    """ページネーション付きドキュメント一覧レスポンス"""
    items: List[DocumentResponse]


# バージョン差分用
class DocumentRevisionDiff(BaseModel):
    """リビジョン間の差分情報"""
    from_version: str
    to_version: str
    sections_added: List[DocumentSectionBase] = []
    sections_removed: List[DocumentSectionBase] = []
    sections_modified: List[Dict[str, Any]] = []

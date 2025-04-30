"""
ドキュメントリビジョン関連のデータベーススキーマ

このモジュールはデータベースとの連携に使用されるPydanticモデルを定義します。
API用のスキーマは別途 api/v1/schemas/document.py に定義されています。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    """ドキュメントの基本情報"""
    title: str
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    """ドキュメント作成用スキーマ"""
    pass


class DocumentUpdate(BaseModel):
    """ドキュメント更新用スキーマ"""
    title: Optional[str] = None
    description: Optional[str] = None


class Document(DocumentBase):
    """ドキュメントDBスキーマ"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DocumentRevisionBase(BaseModel):
    """ドキュメントリビジョンの基本情報"""
    document_id: UUID
    version: str
    storage_key: str
    change_summary: Optional[str] = None
    created_by: Optional[UUID] = None


class DocumentRevisionCreate(BaseModel):
    """ドキュメントリビジョン作成用スキーマ"""
    document_id: UUID
    version: str
    content: Dict[str, Any]  # 実際のコンテンツJSONデータ
    change_summary: Optional[str] = None
    created_by: Optional[UUID] = None


class DocumentRevision(DocumentRevisionBase):
    """ドキュメントリビジョンDBスキーマ"""
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class NodeDocumentLinkBase(BaseModel):
    """ノードとドキュメントのリンク基本情報"""
    node_id: UUID
    document_id: UUID
    order_position: Optional[int] = None
    relation_type: str = "primary"


class NodeDocumentLinkCreate(NodeDocumentLinkBase):
    """ノードとドキュメントのリンク作成用スキーマ"""
    pass


class NodeDocumentLink(NodeDocumentLinkBase):
    """ノードとドキュメントのリンクDBスキーマ"""
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class DocumentWithRevisions(Document):
    """リビジョン情報を含むドキュメントスキーマ"""
    revisions: List[DocumentRevision]


class NodeWithDocuments(BaseModel):
    """ドキュメント情報を含むノードスキーマ"""
    id: UUID
    handle: str
    title: str
    node_type: str
    documents: List[Document]

    class Config:
        orm_mode = True

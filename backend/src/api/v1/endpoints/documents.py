"""
ドキュメントリビジョン管理のAPIエンドポイント

このモジュールは、ドキュメントとリビジョン管理に関するAPIエンドポイントを定義します。
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.main import get_db
from src.db.models import Document, DocumentRevision, NodeDocumentLink, RoadmapNode
from src.api.v1.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentDetailResponse,
    DocumentRevisionResponse,
    DocumentRevisionCreate,
    DocumentRevisionContentResponse,
    DocumentWithRevisionsResponse,
    NodeDocumentLinkCreate,
    NodeDocumentLinkResponse,
    NodeDocumentsResponse,
    PaginatedDocumentResponse,
    DocumentSearchParams,
    DocumentContentBase,
    DocumentRevisionDiff
)
from src.services.document import DocumentService
from src.api.v1.schemas.common import PaginationMeta

router = APIRouter(prefix="/documents")
document_service = DocumentService()

# ドキュメント一覧取得
@router.get("/", response_model=PaginatedDocumentResponse)
async def get_documents(
    params: DocumentSearchParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """ドキュメント一覧を取得する"""
    # ここにドキュメント一覧取得の実装を追加
    # DocumentServiceを使って実装する予定
    # 実装がない場合は暫定的に空のレスポンスを返す
    return PaginatedDocumentResponse(
        items=[],
        meta=PaginationMeta(
            current_page=params.page,
            total_pages=0,
            total_items=0,
            items_per_page=params.per_page
        )
    )

# ドキュメント詳細取得
@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたIDのドキュメント詳細を取得する"""
    document = await document_service.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    # 最新リビジョン取得
    latest_revision = None
    if hasattr(document, "revisions") and document.revisions:
        latest_revision = max(document.revisions, key=lambda r: r.created_at)
    else:
        # リレーションがない場合は個別に取得
        from src.db.models.document import DocumentRevision
        from sqlalchemy import select, desc
        result = await db.execute(
            select(DocumentRevision)
            .where(DocumentRevision.document_id == document_id)
            .order_by(desc(DocumentRevision.created_at))
            .limit(1)
        )
        latest_revision = result.scalar_one_or_none()
    # Pydanticモデルに変換して返す
    return DocumentDetailResponse(
        id=document.id,
        title=document.title,
        description=document.description,
        created_at=document.created_at,
        updated_at=document.updated_at,
        latest_revision=DocumentRevisionResponse.model_validate(latest_revision, from_attributes=True) if latest_revision else None
    )

# 最新コンテンツ取得
@router.get("/{document_id}/content", response_model=DocumentRevisionContentResponse)
async def get_document_content(
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントの最新コンテンツを取得する"""
    # ここに最新コンテンツ取得の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="最新コンテンツ取得機能は実装中です"
    )

# 特定バージョン取得
@router.get("/{document_id}/content/version/{version}", response_model=DocumentRevisionContentResponse)
async def get_document_version_content(
    document_id: UUID = Path(..., description="ドキュメントID"),
    version: str = Path(..., description="バージョン番号"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントの特定バージョンのコンテンツを取得する"""
    # ここに特定バージョン取得の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="特定バージョン取得機能は実装中です"
    )

# バージョン履歴取得
@router.get("/{document_id}/revisions", response_model=DocumentWithRevisionsResponse)
async def get_document_revisions(
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントのバージョン履歴を取得する"""
    # ここにバージョン履歴取得の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="バージョン履歴取得機能は実装中です"
    )

# ドキュメント新規作成
@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """新規ドキュメントを作成する"""
    # ここにドキュメント新規作成の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ドキュメント新規作成機能は実装中です"
    )

# ドキュメント更新（新リビジョン作成）
@router.put("/{document_id}", response_model=DocumentRevisionResponse)
async def update_document(
    document_id: UUID = Path(..., description="ドキュメントID"),
    revision: DocumentRevisionCreate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """ドキュメントを更新して新しいリビジョンを作成する"""
    # ここにドキュメント更新の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ドキュメント更新機能は実装中です"
    )

# ドキュメント間のバージョン差分取得
@router.get("/{document_id}/diff", response_model=DocumentRevisionDiff)
async def get_document_diff(
    document_id: UUID = Path(..., description="ドキュメントID"),
    from_version: str = Query(..., description="比較元バージョン"),
    to_version: str = Query(..., description="比較先バージョン"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントの2つのバージョン間の差分を取得する"""
    # ここにバージョン差分取得の実装を追加
    # DocumentDiffUtilityを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="バージョン差分取得機能は実装中です"
    )


# ノード関連のルーター
node_router = APIRouter(prefix="/nodes")

# ノード関連ドキュメント取得
@node_router.get("/{node_id}/documents", response_model=NodeDocumentsResponse)
async def get_node_documents(
    node_id: UUID = Path(..., description="ノードID"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたノードに関連するドキュメント一覧を取得する"""
    # ここにノード関連ドキュメント取得の実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ノード関連ドキュメント取得機能は実装中です"
    )

# ノードとドキュメントの関連付け
@node_router.post("/{node_id}/documents", response_model=NodeDocumentLinkResponse, status_code=status.HTTP_201_CREATED)
async def link_node_document(
    node_id: UUID = Path(..., description="ノードID"),
    link: NodeDocumentLinkCreate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """ノードとドキュメントを関連付ける"""
    # ここにノードとドキュメントの関連付け実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ノードとドキュメントの関連付け機能は実装中です"
    )

# ノードとドキュメントの関連解除
@node_router.delete("/{node_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unlink_node_document(
    node_id: UUID = Path(..., description="ノードID"),
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """ノードとドキュメントの関連付けを解除する"""
    # ここにノードとドキュメントの関連解除実装を追加
    # DocumentServiceを使って実装する予定
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ノードとドキュメントの関連解除機能は実装中です"
    )

"""
ドキュメントリビジョン管理のAPIエンドポイント

このモジュールは、ドキュメントとリビジョン管理に関するAPIエンドポイントを定義します。
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, Response
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
from src.api.v1.schemas.common import PaginationMeta
from src.services.exceptions import DocumentNotFoundError
from src.utils.logger import logger

router = APIRouter(prefix="/documents")

# ドキュメント一覧取得
@router.get("/", response_model=PaginatedDocumentResponse)
async def get_documents(
    params: DocumentSearchParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """ドキュメント一覧を取得する"""
    # APIエンドポイント内でDocumentServiceをインポート
    from src.services.document import DocumentService

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
    # APIエンドポイント内でDocumentServiceをインポート
    from src.services.document import DocumentService

    document_service = DocumentService(db)
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    # 最新リビジョン取得
    latest_revision = None
    if hasattr(document, "revisions") and document.revisions:
        latest_revision = max(document.revisions, key=lambda r: r.created_at)
    else:
        # リレーションがない場合は個別に取得
        latest_revision = await document_service.get_latest_revision(document_id)
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
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)
        content = await document_service.get_latest_content(document_id)
        return content
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ドキュメントID {document_id} は存在しません"
        )
    except Exception as e:
        logger.error(f"ドキュメントコンテンツの取得中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ドキュメントコンテンツの取得中にエラーが発生しました"
        )

# 特定バージョン取得
@router.get("/{document_id}/content/version/{version}", response_model=DocumentRevisionContentResponse)
async def get_document_version_content(
    document_id: UUID = Path(..., description="ドキュメントID"),
    version: str = Path(..., description="バージョン番号"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントの特定バージョンのコンテンツを取得する"""
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)
        content = await document_service.get_version_content(document_id, version)
        return content
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ドキュメントID {document_id} は存在しません"
        )
    except ValueError as e:
        logger.error(f"バージョン取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"バージョン {version} が見つかりません"
        )
    except Exception as e:
        logger.error(f"ドキュメントバージョンの取得中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ドキュメントバージョンの取得中にエラーが発生しました"
        )

# バージョン履歴取得
@router.get("/{document_id}/revisions", response_model=DocumentWithRevisionsResponse)
async def get_document_revisions(
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたドキュメントのバージョン履歴を取得する"""
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)

        # ドキュメントとリビジョン情報を取得
        document = await document_service.get_document_with_revisions(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ドキュメントID {document_id} は存在しません"
            )

        # レスポンスを構築
        revisions = []
        if hasattr(document, "revisions") and document.revisions:
            # 作成日時の降順にソート
            sorted_revisions = sorted(document.revisions, key=lambda r: r.created_at, reverse=True)
            revisions = [DocumentRevisionResponse.model_validate(rev, from_attributes=True) for rev in sorted_revisions]

        return DocumentWithRevisionsResponse(
            id=document.id,
            title=document.title,
            description=document.description,
            created_at=document.created_at,
            updated_at=document.updated_at,
            revisions=revisions
        )
    except Exception as e:
        logger.error(f"バージョン履歴取得中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="バージョン履歴取得中にエラーが発生しました"
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
    node_id: str = Path(..., description="ノードIDまたはハンドル名"),
    db: AsyncSession = Depends(get_db)
):
    """指定されたノードに関連するドキュメント一覧を取得する

    ノードIDはUUID形式、またはノードハンドル名（例：'javascript'）のどちらでも指定可能です。
    """
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)

        # UUIDまたはハンドル名でノードを検索
        node, documents = await document_service.get_node_documents(node_id)

        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ノードID または ハンドル名 {node_id} は存在しません"
            )

        # レスポンスを構築
        document_responses = [DocumentResponse.model_validate(doc, from_attributes=True) for doc in documents]

        return NodeDocumentsResponse(
            node_id=node.id,
            node_title=node.title,
            documents=document_responses
        )
    except Exception as e:
        logger.error(f"ノード関連ドキュメント取得中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ノード関連ドキュメント取得中にエラーが発生しました"
        )

# ノードとドキュメントの関連付け
@node_router.post("/{node_id}/documents", response_model=NodeDocumentLinkResponse, status_code=status.HTTP_201_CREATED)
async def link_node_document(
    node_id: UUID = Path(..., description="ノードID"),
    link: NodeDocumentLinkCreate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """ノードとドキュメントを関連付ける"""
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)

        # node_idが一致しない場合はエラー
        if link.node_id != node_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="リクエストボディのnode_idとパスパラメータのnode_idが一致しません"
            )

        node_document_link = await document_service.link_node_document(
            node_id=node_id,
            document_id=link.document_id,
            relation_type=link.relation_type,
            order_position=link.order_position
        )

        return NodeDocumentLinkResponse.model_validate(node_document_link, from_attributes=True)
    except ValueError as e:
        logger.error(f"ノードとドキュメントの関連付けエラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"ノードとドキュメントの関連付け中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ノードとドキュメントの関連付け中にエラーが発生しました"
        )

# ノードとドキュメントの関連解除
@node_router.delete("/{node_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unlink_node_document(
    node_id: UUID = Path(..., description="ノードID"),
    document_id: UUID = Path(..., description="ドキュメントID"),
    db: AsyncSession = Depends(get_db)
):
    """ノードとドキュメントの関連付けを解除する"""
    try:
        # APIエンドポイント内でDocumentServiceをインポート
        from src.services.document import DocumentService

        document_service = DocumentService(db)
        result = await document_service.unlink_node_document(node_id, document_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ノードID {node_id} とドキュメントID {document_id} の関連付けが見つかりません"
            )

        # 成功した場合は204 No Contentを返す
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"ノードとドキュメントの関連解除中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ノードとドキュメントの関連解除中にエラーが発生しました"
        )

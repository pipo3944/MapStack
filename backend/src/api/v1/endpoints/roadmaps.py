from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# データベース用のスキーマをインポート
from ....db.schemas.roadmap import (
    Category as CategoryDB, CategoryCreate as CategoryCreateDB, CategoryUpdate as CategoryUpdateDB,
    Theme as ThemeDB, ThemeCreate as ThemeCreateDB, ThemeUpdate as ThemeUpdateDB, ThemeWithCategory as ThemeWithCategoryDB,
    Roadmap as RoadmapDB, RoadmapCreate as RoadmapCreateDB, RoadmapUpdate as RoadmapUpdateDB,
    RoadmapDetail as RoadmapDetailDB, RoadmapVersion as RoadmapVersionDB,
    RoadmapNode as RoadmapNodeDB, RoadmapNodeCreate as RoadmapNodeCreateDB, RoadmapNodeUpdate as RoadmapNodeUpdateDB,
    RoadmapEdge as RoadmapEdgeDB, RoadmapEdgeCreate as RoadmapEdgeCreateDB, RoadmapEdgeUpdate as RoadmapEdgeUpdateDB
)

# API用のスキーマをインポート
from ..schemas.roadmap import (
    CategoryResponse, CategoryCreateRequest, CategoryUpdateRequest, CategoryDetailResponse, CategoryListResponse,
    ThemeResponse, ThemeCreateRequest, ThemeUpdateRequest, ThemeWithCategoryResponse, ThemeDetailResponse, ThemeListResponse,
    RoadmapResponse, RoadmapCreateRequest, RoadmapUpdateRequest, RoadmapDetailResponse, RoadmapDetailApiResponse, RoadmapListResponse,
    RoadmapNodeResponse, RoadmapNodeCreateRequest, RoadmapNodeUpdateRequest,
    RoadmapEdgeResponse, RoadmapEdgeCreateRequest, RoadmapEdgeUpdateRequest,
    RoadmapVersionResponse, RoadmapVersionListResponse
)

from ....services.roadmap import (
    # カテゴリ関連
    get_categories, get_category, create_category, update_category, delete_category,
    # テーマ関連
    get_themes, get_theme, create_theme, update_theme, delete_theme,
    # ロードマップ関連
    get_roadmaps, get_roadmap, create_roadmap, update_roadmap,
    get_roadmap_versions, publish_roadmap, clone_roadmap_for_new_version,
    # ノードとエッジ関連
    get_roadmap_nodes, get_roadmap_node, create_roadmap_node, update_roadmap_node, delete_roadmap_node,
    get_roadmap_edges, get_roadmap_edge, create_roadmap_edge, update_roadmap_edge, delete_roadmap_edge
)
from ....db.main import get_async_db
# 以下のimportについては、これから作成するサービスに関するものなので、コメントアウトしておきます
# from ....services.roadmap import (
#     get_categories, get_category, create_category, update_category, delete_category,
#     get_themes, get_theme, create_theme, update_theme, delete_theme,
#     get_roadmaps, get_roadmap, create_roadmap, update_roadmap, delete_roadmap,
#     get_roadmap_nodes, get_roadmap_node, create_roadmap_node, update_roadmap_node, delete_roadmap_node,
#     get_roadmap_edges, get_roadmap_edge, create_roadmap_edge, update_roadmap_edge, delete_roadmap_edge,
#     get_roadmap_versions, publish_roadmap
# )
# from ....db import get_db

router = APIRouter()


# カテゴリ関連エンドポイント
@router.get("/categories/", response_model=CategoryListResponse)
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    カテゴリ一覧を取得する
    """
    categories = await get_categories(db, skip=skip, limit=limit, is_active=is_active)
    category_responses = [CategoryResponse(**category.__dict__) for category in categories]
    return CategoryListResponse(success=True, data=category_responses)


@router.get("/categories/{category_id}", response_model=CategoryDetailResponse)
async def read_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のカテゴリを取得する
    """
    category = await get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_response = CategoryResponse(**category.__dict__)
    return CategoryDetailResponse(success=True, data=category_response)


@router.post("/categories/", response_model=CategoryDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(
    category: CategoryCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいカテゴリを作成する
    """
    # APIスキーマをDBスキーマに変換
    db_category = CategoryCreateDB(**category.dict())
    result = await create_category(db=db, category=db_category)
    category_response = CategoryResponse(**result.__dict__)
    return CategoryDetailResponse(success=True, data=category_response)


@router.put("/categories/{category_id}", response_model=CategoryDetailResponse)
async def update_category_endpoint(
    category_id: UUID,
    category: CategoryUpdateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のカテゴリを更新する
    """
    db_category = await get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # APIスキーマをDBスキーマに変換
    db_category_update = CategoryUpdateDB(**category.dict(exclude_unset=True))
    result = await update_category(db=db, category_id=category_id, category=db_category_update)
    category_response = CategoryResponse(**result.__dict__)
    return CategoryDetailResponse(success=True, data=category_response)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_endpoint(
    category_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のカテゴリを削除する
    """
    db_category = await get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await delete_category(db=db, category_id=category_id)
    return None


# テーマ関連エンドポイント
@router.get("/themes/", response_model=ThemeListResponse)
async def read_themes(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    テーマ一覧を取得する
    """
    themes = await get_themes(db, skip=skip, limit=limit, category_id=category_id, is_active=is_active)
    theme_responses = [ThemeResponse(**theme.__dict__) for theme in themes]
    return ThemeListResponse(success=True, data=theme_responses)


@router.get("/themes/{theme_id}", response_model=ThemeDetailResponse)
async def read_theme(
    theme_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマを取得する
    """
    theme = await get_theme(db, theme_id=theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    # テーマレスポンスの作成
    theme_response = ThemeResponse(**theme.__dict__)

    # カテゴリ情報の取得（joinedloadによりtheme.categoryで取得可能）
    category = theme.category
    category_response = CategoryResponse(
        id=str(category.id),
        title=category.title,
        description=category.description,
        code=category.code,
        order_index=category.order_index,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at
    )

    # ThemeWithCategoryResponseを作成
    theme_with_category_response = ThemeWithCategoryResponse(
        **theme_response.__dict__,
        category=category_response
    )

    return ThemeDetailResponse(success=True, data=theme_with_category_response)


@router.post("/themes/", response_model=ThemeDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_theme_endpoint(
    theme: ThemeCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいテーマを作成する
    """
    # APIスキーマをDBスキーマに変換
    db_theme = ThemeCreateDB(**theme.dict())
    result = await create_theme(db=db, theme=db_theme)
    theme_response = ThemeResponse(**result.__dict__)
    return ThemeDetailResponse(success=True, data=theme_response)


@router.put("/themes/{theme_id}", response_model=ThemeDetailResponse)
async def update_theme_endpoint(
    theme_id: UUID,
    theme: ThemeUpdateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマを更新する
    """
    db_theme = await get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    # APIスキーマをDBスキーマに変換
    db_theme_update = ThemeUpdateDB(**theme.dict(exclude_unset=True))
    result = await update_theme(db=db, theme_id=theme_id, theme=db_theme_update)
    theme_response = ThemeResponse(**result.__dict__)
    return ThemeDetailResponse(success=True, data=theme_response)


@router.delete("/themes/{theme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_theme_endpoint(
    theme_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマを削除する
    """
    db_theme = await get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    await delete_theme(db=db, theme_id=theme_id)
    return None


# ロードマップ関連エンドポイント
@router.get("/roadmaps/", response_model=RoadmapListResponse)
async def read_roadmaps(
    skip: int = 0,
    limit: int = 100,
    theme_id: Optional[UUID] = None,
    is_published: Optional[bool] = None,
    is_latest: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    ロードマップ一覧を取得する
    """
    roadmaps = await get_roadmaps(
        db, skip=skip, limit=limit, theme_id=theme_id,
        is_published=is_published, is_latest=is_latest
    )
    roadmap_responses = [RoadmapResponse(**roadmap.__dict__) for roadmap in roadmaps]
    return RoadmapListResponse(success=True, data=roadmap_responses)


@router.get("/roadmaps/{roadmap_id}", response_model=RoadmapDetailApiResponse)
async def read_roadmap(
    roadmap_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップを取得する
    """
    roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    if roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    roadmap_response = RoadmapDetailResponse(**roadmap.__dict__)
    return RoadmapDetailApiResponse(success=True, data=roadmap_response)


@router.get("/themes/{theme_id}/roadmaps/versions", response_model=RoadmapVersionListResponse)
async def read_roadmap_versions(
    theme_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマに関連するすべてのロードマップバージョンを取得する
    """
    versions = await get_roadmap_versions(db, theme_id=theme_id)

    # versions は辞書オブジェクトのリストなので、直接 RoadmapVersionResponse に渡す
    version_responses = [RoadmapVersionResponse(**version) for version in versions]

    return RoadmapVersionListResponse(success=True, data=version_responses)


@router.post("/roadmaps/", response_model=RoadmapDetailApiResponse, status_code=status.HTTP_201_CREATED)
async def create_roadmap_endpoint(
    roadmap: RoadmapCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいロードマップを作成する
    """
    # APIスキーマをDBスキーマに変換
    db_roadmap = RoadmapCreateDB(**roadmap.dict())
    result = await create_roadmap(db=db, roadmap=db_roadmap)
    roadmap_response = RoadmapDetailResponse(**result.__dict__)
    return RoadmapDetailApiResponse(success=True, data=roadmap_response)


@router.put("/roadmaps/{roadmap_id}", response_model=RoadmapDetailApiResponse)
async def update_roadmap_endpoint(
    roadmap_id: UUID,
    roadmap: RoadmapUpdateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップを更新する
    """
    db_roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    # APIスキーマをDBスキーマに変換
    db_roadmap_update = RoadmapUpdateDB(**roadmap.dict(exclude_unset=True))
    result = await update_roadmap(db=db, roadmap_id=roadmap_id, roadmap=db_roadmap_update)
    roadmap_response = RoadmapDetailResponse(**result.__dict__)
    return RoadmapDetailApiResponse(success=True, data=roadmap_response)


@router.post("/roadmaps/{roadmap_id}/publish", response_model=RoadmapDetailApiResponse)
async def publish_roadmap_endpoint(
    roadmap_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップを公開状態にする
    """
    db_roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    result = await publish_roadmap(db=db, roadmap_id=roadmap_id)
    roadmap_response = RoadmapDetailResponse(**result.__dict__)
    return RoadmapDetailApiResponse(success=True, data=roadmap_response)


@router.post("/roadmaps/{roadmap_id}/new-version", response_model=RoadmapDetailApiResponse)
async def create_new_version_endpoint(
    roadmap_id: UUID,
    new_version: str = Query(..., description="新しいバージョン番号（セマンティックバージョニング形式、例：1.1.0）"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    既存のロードマップから新しいバージョンを作成する
    """
    db_roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    result = await clone_roadmap_for_new_version(db=db, roadmap_id=roadmap_id, new_version=new_version)
    roadmap_response = RoadmapDetailResponse(**result.__dict__)
    return RoadmapDetailApiResponse(success=True, data=roadmap_response)


@router.delete("/roadmaps/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap_endpoint(
    roadmap_id: UUID,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップを削除する
    """
    # db_roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    # if db_roadmap is None:
    #     raise HTTPException(status_code=404, detail="Roadmap not found")
    # await delete_roadmap(db=db, roadmap_id=roadmap_id)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


# ノード関連エンドポイント
@router.get("/roadmaps/{roadmap_id}/nodes", response_model=List[RoadmapNodeResponse])
async def read_roadmap_nodes(
    roadmap_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップのノード一覧を取得する
    """
    nodes = await get_roadmap_nodes(db, roadmap_id=roadmap_id)

    # SQLAlchemyモデルをPydanticモデルに変換する前に調整
    result_nodes = []
    for node in nodes:
        # ノードデータをディクショナリに変換
        node_dict = {
            "id": node.id,
            "roadmap_id": node.roadmap_id,
            "handle": node.handle,
            "node_type": node.node_type,
            "title": node.title,
            "description": node.description,
            "position_x": node.position_x,
            "position_y": node.position_y,
            "metadata": dict(node.meta_data) if node.meta_data else {},  # meta_dataを辞書に変換
            "is_required": node.is_required,
            "created_at": node.created_at,
            "updated_at": node.updated_at
        }
        result_nodes.append(node_dict)

    return result_nodes


@router.post("/roadmaps/nodes", response_model=RoadmapNodeResponse, status_code=status.HTTP_201_CREATED)
async def create_roadmap_node_endpoint(
    node: RoadmapNodeCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいロードマップノードを作成する
    """
    # APIスキーマをDBスキーマに変換
    db_node = RoadmapNodeCreateDB(**node.dict())
    result = await create_roadmap_node(db=db, node=db_node)
    return result


@router.put("/roadmaps/nodes/{node_id}", response_model=RoadmapNodeResponse)
async def update_roadmap_node_endpoint(
    node_id: UUID,
    node: RoadmapNodeUpdateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップノードを更新する
    """
    db_node = await get_roadmap_node(db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    # APIスキーマをDBスキーマに変換
    db_node_update = RoadmapNodeUpdateDB(**node.dict(exclude_unset=True))
    result = await update_roadmap_node(db=db, node_id=node_id, node=db_node_update)
    return result


@router.delete("/roadmaps/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap_node_endpoint(
    node_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップノードを削除する
    """
    db_node = await get_roadmap_node(db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    await delete_roadmap_node(db=db, node_id=node_id)


# エッジ関連エンドポイント
@router.get("/roadmaps/{roadmap_id}/edges", response_model=List[RoadmapEdgeResponse])
async def read_roadmap_edges(
    roadmap_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップのエッジ一覧を取得する
    """
    print("Fetching edges for roadmap:", roadmap_id)
    edges = await get_roadmap_edges(db, roadmap_id=roadmap_id)
    print("Found edges:", edges)

    result_edges = []
    for edge in edges:
        # エッジデータをディクショナリに変換
        edge_dict = {
            "id": edge.id,
            "roadmap_id": edge.roadmap_id,
            "handle": edge.handle,
            "source_node_id": edge.source_node_id,
            "target_node_id": edge.target_node_id,
            "edge_type": edge.edge_type,
            "source_handle": edge.source_handle,
            "target_handle": edge.target_handle,
            "metadata": dict(edge.meta_data) if edge.meta_data else None,  # Noneに変更
            "created_at": edge.created_at,
            "updated_at": edge.updated_at
        }
        result_edges.append(edge_dict)

    print("Returning edges:", result_edges)
    return result_edges


@router.post("/roadmaps/edges", response_model=RoadmapEdgeResponse, status_code=status.HTTP_201_CREATED)
async def create_roadmap_edge_endpoint(
    edge: RoadmapEdgeCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいロードマップエッジを作成する
    """
    # APIスキーマをDBスキーマに変換
    db_edge = RoadmapEdgeCreateDB(**edge.dict())
    result = await create_roadmap_edge(db=db, edge=db_edge)
    return result


@router.put("/roadmaps/edges/{edge_id}", response_model=RoadmapEdgeResponse)
async def update_roadmap_edge_endpoint(
    edge_id: UUID,
    edge: RoadmapEdgeUpdateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップエッジを更新する
    """
    db_edge = await get_roadmap_edge(db, edge_id=edge_id)
    if db_edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")
    # APIスキーマをDBスキーマに変換
    db_edge_update = RoadmapEdgeUpdateDB(**edge.dict(exclude_unset=True))
    result = await update_roadmap_edge(db=db, edge_id=edge_id, edge=db_edge_update)
    return result


@router.delete("/roadmaps/edges/{edge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap_edge_endpoint(
    edge_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップエッジを削除する
    """
    db_edge = await get_roadmap_edge(db, edge_id=edge_id)
    if db_edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")
    await delete_roadmap_edge(db=db, edge_id=edge_id)

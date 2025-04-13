from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ....db.schemas.roadmap import (
    Category, CategoryCreate, CategoryUpdate,
    Theme, ThemeCreate, ThemeUpdate, ThemeWithCategory,
    Roadmap, RoadmapCreate, RoadmapUpdate, RoadmapDetail, RoadmapVersion,
    RoadmapNode, RoadmapNodeCreate, RoadmapNodeUpdate,
    RoadmapEdge, RoadmapEdgeCreate, RoadmapEdgeUpdate
)
from ....services.roadmap import (
    # カテゴリ関連
    get_categories, get_category, create_category, update_category, delete_category,
    # テーマ関連
    get_themes, get_theme, create_theme, update_theme, delete_theme,
    # ロードマップ関連
    get_roadmaps, get_roadmap, create_roadmap, update_roadmap,
    get_roadmap_versions, publish_roadmap, clone_roadmap_for_new_version
    # ノードとエッジ関連の関数はまだ実装していません
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
@router.get("/categories/", response_model=List[Category])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    カテゴリ一覧を取得する
    """
    return await get_categories(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/categories/{category_id}", response_model=Category)
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
    return category


@router.post("/categories/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいカテゴリを作成する
    """
    return await create_category(db=db, category=category)


@router.put("/categories/{category_id}", response_model=Category)
async def update_category_endpoint(
    category_id: UUID,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のカテゴリを更新する
    """
    db_category = await get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return await update_category(db=db, category_id=category_id, category=category)


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


# テーマ関連エンドポイント
@router.get("/themes/", response_model=List[Theme])
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
    return await get_themes(db, skip=skip, limit=limit, category_id=category_id, is_active=is_active)


@router.get("/themes/{theme_id}", response_model=ThemeWithCategory)
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
    return theme


@router.post("/themes/", response_model=Theme, status_code=status.HTTP_201_CREATED)
async def create_theme_endpoint(
    theme: ThemeCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいテーマを作成する
    """
    return await create_theme(db=db, theme=theme)


@router.put("/themes/{theme_id}", response_model=Theme)
async def update_theme_endpoint(
    theme_id: UUID,
    theme: ThemeUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマを更新する
    """
    db_theme = await get_theme(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return await update_theme(db=db, theme_id=theme_id, theme=theme)


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


# ロードマップ関連エンドポイント
@router.get("/roadmaps/", response_model=List[Roadmap])
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
    return await get_roadmaps(
        db, skip=skip, limit=limit, theme_id=theme_id,
        is_published=is_published, is_latest=is_latest
    )


@router.get("/roadmaps/{roadmap_id}", response_model=RoadmapDetail)
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
    return roadmap


@router.get("/themes/{theme_id}/roadmaps/versions", response_model=List[RoadmapVersion])
async def read_roadmap_versions(
    theme_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のテーマに属するロードマップのバージョン一覧を取得する
    """
    return await get_roadmap_versions(db, theme_id=theme_id)


@router.post("/roadmaps/", response_model=RoadmapDetail, status_code=status.HTTP_201_CREATED)
async def create_roadmap_endpoint(
    roadmap: RoadmapCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    新しいロードマップを作成する
    """
    return await create_roadmap(db=db, roadmap=roadmap)


@router.put("/roadmaps/{roadmap_id}", response_model=Roadmap)
async def update_roadmap_endpoint(
    roadmap_id: UUID,
    roadmap: RoadmapUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップを更新する
    """
    db_roadmap = await get_roadmap(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return await update_roadmap(db=db, roadmap_id=roadmap_id, roadmap=roadmap)


@router.post("/roadmaps/{roadmap_id}/publish", response_model=Roadmap)
async def publish_roadmap_endpoint(
    roadmap_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """
    特定のロードマップを公開する
    """
    return await publish_roadmap(db=db, roadmap_id=roadmap_id)


@router.post("/roadmaps/{roadmap_id}/new-version", response_model=Roadmap)
async def create_new_version_endpoint(
    roadmap_id: UUID,
    new_version: str = Query(..., description="新しいバージョン番号（セマンティックバージョニング形式、例：1.1.0）"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    既存のロードマップから新しいバージョンを作成する
    """
    return await clone_roadmap_for_new_version(
        db=db,
        roadmap_id=roadmap_id,
        new_version=new_version
    )


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
@router.get("/roadmaps/{roadmap_id}/nodes", response_model=List[RoadmapNode])
async def read_roadmap_nodes(
    roadmap_id: UUID,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップのノード一覧を取得する
    """
    # return await get_roadmap_nodes(db, roadmap_id=roadmap_id)
    # 実装前なのでモックを返す
    return []


@router.post("/roadmaps/nodes", response_model=RoadmapNode, status_code=status.HTTP_201_CREATED)
async def create_roadmap_node_endpoint(
    node: RoadmapNodeCreate,
    # db: AsyncSession = Depends(get_db)
):
    """
    新しいロードマップノードを作成する
    """
    # return await create_roadmap_node(db=db, node=node)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/roadmaps/nodes/{node_id}", response_model=RoadmapNode)
async def update_roadmap_node_endpoint(
    node_id: UUID,
    node: RoadmapNodeUpdate,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップノードを更新する
    """
    # db_node = await get_roadmap_node(db, node_id=node_id)
    # if db_node is None:
    #     raise HTTPException(status_code=404, detail="Node not found")
    # return await update_roadmap_node(db=db, node_id=node_id, node=node)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/roadmaps/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap_node_endpoint(
    node_id: UUID,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップノードを削除する
    """
    # db_node = await get_roadmap_node(db, node_id=node_id)
    # if db_node is None:
    #     raise HTTPException(status_code=404, detail="Node not found")
    # await delete_roadmap_node(db=db, node_id=node_id)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


# エッジ関連エンドポイント
@router.get("/roadmaps/{roadmap_id}/edges", response_model=List[RoadmapEdge])
async def read_roadmap_edges(
    roadmap_id: UUID,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップのエッジ一覧を取得する
    """
    # return await get_roadmap_edges(db, roadmap_id=roadmap_id)
    # 実装前なのでモックを返す
    return []


@router.post("/roadmaps/edges", response_model=RoadmapEdge, status_code=status.HTTP_201_CREATED)
async def create_roadmap_edge_endpoint(
    edge: RoadmapEdgeCreate,
    # db: AsyncSession = Depends(get_db)
):
    """
    新しいロードマップエッジを作成する
    """
    # return await create_roadmap_edge(db=db, edge=edge)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/roadmaps/edges/{edge_id}", response_model=RoadmapEdge)
async def update_roadmap_edge_endpoint(
    edge_id: UUID,
    edge: RoadmapEdgeUpdate,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップエッジを更新する
    """
    # db_edge = await get_roadmap_edge(db, edge_id=edge_id)
    # if db_edge is None:
    #     raise HTTPException(status_code=404, detail="Edge not found")
    # return await update_roadmap_edge(db=db, edge_id=edge_id, edge=edge)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/roadmaps/edges/{edge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap_edge_endpoint(
    edge_id: UUID,
    # db: AsyncSession = Depends(get_db)
):
    """
    特定のロードマップエッジを削除する
    """
    # db_edge = await get_roadmap_edge(db, edge_id=edge_id)
    # if db_edge is None:
    #     raise HTTPException(status_code=404, detail="Edge not found")
    # await delete_roadmap_edge(db=db, edge_id=edge_id)
    # 実装前なのでモックを返す
    raise HTTPException(status_code=501, detail="Not implemented")

"""
ロードマップ関連のサービス関数

このモジュールはロードマップ関連のビジネスロジックを提供します。
ロードマップ、ノード、エッジの作成、取得、更新、削除などの機能や、
バージョン管理に関する機能を実装しています。
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from fastapi import HTTPException
from packaging import version
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db.models.roadmap import (
    Category, Theme, Roadmap, RoadmapNode, RoadmapEdge
)
from ..db.schemas.roadmap import (
    CategoryCreate, CategoryUpdate,
    ThemeCreate, ThemeUpdate,
    RoadmapCreate, RoadmapUpdate,
    RoadmapNodeCreate, RoadmapNodeUpdate,
    RoadmapEdgeCreate, RoadmapEdgeUpdate
)

logger = logging.getLogger(__name__)


# カテゴリ関連の関数
async def get_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Category]:
    """カテゴリ一覧を取得する"""
    query = select(Category)

    if is_active is not None:
        query = query.where(Category.is_active == is_active)

    query = query.offset(skip).limit(limit).order_by(Category.order_index)
    result = await db.execute(query)
    return result.scalars().all()


async def get_category(
    db: AsyncSession,
    category_id: UUID
) -> Optional[Category]:
    """指定されたIDのカテゴリを取得する"""
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_category(
    db: AsyncSession,
    category: CategoryCreate
) -> Category:
    """新しいカテゴリを作成する"""
    db_category = Category(
        code=category.code,
        title=category.title,
        description=category.description,
        order_index=category.order_index,
        is_active=category.is_active
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(
    db: AsyncSession,
    category_id: UUID,
    category: CategoryUpdate
) -> Category:
    """既存のカテゴリを更新する"""
    db_category = await get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    category_data = category.dict(exclude_unset=True)
    for field in category_data:
        setattr(db_category, field, category_data[field])

    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(
    db: AsyncSession,
    category_id: UUID
) -> None:
    """カテゴリを削除する"""
    db_category = await get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(db_category)
    await db.commit()


# テーマ関連の関数
async def get_themes(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[UUID] = None,
    is_active: Optional[bool] = None
) -> List[Theme]:
    """テーマ一覧を取得する"""
    query = select(Theme)

    if category_id is not None:
        query = query.where(Theme.category_id == category_id)

    if is_active is not None:
        query = query.where(Theme.is_active == is_active)

    query = query.offset(skip).limit(limit).order_by(Theme.order_index)
    result = await db.execute(query)
    return result.scalars().all()


async def get_theme(
    db: AsyncSession,
    theme_id: UUID
) -> Optional[Theme]:
    """指定されたIDのテーマを取得する"""
    query = select(Theme).where(Theme.id == theme_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_theme(
    db: AsyncSession,
    theme: ThemeCreate
) -> Theme:
    """新しいテーマを作成する"""
    # カテゴリの存在確認
    category_query = select(Category).where(Category.id == theme.category_id)
    category_result = await db.execute(category_query)
    category = category_result.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_theme = Theme(
        category_id=theme.category_id,
        code=theme.code,
        title=theme.title,
        description=theme.description,
        order_index=theme.order_index,
        is_active=theme.is_active
    )
    db.add(db_theme)
    await db.commit()
    await db.refresh(db_theme)
    return db_theme


async def update_theme(
    db: AsyncSession,
    theme_id: UUID,
    theme: ThemeUpdate
) -> Theme:
    """既存のテーマを更新する"""
    db_theme = await get_theme(db, theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    # カテゴリIDが変更される場合は存在確認
    if theme.category_id is not None and theme.category_id != db_theme.category_id:
        category_query = select(Category).where(Category.id == theme.category_id)
        category_result = await db.execute(category_query)
        category = category_result.scalars().first()

        if not category:
            raise HTTPException(status_code=404, detail="New category not found")

    theme_data = theme.dict(exclude_unset=True)
    for field in theme_data:
        setattr(db_theme, field, theme_data[field])

    await db.commit()
    await db.refresh(db_theme)
    return db_theme


async def delete_theme(
    db: AsyncSession,
    theme_id: UUID
) -> None:
    """テーマを削除する"""
    db_theme = await get_theme(db, theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    await db.delete(db_theme)
    await db.commit()


# ロードマップ関連の関数
async def get_roadmaps(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    theme_id: Optional[UUID] = None,
    is_published: Optional[bool] = None,
    is_latest: Optional[bool] = None
) -> List[Roadmap]:
    """ロードマップ一覧を取得する"""
    query = select(Roadmap)

    if theme_id is not None:
        query = query.where(Roadmap.theme_id == theme_id)

    if is_published is not None:
        query = query.where(Roadmap.is_published == is_published)

    if is_latest is not None:
        query = query.where(Roadmap.is_latest == is_latest)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_roadmap(
    db: AsyncSession,
    roadmap_id: UUID
) -> Optional[Roadmap]:
    """指定されたIDのロードマップを取得する"""
    query = select(Roadmap).where(Roadmap.id == roadmap_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_roadmap(
    db: AsyncSession,
    roadmap: RoadmapCreate
) -> Roadmap:
    """新しいロードマップを作成する"""
    # テーマの存在確認
    theme_query = select(Theme).where(Theme.id == roadmap.theme_id)
    theme_result = await db.execute(theme_query)
    theme = theme_result.scalars().first()

    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    # 初期バージョンは1.0.0
    new_roadmap = Roadmap(
        theme_id=roadmap.theme_id,
        version="1.0.0",
        title=roadmap.title,
        description=roadmap.description,
        is_published=False,  # 初期状態では非公開
        is_latest=True       # 初期状態では最新
    )

    db.add(new_roadmap)
    await db.commit()
    await db.refresh(new_roadmap)
    return new_roadmap


async def update_roadmap(
    db: AsyncSession,
    roadmap_id: UUID,
    roadmap: RoadmapUpdate
) -> Roadmap:
    """既存のロードマップを更新する"""
    db_roadmap = await get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    # 公開済みのロードマップの場合、一部のフィールドは変更不可
    if db_roadmap.is_published:
        if roadmap.theme_id is not None and roadmap.theme_id != db_roadmap.theme_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot change theme of published roadmap"
            )

    # バージョン管理フィールドは直接変更不可
    roadmap_data = roadmap.dict(exclude_unset=True)
    for field in roadmap_data:
        if field not in ["is_published", "is_latest", "published_at"] or not db_roadmap.is_published:
            setattr(db_roadmap, field, roadmap_data[field])

    await db.commit()
    await db.refresh(db_roadmap)
    return db_roadmap


async def clone_roadmap_for_new_version(
    db: AsyncSession,
    roadmap_id: UUID,
    new_version: str
) -> Roadmap:
    """ロードマップを複製して新しいバージョンを作成する"""
    # 元のロードマップを取得
    original_roadmap = await get_roadmap(db, roadmap_id)
    if not original_roadmap:
        raise HTTPException(status_code=404, detail="Original roadmap not found")

    # 既に公開されているか確認
    if not original_roadmap.is_published:
        raise HTTPException(
            status_code=400,
            detail="Cannot create new version from unpublished roadmap"
        )

    # バージョン番号の検証
    try:
        if version.parse(new_version) <= version.parse(original_roadmap.version):
            raise HTTPException(
                status_code=400,
                detail="New version must be greater than current version"
            )
    except version.InvalidVersion:
        raise HTTPException(
            status_code=400,
            detail="Invalid version format. Use semantic versioning (e.g., 1.0.0)"
        )

    # テーマが存在するか確認
    theme_query = select(Theme).where(Theme.id == original_roadmap.theme_id)
    theme_result = await db.execute(theme_query)
    theme = theme_result.scalars().first()

    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    # 旧バージョンを最新ではなくする
    original_roadmap.is_latest = False
    await db.commit()

    # 新しいロードマップを作成
    new_roadmap = Roadmap(
        theme_id=original_roadmap.theme_id,
        version=new_version,
        title=original_roadmap.title,
        description=original_roadmap.description,
        is_published=False,  # 初期状態では非公開
        is_latest=True       # 新バージョンは最新
    )

    db.add(new_roadmap)
    await db.flush()

    # 元のノードを取得
    node_query = select(RoadmapNode).where(RoadmapNode.roadmap_id == original_roadmap.id)
    node_result = await db.execute(node_query)
    original_nodes = node_result.scalars().all()

    # ノードIDの対応マップ（旧ID -> 新ID）
    node_id_map = {}

    # ノードを複製
    for original_node in original_nodes:
        new_node = RoadmapNode(
            roadmap_id=new_roadmap.id,
            handle=original_node.handle,
            node_type=original_node.node_type,
            title=original_node.title,
            description=original_node.description,
            position_x=original_node.position_x,
            position_y=original_node.position_y,
            meta_data=original_node.meta_data,
            is_required=original_node.is_required
        )
        db.add(new_node)
        await db.flush()

        # 旧IDと新IDのマッピングを保存
        node_id_map[original_node.id] = new_node.id

    # 元のエッジを取得
    edge_query = select(RoadmapEdge).where(RoadmapEdge.roadmap_id == original_roadmap.id)
    edge_result = await db.execute(edge_query)
    original_edges = edge_result.scalars().all()

    # エッジを複製
    for original_edge in original_edges:
        new_edge = RoadmapEdge(
            roadmap_id=new_roadmap.id,
            handle=original_edge.handle,
            source_node_id=node_id_map[original_edge.source_node_id],
            target_node_id=node_id_map[original_edge.target_node_id],
            edge_type=original_edge.edge_type,
            meta_data=original_edge.meta_data
        )
        db.add(new_edge)

    await db.commit()
    await db.refresh(new_roadmap)
    return new_roadmap


async def publish_roadmap(
    db: AsyncSession,
    roadmap_id: UUID
) -> Roadmap:
    """ロードマップを公開する"""
    db_roadmap = await get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if db_roadmap.is_published:
        raise HTTPException(
            status_code=400,
            detail="Roadmap is already published"
        )

    # ノードが存在するか確認
    node_count_query = select(func.count(RoadmapNode.id)).where(
        RoadmapNode.roadmap_id == roadmap_id
    )
    node_count_result = await db.execute(node_count_query)
    node_count = node_count_result.scalar()

    if node_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot publish roadmap with no nodes"
        )

    # エッジが存在するか確認（ノードが複数ある場合）
    if node_count > 1:
        edge_count_query = select(func.count(RoadmapEdge.id)).where(
            RoadmapEdge.roadmap_id == roadmap_id
        )
        edge_count_result = await db.execute(edge_count_query)
        edge_count = edge_count_result.scalar()

        if edge_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Roadmap with multiple nodes must have edges"
            )

    # 公開処理
    db_roadmap.is_published = True
    db_roadmap.published_at = datetime.now()

    await db.commit()
    await db.refresh(db_roadmap)
    return db_roadmap


async def get_roadmap_versions(
    db: AsyncSession,
    theme_id: UUID
) -> List[Dict[str, Any]]:
    """テーマに属するロードマップのバージョン一覧を取得する"""
    query = select(
        Roadmap.id,
        Roadmap.version,
        Roadmap.title,
        Roadmap.is_published,
        Roadmap.is_latest,
        Roadmap.published_at,
        Roadmap.created_at
    ).where(
        Roadmap.theme_id == theme_id
    ).order_by(
        Roadmap.created_at.desc()
    )

    result = await db.execute(query)
    versions = []

    for row in result:
        versions.append({
            "id": row.id,
            "version": row.version,
            "title": row.title,
            "is_published": row.is_published,
            "is_latest": row.is_latest,
            "published_at": row.published_at,
            "created_at": row.created_at
        })

    return versions

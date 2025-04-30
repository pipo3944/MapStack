"""
ロードマップ関連のデータベーススキーマ

このモジュールはデータベースとの連携に使用されるPydanticモデルを定義します。
API用のスキーマは別途 api/v1/schemas/roadmap.py に定義されています。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[float] = None
    is_active: Optional[bool] = None


class Category(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ThemeBase(BaseModel):
    category_id: UUID
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool = True


class ThemeCreate(ThemeBase):
    pass


class ThemeUpdate(BaseModel):
    category_id: Optional[UUID] = None
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[float] = None
    is_active: Optional[bool] = None


class Theme(ThemeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ThemeWithCategory(Theme):
    category: Category


class RoadmapNodeBase(BaseModel):
    handle: str
    node_type: str
    title: str
    description: Optional[str] = None
    position_x: float = 0
    position_y: float = 0
    metadata: Optional[Dict[str, Any]] = None
    is_required: bool = False


class RoadmapNodeCreate(RoadmapNodeBase):
    roadmap_id: UUID


class RoadmapNodeUpdate(BaseModel):
    handle: Optional[str] = None
    node_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    is_required: Optional[bool] = None


class RoadmapNode(RoadmapNodeBase):
    id: UUID
    roadmap_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoadmapEdgeBase(BaseModel):
    handle: str
    source_node_id: UUID
    target_node_id: UUID
    edge_type: str = "default"
    label: Optional[str] = None
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RoadmapEdgeCreate(RoadmapEdgeBase):
    roadmap_id: UUID


class RoadmapEdgeUpdate(BaseModel):
    handle: Optional[str] = None
    source_node_id: Optional[UUID] = None
    target_node_id: Optional[UUID] = None
    edge_type: Optional[str] = None
    label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RoadmapEdge(RoadmapEdgeBase):
    id: UUID
    roadmap_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoadmapBase(BaseModel):
    theme_id: UUID
    version: str
    title: str
    description: Optional[str] = None
    is_published: bool = False
    is_latest: bool = True
    published_at: Optional[datetime] = None


class RoadmapCreate(RoadmapBase):
    nodes: List[RoadmapNodeBase]
    edges: List[RoadmapEdgeBase]


class RoadmapUpdate(BaseModel):
    theme_id: Optional[UUID] = None
    version: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    is_latest: Optional[bool] = None
    published_at: Optional[datetime] = None


class Roadmap(RoadmapBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoadmapDetail(Roadmap):
    theme: Theme
    nodes: List[RoadmapNode]
    edges: List[RoadmapEdge]


class RoadmapVersion(BaseModel):
    id: UUID
    version: str
    title: str
    is_published: bool
    is_latest: bool
    published_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

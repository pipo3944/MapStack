"""
ロードマップ関連のAPIスキーマ

このモジュールはロードマップ、テーマ、カテゴリなどに関するAPI用のPydanticモデルを定義します。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from .common import ApiResponse, PaginatedResponse


# カテゴリスキーマ
class CategoryResponse(BaseModel):
    """カテゴリのレスポンススキーマ"""
    id: UUID
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CategoryCreateRequest(BaseModel):
    """カテゴリの作成リクエストスキーマ"""
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool = True


class CategoryUpdateRequest(BaseModel):
    """カテゴリの更新リクエストスキーマ"""
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[float] = None
    is_active: Optional[bool] = None


# テーマスキーマ
class ThemeResponse(BaseModel):
    """テーマのレスポンススキーマ"""
    id: UUID
    category_id: UUID
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ThemeWithCategoryResponse(ThemeResponse):
    """カテゴリ情報を含むテーマのレスポンススキーマ"""
    category: CategoryResponse


class ThemeCreateRequest(BaseModel):
    """テーマの作成リクエストスキーマ"""
    category_id: UUID
    code: str
    title: str
    description: Optional[str] = None
    order_index: float
    is_active: bool = True


class ThemeUpdateRequest(BaseModel):
    """テーマの更新リクエストスキーマ"""
    category_id: Optional[UUID] = None
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[float] = None
    is_active: Optional[bool] = None


# ロードマップノードスキーマ
class RoadmapNodeResponse(BaseModel):
    """ロードマップノードのレスポンススキーマ"""
    id: UUID
    roadmap_id: UUID
    handle: str
    node_type: str
    title: str
    description: Optional[str] = None
    position_x: float
    position_y: float
    metadata: Optional[Dict[str, Any]] = None
    is_required: bool
    created_at: datetime
    updated_at: datetime


class RoadmapNodeRequest(BaseModel):
    """ロードマップノードのリクエストスキーマ（作成用）"""
    handle: str
    node_type: str
    title: str
    description: Optional[str] = None
    position_x: float = 0
    position_y: float = 0
    metadata: Optional[Dict[str, Any]] = None
    is_required: bool = False


class RoadmapNodeCreateRequest(RoadmapNodeRequest):
    """ロードマップノードの作成リクエストスキーマ"""
    roadmap_id: UUID


class RoadmapNodeUpdateRequest(BaseModel):
    """ロードマップノードの更新リクエストスキーマ"""
    handle: Optional[str] = None
    node_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    is_required: Optional[bool] = None


# ロードマップエッジスキーマ
class RoadmapEdgeResponse(BaseModel):
    """ロードマップエッジのレスポンススキーマ"""
    id: UUID
    roadmap_id: UUID
    handle: str
    source_node_id: UUID
    target_node_id: UUID
    edge_type: str
    label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class RoadmapEdgeRequest(BaseModel):
    """ロードマップエッジのリクエストスキーマ（基本）"""
    handle: str
    source_node_id: UUID
    target_node_id: UUID
    edge_type: str = "default"
    label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RoadmapEdgeCreateRequest(RoadmapEdgeRequest):
    """ロードマップエッジの作成リクエストスキーマ"""
    roadmap_id: UUID


class RoadmapEdgeUpdateRequest(BaseModel):
    """ロードマップエッジの更新リクエストスキーマ"""
    handle: Optional[str] = None
    source_node_id: Optional[UUID] = None
    target_node_id: Optional[UUID] = None
    edge_type: Optional[str] = None
    label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ロードマップスキーマ
class RoadmapResponse(BaseModel):
    """ロードマップのレスポンススキーマ"""
    id: UUID
    theme_id: UUID
    version: str
    title: str
    description: Optional[str] = None
    is_published: bool
    is_latest: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class RoadmapDetailResponse(RoadmapResponse):
    """詳細情報を含むロードマップのレスポンススキーマ"""
    theme: ThemeResponse
    nodes: List[RoadmapNodeResponse]
    edges: List[RoadmapEdgeResponse]


class RoadmapCreateRequest(BaseModel):
    """ロードマップの作成リクエストスキーマ"""
    theme_id: UUID
    version: str
    title: str
    description: Optional[str] = None
    is_published: bool = False
    nodes: List[RoadmapNodeRequest]
    edges: List[RoadmapEdgeRequest]


class RoadmapUpdateRequest(BaseModel):
    """ロードマップの更新リクエストスキーマ"""
    theme_id: Optional[UUID] = None
    version: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None


class RoadmapVersionResponse(BaseModel):
    """ロードマップバージョンのレスポンススキーマ"""
    id: UUID
    version: str
    title: str
    is_published: bool
    is_latest: bool
    published_at: Optional[datetime]
    created_at: datetime


# APIレスポンスラッパー
class CategoryListResponse(ApiResponse[List[CategoryResponse]]):
    """カテゴリ一覧のAPIレスポンス"""
    pass


class CategoryDetailResponse(ApiResponse[CategoryResponse]):
    """カテゴリ詳細のAPIレスポンス"""
    pass


class ThemeListResponse(ApiResponse[List[ThemeResponse]]):
    """テーマ一覧のAPIレスポンス"""
    pass


class ThemeDetailResponse(ApiResponse[ThemeWithCategoryResponse]):
    """テーマ詳細のAPIレスポンス"""
    pass


class RoadmapListResponse(ApiResponse[List[RoadmapResponse]]):
    """ロードマップ一覧のAPIレスポンス"""
    pass


class RoadmapDetailApiResponse(ApiResponse[RoadmapDetailResponse]):
    """ロードマップ詳細のAPIレスポンス"""
    pass


class RoadmapVersionListResponse(ApiResponse[List[RoadmapVersionResponse]]):
    """ロードマップバージョン一覧のAPIレスポンス"""
    pass


# ページネーション対応レスポンス
class PaginatedCategoryListResponse(ApiResponse[PaginatedResponse[CategoryResponse]]):
    """ページネーション付きカテゴリ一覧のAPIレスポンス"""
    pass


class PaginatedThemeListResponse(ApiResponse[PaginatedResponse[ThemeResponse]]):
    """ページネーション付きテーマ一覧のAPIレスポンス"""
    pass


class PaginatedRoadmapListResponse(ApiResponse[PaginatedResponse[RoadmapResponse]]):
    """ページネーション付きロードマップ一覧のAPIレスポンス"""
    pass

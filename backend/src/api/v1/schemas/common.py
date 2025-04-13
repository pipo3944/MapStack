"""
共通レスポンスモデル

このモジュールはAPIのレスポンスで使用される共通のPydanticモデルを定義します。
統一されたレスポンス形式を提供し、OpenAPI仕様の一貫性を確保します。
"""

from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel

# ジェネリック型変数
T = TypeVar('T')

class ErrorResponse(BaseModel):
    """APIエラーレスポンスモデル"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class PaginationMeta(BaseModel):
    """ページネーション情報"""
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int

class PaginatedResponse(BaseModel, Generic[T]):
    """ページネーション付きのレスポンスモデル"""
    items: List[T]
    meta: PaginationMeta

class ApiResponse(BaseModel, Generic[T]):
    """統一APIレスポンスモデル

    全てのAPIレスポンスはこの形式で返されます。
    success: 処理が成功したかどうかを示す真偽値
    data: 成功時のレスポンスデータ（任意の型）
    error: エラー時のエラー情報
    """
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None

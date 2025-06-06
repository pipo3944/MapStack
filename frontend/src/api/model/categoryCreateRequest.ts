/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * MapStack API
 * AI学習プラットフォーム MapStack のバックエンドAPI
 * OpenAPI spec version: 0.1.0
 */
import type { CategoryCreateRequestDescription } from './categoryCreateRequestDescription';

/**
 * カテゴリの作成リクエストスキーマ
 */
export interface CategoryCreateRequest {
  code: string;
  title: string;
  description?: CategoryCreateRequestDescription;
  order_index: number;
  is_active?: boolean;
}

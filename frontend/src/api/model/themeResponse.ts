/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * MapStack API
 * AI学習プラットフォーム MapStack のバックエンドAPI
 * OpenAPI spec version: 0.1.0
 */
import type { ThemeResponseDescription } from './themeResponseDescription';

/**
 * テーマのレスポンススキーマ
 */
export interface ThemeResponse {
  id: string;
  category_id: string;
  code: string;
  title: string;
  description?: ThemeResponseDescription;
  order_index: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

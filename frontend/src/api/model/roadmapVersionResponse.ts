/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * MapStack API
 * AI学習プラットフォーム MapStack のバックエンドAPI
 * OpenAPI spec version: 0.1.0
 */
import type { RoadmapVersionResponsePublishedAt } from './roadmapVersionResponsePublishedAt';

/**
 * ロードマップバージョンのレスポンススキーマ
 */
export interface RoadmapVersionResponse {
  id: string;
  version: string;
  title: string;
  is_published: boolean;
  is_latest: boolean;
  published_at: RoadmapVersionResponsePublishedAt;
  created_at: string;
}

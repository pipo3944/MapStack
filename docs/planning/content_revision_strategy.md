# ドキュメントページ・学習コンテンツのリビジョン管理方針

## 1. 目的・背景

- MapStackではAIによる最新の学習コンテンツをユーザーに常に提供することを重視する。
- 学習コンテンツのドキュメントページは頻繁に更新され、内容の陳腐化を防ぐ必要がある。
- ユーザーが過去のバージョンや更新履歴も参照できる仕組みを持つことで、透明性と信頼性を高める。

## 2. 実現したいこと（要件）

- 各ドキュメントページごとに独立してリビジョン（バージョン）を管理したい
- ユーザーがフロントエンドから過去バージョンや履歴を参照できる
- 主要な更新内容や差分を分かりやすく表示できる
- ロードマップのノードは必要なドキュメントページへのリンクを持つ構造

## 3. ドキュメントとノードの関係性

- ドキュメントページは独立したエンティティとして存在する
- 各ロードマップノードは、関連するドキュメントページへのリンクを持つ
- 1つのドキュメントページが複数のノードから参照される可能性がある
- ドキュメントの更新はノードとは独立して行われる

## 4. 採用方針（ハイブリッドアプローチ概要）

- コンテンツ本体（ページ内容）はS3/MinIO等のオブジェクトストレージに保存
- メタデータ（バージョン、作成日時、要約など）はPostgreSQLで管理
- ノードとドキュメントの関連付けはDBで管理

## 5. 技術選定理由

- DBとストレージの役割分担でスケーラビリティとコスト効率を両立
- オブジェクトストレージは大容量・多バージョンの管理に強い
- DBはメタ管理とノード・ドキュメント間の関連性管理に最適

## 6. 実装方針

### DB設計
- `documents`テーブル：ドキュメントのメタ情報（タイトル、説明など）
- `document_revisions`テーブル：各ドキュメントのバージョン・メタ情報
- `node_document_links`テーブル：ノードとドキュメントの関連付け

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_revisions (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  version VARCHAR(20) NOT NULL,
  storage_key VARCHAR(255) NOT NULL,
  change_summary TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_by UUID,
  UNIQUE(document_id, version)
);

CREATE TABLE node_document_links (
  id UUID PRIMARY KEY,
  node_id UUID REFERENCES roadmap_nodes(id) ON DELETE CASCADE,
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  order_position INTEGER,
  relation_type VARCHAR(50) NOT NULL DEFAULT 'primary',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(node_id, document_id)
);
```

### ストレージ設計
- S3/MinIOに`documents/{document_id}/{version}/content.json`形式で保存
- JSONで本文・リソース・メタ情報を格納

### API設計
- ドキュメント情報取得API：`GET /api/v1/documents/{document_id}`
- 最新版コンテンツ取得：`GET /api/v1/documents/{document_id}/content`
- 特定バージョン取得：`GET /api/v1/documents/{document_id}/content/version/{version}`
- バージョン履歴取得：`GET /api/v1/documents/{document_id}/revisions`
- ノード関連ドキュメント取得：`GET /api/v1/nodes/{node_id}/documents`

### フロントエンド
- ドキュメントビューアーコンポーネント
- バージョン選択UI、履歴タイムライン、差分表示UI
- ノードページからの関連ドキュメントリンク表示

## 7. 将来的な検討事項

### 検索機能
- 将来的な拡張として全文検索の導入を検討
- 実装方法としては：
  1. DBに簡易的な検索用キーワード・抜粋を保存
  2. 必要に応じてElasticSearchやS3 Select等の導入

### その他の拡張余地
- 画像・動画など他メディアも同様にバージョン管理
- AIによる自動要約・変更サマリー生成
- 承認フローや下書き・公開管理

## 8. このドキュメントの更新方針

- 実装・運用の進捗や要件変更に応じて随時アップデート
- 重要な意思決定や設計変更は本ドキュメントに追記

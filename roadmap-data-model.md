# MapStack ロードマップデータモデル設計

このドキュメントは、MapStackのロードマップ機能におけるデータモデル設計のガイドラインです。
データベーススキーマ、API設計、フロントエンドインターフェースの定義を含みます。

## 1. データベーススキーマ設計

### カテゴリテーブル (categories)
カテゴリはロードマップの最上位分類です。

```sql
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ノードタイプマスターテーブル (node_types)
拡張可能なノードタイプの定義テーブルです。

```sql
CREATE TABLE node_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 初期データ
INSERT INTO node_types (code, title, description, color) VALUES
('primary', '主要技術', '学習パスの主要な技術や概念', '#1E88E5'),
('secondary', '基本スキル', '主要技術の詳細や基本的なスキル', '#FFE082'),
('recommended', '推奨スキル', '習得が推奨されるスキル', '#C8E6C9'),
('optional', 'オプション', '必須ではないが役立つスキル', '#DDDDDD');
```

### リソースタイプマスターテーブル (resource_types)
拡張可能なリソースタイプの定義テーブルです。

```sql
CREATE TABLE resource_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 初期データ
INSERT INTO resource_types (code, title, description, icon) VALUES
('article', '記事', 'ブログ記事やチュートリアル', 'file-text'),
('video', '動画', '動画コンテンツやスクリーンキャスト', 'video'),
('course', 'コース', 'オンラインコースや体系的な学習', 'book-open'),
('book', '書籍', '書籍や電子書籍', 'book'),
('docs', 'ドキュメント', '公式ドキュメントやリファレンス', 'bookmark');
```

### 難易度レベルマスターテーブル (skill_levels)
拡張可能な難易度レベルの定義テーブルです。

```sql
CREATE TABLE skill_levels (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 初期データ
INSERT INTO skill_levels (code, title, description) VALUES
('beginner', '初級', '基本的な知識や初めて学ぶ方向け'),
('intermediate', '中級', '基礎的な理解がある方向け'),
('advanced', '上級', '高度な知識や経験がある方向け');
```

### 進捗ステータスマスターテーブル (progress_statuses)
拡張可能な進捗ステータスの定義テーブルです。

```sql
CREATE TABLE progress_statuses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 初期データ
INSERT INTO progress_statuses (code, title, description, color) VALUES
('not-started', '未着手', 'まだ学習を開始していない状態', '#BBBBBB'),
('in-progress', '学習中', '現在学習を進めている状態', '#FFC107'),
('completed', '完了', '学習を完了した状態', '#4CAF50'),
('skipped', 'スキップ', '学習をスキップした状態', '#9E9E9E');
```

### テーマテーブル (themes)
テーマはカテゴリ内のサブカテゴリです。

```sql
CREATE TABLE themes (
    id VARCHAR(50) PRIMARY KEY,
    category_id VARCHAR(50) NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ロードマップテーブル (roadmaps)
ロードマップはテーマに紐づく学習パスの全体構造です。

```sql
CREATE TABLE roadmaps (
    id VARCHAR(50) PRIMARY KEY,
    theme_id VARCHAR(50) NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    version VARCHAR(20) NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ロードマップバージョンテーブル (roadmap_versions)
ロードマップの構造的変更のバージョン履歴です。

```sql
CREATE TABLE roadmap_versions (
    id SERIAL PRIMARY KEY,
    roadmap_id VARCHAR(50) NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    changes TEXT[] NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ノードテーブル (nodes)
ノードはロードマップ内の学習項目です。

```sql
CREATE TABLE nodes (
    id VARCHAR(50) PRIMARY KEY,
    roadmap_id VARCHAR(50) NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    node_type_code VARCHAR(50) NOT NULL REFERENCES node_types(code),
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    version VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ノード変更履歴テーブル (node_change_history)
個々のノードの変更履歴を記録します。

```sql
CREATE TABLE node_change_history (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    change_date TIMESTAMP WITH TIME ZONE NOT NULL,
    change_description TEXT NOT NULL,
    previous_version VARCHAR(20),
    new_version VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### エッジテーブル (edges)
エッジはノード間の接続を表します。

```sql
CREATE TABLE edges (
    id VARCHAR(50) PRIMARY KEY,
    roadmap_id VARCHAR(50) NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    source_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    target_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    source_handle VARCHAR(20),
    target_handle VARCHAR(20),
    edge_type VARCHAR(20),
    animated BOOLEAN DEFAULT FALSE,
    style JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### リソーステーブル (resources)
学習リソースはノードに紐づくコンテンツです。

```sql
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    url TEXT NOT NULL,
    resource_type_code VARCHAR(50) NOT NULL REFERENCES resource_types(code),
    description TEXT,
    skill_level_code VARCHAR(50) REFERENCES skill_levels(code),
    estimated_time VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### ユーザー進捗テーブル (user_progress)
ユーザーの学習進捗状況です。

```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    roadmap_id VARCHAR(50) NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_accessed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, roadmap_id)
);
```

### ノード進捗テーブル (node_progress)
各ノードに対するユーザーの進捗状況です。

```sql
CREATE TABLE node_progress (
    id SERIAL PRIMARY KEY,
    user_progress_id INTEGER NOT NULL REFERENCES user_progress(id) ON DELETE CASCADE,
    node_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    status_code VARCHAR(50) NOT NULL REFERENCES progress_statuses(code),
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_progress_id, node_id)
);
```

## 2. FastAPI モデル定義

Pydanticモデルを使用して、APIのデータモデルを定義します。

```python
# ベースモデル
class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True

# ノードタイプモデル
class NodeType(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

# リソースタイプモデル
class ResourceType(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

# スキルレベルモデル
class SkillLevel(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

# 進捗ステータスモデル
class ProgressStatus(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

# ノードモデル
class Node(BaseModel):
    id: str
    roadmap_id: str
    title: str
    description: Optional[str] = None
    node_type_code: str  # 参照コード
    node_type: Optional[NodeType] = None  # 展開時
    position_x: float
    position_y: float
    version: str
    created_at: datetime
    updated_at: datetime

# リソースモデル
class Resource(BaseModel):
    id: int
    node_id: str
    title: str
    url: str
    resource_type_code: str  # 参照コード
    resource_type: Optional[ResourceType] = None  # 展開時
    description: Optional[str]
    skill_level_code: Optional[str]  # 参照コード
    skill_level: Optional[SkillLevel] = None  # 展開時
    estimated_time: Optional[str]
    created_at: datetime
    updated_at: datetime

# ロードマップモデル（完全なデータを含む）
class Roadmap(BaseModel):
    id: str
    theme_id: str
    title: str
    description: Optional[str]
    version: str
    nodes: List[Node]
    edges: List[Edge]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

# ロードマップバージョンモデル
class RoadmapVersion(BaseModel):
    id: int
    roadmap_id: str
    version: str
    changes: List[str]
    published_at: datetime
    created_at: datetime

# ユーザー進捗モデル
class UserProgress(BaseModel):
    id: int
    user_id: str
    roadmap_id: str
    started_at: datetime
    last_accessed_at: datetime
    created_at: datetime
    updated_at: datetime

# ノード進捗モデル
class NodeProgress(BaseModel):
    id: int
    user_progress_id: int
    node_id: str
    status_code: str  # 参照コード
    status: Optional[ProgressStatus] = None  # 展開時
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

## 3. API エンドポイント設計

### カテゴリ関連
- `GET /api/categories` - カテゴリ一覧取得
- `GET /api/categories/{category_id}` - 特定カテゴリの取得

### テーマ関連
- `GET /api/categories/{category_id}/themes` - カテゴリに紐づくテーマ一覧取得
- `GET /api/themes/{theme_id}` - 特定テーマの取得

### ロードマップ関連
- `GET /api/themes/{theme_id}/roadmap` - テーマに紐づくロードマップ取得
- `GET /api/roadmaps/{roadmap_id}` - 特定ロードマップの取得
- `GET /api/roadmaps/{roadmap_id}/versions` - ロードマップのバージョン履歴取得

### ノード関連
- `GET /api/nodes/{node_id}` - 特定ノードの詳細取得
- `GET /api/nodes/{node_id}/history` - ノードの変更履歴取得
- `GET /api/nodes/{node_id}/resources` - ノードに紐づくリソース取得

### ユーザー進捗関連
- `GET /api/users/{user_id}/progress/{roadmap_id}` - ユーザーのロードマップ進捗取得
- `PATCH /api/users/{user_id}/progress/{roadmap_id}/nodes/{node_id}` - ノード進捗状況更新
- `GET /api/users/{user_id}/roadmaps/{roadmap_id}/updates` - 前回アクセス以降の更新確認

## 4. フロントエンドの型定義 (TypeScript)

```typescript
// マスターデータの基本型
interface BaseMaster {
  code: string;
  title: string;
  description?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

// ノードタイプ型
interface NodeType extends BaseMaster {
  color?: string;
}

// リソースタイプ型
interface ResourceType extends BaseMaster {
  icon?: string;
}

// スキルレベル型
interface SkillLevel extends BaseMaster {
}

// 進捗ステータス型
interface ProgressStatus extends BaseMaster {
  color?: string;
}

// ノード型
interface RoadmapNode {
  id: string;
  roadmapId: string;
  title: string;
  description?: string;
  nodeTypeCode: string;
  nodeType?: NodeType;  // 展開時
  position: {
    x: number;
    y: number;
  };
  version: string;
  createdAt: string;
  updatedAt: string;
  resources?: Resource[];
}

// リソース型
interface Resource {
  id: number;
  nodeId: string;
  title: string;
  url: string;
  resourceTypeCode: string;
  resourceType?: ResourceType;  // 展開時
  description?: string;
  skillLevelCode?: string;
  skillLevel?: SkillLevel;  // 展開時
  estimatedTime?: string;
  createdAt: string;
  updatedAt: string;
}

// ノード進捗型
interface NodeProgress {
  id: number;
  userProgressId: number;
  nodeId: string;
  statusCode: string;
  status?: ProgressStatus;  // 展開時
  completedAt?: string;
  createdAt: string;
  updatedAt: string;
}
```

## 5. バージョン管理のルール

1. **ロードマップ全体のバージョン**
   - セマンティックバージョニング（x.y.z）を採用
   - x: 構造的大幅変更（ノードの追加削除、関係性の変更）
   - y: 既存ノード内容の大幅更新
   - z: 軽微な修正

2. **ノード単位のバージョン**
   - 各ノードも独自にセマンティックバージョニングを持つ
   - ノードの内容が更新されると、適切なバージョン番号がインクリメント
   - 変更履歴テーブルに更新内容を記録

3. **更新通知**
   - ユーザーが最後にアクセスした時点と比較して、更新があったノードをハイライト
   - ロードマップページ表示時に、全体の更新状況を通知

## 6. サンプルデータ

```sql
-- カテゴリサンプル
INSERT INTO categories (id, title, description, order_index)
VALUES ('web-development', 'Web開発', 'ウェブ開発に関するロードマップ', 1);

-- テーマサンプル
INSERT INTO themes (id, category_id, title, description, order_index)
VALUES ('frontend', 'web-development', 'フロントエンド開発', 'フロントエンド開発のスキルセット', 1);

-- ロードマップサンプル
INSERT INTO roadmaps (id, theme_id, title, description, version, published_at)
VALUES ('frontend-roadmap', 'frontend', 'フロントエンド開発ロードマップ',
        'HTML、CSS、JavaScriptからモダンフレームワークまでのフロントエンド開発学習パス',
        '1.0.0', NOW());

-- ノードサンプル
INSERT INTO nodes (id, roadmap_id, title, description, node_type_code, position_x, position_y, version)
VALUES
('internet', 'frontend-roadmap', 'インターネット', 'インターネットの仕組み、ブラウザの動作原理、HTTP/HTTPSプロトコルについて学ぶ', 'primary', 250, 0, '1.0.0'),
('html', 'frontend-roadmap', 'HTML', 'HTMLの基本構造、セマンティックHTML、フォーム、アクセシビリティについて学ぶ', 'primary', 100, 100, '1.0.0');

-- エッジサンプル
INSERT INTO edges (id, roadmap_id, source_id, target_id, source_handle, target_handle, edge_type, animated)
VALUES
('internet-to-html', 'frontend-roadmap', 'internet', 'html', 'bottom', 'top', 'smoothstep', false);

-- リソースサンプル
INSERT INTO resources (node_id, title, url, resource_type_code, description, skill_level_code)
VALUES
('internet', 'インターネットの仕組み入門', 'https://developer.mozilla.org/ja/docs/Learn/Common_questions/How_does_the_Internet_work', 'article', 'MDNによるインターネットの仕組みの解説', 'beginner');
```

## 7. 次のステップ

1. PostgreSQLにスキーマを作成
2. FastAPIでAPIエンドポイントを実装
3. フロントエンドをAPIに接続
4. ユーザー進捗機能の実装
5. バージョン管理とその通知機能の実装

このデータモデルは初期設計であり、実装過程で調整が必要になる可能性があります。実装中の学びに基づいて、継続的に改善していきましょう。

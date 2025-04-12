# MapStack 技術スタック

---
title: 技術スタック
importance: high
last_updated: 2025-04-04
for_ai_assistant: このドキュメントはMapStackで採用する技術スタックと開発環境について説明しています。実装時は、ここで定義された技術と設定に従ってください。
---

## 採用技術一覧と選定理由

### フロントエンド

| 技術 | 選定理由 |
|------|------------|----------|
| **Next.js** | • サーバーサイドレンダリング/静的生成によるパフォーマンスとSEO最適化<br>• App Routerによるシンプルなルーティング<br>• React Server Componentsによる効率的なレンダリング<br>• APIルートによるBFFパターンの実装<br>• 豊富なエコシステムとコミュニティサポート |
| **TypeScript** | • 型安全性による開発効率とエラー検出の向上<br>• IDEでの自動補完とリファクタリングのサポート<br>• コードベースの保守性と拡張性の向上<br>• チーム間の明確なインターフェース定義 |
| **Tailwind CSS** | • ユーティリティファーストアプローチによる高速な開発<br>• 一貫したデザインシステムの実装が容易<br>• カスタマイズ性の高さ<br>• 小さなバンドルサイズによるパフォーマンス向上<br>• レスポンシブデザインの簡素な実装 |
| **Zustand** | • シンプルで学習コストが低い状態管理<br>• React Hooksとの高い互換性<br>• サーバーコンポーネントとの親和性<br>• 最小限のボイラープレートコード<br>• コンポーネント外からのアクセスが容易 |
| **React Hook Form** | • パフォーマンスに優れたフォーム管理<br>• Uncontrolled Componentsによる再レンダリング最小化<br>• Zod/Yupとの統合による型安全なバリデーション<br>• カスタムバリデーションの容易な実装 |
| **SWR** | • データフェッチの自動キャッシュと再検証<br>• リアルタイム更新とオフライン対応<br>• ページング、無限スクロールなどの組み込みサポート<br>• エラーハンドリングと再試行の自動化 |
| **Monaco Editor** | • VSCodeと同じエディタエンジン<br>• インテリセンスと構文ハイライト<br>• 高度なコード編集機能<br>• 多言語サポート<br>• カスタマイズ性の高さ |

### バックエンド

| 技術 | 選定理由 |
|------|------------|----------|
| **FastAPI** | • 高速なパフォーマンス（StarlettePythonフレームワーク中最速レベル）<br>• OpenAPI仕様による自動ドキュメント生成<br>• Pydanticによる型検証とシリアライゼーション<br>• 非同期サポート（async/await）<br>• Pythonの学習価値とAI関連ライブラリの豊富さ |
| **SQLAlchemy** | • 柔軟なORMとSQL式言語<br>• トランザクション管理<br>• 複雑なクエリの構築と最適化<br>• マイグレーション管理（Alembic）<br>• マルチデータベース対応 |
| **Pydantic** | • データバリデーションとパース<br>• TypeScriptとの型共有が容易<br>• スキーマ生成とドキュメント自動化<br>• 設定管理の単純化<br>• 高速なパフォーマンス |
| **Pytest** | • シンプルで表現力の高いテスト構文<br>• フィクスチャによる依存性注入とセットアップ<br>• 拡張可能なプラグインシステム<br>• パラメータ化テストのサポート<br>• 高度なアサーション機能 |
| **Celery** | • 分散型タスクキュー<br>• スケジュールタスクのサポート<br>• リトライとエラーハンドリングの組み込み<br>• モニタリングツール（Flower）<br>• 様々なブローカーとの互換性（Redis, RabbitMQ） |

### データベースとストレージ

| 技術 | 選定理由 |
|------|------------|----------|
| **PostgreSQL** | • 高度なリレーショナルデータ機能<br>• JSONBによる柔軟なデータ構造（半構造化データ）<br>• 全文検索機能<br>• 高い信頼性と長期サポート<br>• 拡張機能の豊富さ |
| **Redis** | • 高速インメモリキャッシュ<br>• セッション管理<br>• レート制限実装<br>• パブサブ機能<br>• リーダーボードなどのリアルタイム機能 |
| **Amazon S3** / **Cloudflare R2** | • スケーラブルなオブジェクトストレージ<br>• ユーザーアップロードの安全な保存<br>• CDN統合によるコンテンツ配信の最適化<br>• バックアップと永続化<br>• コスト効率の良さ |

### AI・ML関連

| 技術 | 選定理由 |
|------|----------|
| **OpenAI API** | • 高品質なAIレスポンス生成<br>• 質問応答、コードレビュー機能<br>• コードの自動生成と補完<br>• コンテンツパーソナライゼーション<br>• 使いやすいAPI |
| **LangChain** | • LLMとのインタラクション簡素化<br>• コンテキスト管理とRAG実装<br>• 複雑なAIワークフローの構築<br>• 外部ツールとの統合<br>• プロンプトエンジニアリング支援 |
| **Vector DB (Pinecone/Chroma)** | • セマンティック検索機能<br>• 類似コンテンツの発見<br>• パーソナライズされた推奨<br>• コンテンツ理解の強化<br>• RAG（検索拡張生成）の基盤 |

### インフラストラクチャ

| 技術 | 選定理由 |
|------|----------|
| **Vercel** | • Next.jsとの完璧な互換性<br>• GitHubとの簡単な統合とCI/CD<br>• エッジでのサーバーレス関数<br>• グローバルCDN<br>• PoC段階での低コストと高速なイテレーション |
| **Docker** | • 開発と本番環境の一貫性<br>• マイクロサービスのコンテナ化<br>• 依存関係の分離<br>• CI/CDパイプラインとの統合<br>• スケーリングとオーケストレーションの容易さ |
| **AWS (将来的)** | • 高いスケーラビリティと信頼性<br>• 豊富なマネージドサービス（RDS, ECS, Lambda）<br>• グローバルなインフラストラクチャ<br>• 成熟したセキュリティ機能<br>• 将来的な成長に対応 |

### 開発ツール

| 技術 | 選定理由 |
|------|----------|
| **Git / GitHub** | • バージョン管理とコラボレーション<br>• PRベースの開発ワークフロー<br>• GitHub Actionsによる自動化<br>• コードレビュープロセス<br>• イシュートラッキングとプロジェクト管理 |
| **ESLint / Prettier** | • コード品質の向上<br>• 一貫したコーディングスタイル<br>• 潜在的なバグの早期発見<br>• 自動フォーマット化<br>• チーム間の標準化 |
| **Husky / lint-staged** | • コミット前の自動リントとテスト<br>• CI前の問題検出<br>• 品質ゲートの確保<br>• チーム全体での一貫した品質管理 |
| **Vitest / Testing Library** | • ユニットテストとインテグレーションテスト<br>• モックとスパイ機能<br>• スナップショットテスト<br>• 並列テスト実行<br>• アクセシビリティテスト |

## 開発環境セットアップ手順

### 前提条件

- Git 
- Node.js 
- Python 
- Docker Desktop
- VS Code（推奨エディタ）

### フロントエンド開発環境のセットアップ

1. **リポジトリのクローン**

```bash
git clone https://github.com/mapstack/mapstack.git
cd mapstack
```

2. **フロントエンド依存関係のインストール**

```bash
cd frontend
npm install
```

3. **環境変数の設定**

```bash
cp .env.example .env.local
```
`.env.local`ファイルを編集し、必要な環境変数を設定します。

4. **開発サーバーの起動**

```bash
npm run dev
```

アプリケーションは `http://localhost:3000` で実行されます。

### バックエンド開発環境のセットアップ

1. **Python環境の準備**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
```

2. **環境変数の設定**

```bash
cp .env.example .env
```
`.env`ファイルを編集し、必要な環境変数を設定します。

3. **データベースの起動（Docker）**

```bash
docker-compose up -d postgres redis
```

4. **データベースのマイグレーション**

```bash
alembic upgrade head
```

5. **開発サーバーの起動**

```bash
uvicorn app.main:app --reload
```

APIは `http://localhost:8000` で実行され、SwaggerドキュメントはURL `/docs` でアクセスできます。

### 統合開発環境

全体のシステムをDockerで起動することも可能です：

```bash
docker-compose up -d
```

これにより、フロントエンド、バックエンド、PostgreSQL、Redis、Celeryワーカーを含むすべてのサービスが起動します。

### VS Code拡張機能（推奨）

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- Python
- Pylance
- Docker
- GitLens
- REST Client

## デプロイパイプライン設計

### 開発ワークフロー

1. **ブランチ戦略**
   - `main`: 本番環境反映用のブランチ
   - `develop`: 開発環境反映用のブランチ
   - `feature/*`: 機能開発用のブランチ
   - `bugfix/*`: バグ修正用のブランチ
   - `release/*`: リリース準備用のブランチ

2. **プルリクエストフロー**
   - Feature branchから`develop`へのPR
   - PRはコードレビュー必須
   - CIパイプラインのテスト通過が必要
   - マージ後、自動的に開発環境へデプロイ

3. **リリースフロー**
   - `develop`から`release/vX.Y.Z`へのブランチ作成
   - リリース候補のテスト実施
   - 問題がなければ`main`へのPR作成
   - マージ後、自動的に本番環境へデプロイ

### CI/CDパイプライン

#### フロントエンド（GitHub Actions + Vercel）

```yaml
# .github/workflows/frontend.yml
name: Frontend Pipeline

on:
  push:
    branches: [develop, main]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [develop, main]
    paths:
      - 'frontend/**'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'frontend/package-lock.json'
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Lint
        run: cd frontend && npm run lint
      
      - name: Type check
        run: cd frontend && npm run type-check
      
      - name: Test
        run: cd frontend && npm run test
  
  # Vercelへのデプロイは、Vercelの連携により自動的に実行
```

#### バックエンド（GitHub Actions + DockerHub + AWS）

```yaml
# .github/workflows/backend.yml
name: Backend Pipeline

on:
  push:
    branches: [develop, main]
    paths:
      - 'backend/**'
  pull_request:
    branches: [develop, main]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
          cache-dependency-path: 'backend/requirements.txt'
      
      - name: Install dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint
        run: |
          cd backend
          flake8 .
          mypy .
      
      - name: Test
        run: |
          cd backend
          pytest --cov=app tests/
  
  build-and-push:
    needs: test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: |
            mapstack/backend:latest
            mapstack/backend:${{ github.sha }}
```

### インフラストラクチャ（Terraform）

```hcl
# main.tf（一部抜粋）
provider "aws" {
  region = "ap-northeast-1"
}

# VPC設定
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "mapstack-vpc"
    Environment = var.environment
  }
}

# データベース
resource "aws_db_instance" "postgres" {
  identifier           = "mapstack-db-${var.environment}"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  allocated_storage    = 20
  max_allocated_storage = 100
  name                 = "mapstack"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  backup_retention_period = 7
  skip_final_snapshot  = var.environment != "production"
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  
  tags = {
    Name = "mapstack-db"
    Environment = var.environment
  }
}

# ECS設定
resource "aws_ecs_cluster" "main" {
  name = "mapstack-cluster-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "backend" {
  name            = "mapstack-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = var.backend_instances
  launch_type     = "FARGATE"
  
  network_configuration {
    security_groups = [aws_security_group.backend.id]
    subnets         = aws_subnet.private.*.id
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = 8000
  }
}
```

### 監視とロギング

- AWS CloudWatch: メトリクス監視、ログ集約
- Sentry: エラートラッキング
- Datadog（将来的）: 高度なモニタリングとAPM

### バックアップ戦略

- データベース: 自動日次バックアップ、ポイントインタイムリカバリ（PITR）
- ユーザーアップロードファイル: S3のクロスリージョンレプリケーション
- 構成管理: Terraformステートファイルのバージョン管理

---

*このドキュメントは進行中のプロジェクトの技術選定とインフラストラクチャ設計を示すものです。実際の実装では、要件や制約に応じて調整される場合があります。*

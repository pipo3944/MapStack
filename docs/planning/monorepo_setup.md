# MapStack モノレポ環境セットアップガイド

---
title: モノレポ環境セットアップガイド
importance: high
last_updated: 2025-04-04
for_ai_assistant: このドキュメントはMapStackのモノレポ環境のセットアップと管理方法について説明しています。実装時はこのガイドラインに従ってください。
---

## モノレポ構造

MapStackプロジェクトは単一のリポジトリ（モノレポ）でフロントエンド、バックエンド、インフラを管理します。この構造により、次のメリットを得られます：

- 統一された開発環境
- シンプルな依存関係管理
- 一貫したコード規約とテスト
- 効率的なCI/CDパイプライン

### ディレクトリ構造

```
mapstack/
├── docker-compose.yml   # ルートにDockerComposeファイル配置
├── package.json         # ルートパッケージ設定（スクリプト、dev依存関係等）
├── .github/             # GitHub Actions設定
├── frontend/            # Next.jsフロントエンド
│   ├── package.json     # フロントエンド依存関係
│   └── ...
├── backend/             # FastAPIバックエンド
│   ├── Dockerfile       # バックエンド用Dockerfile
│   ├── requirements.txt # Pythonパッケージ依存関係
│   └── ...
├── db/                  # データベース関連ファイル
│   ├── init/            # 初期化スクリプト
│   └── data/            # ボリュームマウント用
└── docs/                # プロジェクトドキュメント
    └── ...
```

## ルートpackage.json

ルートディレクトリの`package.json`にはプロジェクト全体を管理するためのスクリプトが設定されています。これにより、開発者は単一のコマンドで環境のセットアップや起動が可能になります。

```json
{
  "name": "mapstack",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "install-all": "npm install && npm run install:frontend && npm run install:backend",
    "install:frontend": "cd frontend && npm install",
    "install:backend": "cd backend && pip install -r requirements.txt",
    
    "dev": "npm-run-all --parallel dev:frontend dev:docker",
    "dev:frontend": "cd frontend && npm run dev",
    "dev:backend": "cd backend && uvicorn app.main:app --reload",
    "dev:docker": "docker-compose up",
    
    "build": "npm-run-all --parallel build:frontend build:backend",
    "build:frontend": "cd frontend && npm run build",
    "build:backend": "cd backend && echo 'Backend build steps'",
    
    "test": "npm-run-all --parallel test:frontend test:backend",
    "test:frontend": "cd frontend && npm test",
    "test:backend": "cd backend && pytest",
    
    "lint": "npm-run-all --parallel lint:frontend lint:backend",
    "lint:frontend": "cd frontend && npm run lint",
    "lint:backend": "cd backend && flake8",
    
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down",
    "docker:build": "docker-compose build",
    "docker:logs": "docker-compose logs -f",
    
    "db:up": "docker-compose up -d db redis",
    "db:migrate": "docker-compose exec backend alembic upgrade head",
    "db:seed": "docker-compose exec backend python -m app.scripts.seed_data",
    
    "clean": "npm-run-all --parallel clean:frontend clean:backend",
    "clean:frontend": "cd frontend && rm -rf node_modules .next",
    "clean:backend": "cd backend && rm -rf venv __pycache__ .pytest_cache"
  },
  "devDependencies": {
    "npm-run-all": "^4.1.5",
    "concurrently": "^7.6.0"
  }
}
```

## docker-compose.yml

ルートディレクトリに以下のような`docker-compose.yml`を配置します：

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/mapstack
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  db:
    image: postgres:14
    ports:
      - "5432:5432"
    volumes:
      - ./db/data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=mapstack

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

## バックエンドのDockerfile

`backend/Dockerfile`には以下のような内容を記述します：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
```

## 開発環境のセットアップ

### 初回セットアップ

プロジェクトのセットアップには、以下のコマンドを実行します：

```bash
# リポジトリのクローン
git clone https://github.com/mapstack/mapstack.git
cd mapstack

# フロントエンド依存関係のインストール
npm run install:frontend

# Dockerイメージのビルドと起動
npm run docker:build
npm run docker:up

# または一括で開発環境起動
npm run dev
```

### 開発サーバーの起動

以下のコマンドで、フロントエンド、バックエンド、およびデータベースを含む開発環境が起動します：

```bash
npm run dev
```

このコマンド一つで：
- Next.jsフロントエンド（http://localhost:3000）
- FastAPIバックエンド（http://localhost:8000、Dockerコンテナ内）
- PostgreSQLデータベース（Dockerコンテナ内）
- Redisキャッシュ（Dockerコンテナ内）

がすべて起動します。

### 個別サービスの起動

必要に応じて各サービスを個別に起動することも可能です：

```bash
# フロントエンドのみ起動
npm run dev:frontend

# バックエンドとデータベースを起動（Docker経由）
npm run docker:up

# データベースのみ起動
npm run db:up
```

## Docker環境の操作

### ログの確認

コンテナのログを確認するには：

```bash
npm run docker:logs
```

特定のサービスのログのみを確認する場合：

```bash
docker-compose logs -f backend
docker-compose logs -f db
```

### コンテナ内でのコマンド実行

マイグレーションやその他のコマンドをコンテナ内で実行する場合：

```bash
# マイグレーション実行
npm run db:migrate

# バックエンドコンテナ内でコマンド実行
docker-compose exec backend python -m app.scripts.other_command
```

### コンテナの停止

開発環境を停止するには：

```bash
npm run docker:down
```

## 新しいパッケージの追加

### フロントエンドへのパッケージ追加

```bash
cd frontend
npm install パッケージ名
```

### バックエンドへのパッケージ追加

バックエンドにパッケージを追加する際は、Dockerコンテナの再ビルドが必要です：

```bash
# ローカル環境に依存関係を追加
cd backend
pip install パッケージ名
pip freeze > requirements.txt

# Dockerコンテナを再ビルド
npm run docker:build
```

## CI/CD統合

ルートディレクトリのスクリプトはGitHub Actionsなどの
CI/CDパイプラインとシームレスに統合できます：

```yaml
# .github/workflows/ci.yml
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Docker
        uses: docker/setup-buildx-action@v1
      - name: Build and test
        run: |
          npm run install:frontend
          npm run docker:build
          npm run lint:frontend
          npm run test:frontend
          npm run build:frontend
          docker-compose run backend pytest
```

## トラブルシューティング

### よくある問題と解決策

1. **Docker関連の問題**
   ```bash
   # コンテナをクリーンアップ
   docker-compose down -v
   docker-compose build --no-cache
   npm run docker:up
   ```

2. **データベース接続エラー**
   ```bash
   # DBコンテナのログを確認
   docker-compose logs db
   
   # DBコンテナを再起動
   docker-compose restart db
   ```

3. **バックエンドコードの変更が反映されない**
   ```bash
   # バックエンドコンテナを再起動
   docker-compose restart backend
   ```

4. **開発サーバーの競合**
   他のプロセスがポートを使用している場合は、ポートマッピングを変更：
   ```yaml
   # docker-compose.yml内のポート設定を変更
   ports:
     - "8001:8000"  # ホスト側:コンテナ側
   ```

## ベストプラクティス

1. **Docker開発環境の効率的利用**
   - ボリュームマウントを活用してコードの変更をリアルタイムに反映
   - ホットリロードを有効にして開発サイクルを高速化
   - 環境変数を適切に管理（.envファイル、Docker Composeの環境変数）

2. **インクリメンタル開発**
   - フロントエンドとバックエンドの変更を小さな単位でコミット
   - APIの変更は互換性を維持

3. **一貫したコード規約**
   - ESLint、Prettier、flake8を使用した統一的なコードスタイル
   - すべてのコンポーネントでの型安全性（TypeScript、Pydantic）

4. **テスト駆動開発**
   - 新機能は適切なテストカバレッジを伴うこと
   - `npm run test`で全テストを実行可能に

---

*このドキュメントはプロジェクトの進行に伴い更新されます。最新のモノレポ構造や環境設定については、このドキュメントを参照してください。* 
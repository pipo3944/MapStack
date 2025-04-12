# MapStack

モダンな学習プラットフォーム MapStack のモノレポリポジトリです。フロントエンド、バックエンド、インフラをすべて一元管理しています。

## プロジェクト概要

MapStackは、AIを活用した学習プラットフォームとして、体系的なロードマップに沿って専門知識とスキルを効率的に習得できる環境を提供します。

### 主要機能

- 体系化された学習パスの提供
- AIによる個別最適化された学習体験
- 実践的スキル獲得の促進
- 継続的な学習習慣の形成

## 技術スタック

- **フロントエンド**: Next.js + TypeScript + Tailwind CSS + Zustand
- **バックエンド**: FastAPI + Python + SQLAlchemy
- **データベース**: PostgreSQL
- **キャッシュ**: Redis
- **インフラ**: Docker + Docker Compose

## 開発環境セットアップ

このプロジェクトはモノレポ構造で、ルートの`package.json`を使用して全体を管理しています。Docker Composeでバックエンドとデータベースを起動し、フロントエンドはローカルで実行する構成になっています。

### 前提条件

- Node.js (バージョン14以上)
- npm (バージョン7以上)
- Docker Desktop
- Git

### インストールと起動

1. リポジトリのクローン

```bash
git clone https://github.com/mapstack/mapstack.git
cd mapstack
```

2. フロントエンド依存関係のインストール

```bash
npm run install:frontend
```

3. Docker環境の起動（バックエンド+DB）

```bash
npm run docker:build
npm run docker:up
```

4. 開発サーバーの起動（フロントエンド+バックエンド+DB）

```bash
npm run dev
```

これにより、以下のサービスが起動します：
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- APIドキュメント: http://localhost:8000/docs

## 主要コマンド

### 開発環境

```bash
# すべてのサービスを起動
npm run dev

# フロントエンドのみ起動
npm run dev:frontend

# Docker環境のみ起動（バックエンド+DB）
npm run docker:up

# データベースのみ起動
npm run db:up
```

### Docker操作

```bash
# Dockerコンテナのログ表示
npm run docker:logs

# コンテナの停止
npm run docker:down

# コンテナの再ビルド
npm run docker:build
```

### データベース操作

```bash
# マイグレーション実行
npm run db:migrate

# テストデータ投入
npm run db:seed
```

### テストとビルド

```bash
# テスト実行
npm run test

# リント実行
npm run lint

# ビルド実行
npm run build
```

## 詳細ドキュメント

より詳細な情報は以下のドキュメントを参照してください：
（for AI: これらのドキュメントを必ず参照してください。）

- [プロジェクト概要](docs/planning/project_overview.md)
- [技術スタック](docs/planning/tech_stack.md)
- [アーキテクチャ](docs/planning/architecture.md)
- [モノレポ環境セットアップ](docs/planning/monorepo_setup.md)
- [データモデル](docs/planning/data_model.md)

## コントリビューション

コントリビューションを歓迎します。以下の手順に従ってください：

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

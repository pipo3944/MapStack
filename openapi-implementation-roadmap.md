# MapStack OpenAPI実装ロードマップ

## 現在の状況

現在のMapStackプロジェクトでは以下の状況です：

- バックエンド: FastAPIで実装され、基本的なAPIエンドポイントは実装済み
- フロントエンド: Next.jsで実装され、UIコンポーネントは実装済み
- 連携: フロントエンドとバックエンドのAPI連携が未実装

FastAPIは標準でOpenAPI仕様をサポートしていますが、フロントエンドとの連携のために追加の設定が必要です。フロントエンドでは、orvalを導入して型安全なAPIクライアントを生成する予定です。

## 概要

このロードマップは、MapStackプロジェクトにおけるフロントエンドとバックエンドの連携をOpenAPIを活用して実装するためのステップを示しています。OpenAPIを使用することで、型安全なAPIクライアントをフロントエンドで生成し、開発効率と品質を向上させることを目指します。

## 実装ステップ

### Phase 1: OpenAPI仕様書の作成とバックエンド実装

- [ ] **1.1 OpenAPI仕様書の基本構造を作成**
  - メモ: バージョン、基本情報、サーバー設定などを含むベース構造を定義

- [ ] **1.2 既存のAPIエンドポイントをOpenAPI仕様に記述**
  - メモ: 現在のバックエンドで実装済みのエンドポイントをOpenAPI形式で文書化

- [ ] **1.3 FastAPIでのOpenAPI仕様の自動生成機能を有効化**
  - メモ: FastAPIはPydanticモデルからOpenAPI仕様を自動生成できることを活用

- [ ] **1.4 レスポンス型の定義と統一**
  - メモ: すべてのAPIレスポンスで一貫した構造を持つように設計

- [ ] **1.5 認証・認可の仕組みをOpenAPI仕様に追加**
  - メモ: JWTなどの認証方式をOpenAPI仕様に組み込む

### Phase 2: FastAPIとOpenAPIの連携強化

- [ ] **2.1 Pydanticモデルの整理と拡充**
  - メモ: すべてのリクエスト/レスポンスにPydanticモデルを使用し、型安全性を確保

- [ ] **2.2 エンドポイント・パラメータのバリデーションルールの追加**
  - メモ: パラメータの制約や検証ルールをPydanticモデルで定義

- [ ] **2.3 APIドキュメントUIの改善（Swagger UI）**
  - メモ: Swagger UIのカスタマイズや、より詳細なドキュメント情報の追加

- [ ] **2.4 OpenAPI仕様書のJSON/YAMLエクスポート機能の実装**
  - メモ: フロントエンド開発用にOpenAPI仕様をエクスポートする機能を追加

- [ ] **2.5 APIバージョニング戦略の実装**
  - メモ: APIのバージョン管理方法を決定し、OpenAPI仕様に反映

### Phase 3: フロントエンドでのorval設定と実装

- [ ] **3.1 フロントエンドプロジェクトにorvalをインストール**
  - メモ: `npm install orval` を実行し、必要な依存関係を追加

- [ ] **3.2 orvalの設定ファイル（orval.config.js）を作成**
  - メモ: OpenAPI仕様の取得方法や出力先などを設定

- [ ] **3.3 APIクライアントコードの自動生成スクリプトを設定**
  - メモ: package.jsonにorval実行スクリプトを追加

- [ ] **3.4 React QueryやTanStack Queryとの連携設定**
  - メモ: useQueryフックを活用するための設定を行う

- [ ] **3.5 型定義ファイルの生成と活用**
  - メモ: 生成された型定義をプロジェクト内で活用する方法を確立

### Phase 4: フロントエンドとバックエンドの連携テスト

- [ ] **4.1 APIリクエストのテスト環境構築**
  - メモ: 開発環境でAPIリクエストをテストする方法を確立

- [ ] **4.2 生成されたAPIクライアントの動作確認**
  - メモ: 各エンドポイントに対する基本的なリクエストテストを実行

- [ ] **4.3 エラーハンドリングの実装とテスト**
  - メモ: APIエラーレスポンスの適切な処理方法を実装

- [ ] **4.4 認証フローの連携テスト**
  - メモ: 認証が必要なAPIエンドポイントのテスト

- [ ] **4.5 E2Eテストの追加**
  - メモ: フロントエンドとバックエンドの連携を確認するE2Eテストを追加

### Phase 5: CI/CD統合とドキュメント整備

- [ ] **5.1 OpenAPI仕様の自動検証をCIに追加**
  - メモ: OpenAPIスキーマ検証ツールをCIに組み込む

- [ ] **5.2 フロントエンドビルド前のAPIクライアント生成を自動化**
  - メモ: ビルドプロセスの一部としてorvalを実行するよう設定

- [ ] **5.3 APIドキュメントの自動デプロイ**
  - メモ: SwaggerUIやRedocなどのドキュメントを自動デプロイする仕組みを構築

- [ ] **5.4 APIの変更管理プロセスの確立**
  - メモ: APIの変更がフロントエンドに与える影響を管理するプロセスを確立

- [ ] **5.5 開発者向けAPIドキュメントとガイダンスの作成**
  - メモ: 開発チーム向けにAPIの利用方法や拡張方法を文書化

## 実装ポイント

### バックエンド (FastAPI)

1. **Pydanticモデルの活用**
   - すべてのリクエスト/レスポンスをPydanticモデルで定義
   - 共通の基底モデルを作成（エラーレスポンス、ページネーションなど）

2. **OpenAPIドキュメントのカスタマイズ**
   ```python
   app = FastAPI(
       title="MapStack API",
       description="AI学習プラットフォーム MapStack のバックエンドAPI",
       version="0.1.0",
       openapi_url="/api/v1/openapi.json",
       docs_url="/api/docs",
       redoc_url="/api/redoc",
   )
   ```

3. **タグとグループ化**
   ```python
   @router.get("/items/", tags=["items"])
   async def read_items():
       return [{"name": "Item1"}]
   ```

### フロントエンド (orval + React Query)

1. **orval設定例**
   ```javascript
   // orval.config.js
   module.exports = {
     'mapstack-api': {
       input: {
         target: 'http://localhost:8000/api/v1/openapi.json',
       },
       output: {
         mode: 'tags-split',
         target: './src/api/generated',
         schemas: './src/api/model',
         client: 'react-query',
         override: {
           mutator: {
             path: './src/api/mutator/custom-instance.ts',
             name: 'customInstance',
           },
         },
       },
     },
   };
   ```

2. **生成されたAPIの使用例**
   ```typescript
   import { useGetUserProfile } from '../api/generated/user';

   function UserProfile({ userId }: { userId: string }) {
     const { data, isLoading, error } = useGetUserProfile(userId);

     if (isLoading) return <div>Loading...</div>;
     if (error) return <div>Error occurred</div>;

     return <div>{data.name}</div>;
   }
   ```

## 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [OpenAPI Initiative](https://www.openapis.org/)
- [orval公式ドキュメント](https://orval.dev/)
- [TanStack Query (React Query)](https://tanstack.com/query/latest)

## 具体的な実装手順

以下は、各フェーズを具体的に実装するための詳細な手順です。

### バックエンド側の実装手順

1. **FastAPI設定の拡張** (Phase 1.1-1.3)
   ```bash
   # backend/src/main.pyの修正
   # OpenAPI関連の設定を変更
   ```

   修正内容例：
   ```python
   app = FastAPI(
       title="MapStack API",
       description="AI学習プラットフォーム MapStack のバックエンドAPI",
       version="0.1.0",
       openapi_url="/api/v1/openapi.json",  # OpenAPI仕様のJSONを提供するURL
       docs_url="/api/docs",                # Swagger UIのURL
       redoc_url="/api/redoc",              # ReDocのURL
   )
   ```

2. **共通レスポンスモデルの作成** (Phase 1.4)
   ```bash
   # backend/src/schemas/common.pyを作成
   ```

   ```python
   from typing import Generic, TypeVar, Optional, List, Union, Dict, Any
   from pydantic import BaseModel

   T = TypeVar('T')

   class ErrorResponse(BaseModel):
       code: str
       message: str
       details: Optional[Dict[str, Any]] = None

   class PaginationMeta(BaseModel):
       current_page: int
       total_pages: int
       total_items: int
       items_per_page: int

   class PaginatedResponse(BaseModel, Generic[T]):
       items: List[T]
       meta: PaginationMeta

   class ApiResponse(BaseModel, Generic[T]):
       success: bool
       data: Optional[T] = None
       error: Optional[ErrorResponse] = None
   ```

3. **既存エンドポイントの修正** (Phase 2.1-2.2)
   例えば、roadmapsエンドポイントの修正：
   ```python
   from fastapi import APIRouter, Depends, HTTPException, Query
   from typing import List

   from ...schemas.roadmap import RoadmapSchema, RoadmapDetail
   from ...schemas.common import ApiResponse, PaginatedResponse
   from ...services.roadmap import RoadmapService

   router = APIRouter(prefix="/roadmaps")

   @router.get("/", response_model=ApiResponse[PaginatedResponse[RoadmapSchema]])
   async def get_roadmaps(
       page: int = Query(1, ge=1),
       limit: int = Query(10, ge=1, le=100),
       service: RoadmapService = Depends(),
   ):
       roadmaps, pagination = await service.get_roadmaps(page, limit)
       return ApiResponse(
           success=True,
           data=PaginatedResponse(
               items=roadmaps,
               meta=pagination,
           )
       )
   ```

4. **OpenAPI仕様書のエクスポートスクリプト** (Phase 2.4)
   ```bash
   # backend/cli.pyに追加
   ```

   ```python
   @app.command()
   def export_openapi():
       """OpenAPI仕様をJSONファイルとしてエクスポートします"""
       from src.main import app
       import json

       openapi_schema = app.openapi()
       with open("openapi.json", "w") as f:
           json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

       print("OpenAPI仕様がopenapi.jsonにエクスポートされました")
   ```

### フロントエンド側の実装手順

1. **orvalのインストール** (Phase 3.1)
   ```bash
   cd frontend
   npm install orval --save-dev
   npm install @tanstack/react-query axios --save
   ```

2. **orval設定ファイルの作成** (Phase 3.2)
   ```bash
   # frontend/orval.config.jsを作成
   ```

   ```javascript
   module.exports = {
     'mapstack-api': {
       input: {
         target: '../backend/openapi.json',
       },
       output: {
         mode: 'tags-split',
         target: './src/api/generated',
         schemas: './src/api/model',
         client: 'react-query',
         override: {
           mutator: {
             path: './src/api/mutator/custom-instance.ts',
             name: 'customInstance',
           },
         },
       },
     },
   };
   ```

3. **APIクライアントの自動生成設定** (Phase 3.3)
   ```bash
   # frontend/package.jsonに追加
   ```

   ```json
   "scripts": {
     // ... 既存のスクリプト ...
     "api:generate": "orval"
   }
   ```

4. **カスタムmutatorの作成** (Phase 3.4)
   ```bash
   # frontend/src/api/mutator/custom-instance.tsを作成
   ```

   ```typescript
   import axios, { AxiosRequestConfig } from 'axios';

   const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

   export const customInstance = <T>(config: AxiosRequestConfig): Promise<T> => {
     const source = axios.CancelToken.source();
     const instance = axios.create({
       baseURL: API_URL,
       cancelToken: source.token,
     });

     // リクエストインターセプター（認証トークンの追加など）
     instance.interceptors.request.use(
       (config) => {
         // クライアントサイドの場合のみトークンを取得
         if (typeof window !== 'undefined') {
           const token = localStorage.getItem('token');
           if (token) {
             config.headers = {
               ...config.headers,
               Authorization: `Bearer ${token}`,
             };
           }
         }
         return config;
       },
       (error) => {
         return Promise.reject(error);
       }
     );

     // レスポンスインターセプター（エラーハンドリングなど）
     instance.interceptors.response.use(
       (response) => {
         return response.data;
       },
       (error) => {
         return Promise.reject(error);
       }
     );

     return instance(config) as Promise<T>;
   };
   ```

5. **React Queryプロバイダーの設定** (Phase 3.4)
   ```bash
   # frontend/src/pages/_app.tsxを修正
   ```

   ```tsx
   import type { AppProps } from 'next/app';
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
   import '../styles/globals.css';

   // React Queryクライアントの作成
   const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         refetchOnWindowFocus: false,
         retry: false,
       },
     },
   });

   function MyApp({ Component, pageProps }: AppProps) {
     return (
       <QueryClientProvider client={queryClient}>
         <Component {...pageProps} />
       </QueryClientProvider>
     );
   }

   export default MyApp;
   ```

### ワークフローの自動化

1. **ルートpackage.jsonの更新** (Phase 5.2)
   ```json
   "scripts": {
     // ... 既存のスクリプト ...
     "openapi:export": "docker-compose run --rm ms-backend python -m cli export_openapi",
     "openapi:generate": "npm run openapi:export && cd frontend && npm run api:generate",
     "dev:with-api": "npm run openapi:generate && npm run dev"
   }
   ```

2. **CIパイプラインへの追加** (Phase 5.1)
   GitHub Actionsの例:
   ```yaml
   # .github/workflows/openapi-validation.yml

   name: OpenAPI Validation

   on:
     push:
       paths:
         - 'backend/src/**/*.py'
         - '.github/workflows/openapi-validation.yml'

   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2

         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.10'

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             cd backend
             pip install -r requirements.txt

         - name: Export OpenAPI Schema
           run: |
             cd backend
             python -m cli export_openapi

         - name: Validate OpenAPI Schema
           uses: swagger-api/validator-badge@v1
           with:
             specs-url: ./backend/openapi.json
   ```

# MapStack システムアーキテクチャ

---
title: システムアーキテクチャ
importance: high
last_updated: 2025-04-04
for_ai_assistant: このドキュメントはMapStackのシステム設計と構造を定義しています。コード実装時は、ここで定義されたアーキテクチャパターンと設計原則に従ってください。
---

## システム全体構成図

```
                                  ┌───────────────────────┐
                                  │    CDN (Cloudflare)   │
                                  └───────────┬───────────┘
                                              │
                                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                         ┌────────────────────────┐                    │
│                         │   Vercel (PoC phase)   │                    │
│                         └─────────┬──────────────┘                    │
│                                   │                                   │
│  ┌─────────────────┐      ┌───────┴───────┐     ┌──────────────────┐  │
│  │  Next.js App    │      │  API Gateway  │     │  Authentication  │  │
│  │   (Frontend)    ├─────►│ (Next.js API) ├────►│    Service       │  │
│  └─────────────────┘      └───────┬───────┘     └──────────────────┘  │
│                                   │                                   │
└───────────────────────────────────┼───────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  ┌────────────────┐     ┌────────────────┐     ┌────────────────────┐  │
│  │  FastAPI       │     │  Content       │     │  AI Service        │  │
│  │  Backend       ├────►│  Service       │     │  (OpenAI API)      │  │
│  └───────┬────────┘     └───────┬────────┘     └──────────┬─────────┘  │
│          │                      │                         │            │
│          │                      │                         │            │
│  ┌───────┴────────┐     ┌───────┴────────┐     ┌──────────┴─────────┐  │
│  │  User          │     │  Learning      │     │  Execution         │  │
│  │  Service       │     │  Service       │     │  Environment       │  │
│  └───────┬────────┘     └───────┬────────┘     └──────────┬─────────┘  │
│          │                      │                         │            │
│          │                      │                         │            │
│          └──────────────────────┼─────────────────────────┘            │
│                                 │                                      │
│                        ┌────────┴─────────┐                            │
│                        │  PostgreSQL      │                            │
│                        │  Database        │                            │
│                        └──────────────────┘                            │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 主要コンポーネント概要

1. **フロントエンド層**
   - **Next.js Application**: ユーザーインターフェイスとクライアントサイドのロジック
   - **API Gateway**: バックエンドサービスへのインターフェイス（Next.js API Routes）
   - **認証サービス**: ユーザー認証と認可の管理

2. **バックエンド層**
   - **FastAPI Backend**: コアバックエンドアプリケーション
   - **User Service**: ユーザー管理と関連機能
   - **Learning Service**: 学習コンテンツと進捗管理
   - **Content Service**: コンテンツの保存、取得、変換
   - **AI Service**: OpenAI APIとの統合、質問応答、コードレビュー
   - **Execution Environment**: コードの安全な実行環境

3. **データ層**
   - **PostgreSQL Database**: 永続的データストレージ

4. **インフラ層**
   - **Vercel**: フロントエンドとAPIゲートウェイのホスティング（PoCフェーズ）
   - **Cloudflare**: CDNとDDoS保護
   - **Backend Hosting**: FastAPIサービスのホスティング（将来的にはAWSやGCP）

## コンポーネント間の関係性

### データフロー

1. **ユーザー認証フロー**
   ```
   ユーザー → Next.js App → 認証サービス → User Service → DB
           ↑                    ↓
           └───── JWT Token ────┘
   ```

2. **ロードマップ閲覧フロー**
   ```
   ユーザー → Next.js App → API Gateway → Learning Service → DB
           ↑                                     ↓
           └─────────── ロードマップデータ ────────┘
   ```

3. **学習コンテンツ消費フロー**
   ```
   ユーザー → Next.js App → API Gateway → Content Service → DB
           ↑                                     ↓
           └──────────── コンテンツデータ ────────┘
   ```

4. **AI質問応答フロー**
   ```
   ユーザー → Next.js App → API Gateway → AI Service → OpenAI API
           ↑                                  ↓
           └──────────── 応答データ ───────────┘
   ```

5. **コード実行フロー**
   ```
   ユーザー → Next.js App → API Gateway → Execution Environment
           ↑                                     ↓
           └───────────── 実行結果 ───────────────┘
   ```

6. **学習進捗記録フロー**
   ```
   ユーザー活動 → Next.js App → API Gateway → Learning Service → DB
                                                    ↓
   ユーザー ← ダッシュボード更新 ← Next.js App ← 進捗データ 
   ```

### コンポーネント間の依存関係

- **フロントエンド依存関係**:
  - Next.jsアプリケーションはAPI Gatewayを通じてバックエンドサービスと通信
  - クライアントサイド状態管理はZustandを使用
  - UIコンポーネントはTailwind CSSで構築

- **バックエンド依存関係**:
  - FastAPIは各マイクロサービス間の調整を担当
  - 各サービスは独自のドメインロジックをカプセル化
  - サービス間通信は同期RESTful APIを使用（将来的に非同期イベント駆動に移行可能）

- **データ層依存関係**:
  - すべてのサービスはPostgreSQLデータベースを共有
  - SQLAlchemyをORMとして使用
  - 各サービスは自身のスキーマを管理

## DDDモデルとドメイン構造

### 戦略的設計

#### バウンデッドコンテキスト

1. **ユーザーコンテキスト**
   - **責任**: ユーザー登録、認証、プロフィール管理
   - **エンティティ**: User, Role, Permission
   - **値オブジェクト**: Email, Password, Profile

2. **ロードマップコンテキスト**
   - **責任**: 学習パス、テーマ、ノード管理
   - **エンティティ**: Roadmap, Theme, Node, Prerequisite
   - **値オブジェクト**: SkillLevel, Duration, Difficulty

3. **学習コンテキスト**
   - **責任**: 学習活動、進捗追跡、達成管理
   - **エンティティ**: LearningActivity, Progress, Achievement
   - **値オブジェクト**: CompletionStatus, Score, Feedback

4. **コンテンツコンテキスト**
   - **責任**: 教材、課題、テスト管理
   - **エンティティ**: Content, Exercise, Quiz, Resource
   - **値オブジェクト**: ContentType, Difficulty, Duration

5. **AIサポートコンテキスト**
   - **責任**: 質問応答、コードレビュー、学習推奨
   - **エンティティ**: Question, Answer, CodeReview
   - **値オブジェクト**: Relevance, Confidence, Suggestion

#### コンテキストマップ

```
         ┌───────────────┐            ┌───────────────┐
         │ ユーザー      │◄───────────┤ AIサポート    │
         │ コンテキスト   │            │ コンテキスト   │
         └───────┬───────┘            └───────▲───────┘
                 │                            │
                 │                            │
                 ▼                            │
         ┌───────────────┐            ┌───────┴───────┐
         │ ロードマップ   │◄───────────┤ 学習         │
         │ コンテキスト   │            │ コンテキスト   │
         └───────┬───────┘            └───────▲───────┘
                 │                            │
                 │                            │
                 ▼                            │
         ┌───────────────┐                    │
         │ コンテンツ    ├────────────────────┘
         │ コンテキスト   │
         └───────────────┘
```

### 戦術的設計

#### ドメインモデル例：ロードマップコンテキスト

```python
# エンティティ
class Roadmap:
    id: UUID
    title: str
    description: str
    skill_level: SkillLevel
    estimated_duration: Duration
    nodes: List[Node]
    created_at: datetime
    updated_at: datetime
    
    def add_node(self, node: Node) -> None:
        # ビジネスルール: ノードの前提条件チェック
        pass
        
    def calculate_completion_percentage(self, progress: Progress) -> float:
        # ビジネスルール: 進捗率の計算
        pass

# 値オブジェクト
class SkillLevel:
    level: str  # beginner, intermediate, advanced
    
    def __init__(self, level: str):
        if level not in ["beginner", "intermediate", "advanced"]:
            raise ValueError("Invalid skill level")
        self.level = level
    
    def __eq__(self, other):
        if not isinstance(other, SkillLevel):
            return False
        return self.level == other.level

# リポジトリインターフェース
class RoadmapRepository(Protocol):
    def get_by_id(self, id: UUID) -> Optional[Roadmap]:
        pass
    
    def save(self, roadmap: Roadmap) -> None:
        pass
    
    def find_by_theme(self, theme: str) -> List[Roadmap]:
        pass
```

#### ドメインサービス例

```python
class RoadmapRecommendationService:
    def __init__(
        self, 
        roadmap_repo: RoadmapRepository,
        user_repo: UserRepository,
        progress_repo: ProgressRepository
    ):
        self.roadmap_repo = roadmap_repo
        self.user_repo = user_repo
        self.progress_repo = progress_repo
    
    def recommend_roadmaps_for_user(self, user_id: UUID) -> List[Roadmap]:
        # ドメインロジック: ユーザープロフィール、過去の進捗、興味に基づいて
        # 最適なロードマップを推奨する
        user = self.user_repo.get_by_id(user_id)
        progress_history = self.progress_repo.get_by_user_id(user_id)
        
        # 推奨アルゴリズム...
        
        return recommended_roadmaps
```

## セキュリティアーキテクチャ

### 認証と認可

1. **認証システム**
   - JWT (JSON Web Tokens)ベースの認証
   - OAuth 2.0 / OpenID Connectによるソーシャルログイン
   - 多要素認証（MFA）オプション
   - パスワードハッシュにはbcryptを使用

2. **認可フレームワーク**
   - ロールベースアクセス制御（RBAC）
   - 属性ベースアクセス制御（ABAC）の要素を組み合わせ
   - 細粒度の権限管理（読み取り、作成、編集、削除）
   - APIエンドポイントごとの権限チェック

3. **トークン管理**
   - アクセストークン（短期間有効）とリフレッシュトークン（長期間有効）の分離
   - サーバーサイドでのトークン無効化機能
   - セキュアなHTTPOnly Cookieでのトークン保存

### データ保護

1. **保存データの暗号化**
   - 個人識別情報（PII）の暗号化（AES-256）
   - データベースレベルの透過的な暗号化（TDE）
   - バックアップも暗号化

2. **転送中データの保護**
   - TLS 1.3によるすべての通信の暗号化
   - 強力な暗号スイートの適用
   - HTTP Strict Transport Security (HSTS)の実装

3. **秘密情報の管理**
   - AWS Secrets ManagerやHashicorp Vaultなどのシークレット管理サービスの利用
   - 環境変数による秘密情報の分離
   - 定期的な認証情報のローテーション

### 環境分離とサンドボックス

1. **コード実行環境の分離**
   - コンテナ技術を使用した実行環境の分離
   - リソース制限（CPU、メモリ、ネットワーク、ディスク）
   - タイムアウト制限
   - ファイルシステムの隔離

2. **サンドボックスセキュリティ**
   - ホワイトリストベースのライブラリと関数アクセス
   - 危険なコード検出パターン
   - ユーザー間のデータ分離

### セキュリティ監視と対応

1. **ログ記録と監査**
   - すべての認証イベントの記録
   - アクセスログとアクティビティログの分離
   - セキュリティ関連イベントの集中管理

2. **侵入検知と防止**
   - 異常ログインパターン検知
   - レート制限による暴力的攻撃の防止
   - Web Application Firewall (WAF)の実装

3. **セキュリティインシデント対応**
   - セキュリティインシデント対応計画
   - 定期的なセキュリティレビュー
   - 脆弱性管理プロセス

## スケーラビリティ設計

### 水平スケーリング

1. **ステートレスアーキテクチャ**
   - バックエンドサービスの完全なステートレス化
   - セッション状態の外部化（Redis/DynamoDB）
   - ロードバランサーを通じた複数インスタンスへのトラフィック分散

2. **サービスの独立スケーリング**
   - マイクロサービスアーキテクチャによる独立したスケーリング
   - 負荷が高いサービス（AIサービス、実行環境）の選択的スケールアウト
   - コンテナオーケストレーション（Kubernetes）の採用

3. **自動スケーリング**
   - 負荷メトリクスに基づく自動スケールアウト/イン
   - 予測的スケーリング（使用パターンに基づく）
   - スケーリングイベントのアラートと監視

### データベーススケーリング

1. **読み取りスケーリング**
   - 読み取り専用レプリカの配置
   - キャッシュ層（Redis）の導入
   - 読み取り/書き込みの分離

2. **書き込みスケーリング**
   - データベースシャーディング（将来的な拡張として）
   - バッチ処理と非同期処理の活用
   - 書き込みバッファリング

3. **コネクションプール最適化**
   - データベースコネクションプールの適切なサイジング
   - サービスごとの分離されたプール
   - デッドロック防止メカニズム

### パフォーマンス最適化

1. **キャッシング戦略**
   - 多層キャッシング（ブラウザ、CDN、アプリケーション、データ）
   - 時間ベースとイベントベースのキャッシュ無効化
   - 分散キャッシュ（Redis）の使用

2. **非同期処理**
   - 長時間実行タスクの非同期処理（Celery/RQ）
   - イベント駆動型アーキテクチャ
   - バックグラウンドジョブのキュー化

3. **最適化テクニック**
   - データベースインデックス最適化
   - クエリパフォーマンスチューニング
   - APIレスポンスのページネーションと部分取得

### 弾力性と障害耐性

1. **サーキットブレーカーパターン**
   - サービス間呼び出しのサーキットブレーカー実装
   - フォールバックメカニズム
   - グレースフル劣化

2. **リトライメカニズム**
   - 指数バックオフによるリトライ
   - べき等性の確保
   - デッドレターキュー

3. **障害検出と自動復旧**
   - ヘルスチェックと自動再起動
   - 障害インスタンスの自動置換
   - ブルー/グリーンデプロイメント

---

*このアーキテクチャドキュメントはシステムの発展に伴い継続的に更新されます。設計上の決定は、実装経験とパフォーマンステストの結果に基づいて見直されます。*

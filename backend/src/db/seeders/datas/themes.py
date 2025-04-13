"""
テーマデータを提供するモジュール
"""

# テーマデータ（カテゴリーIDはシード処理時に割り当て）
themes_by_category = {
    "web-development": [
        {
            "code": "frontend",
            "title": "フロントエンド開発",
            "description": "HTML、CSS、JavaScriptからモダンフレームワークまでのフロントエンド技術",
            "order_index": 1.0,
        },
        {
            "code": "backend",
            "title": "バックエンド開発",
            "description": "サーバーサイド開発、API設計、データベース連携などのバックエンド技術",
            "order_index": 2.0,
        },
        {
            "code": "fullstack",
            "title": "フルスタック開発",
            "description": "フロントエンドとバックエンドの両方を扱うフルスタック開発者になるためのパス",
            "order_index": 3.0,
        },
        {
            "code": "devops",
            "title": "DevOps",
            "description": "継続的インテグレーション、デリバリー、デプロイメントのための自動化とツール",
            "order_index": 4.0,
        },
    ],
    "data-science": [
        {
            "code": "data-analysis",
            "title": "データ分析",
            "description": "データの収集、クリーニング、分析、可視化の基礎スキル",
            "order_index": 1.0,
        },
        {
            "code": "machine-learning",
            "title": "機械学習",
            "description": "機械学習アルゴリズム、モデル構築、評価手法の習得",
            "order_index": 2.0,
        },
        {
            "code": "big-data",
            "title": "ビッグデータ",
            "description": "大規模データの処理、分散処理フレームワークの活用",
            "order_index": 3.0,
        },
        {
            "code": "deep-learning",
            "title": "ディープラーニング",
            "description": "ニューラルネットワーク、ディープラーニングモデルの構築と応用",
            "order_index": 4.0,
        },
    ],
    "mobile-development": [
        {
            "code": "ios",
            "title": "iOS開発",
            "description": "Swift、UIKitを使ったiOSアプリケーション開発",
            "order_index": 1.0,
        },
        {
            "code": "android",
            "title": "Android開発",
            "description": "KotlinやJavaを使ったAndroidアプリケーション開発",
            "order_index": 2.0,
        },
        {
            "code": "react-native",
            "title": "React Native",
            "description": "JavaScriptを使ったクロスプラットフォームモバイルアプリ開発",
            "order_index": 3.0,
        },
        {
            "code": "flutter",
            "title": "Flutter",
            "description": "Dartを使ったクロスプラットフォームモバイルアプリ開発",
            "order_index": 4.0,
        },
    ],
    "infrastructure": [
        {
            "code": "cloud",
            "title": "クラウドコンピューティング",
            "description": "AWS、Azure、GCPなどのクラウドプラットフォーム活用スキル",
            "order_index": 1.0,
        },
        {
            "code": "networking",
            "title": "ネットワーキング",
            "description": "ネットワークの基礎、設計、セキュリティ、トラブルシューティング",
            "order_index": 2.0,
        },
        {
            "code": "server-admin",
            "title": "サーバー管理",
            "description": "Linux/Windowsサーバーの構築、管理、最適化",
            "order_index": 3.0,
        },
        {
            "code": "containerization",
            "title": "コンテナ技術",
            "description": "Docker、Kubernetes、コンテナオーケストレーション",
            "order_index": 4.0,
        },
    ],
}

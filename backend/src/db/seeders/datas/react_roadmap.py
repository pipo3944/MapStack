"""
Reactロードマップのデータを提供するモジュール
"""

# Reactロードマップのノードデータ
react_roadmap_nodes = [
    {
        "title": "Reactの基本概念",
        "description": "Reactのコンポーネント、JSX、仮想DOMなどの基本概念を学ぶ",
        "position_x": 100,
        "position_y": 100,
        "handle": "react-basics",
        "node_type": "primary",
        "is_required": False,
        "meta_data": {
            "status": "未完了",
            "content_url": "https://example.com/react-basics",
            "concepts": ["JSX", "Virtual DOM", "Components"],
            "resources": [
                {"title": "React公式ドキュメント", "url": "https://reactjs.org/docs/getting-started.html"},
                {"title": "React入門チュートリアル", "url": "https://ja.reactjs.org/tutorial/tutorial.html"}
            ]
        }
    },
    {
        "title": "コンポーネント設計",
        "description": "効率的なコンポーネント設計とプロップの受け渡しについて",
        "position_x": 250,
        "position_y": 100,
        "handle": "component-design",
        "node_type": "primary",
        "is_required": False,
        "meta_data": {
            "status": "未完了",
            "content_url": "https://example.com/component-design",
            "concepts": ["Props", "Composition", "Reusability"],
            "resources": [
                {"title": "コンポーネント設計パターン", "url": "https://example.com/component-patterns"},
                {"title": "React Compositionガイド", "url": "https://example.com/react-composition"}
            ]
        }
    },
    {
        "title": "状態管理",
        "description": "ReactのState管理とStateフックの使い方",
        "position_x": 400,
        "position_y": 100,
        "handle": "state-management",
        "node_type": "primary",
        "is_required": False,
        "meta_data": {
            "status": "未完了",
            "content_url": "https://example.com/state-management",
            "concepts": ["useState", "useReducer", "Context API"],
            "resources": [
                {"title": "React Hooks入門", "url": "https://example.com/react-hooks"},
                {"title": "Context APIの使い方", "url": "https://example.com/context-api"}
            ]
        }
    },
    {
        "title": "Reactルーティング",
        "description": "React Routerを使ったSPA開発",
        "position_x": 250,
        "position_y": 200,
        "handle": "react-routing",
        "node_type": "primary",
        "is_required": False,
        "meta_data": {
            "status": "未完了",
            "content_url": "https://example.com/react-routing",
            "concepts": ["React Router", "Navigation", "Route Guards"],
            "resources": [
                {"title": "React Router公式ガイド", "url": "https://reactrouter.com/web/guides/quick-start"},
                {"title": "SPAのルーティング設計", "url": "https://example.com/spa-routing"}
            ]
        }
    },
    {
        "title": "Reactテスト",
        "description": "Jest/React Testing Libraryを使ったテスト",
        "position_x": 400,
        "position_y": 200,
        "handle": "react-testing",
        "node_type": "primary",
        "is_required": False,
        "meta_data": {
            "status": "未完了",
            "content_url": "https://example.com/react-testing",
            "concepts": ["Jest", "React Testing Library", "Mocking"],
            "resources": [
                {"title": "Reactコンポーネントのテスト", "url": "https://example.com/testing-components"},
                {"title": "テスト駆動React開発", "url": "https://example.com/tdd-react"}
            ]
        }
    }
]

# Reactロードマップのエッジデータ（ノード間の接続）
react_roadmap_edges = [
    {
        "source_node_idx": 0,  # Reactの基本概念
        "target_node_idx": 1,  # コンポーネント設計
        "handle": "basics-to-components",
        "edge_type": "default",
        "source_handle": "right",
        "target_handle": "left",
    },
    {
        "source_node_idx": 1,  # コンポーネント設計
        "target_node_idx": 2,  # 状態管理
        "handle": "components-to-state",
        "edge_type": "default",
        "source_handle": "right",
        "target_handle": "left",
    },
    {
        "source_node_idx": 2,  # 状態管理
        "target_node_idx": 3,  # Reactルーティング
        "handle": "state-to-routing",
        "edge_type": "default",
        "source_handle": "bottom",
        "target_handle": "top",
    },
    {
        "source_node_idx": 3,  # Reactルーティング
        "target_node_idx": 4,  # Reactテスト
        "handle": "routing-to-testing",
        "edge_type": "default",
        "source_handle": "right",
        "target_handle": "left",
    }
]

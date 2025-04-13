"""
ロードマップ関連のシードデータを提供するモジュール
"""
import asyncio
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from sqlalchemy.orm import Session

from ..models.roadmap import Category, Theme, Roadmap, RoadmapNode, RoadmapEdge
from .datas.categories import categories
from .datas.themes import themes_by_category
from .datas.frontend_roadmap import frontend_roadmap_nodes, frontend_roadmap_edges
from .datas.react_roadmap import react_roadmap_nodes, react_roadmap_edges

logger = logging.getLogger(__name__)

def seed_roadmap_data_sync(session: Session) -> None:
    """初期ロードマップデータをデータベースに投入する"""
    # カテゴリーの投入
    logger.info("カテゴリーデータの投入を開始します...")
    category_dict = {}  # カテゴリーコードとIDのマッピング

    for category_data in categories:
        # カテゴリーが既に存在するか確認
        stmt = select(Category).where(Category.code == category_data["code"])
        result = session.execute(stmt)
        category = result.scalars().first()

        # 存在しない場合は新規作成
        if not category:
            category = Category(
                code=category_data["code"],
                title=category_data["title"],
                description=category_data["description"],
                order_index=category_data["order_index"]
            )
            session.add(category)
            session.flush()
            logger.info(f"新規カテゴリーを作成: {category_data['title']}")

        # マッピング辞書に登録
        category_dict[category_data["code"]] = category.id

    # テーマの投入
    logger.info("テーマデータの投入を開始します...")
    theme_dict = {}  # テーマコードとIDのマッピング

    for category_code, themes in themes_by_category.items():
        if category_code not in category_dict:
            logger.warning(f"カテゴリーコード '{category_code}' に対応するカテゴリーが見つかりません")
            continue

        category_id = category_dict[category_code]

        for theme_data in themes:
            # テーマが既に存在するか確認
            stmt = select(Theme).where(Theme.code == theme_data["code"])
            result = session.execute(stmt)
            theme = result.scalars().first()

            # 存在しない場合は新規作成
            if not theme:
                theme = Theme(
                    code=theme_data["code"],
                    title=theme_data["title"],
                    description=theme_data["description"],
                    category_id=category_id,
                    order_index=theme_data["order_index"]
                )
                session.add(theme)
                session.flush()
                logger.info(f"新規テーマを作成: {theme_data['title']}")

            # マッピング辞書に登録
            theme_dict[theme_data["code"]] = theme.id

    # フロントエンドロードマップの作成（サンプル）
    logger.info("フロントエンドロードマップのサンプルを作成します...")

    # フロントエンドテーマが存在するか確認
    frontend_theme_id = theme_dict.get("frontend")
    if not frontend_theme_id:
        # テーマが存在しない場合は警告を出して終了
        logger.warning("フロントエンドテーマが見つかりません。フロントエンドロードマップは作成されません。")
    else:
        # ロードマップの作成
        frontend_roadmap = Roadmap(
            title="フロントエンド開発ロードマップ",
            description="フロントエンド開発の基礎から応用までのロードマップ",
            theme_id=frontend_theme_id,
            version="1.0.0",
            is_published=True,
            is_latest=True,
            published_at=datetime.now()
        )
        session.add(frontend_roadmap)
        session.flush()

        # ノードの作成
        node_dict = {}  # ノードハンドルとIDのマッピング

        for node_data in frontend_roadmap_nodes:
            node = RoadmapNode(
                roadmap_id=frontend_roadmap.id,
                title=node_data["title"],
                description=node_data["description"],
                position_x=node_data["position_x"],
                position_y=node_data["position_y"],
                handle=node_data["handle"],
                node_type=node_data["node_type"],
                is_required=False,
                meta_data={
                    "status": "未完了",
                    "content_url": f"https://example.com/{node_data['handle']}",
                    "concepts": [node_data["title"]],
                    "resources": [
                        {"title": f"{node_data['title']}の学習リソース", "url": f"https://example.com/{node_data['handle']}-resources"}
                    ]
                }
            )
            session.add(node)
            session.flush()
            node_dict[node_data["handle"]] = node.id

        # エッジの作成
        for edge_data in frontend_roadmap_edges:
            if edge_data["source_node_id"] in node_dict and edge_data["target_node_id"] in node_dict:
                edge = RoadmapEdge(
                    roadmap_id=frontend_roadmap.id,
                    source_node_id=node_dict[edge_data["source_node_id"]],
                    target_node_id=node_dict[edge_data["target_node_id"]],
                    handle=edge_data["handle"],
                    edge_type=edge_data["edge_type"],
                    source_handle=edge_data.get("source_handle"),
                    target_handle=edge_data.get("target_handle"),
                    meta_data={}
                )
                session.add(edge)

    # React ロードマップサンプルも追加
    logger.info("Reactロードマップのサンプルを作成します...")
    if "react-native" in theme_dict:
        react_theme_id = theme_dict["react-native"]

        react_roadmap = Roadmap(
            title="React基礎から応用まで",
            description="Reactの基礎から応用までのロードマップ",
            theme_id=react_theme_id,
            version="1.0.0",
            is_published=True,
            is_latest=True,
            published_at=datetime.now()
        )
        session.add(react_roadmap)
        session.flush()

        # ノード作成
        nodes = []
        for node_data in react_roadmap_nodes:
            node = RoadmapNode(
                roadmap_id=react_roadmap.id,
                title=node_data["title"],
                description=node_data["description"],
                position_x=node_data["position_x"],
                position_y=node_data["position_y"],
                handle=node_data["handle"],
                node_type=node_data["node_type"],
                is_required=node_data["is_required"],
                meta_data=node_data["meta_data"]
            )
            session.add(node)
            session.flush()
            nodes.append(node)

        # エッジ作成（ノード間の関連付け）
        for edge_data in react_roadmap_edges:
            edge = RoadmapEdge(
                roadmap_id=react_roadmap.id,
                source_node_id=nodes[edge_data["source_node_idx"]].id,
                target_node_id=nodes[edge_data["target_node_idx"]].id,
                handle=edge_data["handle"],
                edge_type=edge_data["edge_type"],
                source_handle=edge_data.get("source_handle"),
                target_handle=edge_data.get("target_handle"),
                meta_data={}
            )
            session.add(edge)

    session.commit()
    logger.info("ロードマップデータのシードが完了しました（同期処理）")

def run_seeds_sync(db):
    """
    全てのシードデータを同期的に実行
    """
    logger.info("同期的にシードデータを実行します...")
    seed_roadmap_data_sync(db)
    logger.info("シードデータの実行が完了しました。")

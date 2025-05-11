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
        else:
            logger.info(f"既存カテゴリーを使用: {category_data['title']}")

        # マッピング辞書に登録
        category_dict[category_data["code"]] = category.id

    # テーマの投入
    logger.info("テーマデータの投入を開始します...")
    theme_dict = {}  # テーマコードとIDのマッピング

    for category_code, themes_data in themes_by_category.items():
        if category_code not in category_dict:
            logger.warning(f"カテゴリーコード '{category_code}' は存在しません")
            continue

        category_id = category_dict[category_code]

        for theme_data in themes_data:
            # テーマが既に存在するか確認
            stmt = select(Theme).where(Theme.code == theme_data["code"])
            result = session.execute(stmt)
            theme = result.scalars().first()

            # 存在しない場合は新規作成
            if not theme:
                theme = Theme(
                    category_id=category_id,
                    code=theme_data["code"],
                    title=theme_data["title"],
                    description=theme_data["description"],
                    order_index=theme_data["order_index"]
                )
                session.add(theme)
                session.flush()
                logger.info(f"新規テーマを作成: {theme_data['title']}")
            else:
                logger.info(f"既存テーマを使用: {theme_data['title']}")

            # マッピング辞書に登録
            theme_dict[theme_data["code"]] = theme.id

    # ロードマップの作成
    logger.info("ロードマップデータの投入を開始します...")
    roadmap_data = {
        "theme_code": "frontend",
        "version": "1.0.0",
        "title": "フロントエンド開発ロードマップ",
        "description": "フロントエンド開発の基礎から応用までのロードマップ",
        "nodes": frontend_roadmap_nodes,
        "edges": frontend_roadmap_edges
    }

    # ロードマップが既に存在するか確認
    theme_id = theme_dict.get(roadmap_data["theme_code"])
    if not theme_id:
        logger.warning(f"テーマコード '{roadmap_data['theme_code']}' は存在しません")
        return

    stmt = select(Roadmap).where(
        Roadmap.theme_id == theme_id,
        Roadmap.version == roadmap_data["version"]
    )
    result = session.execute(stmt)
    existing_roadmap = result.scalars().first()

    if existing_roadmap:
        logger.info(f"ロードマップは既に存在します: {roadmap_data['title']} (バージョン: {roadmap_data['version']})")
        roadmap = existing_roadmap
    else:
        # 新規ロードマップの作成
        roadmap = Roadmap(
            theme_id=theme_id,
            version=roadmap_data["version"],
            title=roadmap_data["title"],
            description=roadmap_data["description"],
            is_published=True,
            is_latest=True,
            published_at=datetime.now()
        )
        session.add(roadmap)
        session.flush()
        logger.info(f"新規ロードマップを作成: {roadmap_data['title']}")

    # ノードの作成（ロードマップが新規の場合のみ）
    if not existing_roadmap:
        logger.info("ノードデータの投入を開始します...")
        node_dict = {}  # ノードハンドルとIDのマッピング

        for node_data in roadmap_data["nodes"]:
            node = RoadmapNode(
                roadmap_id=roadmap.id,
                handle=node_data["handle"],
                node_type=node_data["node_type"],
                title=node_data["title"],
                description=node_data.get("description", ""),
                position_x=node_data["position_x"],
                position_y=node_data["position_y"],
                meta_data=node_data.get("meta_data", {}),
                is_required=node_data.get("is_required", False)
            )
            session.add(node)
            node_dict[node_data["handle"]] = node  # ノードオブジェクトを一時保存

        session.flush()
        logger.info(f"{len(node_dict)} 件のノードを作成しました")

        # エッジの作成
        logger.info("エッジデータの投入を開始します...")
        for edge_data in roadmap_data["edges"]:
            # ソースノードとターゲットノードが存在するか確認
            if edge_data["source_node_id"] not in node_dict or edge_data["target_node_id"] not in node_dict:
                logger.warning(f"エッジに関連するノードが見つかりません: {edge_data['handle']}")
                continue

            source_node = node_dict[edge_data["source_node_id"]]
            target_node = node_dict[edge_data["target_node_id"]]

            edge = RoadmapEdge(
                roadmap_id=roadmap.id,
                handle=edge_data["handle"],
                source_node_id=source_node.id,
                target_node_id=target_node.id,
                edge_type=edge_data.get("edge_type", "default"),
                source_handle=edge_data.get("source_handle"),
                target_handle=edge_data.get("target_handle"),
                meta_data=edge_data.get("meta_data", {})
            )
            session.add(edge)

        session.flush()
        logger.info(f"{len(roadmap_data['edges'])} 件のエッジを作成しました")

    # React ロードマップの作成
    react_roadmap_data = {
        "theme_code": "react",
        "version": "1.0.0",
        "title": "React開発ロードマップ",
        "description": "Reactの基礎から応用までのロードマップ",
        "nodes": react_roadmap_nodes,
        "edges": react_roadmap_edges
    }

    # React ロードマップが既に存在するか確認
    react_theme_id = theme_dict.get(react_roadmap_data["theme_code"])
    if not react_theme_id:
        logger.warning(f"テーマコード '{react_roadmap_data['theme_code']}' は存在しません")
        return

    stmt = select(Roadmap).where(
        Roadmap.theme_id == react_theme_id,
        Roadmap.version == react_roadmap_data["version"]
    )
    result = session.execute(stmt)
    existing_react_roadmap = result.scalars().first()

    if existing_react_roadmap:
        logger.info(f"Reactロードマップは既に存在します: {react_roadmap_data['title']} (バージョン: {react_roadmap_data['version']})")
    else:
        # 新規React ロードマップの作成
        react_roadmap = Roadmap(
            theme_id=react_theme_id,
            version=react_roadmap_data["version"],
            title=react_roadmap_data["title"],
            description=react_roadmap_data["description"],
            is_published=True,
            is_latest=True,
            published_at=datetime.now()
        )
        session.add(react_roadmap)
        session.flush()
        logger.info(f"新規Reactロードマップを作成: {react_roadmap_data['title']}")

        # React ノードの作成
        logger.info("Reactノードデータの投入を開始します...")
        react_node_dict = {}  # ノードハンドルとIDのマッピング

        for node_data in react_roadmap_data["nodes"]:
            node = RoadmapNode(
                roadmap_id=react_roadmap.id,
                handle=node_data["handle"],
                node_type=node_data["node_type"],
                title=node_data["title"],
                description=node_data.get("description", ""),
                position_x=node_data["position_x"],
                position_y=node_data["position_y"],
                meta_data=node_data.get("meta_data", {}),
                is_required=node_data.get("is_required", False)
            )
            session.add(node)
            react_node_dict[node_data["handle"]] = node  # ノードオブジェクトを一時保存

        session.flush()
        logger.info(f"{len(react_node_dict)} 件のReactノードを作成しました")

        # React エッジの作成
        logger.info("Reactエッジデータの投入を開始します...")
        for edge_data in react_roadmap_data["edges"]:
            # ソースノードとターゲットノードが存在するか確認
            if edge_data["source_node_id"] not in react_node_dict or edge_data["target_node_id"] not in react_node_dict:
                logger.warning(f"Reactエッジに関連するノードが見つかりません: {edge_data['handle']}")
                continue

            source_node = react_node_dict[edge_data["source_node_id"]]
            target_node = react_node_dict[edge_data["target_node_id"]]

            edge = RoadmapEdge(
                roadmap_id=react_roadmap.id,
                handle=edge_data["handle"],
                source_node_id=source_node.id,
                target_node_id=target_node.id,
                edge_type=edge_data.get("edge_type", "default"),
                source_handle=edge_data.get("source_handle"),
                target_handle=edge_data.get("target_handle"),
                meta_data=edge_data.get("meta_data", {})
            )
            session.add(edge)

        session.flush()
        logger.info(f"{len(react_roadmap_data['edges'])} 件のReactエッジを作成しました")

    # 変更をコミット
    session.commit()
    logger.info("ロードマップデータの投入が完了しました")

def run_seeds_sync(db):
    """
    全てのシードデータを同期的に実行
    """
    logger.info("同期的にシードデータを実行します...")
    seed_roadmap_data_sync(db)
    logger.info("シードデータの実行が完了しました。")

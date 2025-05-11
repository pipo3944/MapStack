"""
データベースシーディングモジュール

このモジュールは、開発・テスト環境用のデータ生成を担当します。
"""
import logging
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from .roadmap_seed import run_seeds_sync as roadmap_run_seeds_sync, seed_roadmap_data_sync
from .document_seed import seed_document_data_sync, seed_document_data
from .document_content import create_document_content

logger = logging.getLogger(__name__)

# このモジュールの関数をそのまま再エクスポート
# デフォルトではrun_seeds_syncを呼び出す

def run_seeds_sync(session: Session, seed_type="all"):
    """
    シードデータを作成する（同期版）

    Parameters:
        session: SQLAlchemyセッション
        seed_type: シードの種類 ("all", "roadmap", "document" など)
    """
    logger.info(f"シードデータ作成開始: タイプ={seed_type}")

    if seed_type in ["all", "roadmap"]:
        seed_roadmap_data_sync(session)
        logger.info("ロードマップのシード作成完了")

    if seed_type in ["all", "document"]:
        seed_document_data_sync(session)
        logger.info("ドキュメントのシード作成完了")

        # ドキュメントコンテンツの作成（非同期関数を同期的に実行）
        logger.info("ドキュメントコンテンツの作成を開始します...")
        asyncio.run(create_document_content())
        logger.info("ドキュメントコンテンツの作成が完了しました")

    # 他のシードタイプがあれば追加

    logger.info("シード処理完了")

async def run_seeds(session: AsyncSession, seed_type="all"):
    """
    シードデータを作成する（非同期版）

    Parameters:
        session: 非同期SQLAlchemyセッション
        seed_type: シードの種類 ("all", "roadmap", "document" など)
    """
    logger.info(f"非同期シードデータ作成開始: タイプ={seed_type}")

    # ロードマップシードは現在同期版のみ実装
    # ドキュメントシードは非同期版を使用

    if seed_type in ["all", "document"]:
        await seed_document_data(session)
        logger.info("ドキュメントのシード作成完了")

        # ドキュメントコンテンツの作成
        logger.info("ドキュメントコンテンツの作成を開始します...")
        await create_document_content()
        logger.info("ドキュメントコンテンツの作成が完了しました")

    # 他のシードタイプがあれば追加

    logger.info("非同期シード処理完了")

"""
シードデータを実行するためのスクリプト
"""
import argparse
import asyncio
import logging
import os
import sys

# 親ディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.seeders.roadmap_seed import run_seeds

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


async def init_db():
    """
    DBエンジンとセッションを初期化する
    """
    # 環境変数からDBのURLを取得、もしくはデフォルト値を使用
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/mapstack")

    engine = create_async_engine(
        database_url,
        echo=True,  # SQLのログを表示
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    return engine, async_session


async def main():
    """
    シードデータを実行する
    """
    engine, async_session = await init_db()

    async with async_session() as session:
        try:
            await run_seeds(session)
            logger.info("シードデータの作成が完了しました")
        except Exception as e:
            logger.error(f"シードデータの作成中にエラーが発生しました: {e}")
            raise


if __name__ == "__main__":
    """
    コマンドラインからシードデータを実行する

    使用方法:
        python -m src.db.seeders.run_seeds
    """
    parser = argparse.ArgumentParser(description="モックデータの作成")
    args = parser.parse_args()

    logger.info("モックデータの作成を開始します")
    asyncio.run(main())
    logger.info("モックデータの作成が完了しました")

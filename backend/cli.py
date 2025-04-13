#!/usr/bin/env python
"""
MapStackのバックエンドCLIツール

使用例:
  python cli.py seed            # すべてのシードデータを作成
  python cli.py seed --seed-type roadmap   # ロードマップのシードのみ作成
"""
import argparse
import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def init_db():
    """
    DBエンジンとセッションを初期化する（同期版）
    """
    # 環境変数から直接接続情報を取得
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '5432')
    user = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    database = os.environ.get('POSTGRES_DB', 'mapstack')

    # 接続URLを生成
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    logger.info(f"DB接続先: {host}:{port}/{database}")

    engine = create_engine(
        database_url,
        echo=True,  # SQLのログを表示
    )

    Session = sessionmaker(
        bind=engine,
        expire_on_commit=False
    )

    return engine, Session


def create_seed_data(seed_type="all"):
    """
    シードデータを作成する（同期版）
    """
    from src.db.seeders import run_seeds_sync

    engine, Session = init_db()

    with Session() as session:
        try:
            run_seeds_sync(session, seed_type=seed_type)
            logger.info(f"シードデータの作成が完了しました (タイプ: {seed_type})")
        except Exception as e:
            logger.error(f"シードデータの作成中にエラーが発生しました: {e}")
            raise


def main():
    """
    コマンドラインインターフェース
    """
    parser = argparse.ArgumentParser(description="MapStack Backend CLI")
    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # シードデータ作成コマンド
    seed_parser = subparsers.add_parser("seed", help="シードデータを作成する")
    seed_parser.add_argument("--seed-type", choices=["all", "roadmap"], default="all", help="シードデータのタイプを指定")

    # その他のコマンドは必要に応じて追加

    args = parser.parse_args()

    if args.command == "seed":
        logger.info(f"シードデータの作成を開始します（タイプ: {args.seed_type}）")
        create_seed_data(seed_type=args.seed_type)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

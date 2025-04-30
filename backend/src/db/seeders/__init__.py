"""
データベースシーディングモジュール

このモジュールは、開発・テスト環境用のデータ生成を担当します。
"""
import logging
from sqlalchemy.orm import Session

from .roadmap_seed import run_seeds_sync as roadmap_run_seeds_sync, seed_roadmap_data_sync
from .document_seed import seed_document_data_sync

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

    # 他のシードタイプがあれば追加

    logger.info("シード処理完了")

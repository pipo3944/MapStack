import asyncio
import logging
from sqlalchemy import select

from src.db.main import AsyncSessionLocal
from src.db.models.document import Document, DocumentRevision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def list_documents():
    try:
        # 非同期DBセッションを作成
        async with AsyncSessionLocal() as db:
            # ドキュメント一覧を取得
            query = select(Document)
            result = await db.execute(query)
            documents = result.scalars().all()

            if not documents:
                logger.info("ドキュメントが見つかりません")
                return

            logger.info(f"{len(documents)}件のドキュメントが見つかりました")

            # 各ドキュメントとそのリビジョンを表示
            for doc in documents:
                logger.info(f"ドキュメントID: {doc.id}, タイトル: {doc.title}")

                # リビジョン情報を取得
                rev_query = select(DocumentRevision).where(DocumentRevision.document_id == doc.id)
                rev_result = await db.execute(rev_query)
                revisions = rev_result.scalars().all()

                for rev in revisions:
                    logger.info(f"  リビジョンID: {rev.id}, バージョン: {rev.version}, ストレージキー: {rev.storage_key}")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_documents())

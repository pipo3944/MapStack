import asyncio
import logging
from uuid import UUID

from src.db.main import AsyncSessionLocal
from src.services.document import DocumentService
from src.services.exceptions import DocumentNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_document():
    try:
        # デバッグしたいドキュメントIDを指定
        document_id = UUID('1a6ee739-013f-4773-8b8c-9c29e16f7175')

        # 非同期DBセッションを作成
        async with AsyncSessionLocal() as db:
            # DocumentServiceインスタンスを作成し、DBセッションを渡す
            service = DocumentService(db)

            # 最新コンテンツを取得を試みる
            logger.info(f"ドキュメント {document_id} の最新コンテンツを取得します...")
            content = await service.get_latest_content(document_id)

            logger.info(f"取得成功: {content}")
            return content
    except DocumentNotFoundError as e:
        logger.error(f"ドキュメントが見つかりません: {e}")
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_document())

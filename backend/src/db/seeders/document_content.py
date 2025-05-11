"""
ドキュメントコンテンツを手動で作成するスクリプト
"""
import os
import json
import asyncio
import logging
from pathlib import Path
from uuid import UUID

from src.services.storage import get_storage_service
from src.db.main import AsyncSessionLocal
from src.db.models.document import Document, DocumentRevision
from sqlalchemy import select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# サンプルドキュメントテンプレート
document_templates = {
    "HTML": {
        "title": "HTMLの基礎",
        "sections": [
            {
                "title": "HTMLとは",
                "content": "HTMLはHyperText Markup Languageの略で、Webページの構造を定義するマークアップ言語です。\nHTMLはタグを使用して、テキスト、画像、リンクなどの要素を定義します。"
            },
            {
                "title": "基本構造",
                "content": "HTMLドキュメントは<!DOCTYPE html>宣言から始まり、<html>要素を含みます。\n<html>要素内には<head>と<body>の2つの主要なセクションがあります。\n<head>セクションには、タイトル、メタデータ、スタイルシートなどが含まれます。\n<body>セクションには、ページのメインコンテンツが含まれます。"
            },
            {
                "title": "タグの基本",
                "content": "HTMLタグは通常<tag>と</tag>の形式で記述されます。\n開始タグと終了タグの間にコンテンツを配置します。\n例: <p>これは段落です</p>\n\n一部のタグは自己完結型で、終了タグを必要としません。\n例: <img src=\"image.jpg\" alt=\"画像の説明\">"
            }
        ]
    },
    "JavaScript": {
        "title": "JavaScriptの基礎",
        "sections": [
            {
                "title": "JavaScriptとは",
                "content": "JavaScriptはWebページに動的な機能を追加するためのプログラミング言語です。\nHTMLとCSSと組み合わせて使用され、フロントエンド開発の中核となる言語です。"
            },
            {
                "title": "変数と定数",
                "content": "JavaScriptでは、`var`、`let`、`const`を使って変数や定数を宣言します。\n```javascript\nlet count = 0; // 変数\nconst PI = 3.14; // 定数\n```"
            },
            {
                "title": "関数",
                "content": "関数はコードをまとめて再利用可能にするためのブロックです。\n```javascript\nfunction sum(a, b) {\n  return a + b;\n}\n\n// アロー関数\nconst multiply = (a, b) => a * b;\n```"
            }
        ]
    },
    "DEFAULT": {
        "title": "サンプルドキュメント",
        "sections": [
            {
                "title": "はじめに",
                "content": "これはサンプルドキュメントの最初のセクションです。自動生成されたコンテンツです。"
            },
            {
                "title": "本文",
                "content": "これは本文セクションです。重要な情報がここに記載されます。"
            },
            {
                "title": "まとめ",
                "content": "これはサンプルドキュメントのまとめセクションです。自動生成されたコンテンツです。"
            }
        ]
    }
}

def get_content_template(document_title):
    """ドキュメントタイトルに基づいて適切なテンプレートを選択する"""
    title_lower = document_title.lower()

    if "html" in title_lower:
        return document_templates["HTML"]
    elif "javascript" in title_lower or "js" in title_lower:
        return document_templates["JavaScript"]
    else:
        # デフォルトテンプレートを返す前に、タイトルを設定
        template = document_templates["DEFAULT"].copy()
        template["title"] = document_title
        return template

async def create_document_content():
    try:
        storage_service = get_storage_service()
        logger.info("ドキュメントコンテンツ作成処理を開始します")

        # DBからドキュメント情報を取得
        async with AsyncSessionLocal() as db:
            # すべてのドキュメントを取得
            doc_query = select(Document)
            doc_result = await db.execute(doc_query)
            documents = doc_result.scalars().all()

            logger.info(f"{len(documents)}件のドキュメントを処理します")

            for document in documents:
                logger.info(f"ドキュメント処理: id={document.id}, title={document.title}")

                # ドキュメントに応じたコンテンツテンプレートを選択
                content = get_content_template(document.title)

                # リビジョン情報を取得
                rev_query = select(DocumentRevision).where(DocumentRevision.document_id == document.id)
                rev_result = await db.execute(rev_query)
                revisions = rev_result.scalars().all()

                if not revisions:
                    logger.warning(f"リビジョンが見つかりません: {document.id}")
                    # デフォルトバージョンで作成
                    default_version = "1.0.0"
                    storage_key = storage_service.get_storage_key(str(document.id), default_version)
                    logger.info(f"デフォルトリビジョン作成: {storage_key}")
                    await storage_service.save_content(content, str(document.id), default_version)
                    continue

                for rev in revisions:
                    logger.info(f"リビジョン作成: {rev.storage_key}")

                    # ストレージサービスを使用してコンテンツを保存
                    await storage_service.save_content(content, str(document.id), rev.version)

                    # ファイルが正常に作成されたことを確認
                    try:
                        loaded_content = await storage_service.load_content(rev.storage_key)
                        logger.info(f"コンテンツ読み込み成功: {rev.storage_key}")
                    except Exception as e:
                        logger.error(f"コンテンツ読み込みエラー: {rev.storage_key} - {e}")

            logger.info("ドキュメントコンテンツ作成処理が完了しました")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_document_content())

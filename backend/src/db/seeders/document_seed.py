"""
ドキュメントリビジョン関連のシードデータを提供するモジュール
"""
import asyncio
import logging
import uuid
import os
import json
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from sqlalchemy.orm import Session

from ..models.document import Document, DocumentRevision, NodeDocumentLink
from ..models.roadmap import RoadmapNode
from ...services.storage import get_storage_service

logger = logging.getLogger(__name__)

# サンプルドキュメントデータ
sample_documents = [
    {
        "title": "HTMLの基礎",
        "description": "HTMLの基本構造と主要タグの解説",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "HTMLの基礎",
                    "sections": [
                        {
                            "title": "HTMLとは",
                            "content": "HTMLはWebページの構造を定義するためのマークアップ言語です。"
                        },
                        {
                            "title": "基本的なHTML文書構造",
                            "content": "HTMLドキュメントは<!DOCTYPE html>宣言から始まり、html、head、bodyタグで構成されます。"
                        }
                    ]
                }
            },
            {
                "version": "1.1.0",
                "change_summary": "セマンティックタグのセクションを追加",
                "content": {
                    "title": "HTMLの基礎",
                    "sections": [
                        {
                            "title": "HTMLとは",
                            "content": "HTMLはWebページの構造を定義するためのマークアップ言語です。"
                        },
                        {
                            "title": "基本的なHTML文書構造",
                            "content": "HTMLドキュメントは<!DOCTYPE html>宣言から始まり、html、head、bodyタグで構成されます。"
                        },
                        {
                            "title": "セマンティックHTML",
                            "content": "セマンティックHTMLとは、タグに意味を持たせることです。例えば、article、section、navなどのタグがあります。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["html-basics", "semantic-html"]
    },
    {
        "title": "CSSスタイリング入門",
        "description": "CSSによるWebページのスタイリング方法",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "CSSスタイリング入門",
                    "sections": [
                        {
                            "title": "CSSとは",
                            "content": "CSSはWebページのスタイルを定義するための言語です。"
                        },
                        {
                            "title": "セレクタの基本",
                            "content": "CSSセレクタはスタイルを適用する要素を指定します。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["css-basics"]
    },
    {
        "title": "JavaScriptの基本",
        "description": "JavaScriptプログラミングの基礎知識",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "JavaScriptの基本",
                    "sections": [
                        {
                            "title": "JavaScriptとは",
                            "content": "JavaScriptはWebページに動的な機能を追加するためのプログラミング言語です。"
                        },
                        {
                            "title": "変数と定数",
                            "content": "変数はletキーワード、定数はconstキーワードで宣言します。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["js-basics"]
    }
]

async def save_document_content(content: Dict, document_id: str, version: str) -> str:
    """
    コンテンツをストレージに保存し、ストレージキーを返す
    """
    # ストレージサービスを取得
    storage = get_storage_service()

    # 選択されたストレージサービスを使用してコンテンツを保存
    storage_key = await storage.save_content(content, document_id, version)

    return storage_key

async def seed_document_data(session: AsyncSession) -> None:
    """非同期版: 初期ドキュメントデータをデータベースに投入する"""
    logger.info("ドキュメントデータの投入を開始します...")

    # ノードハンドルとIDのマッピングを取得
    node_mapping = {}
    result = await session.execute(select(RoadmapNode.id, RoadmapNode.handle))
    nodes = result.all()
    for node_id, handle in nodes:
        node_mapping[handle] = node_id

    # ドキュメントの作成
    for doc_data in sample_documents:
        # ドキュメントが既に存在するか確認
        existing_doc_query = select(Document).where(Document.title == doc_data["title"])
        existing_doc_result = await session.execute(existing_doc_query)
        existing_doc = existing_doc_result.scalar_one_or_none()

        if existing_doc:
            logger.info(f"既存ドキュメントを使用: {doc_data['title']}")
            doc = existing_doc
        else:
            # 新規ドキュメントを作成
            doc = Document(
                title=doc_data["title"],
                description=doc_data["description"]
            )
            session.add(doc)
            await session.flush()
            logger.info(f"新規ドキュメントを作成: {doc_data['title']}")

        # リビジョンを作成 (既存ドキュメントの場合は既存のリビジョンをチェック)
        for rev_data in doc_data["revisions"]:
            # リビジョンが既に存在するか確認
            existing_rev_query = select(DocumentRevision).where(
                DocumentRevision.document_id == doc.id,
                DocumentRevision.version == rev_data["version"]
            )
            existing_rev_result = await session.execute(existing_rev_query)
            existing_rev = existing_rev_result.scalar_one_or_none()

            if existing_rev:
                logger.info(f"既存リビジョンをスキップ: {doc.title} v{rev_data['version']}")
                continue

            # コンテンツを保存
            storage_key = await save_document_content(rev_data["content"], str(doc.id), rev_data["version"])

            # リビジョンを作成
            rev = DocumentRevision(
                document_id=doc.id,
                version=rev_data["version"],
                storage_key=storage_key,
                change_summary=rev_data["change_summary"],
                created_by=None  # 実際の環境では認証ユーザーのIDを設定
            )
            session.add(rev)
            logger.info(f"新規リビジョンを作成: {doc.title} v{rev_data['version']}")

        # ノードとの関連付け (既存のリンクをチェック)
        for i, node_handle in enumerate(doc_data["nodes"]):
            if node_handle in node_mapping:
                # リンクが既に存在するか確認
                existing_link_query = select(NodeDocumentLink).where(
                    NodeDocumentLink.node_id == node_mapping[node_handle],
                    NodeDocumentLink.document_id == doc.id
                )
                existing_link_result = await session.execute(existing_link_query)
                existing_link = existing_link_result.scalar_one_or_none()

                if existing_link:
                    logger.info(f"既存ノードリンクをスキップ: {node_handle} -> {doc.title}")
                    continue

                # 新規リンクを作成
                link = NodeDocumentLink(
                    node_id=node_mapping[node_handle],
                    document_id=doc.id,
                    order_position=i,
                    relation_type="primary"
                )
                session.add(link)
                logger.info(f"新規ノードリンクを作成: {node_handle} -> {doc.title}")
            else:
                logger.warning(f"ノードハンドル '{node_handle}' に対応するノードが見つかりません")

    await session.commit()
    logger.info("ドキュメントデータのシードが完了しました")

def seed_document_data_sync(session: Session) -> None:
    """初期ドキュメントデータをデータベースに投入する（同期版）"""
    logger.info("ドキュメントデータの投入を開始します...")

    # ノードハンドルとIDのマッピングを取得
    node_mapping = {}
    nodes = session.execute(select(RoadmapNode.id, RoadmapNode.handle)).all()
    for node_id, handle in nodes:
        node_mapping[handle] = node_id

    # ドキュメントの作成
    for doc_data in sample_documents:
        # ドキュメントが既に存在するか確認
        existing_doc_query = select(Document).where(Document.title == doc_data["title"])
        existing_doc_result = session.execute(existing_doc_query)
        existing_doc = existing_doc_result.scalar_one_or_none()

        if existing_doc:
            logger.info(f"既存ドキュメントを使用: {doc_data['title']}")
            doc = existing_doc
        else:
            # 新規ドキュメントを作成
            doc = Document(
                title=doc_data["title"],
                description=doc_data["description"]
            )
            session.add(doc)
            session.flush()
            logger.info(f"新規ドキュメントを作成: {doc_data['title']}")

        # リビジョンを作成 (既存ドキュメントの場合は既存のリビジョンをチェック)
        for rev_data in doc_data["revisions"]:
            # リビジョンが既に存在するか確認
            existing_rev_query = select(DocumentRevision).where(
                DocumentRevision.document_id == doc.id,
                DocumentRevision.version == rev_data["version"]
            )
            existing_rev_result = session.execute(existing_rev_query)
            existing_rev = existing_rev_result.scalar_one_or_none()

            if existing_rev:
                logger.info(f"既存リビジョンをスキップ: {doc.title} v{rev_data['version']}")
                continue

            # 同期版でのコンテンツ保存
            # 同期処理では非同期のStorageServiceを直接使用できないため、
            # ローカルストレージに直接保存する簡易的な方法を使用
            storage_dir = os.path.join("storage", "documents", str(doc.id))
            os.makedirs(storage_dir, exist_ok=True)
            file_path = os.path.join(storage_dir, f"{rev_data['version']}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rev_data["content"], f, ensure_ascii=False, indent=2)
            storage_key = os.path.join("documents", str(doc.id), f"{rev_data['version']}.json")

            # リビジョンを作成
            rev = DocumentRevision(
                document_id=doc.id,
                version=rev_data["version"],
                storage_key=storage_key,
                change_summary=rev_data["change_summary"],
                created_by=None  # 実際の環境では認証ユーザーのIDを設定
            )
            session.add(rev)
            logger.info(f"新規リビジョンを作成: {doc.title} v{rev_data['version']}")

        # ノードとの関連付け (既存のリンクをチェック)
        for i, node_handle in enumerate(doc_data["nodes"]):
            if node_handle in node_mapping:
                # リンクが既に存在するか確認
                existing_link_query = select(NodeDocumentLink).where(
                    NodeDocumentLink.node_id == node_mapping[node_handle],
                    NodeDocumentLink.document_id == doc.id
                )
                existing_link_result = session.execute(existing_link_query)
                existing_link = existing_link_result.scalar_one_or_none()

                if existing_link:
                    logger.info(f"既存ノードリンクをスキップ: {node_handle} -> {doc.title}")
                    continue

                # 新規リンクを作成
                link = NodeDocumentLink(
                    node_id=node_mapping[node_handle],
                    document_id=doc.id,
                    order_position=i,
                    relation_type="primary"
                )
                session.add(link)
                logger.info(f"新規ノードリンクを作成: {node_handle} -> {doc.title}")
            else:
                logger.warning(f"ノードハンドル '{node_handle}' に対応するノードが見つかりません")

    session.commit()
    logger.info("ドキュメントデータのシードが完了しました")

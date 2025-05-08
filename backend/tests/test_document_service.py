import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.document import DocumentService
from src.db.models import Document, DocumentRevision, NodeDocumentLink, RoadmapNode

# テスト用データ
test_document_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
test_node_id = uuid.UUID("00000000-0000-0000-0000-000000000002")
test_document_content = {
    "title": "テストドキュメント",
    "sections": [
        {"title": "セクション1", "content": "セクション1の内容"},
        {"title": "セクション2", "content": "セクション2の内容"}
    ]
}

@pytest.fixture
def document_service():
    """DocumentServiceのインスタンスを返すフィクスチャ"""
    return DocumentService()

@pytest.fixture
def mock_db():
    """モックDBセッションを返すフィクスチャ"""
    db = AsyncMock(spec=AsyncSession)

    # executeメソッドのモック
    mock_result = MagicMock()
    db.execute.return_value = mock_result

    # scalar_one_or_noneメソッドのモック
    mock_result.scalar_one_or_none.return_value = None

    return db

@pytest.mark.asyncio
async def test_get_document(document_service, mock_db):
    """get_documentメソッドのテスト"""
    # モックドキュメントの作成
    mock_document = Document(
        id=test_document_id,
        title="テストドキュメント",
        description="テスト説明",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # scalar_one_or_noneの戻り値をモックドキュメントに設定
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_document

    # テスト対象メソッドの呼び出し
    result = await document_service.get_document(mock_db, test_document_id)

    # 結果の検証
    assert result == mock_document
    assert result.id == test_document_id
    assert mock_db.execute.called

@pytest.mark.asyncio
async def test_get_document_not_found(document_service, mock_db):
    """存在しないドキュメントIDでget_documentを呼び出した場合のテスト"""
    # scalar_one_or_noneがNoneを返すようにする
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    # テスト対象メソッドの呼び出し
    result = await document_service.get_document(mock_db, test_document_id)

    # 結果の検証
    assert result is None
    assert mock_db.execute.called

@pytest.mark.asyncio
async def test_get_document_with_revisions(document_service, mock_db):
    """get_document_with_revisionsメソッドのテスト"""
    # モックドキュメントの作成
    mock_document = Document(
        id=test_document_id,
        title="テストドキュメント",
        description="テスト説明",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # リビジョンを追加
    mock_document.revisions = [
        DocumentRevision(
            id=uuid.uuid4(),
            document_id=test_document_id,
            version="1.0.0",
            storage_key=f"documents/{test_document_id}/1.0.0.json",
            change_summary="初期バージョン",
            created_at=datetime.now()
        ),
        DocumentRevision(
            id=uuid.uuid4(),
            document_id=test_document_id,
            version="1.1.0",
            storage_key=f"documents/{test_document_id}/1.1.0.json",
            change_summary="更新バージョン",
            created_at=datetime.now()
        )
    ]

    # scalar_one_or_noneの戻り値をモックドキュメントに設定
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_document

    # テスト対象メソッドの呼び出し
    result = await document_service.get_document_with_revisions(mock_db, test_document_id)

    # 結果の検証
    assert result == mock_document
    assert len(result.revisions) == 2
    assert mock_db.execute.called

@pytest.mark.asyncio
async def test_get_latest_revision(document_service, mock_db):
    """get_latest_revisionメソッドのテスト"""
    # モックリビジョンの作成
    latest_revision = DocumentRevision(
        id=uuid.uuid4(),
        document_id=test_document_id,
        version="1.1.0",
        storage_key=f"documents/{test_document_id}/1.1.0.json",
        change_summary="最新バージョン",
        created_at=datetime.now()
    )

    # scalar_one_or_noneの戻り値をモックリビジョンに設定
    mock_db.execute.return_value.scalar_one_or_none.return_value = latest_revision

    # テスト対象メソッドの呼び出し
    result = await document_service.get_latest_revision(mock_db, test_document_id)

    # 結果の検証
    assert result == latest_revision
    assert result.version == "1.1.0"
    assert mock_db.execute.called

@pytest.mark.asyncio
async def test_get_revision_by_version(document_service, mock_db):
    """get_revision_by_versionメソッドのテスト"""
    # モックリビジョンの作成
    target_revision = DocumentRevision(
        id=uuid.uuid4(),
        document_id=test_document_id,
        version="1.0.0",
        storage_key=f"documents/{test_document_id}/1.0.0.json",
        change_summary="指定バージョン",
        created_at=datetime.now()
    )

    # scalar_one_or_noneの戻り値をモックリビジョンに設定
    mock_db.execute.return_value.scalar_one_or_none.return_value = target_revision

    # テスト対象メソッドの呼び出し
    result = await document_service.get_revision_by_version(mock_db, test_document_id, "1.0.0")

    # 結果の検証
    assert result == target_revision
    assert result.version == "1.0.0"
    assert mock_db.execute.called

@pytest.mark.asyncio
@patch.object(DocumentService, 'save_content')
async def test_create_document(mock_save_content, document_service, mock_db):
    """create_documentメソッドのテスト"""
    # save_contentメソッドのモック
    mock_save_content.return_value = f"documents/{test_document_id}/1.0.0.json"

    # flushメソッドのモック
    mock_db.flush = AsyncMock()

    # テスト対象メソッドの呼び出し
    result = await document_service.create_document(
        mock_db,
        title="テストドキュメント",
        description="テスト説明",
        content=test_document_content
    )

    # 結果の検証
    assert isinstance(result, Document)
    assert result.title == "テストドキュメント"
    assert result.description == "テスト説明"
    # addメソッドが呼び出されたことを確認（モックが正しく設定されていることを確認）
    assert mock_db.add.called
    # flushメソッドが呼び出されたことを確認
    assert mock_db.flush.called
    # save_contentメソッドが呼び出されたことを確認
    assert mock_save_content.called

@pytest.mark.asyncio
@patch.object(DocumentService, 'get_document')
@patch.object(DocumentService, 'get_latest_revision')
@patch.object(DocumentService, 'save_content')
@patch.object(DocumentService, 'load_content')
async def test_update_document(mock_load_content, mock_save_content, mock_get_latest_revision, mock_get_document, document_service, mock_db):
    """update_documentメソッドのテスト"""
    # モックドキュメントの作成
    mock_document = Document(
        id=test_document_id,
        title="テストドキュメント",
        description="テスト説明",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # get_documentメソッドのモック
    mock_get_document.return_value = mock_document

    # get_latest_revisionメソッドのモック
    mock_latest_revision = DocumentRevision(
        id=uuid.uuid4(),
        document_id=test_document_id,
        version="1.0.0",
        storage_key=f"documents/{test_document_id}/1.0.0.json",
        change_summary="初期バージョン",
        created_at=datetime.now()
    )
    mock_get_latest_revision.return_value = mock_latest_revision

    # load_contentメソッドのモック
    mock_load_content.return_value = test_document_content

    # save_contentメソッドのモック
    mock_save_content.return_value = f"documents/{test_document_id}/1.1.0.json"

    # flushメソッドのモック
    mock_db.flush = AsyncMock()

    # テスト対象メソッドの呼び出し
    doc, rev = await document_service.update_document(
        mock_db,
        document_id=test_document_id,
        content=test_document_content,
        version_type="minor",
        change_summary="更新内容"
    )

    # 結果の検証
    assert doc == mock_document
    assert isinstance(rev, DocumentRevision)
    assert rev.version == "1.1.0"  # マイナーバージョンアップ
    assert rev.change_summary == "更新内容"
    assert mock_db.add.called
    assert mock_db.flush.called
    assert mock_save_content.called
    assert mock_load_content.called

@pytest.mark.asyncio
async def test_get_node_documents(document_service, mock_db):
    """get_node_documentsメソッドのテスト"""
    # モックノードの作成
    mock_node = RoadmapNode(
        id=test_node_id,
        title="テストノード",
        created_at=datetime.now()
    )

    # モックドキュメントの作成
    mock_document = Document(
        id=test_document_id,
        title="テストドキュメント",
        description="テスト説明",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # 呼び出し順序に応じて異なる結果を返すモックを設定
    mock_result1 = MagicMock()
    mock_result1.scalar_one_or_none.return_value = mock_node

    mock_result2 = MagicMock()
    mock_result2.scalars.return_value = MagicMock()
    mock_result2.scalars.return_value.all.return_value = [mock_document]

    # executeメソッドが呼ばれるたびに順番に結果を返すよう設定
    mock_db.execute.side_effect = [mock_result1, mock_result2]

    # テスト対象メソッドの呼び出し
    node, documents = await document_service.get_node_documents(mock_db, test_node_id)

    # 結果の検証
    assert node == mock_node
    assert len(documents) == 1
    assert documents[0] == mock_document
    assert mock_db.execute.call_count == 2

@pytest.mark.asyncio
async def test_link_node_document(document_service, mock_db):
    """link_node_documentメソッドのテスト"""
    # モックノードの作成
    mock_node = RoadmapNode(
        id=test_node_id,
        title="テストノード",
        created_at=datetime.now()
    )

    # モックドキュメントの作成
    mock_document = Document(
        id=test_document_id,
        title="テストドキュメント",
        created_at=datetime.now()
    )

    # 呼び出し順序に応じて異なる結果を返すモックを設定
    mock_node_result = MagicMock()
    mock_node_result.scalar_one_or_none.return_value = mock_node

    mock_doc_result = MagicMock()
    mock_doc_result.scalar_one_or_none.return_value = mock_document

    mock_link_result = MagicMock()
    mock_link_result.scalar_one_or_none.return_value = None

    mock_max_order_result = MagicMock()
    mock_max_order_result.scalar_one_or_none.return_value = 100

    # executeメソッドが呼ばれるたびに順番に結果を返すよう設定
    mock_db.execute.side_effect = [
        mock_node_result,
        mock_doc_result,
        mock_link_result,
        mock_max_order_result
    ]

    # flushメソッドのモック設定
    mock_db.flush = AsyncMock()

    # テスト対象メソッドの呼び出し
    result = await document_service.link_node_document(
        mock_db,
        node_id=test_node_id,
        document_id=test_document_id,
        relation_type="primary"
    )

    # 結果の検証
    assert isinstance(result, NodeDocumentLink)
    assert result.node_id == test_node_id
    assert result.document_id == test_document_id
    assert result.relation_type == "primary"
    assert mock_db.add.called
    assert mock_db.flush.called
    assert mock_db.execute.call_count == 4

@pytest.mark.asyncio
async def test_unlink_node_document(document_service, mock_db):
    """unlink_node_documentメソッドのテスト"""
    # モックリンクの作成
    mock_link = NodeDocumentLink(
        id=uuid.uuid4(),
        node_id=test_node_id,
        document_id=test_document_id,
        relation_type="primary",
        created_at=datetime.now()
    )

    # scalar_one_or_noneの戻り値をモックリンクに設定
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_link

    # flushメソッドのAsyncMockとして設定
    mock_db.flush = AsyncMock()

    # テスト対象メソッドの呼び出し
    result = await document_service.unlink_node_document(mock_db, test_node_id, test_document_id)

    # 結果の検証
    assert result is True
    assert mock_db.delete.called
    assert mock_db.flush.called

"""
ストレージサービスのテスト

このモジュールでは、ストレージサービスの基本的な機能をテストします。
"""
import os
import json
import pytest
import tempfile
import shutil
from uuid import uuid4
from unittest.mock import patch, MagicMock

# コンテナ内のパスに合わせて修正
from src.services.storage import LocalStorageService, MinioStorageService, get_storage_service

# テスト用のデータ
TEST_DOCUMENT_ID = str(uuid4())
TEST_VERSION = "1.0.0"
TEST_CONTENT = {
    "title": "テスト文書",
    "sections": [
        {
            "title": "セクション1",
            "content": "これはテスト用のコンテンツです。"
        }
    ]
}


class TestLocalStorageService:
    """LocalStorageServiceのテスト"""

    @pytest.fixture
    def temp_storage_dir(self):
        """一時的なストレージディレクトリを作成して提供する"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # テスト終了後にディレクトリを削除
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def local_storage(self, temp_storage_dir):
        """テスト用のLocalStorageServiceインスタンスを作成する"""
        return LocalStorageService(base_storage_path=temp_storage_dir)

    @pytest.mark.asyncio
    async def test_save_and_load_content(self, local_storage):
        """コンテンツの保存と読み込みをテストする"""
        # コンテンツを保存
        storage_key = await local_storage.save_content(TEST_CONTENT, TEST_DOCUMENT_ID, TEST_VERSION)

        # 保存されたキーが正しいか確認
        expected_key = os.path.join("documents", TEST_DOCUMENT_ID, f"{TEST_VERSION}.json")
        assert storage_key == expected_key

        # ディレクトリにファイルが作成されたか確認
        file_path = os.path.join(local_storage.base_path, storage_key)
        assert os.path.exists(file_path)

        # コンテンツを読み込み
        loaded_content = await local_storage.load_content(storage_key)

        # 保存したコンテンツと読み込んだコンテンツが一致するか確認
        assert loaded_content == TEST_CONTENT

    @pytest.mark.asyncio
    async def test_delete_content(self, local_storage):
        """コンテンツの削除をテストする"""
        # コンテンツを保存
        storage_key = await local_storage.save_content(TEST_CONTENT, TEST_DOCUMENT_ID, TEST_VERSION)
        file_path = os.path.join(local_storage.base_path, storage_key)

        # 削除前にファイルが存在することを確認
        assert os.path.exists(file_path)

        # コンテンツを削除
        result = await local_storage.delete_content(storage_key)
        assert result is True

        # 削除後にファイルが存在しないことを確認
        assert not os.path.exists(file_path)

        # 存在しないファイルを削除しようとした場合
        result = await local_storage.delete_content("non_existent_key")
        assert result is False

    @pytest.mark.asyncio
    async def test_list_contents(self, local_storage):
        """コンテンツのリスト取得をテストする"""
        # 複数のコンテンツを保存
        doc_id_1 = str(uuid4())
        doc_id_2 = str(uuid4())

        await local_storage.save_content(TEST_CONTENT, doc_id_1, "1.0.0")
        await local_storage.save_content(TEST_CONTENT, doc_id_1, "1.1.0")
        await local_storage.save_content(TEST_CONTENT, doc_id_2, "1.0.0")

        # doc_id_1のコンテンツだけをリスト取得
        contents = await local_storage.list_contents(f"documents/{doc_id_1}")

        # 結果を検証
        assert len(contents) == 2
        assert all(doc_id_1 in key for key in contents)
        assert all(key.endswith(".json") for key in contents)

        # 存在しないパスの場合
        contents = await local_storage.list_contents("non_existent_path")
        assert len(contents) == 0


class TestMinioStorageService:
    """MinioStorageServiceのテスト（モックを使用）"""

    @pytest.fixture
    def mock_settings(self):
        """設定モジュールをモックする"""
        with patch('src.services.storage.settings', autospec=True) as mock_settings:
            # 設定のモック
            mock_settings.MINIO_BUCKET_NAME = "test-bucket"
            mock_settings.MINIO_ENDPOINT = "localhost"
            mock_settings.MINIO_PORT = "9000"
            mock_settings.MINIO_ROOT_USER = "minioadmin"
            mock_settings.MINIO_ROOT_PASSWORD = "minioadmin"
            mock_settings.MINIO_USE_SSL = False
            mock_settings.STORAGE_TYPE = "minio"
            yield mock_settings

    @pytest.fixture
    def mock_minio_client(self):
        """MinIOクライアントをモックする"""
        with patch('src.services.storage.Minio', autospec=True) as mock_minio:
            # Minioクライアントのモック
            mock_client = MagicMock()
            mock_minio.return_value = mock_client

            # バケット存在チェックのモック
            mock_client.bucket_exists.return_value = True
            yield mock_client

    @pytest.fixture
    def minio_storage(self, mock_settings, mock_minio_client):
        """テスト用のMinioStorageServiceインスタンスを作成する"""
        return MinioStorageService()

    @pytest.mark.asyncio
    async def test_save_content(self, minio_storage, mock_minio_client):
        """MinIOへのコンテンツ保存をテストする"""
        storage_key = await minio_storage.save_content(TEST_CONTENT, TEST_DOCUMENT_ID, TEST_VERSION)

        # 保存されたキーが正しいか確認
        expected_key = f"documents/{TEST_DOCUMENT_ID}/{TEST_VERSION}.json"
        assert storage_key == expected_key

        # Minioのput_objectメソッドが呼ばれたか確認
        mock_minio_client.put_object.assert_called_once()

        # 呼び出し引数を確認
        call_args = mock_minio_client.put_object.call_args[1]
        assert call_args['bucket_name'] == "test-bucket"
        assert call_args['object_name'] == expected_key
        assert call_args['content_type'] == 'application/json'

    @pytest.mark.asyncio
    async def test_load_content(self, minio_storage, mock_minio_client):
        """MinIOからのコンテンツ読み込みをテストする"""
        # get_objectのモック応答を設定
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(TEST_CONTENT).encode('utf-8')
        mock_minio_client.get_object.return_value = mock_response

        # コンテンツを読み込み
        storage_key = f"documents/{TEST_DOCUMENT_ID}/{TEST_VERSION}.json"
        loaded_content = await minio_storage.load_content(storage_key)

        # Minioのget_objectメソッドが呼ばれたか確認
        mock_minio_client.get_object.assert_called_with(
            bucket_name="test-bucket",
            object_name=storage_key
        )

        # 読み込まれたコンテンツが正しいか確認
        assert loaded_content == TEST_CONTENT

    @pytest.mark.asyncio
    async def test_delete_content(self, minio_storage, mock_minio_client):
        """MinIOからのコンテンツ削除をテストする"""
        storage_key = f"documents/{TEST_DOCUMENT_ID}/{TEST_VERSION}.json"

        # コンテンツを削除
        result = await minio_storage.delete_content(storage_key)

        # Minioのremove_objectメソッドが呼ばれたか確認
        mock_minio_client.remove_object.assert_called_with(
            bucket_name="test-bucket",
            object_name=storage_key
        )

        # 削除が成功したか確認
        assert result is True

    @pytest.mark.asyncio
    async def test_list_contents(self, minio_storage, mock_minio_client):
        """MinIOのコンテンツリスト取得をテストする"""
        prefix = f"documents/{TEST_DOCUMENT_ID}"

        # list_objectsのモック応答を設定
        mock_obj1 = MagicMock()
        mock_obj1.object_name = f"{prefix}/1.0.0.json"

        mock_obj2 = MagicMock()
        mock_obj2.object_name = f"{prefix}/1.1.0.json"

        mock_obj3 = MagicMock()
        mock_obj3.object_name = f"{prefix}/data.txt"  # JSONでないファイル

        mock_minio_client.list_objects.return_value = [mock_obj1, mock_obj2, mock_obj3]

        # コンテンツリストを取得
        contents = await minio_storage.list_contents(prefix)

        # Minioのlist_objectsメソッドが呼ばれたか確認
        mock_minio_client.list_objects.assert_called_with(
            bucket_name="test-bucket",
            prefix=prefix,
            recursive=True
        )

        # 結果を検証（JSONファイルのみ取得されるか）
        assert len(contents) == 2
        assert mock_obj1.object_name in contents
        assert mock_obj2.object_name in contents
        assert mock_obj3.object_name not in contents


def test_get_storage_service_local():
    """get_storage_serviceがローカルストレージを返すかテストする"""
    with patch('src.services.storage.settings') as mock_settings:
        mock_settings.STORAGE_TYPE = "local"

        storage = get_storage_service()
        assert isinstance(storage, LocalStorageService)


def test_get_storage_service_minio():
    """get_storage_serviceがMinIOストレージを返すかテストする"""
    with patch('src.services.storage.settings') as mock_settings:
        mock_settings.STORAGE_TYPE = "minio"
        # MinioStorageServiceの初期化中にエラーが発生しないように設定をモック
        mock_settings.MINIO_ENDPOINT = "localhost"
        mock_settings.MINIO_PORT = "9000"
        mock_settings.MINIO_ROOT_USER = "minioadmin"
        mock_settings.MINIO_ROOT_PASSWORD = "minioadmin"
        mock_settings.MINIO_USE_SSL = False
        mock_settings.MINIO_BUCKET_NAME = "test-bucket"

        with patch('src.services.storage.Minio') as mock_minio:
            # バケット存在チェックのモック
            mock_client = MagicMock()
            mock_client.bucket_exists.return_value = True
            mock_minio.return_value = mock_client

            storage = get_storage_service()
            assert isinstance(storage, MinioStorageService)

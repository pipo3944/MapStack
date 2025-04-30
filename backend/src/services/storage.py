"""
ストレージサービスモジュール

このモジュールは、ファイルストレージに関連する機能を提供します。
ローカルファイルシステム、MinIO、S3などの異なるストレージバックエンドを抽象化します。
"""

import os
import json
import logging
from typing import Dict, Union, List, Optional, BinaryIO
from abc import ABC, abstractmethod
from uuid import UUID
import io

from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException

from ..config import settings

logger = logging.getLogger(__name__)


class StorageService(ABC):
    """ストレージサービスの抽象基底クラス"""

    @abstractmethod
    def get_storage_key(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージキーを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        pass

    @abstractmethod
    async def save_content(self, content: Dict, document_id: Union[UUID, str], version: str) -> str:
        """
        コンテンツを保存する

        Args:
            content: 保存するコンテンツデータ
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        pass

    @abstractmethod
    async def load_content(self, storage_key: str) -> Dict:
        """
        コンテンツを読み込む

        Args:
            storage_key: ストレージキー

        Returns:
            読み込んだコンテンツデータ

        Raises:
            FileNotFoundError: 指定されたキーのコンテンツが見つからない場合
        """
        pass

    @abstractmethod
    async def delete_content(self, storage_key: str) -> bool:
        """
        コンテンツを削除する

        Args:
            storage_key: ストレージキー

        Returns:
            削除が成功した場合はTrue、それ以外はFalse
        """
        pass

    @abstractmethod
    async def list_contents(self, prefix: str) -> List[str]:
        """
        指定したプレフィックスに一致するコンテンツの一覧を取得する

        Args:
            prefix: コンテンツのプレフィックス

        Returns:
            一致するストレージキーのリスト
        """
        pass


class LocalStorageService(StorageService):
    """ローカルファイルシステムを使用したストレージサービス"""

    def __init__(self, base_storage_path: str = "storage"):
        """
        Args:
            base_storage_path: ストレージのベースディレクトリ
        """
        self.base_path = base_storage_path
        os.makedirs(os.path.join(self.base_path, "documents"), exist_ok=True)

    def get_document_path(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージパスを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージパス
        """
        document_dir = os.path.join(self.base_path, "documents", str(document_id))
        os.makedirs(document_dir, exist_ok=True)
        return os.path.join(document_dir, f"{version}.json")

    def get_storage_key(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージキーを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        return os.path.join("documents", str(document_id), f"{version}.json")

    async def save_content(self, content: Dict, document_id: Union[UUID, str], version: str) -> str:
        """
        コンテンツをファイルに保存する

        Args:
            content: 保存するコンテンツデータ
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        file_path = self.get_document_path(document_id, version)
        storage_key = self.get_storage_key(document_id, version)

        try:
            # ディレクトリが存在することを確認
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # JSONファイルとして保存
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            logger.info(f"Document content saved to {file_path}")
            return storage_key
        except Exception as e:
            logger.error(f"Error saving document content: {str(e)}")
            raise

    async def load_content(self, storage_key: str) -> Dict:
        """
        コンテンツをファイルから読み込む

        Args:
            storage_key: ストレージキー

        Returns:
            読み込んだコンテンツデータ

        Raises:
            FileNotFoundError: 指定されたキーのコンテンツが見つからない場合
        """
        file_path = os.path.join(self.base_path, storage_key)

        if not os.path.exists(file_path):
            logger.warning(f"Document content not found at {file_path}")
            raise FileNotFoundError(f"Document content not found: {storage_key}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            logger.info(f"Document content loaded from {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error loading document content: {str(e)}")
            raise

    async def delete_content(self, storage_key: str) -> bool:
        """
        コンテンツをファイルから削除する

        Args:
            storage_key: ストレージキー

        Returns:
            削除が成功した場合はTrue、それ以外はFalse
        """
        file_path = os.path.join(self.base_path, storage_key)

        if not os.path.exists(file_path):
            logger.warning(f"Document content not found for deletion: {file_path}")
            return False

        try:
            os.remove(file_path)
            logger.info(f"Document content deleted: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document content: {str(e)}")
            return False

    async def list_contents(self, prefix: str) -> List[str]:
        """
        指定したプレフィックスに一致するコンテンツの一覧を取得する

        Args:
            prefix: コンテンツのプレフィックス

        Returns:
            一致するストレージキーのリスト
        """
        base_dir = os.path.join(self.base_path, prefix)
        result = []

        if not os.path.exists(base_dir):
            return result

        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.json'):
                    # ベースパスからの相対パスに変換
                    rel_path = os.path.relpath(os.path.join(root, file), self.base_path)
                    result.append(rel_path)

        return result


class MinioStorageService(StorageService):
    """MinIO/S3を使用したストレージサービス"""

    def __init__(self):
        """MinIOクライアントを初期化する"""
        try:
            self.client = Minio(
                f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}",
                access_key=settings.MINIO_ROOT_USER,
                secret_key=settings.MINIO_ROOT_PASSWORD,
                secure=settings.MINIO_USE_SSL
            )

            # バケットが存在するか確認し、なければ作成
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
                logger.info(f"Bucket '{settings.MINIO_BUCKET_NAME}' created")
            else:
                logger.info(f"Bucket '{settings.MINIO_BUCKET_NAME}' already exists")
        except S3Error as e:
            logger.error(f"Error initializing MinIO client: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Storage service initialization error: {str(e)}")

    def get_storage_key(self, document_id: Union[UUID, str], version: str) -> str:
        """
        ドキュメントのストレージキーを取得する

        Args:
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        return f"documents/{document_id}/{version}.json"

    async def save_content(self, content: Dict, document_id: Union[UUID, str], version: str) -> str:
        """
        コンテンツをMinIOに保存する

        Args:
            content: 保存するコンテンツデータ
            document_id: ドキュメントID
            version: ドキュメントバージョン

        Returns:
            ストレージキー
        """
        storage_key = self.get_storage_key(document_id, version)

        try:
            # JSONデータをバイトストリームに変換
            json_data = json.dumps(content, ensure_ascii=False, indent=2).encode('utf-8')
            data_stream = io.BytesIO(json_data)
            data_size = len(json_data)

            # MinIOにアップロード
            self.client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=storage_key,
                data=data_stream,
                length=data_size,
                content_type='application/json'
            )

            logger.info(f"Document content saved to MinIO: {storage_key}")
            return storage_key
        except S3Error as e:
            logger.error(f"Error saving document to MinIO: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving document: {str(e)}")

    async def load_content(self, storage_key: str) -> Dict:
        """
        コンテンツをMinIOから読み込む

        Args:
            storage_key: ストレージキー

        Returns:
            読み込んだコンテンツデータ

        Raises:
            FileNotFoundError: 指定されたキーのコンテンツが見つからない場合
        """
        try:
            # オブジェクトを取得
            response = self.client.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=storage_key
            )

            # データを読み込んでJSONとしてパース
            data = response.read().decode('utf-8')
            content = json.loads(data)

            logger.info(f"Document content loaded from MinIO: {storage_key}")
            return content
        except S3Error as e:
            if e.code == 'NoSuchKey':
                logger.warning(f"Document content not found in MinIO: {storage_key}")
                raise FileNotFoundError(f"Document content not found: {storage_key}")
            logger.error(f"Error loading document from MinIO: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error loading document: {str(e)}")

    async def delete_content(self, storage_key: str) -> bool:
        """
        コンテンツをMinIOから削除する

        Args:
            storage_key: ストレージキー

        Returns:
            削除が成功した場合はTrue、それ以外はFalse
        """
        try:
            # オブジェクトを削除
            self.client.remove_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=storage_key
            )

            logger.info(f"Document content deleted from MinIO: {storage_key}")
            return True
        except S3Error as e:
            logger.error(f"Error deleting document from MinIO: {str(e)}")
            return False

    async def list_contents(self, prefix: str) -> List[str]:
        """
        指定したプレフィックスに一致するコンテンツの一覧を取得する

        Args:
            prefix: コンテンツのプレフィックス

        Returns:
            一致するストレージキーのリスト
        """
        try:
            objects = self.client.list_objects(
                bucket_name=settings.MINIO_BUCKET_NAME,
                prefix=prefix,
                recursive=True
            )

            result = [obj.object_name for obj in objects if obj.object_name.endswith('.json')]
            return result
        except S3Error as e:
            logger.error(f"Error listing objects from MinIO: {str(e)}")
            return []


def get_storage_service() -> StorageService:
    """
    設定に基づいて適切なストレージサービスのインスタンスを返す

    Returns:
        StorageServiceのインスタンス
    """
    storage_type = settings.STORAGE_TYPE.lower()

    if storage_type == "minio" or storage_type == "s3":
        return MinioStorageService()
    else:  # "local"または他の値の場合
        return LocalStorageService()

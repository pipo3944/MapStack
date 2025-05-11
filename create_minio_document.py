#!/usr/bin/env python3
"""
MinIOにドキュメントコンテンツを作成するスクリプト

ドキュメントIDとバージョンに対応するコンテンツファイルをMinIOに作成します。
"""

import io
import json
import sys
from uuid import UUID

from minio import Minio
from minio.error import S3Error


# MinIO接続設定
MINIO_ENDPOINT = "localhost:9000"  # ホストからアクセスするため、localhostに変更
MINIO_ROOT_USER = "minioadmin"
MINIO_ROOT_PASSWORD = "minioadmin"
MINIO_USE_SSL = False
MINIO_BUCKET_NAME = "mapstack-documents"


def create_document_content(client, document_id, version="1.0.0"):
    """
    指定されたドキュメントIDとバージョンのコンテンツをMinIOに作成する

    Args:
        client: MinIOクライアントインスタンス
        document_id: ドキュメントID（UUID文字列）
        version: ドキュメントバージョン（デフォルト: 1.0.0）

    Returns:
        作成したオブジェクトのキー
    """
    # ストレージキーの構築
    storage_key = f"documents/{document_id}/{version}.json"

    # サンプルコンテンツの作成
    sample_content = {
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

    # JSONデータをバイトストリームに変換
    json_data = json.dumps(sample_content, ensure_ascii=False, indent=2).encode('utf-8')
    data_stream = io.BytesIO(json_data)
    data_size = len(json_data)

    try:
        # オブジェクトが既に存在するか確認
        try:
            client.stat_object(MINIO_BUCKET_NAME, storage_key)
            print(f"オブジェクトは既に存在します: {storage_key}")
            return storage_key
        except S3Error as e:
            if e.code != 'NoSuchKey':
                raise

        # MinIOにアップロード
        client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=storage_key,
            data=data_stream,
            length=data_size,
            content_type='application/json'
        )

        print(f"ドキュメントコンテンツを作成しました: {storage_key}")
        return storage_key
    except S3Error as e:
        print(f"MinIOエラー: {e.code} - {e.message}")
        raise


def ensure_bucket_exists(client):
    """
    バケットが存在することを確認し、存在しない場合は作成する

    Args:
        client: MinIOクライアントインスタンス
    """
    try:
        if not client.bucket_exists(MINIO_BUCKET_NAME):
            client.make_bucket(MINIO_BUCKET_NAME)
            print(f"バケットを作成しました: {MINIO_BUCKET_NAME}")
        else:
            print(f"バケットは既に存在します: {MINIO_BUCKET_NAME}")
    except S3Error as e:
        print(f"バケット確認中にエラーが発生しました: {e.code} - {e.message}")
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法: python create_minio_document.py <document_id> [version]")
        sys.exit(1)

    document_id = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"

    try:
        # UUIDの検証
        UUID(document_id)

        # MinIOクライアントの初期化
        client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ROOT_USER,
            secret_key=MINIO_ROOT_PASSWORD,
            secure=MINIO_USE_SSL
        )

        # バケットの確認
        ensure_bucket_exists(client)

        # コンテンツの作成
        storage_key = create_document_content(client, document_id, version)
        print(f"完了: {storage_key}")
    except ValueError:
        print(f"エラー: 無効なUUID形式です: {document_id}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {str(e)}")
        sys.exit(1)

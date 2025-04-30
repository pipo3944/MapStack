import os
from functools import lru_cache
from typing import Any, Dict, Optional, List

from pydantic import PostgresDsn, field_validator, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MapStack API"

    # PostgreSQL設定
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "ms-db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mapstack")

    # ホスト環境からの接続用設定
    HOST_POSTGRES_HOST: Optional[str] = os.getenv("HOST_POSTGRES_HOST")
    HOST_POSTGRES_PORT: Optional[str] = os.getenv("HOST_POSTGRES_PORT")

    # SQLAlchemyログ出力設定
    DB_ECHO_LOG: bool = False

    # Redis設定
    REDIS_HOST: str = os.getenv("REDIS_HOST", "ms-redis")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")

    # ストレージ設定
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # 'local', 'minio', 's3'

    # MinIO/S3設定
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "ms-minio")
    MINIO_PORT: str = os.getenv("MINIO_PORT", "9000")
    MINIO_USE_SSL: bool = os.getenv("MINIO_USE_SSL", "false").lower() == "true"
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "mapstack-documents")

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        """Redisの接続URLを構築して返す"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """PostgreSQLの接続URLを構築して返す"""
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=int(self.POSTGRES_PORT),
            path=f"/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def HOST_DATABASE_URL(self) -> Optional[PostgresDsn]:
        """ホストマシンからの接続URLを構築して返す"""
        if not self.HOST_POSTGRES_HOST:
            return None

        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.HOST_POSTGRES_HOST,
            port=int(self.HOST_POSTGRES_PORT or self.POSTGRES_PORT),
            path=f"/{self.POSTGRES_DB}"
        )

    # 環境設定
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # セキュリティ設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "請負業者あわせて使い勝手金髪をかけろ")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "11520"))  # 8日間

    # CORSの設定
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 開発環境かどうかを判定するヘルパーメソッド
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """設定をキャッシュして返す"""
    return Settings()

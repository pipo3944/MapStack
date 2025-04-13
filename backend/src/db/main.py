"""
SQLAlchemyによるデータベース接続とセッションの設定
"""
from typing import AsyncGenerator, Generator
import logging
import os
import asyncpg

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# 相対インポートに変更
from ..config.settings import get_settings
from .base import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
settings = get_settings()

# 環境に基づいてデータベースURLを選択
def get_database_url():
    """環境に基づいて適切なデータベースURLを返す"""
    # 直接ホスト名とポートを指定（コンテナ名を使用）
    host = os.environ.get('POSTGRES_HOST', 'ms-db')
    port = os.environ.get('POSTGRES_PORT', '5432')
    user = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    database = os.environ.get('POSTGRES_DB', 'mapstack')

    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    logger.info(f"Using database URL: {url}")
    return url

# ダイレクト接続テスト（SQLAlchemyを使わない）
async def direct_async_connect():
    try:
        host = os.environ.get('POSTGRES_HOST', 'ms-db')
        port = os.environ.get('POSTGRES_PORT', '5432')
        user = os.environ.get('POSTGRES_USER', 'postgres')
        password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
        database = os.environ.get('POSTGRES_DB', 'mapstack')

        logger.info(f"Trying direct connection to: {host}:{port} (user: {user}, db: {database})")

        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        logger.info("Direct connection successful!")
        await conn.close()
        return True
    except Exception as e:
        logger.error(f"Direct connection failed: {e}")
        return False

# 非同期エンジンの設定
ASYNC_DATABASE_URL = get_database_url().replace("postgresql://", "postgresql+asyncpg://")
logger.info(f"Async database URL: {ASYNC_DATABASE_URL}")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DB_ECHO_LOG,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 同期エンジンの設定
SYNC_DATABASE_URL = get_database_url()
logger.info(f"Sync database URL: {SYNC_DATABASE_URL}")

sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=settings.DB_ECHO_LOG,
    future=True,
)
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPIのDependencyで使用するための非同期セッションファクトリ
    """
    # 事前に直接接続をテスト
    await direct_async_connect()

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db() -> Generator[Session, None, None]:
    """
    同期的なセッションファクトリ
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# CLIコマンドで使うための関数
def get_sync_session() -> Session:
    """
    同期セッションを取得する（CLI用）
    """
    return SessionLocal()

# データベースの初期化関数
def init_db() -> None:
    """
    テーブルを作成する
    """
    Base.metadata.create_all(bind=sync_engine)

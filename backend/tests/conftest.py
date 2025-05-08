import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.main import get_db
from src.db.base import Base
from uuid import UUID
import os
from src.db.models.document import Document, DocumentRevision
import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="function")
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    async_session_maker = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture(autouse=True)
async def setup_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # テスト後にdropしたい場合は以下を有効化
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(autouse=True)
async def seed_data(async_session, setup_database):
    # APIテスト用のドキュメントを投入
    doc = Document(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="テストドキュメント",
        description="テスト用説明"
    )
    async_session.add(doc)
    # ドキュメントリビジョンも追加
    revision = DocumentRevision(
        id=UUID("00000000-0000-0000-0000-000000000101"),
        document_id=doc.id,
        version="1.0.0",
        storage_key="documents/00000000-0000-0000-0000-000000000001/1.0.0.json",
        created_by=None,
        created_at=datetime.datetime.now()
    )
    async_session.add(revision)
    await async_session.commit()

@pytest_asyncio.fixture(autouse=True)
async def override_get_db(async_session):
    async def _override_get_db():
        yield async_session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides = {}

@pytest_asyncio.fixture(autouse=True, scope="function")
def cleanup_db():
    yield
    if os.path.exists("./test.db"):
        os.remove("./test.db")

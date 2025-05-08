from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import logging
import asyncio
from contextlib import asynccontextmanager

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# APIルータをインポート - パスを修正
from .api.v1 import api_router
from .db.main import direct_async_connect

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup処理
    logger.info("=========== 環境変数 ===========")
    for key in ['POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_USER', 'POSTGRES_DB', 'REDIS_HOST']:
        logger.info(f"{key}: {os.environ.get(key, 'Not set')}")

    logger.info("=========== ホスト名解決 ===========")
    try:
        import socket
        db_host = os.environ.get('POSTGRES_HOST', 'ms-db')
        ip_address = socket.gethostbyname(db_host)
        logger.info(f"Resolved {db_host} to {ip_address}")
    except Exception as e:
        logger.error(f"Failed to resolve hostname: {e}")

    logger.info("=========== データベース接続テスト ===========")
    try:
        result = await direct_async_connect()
        if result:
            logger.info("Database connection test: SUCCESS")
        else:
            logger.error("Database connection test: FAILED")
    except Exception as e:
        logger.error(f"Error during database connection test: {e}")
    yield
    # shutdown処理（リソース解放など）
    pass

app = FastAPI(
    title="MapStack API",
    description="AI学習プラットフォーム MapStack のバックエンドAPI",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",  # OpenAPI仕様のJSONを提供するURL
    docs_url="/api/docs",                # Swagger UIのURL
    redoc_url="/api/redoc",              # ReDocのURL
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MapStack API へようこそ！"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# APIルートを登録
app.include_router(api_router, prefix="/api/v1")

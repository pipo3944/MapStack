import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 環境変数から接続URLを取得または開発用デフォルト値を使用
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mapstack")

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)

# セッションファクトリーの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル定義のベースクラス
Base = declarative_base()

# データベースセッションの依存性関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
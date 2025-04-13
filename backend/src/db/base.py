"""
SQLAlchemyのベースモデルとORM関連の基本設定
"""
from sqlalchemy.ext.declarative import declarative_base

# モデル定義のベースクラス
Base = declarative_base()

# モデルクラスをインポートしてAlembicが検出できるようにする
# 新しいモデルを作成したら、ここにインポート文を追加してください
# from ..models.user import User
# from ..models.item import Item

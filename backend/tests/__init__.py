"""
MapStackアプリケーションのテストスイート

このパッケージには、アプリケーションの様々なコンポーネントのテストが含まれています。
"""
import sys
import os

# テストからアプリケーションコードにアクセスできるようにPYTHONPATHを設定
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

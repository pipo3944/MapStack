import logging

# ロガーの設定
logger = logging.getLogger("mapstack")

# デフォルトレベルを INFO に設定
logger.setLevel(logging.INFO)

# 標準出力へのハンドラーを追加
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

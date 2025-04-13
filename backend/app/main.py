from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MapStack API",
    description="AI学習プラットフォーム MapStack のバックエンドAPI",
    version="0.1.0",
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
# from backend.src.api import themes, roadmaps, contents, users
# app.include_router(themes.router, tags=["themes"], prefix="/api/themes")
# app.include_router(roadmaps.router, tags=["roadmaps"], prefix="/api/roadmaps")
# app.include_router(contents.router, tags=["contents"], prefix="/api/contents")
# app.include_router(users.router, tags=["users"], prefix="/api/users")

@app.on_event("startup")
async def startup_event():
    # データベース接続などの初期化処理
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # リソース解放などの終了処理
    pass 
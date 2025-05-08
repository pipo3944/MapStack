from fastapi import APIRouter

from .endpoints import roadmaps, documents

api_router = APIRouter()
api_router.include_router(roadmaps.router, tags=["roadmap"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(documents.node_router, tags=["nodes", "documents"])

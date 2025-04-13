from fastapi import APIRouter

from .endpoints import roadmaps

api_router = APIRouter()
api_router.include_router(roadmaps.router, tags=["roadmap"])

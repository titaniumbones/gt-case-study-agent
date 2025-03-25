from fastapi import APIRouter
from app.api.endpoints import advisor

api_router = APIRouter()

# Include advisor routes
api_router.include_router(advisor.router, tags=["advisor"])
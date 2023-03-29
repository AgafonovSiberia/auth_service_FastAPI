from fastapi import APIRouter
from app.api.routers import signup


api_router = APIRouter()
api_router.include_router(signup.router, tags=["auth"])
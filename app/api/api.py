from fastapi import APIRouter
from .routers import signup


api_router = APIRouter()
api_router.include_router(signup.router, tags=["auth"])

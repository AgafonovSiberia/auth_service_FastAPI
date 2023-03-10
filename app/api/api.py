from fastapi import APIRouter
from .routers import auth


"""Head API-router"""
api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])

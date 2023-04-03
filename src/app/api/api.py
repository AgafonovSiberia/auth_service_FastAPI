from fastapi import APIRouter

from app.api.routers import healhcheck, user

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(healhcheck.router, tags=["healthcheck"])

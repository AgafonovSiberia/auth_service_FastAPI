from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.api.routers import user


api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])


@api_router.get("/")
async def ping():
    return JSONResponse(status_code=200, content={})


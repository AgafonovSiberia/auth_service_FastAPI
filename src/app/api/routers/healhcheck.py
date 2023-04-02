from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/healthcheck")


@router.get("/")
async def health_check():
    return JSONResponse(status_code=200, content={})


def func():
    ...

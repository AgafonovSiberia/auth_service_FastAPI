from app.api.api import api_router
from app.api.routers import signup

api_router.include_router(signup.router, tags=["auth"])


from fastapi import FastAPI
from .config_reader import config
from app.api.api import api_router

app = FastAPI(title="AuthService",
              description="authorization service",
              openapi_url=f"{config.API_V1_URL}/openapi.json")

app.include_router(api_router)



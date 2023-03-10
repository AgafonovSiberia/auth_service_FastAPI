from fastapi import FastAPI
from .config_reader import config
from app.db.models import User, RefreshToken

app = FastAPI(title="AuthService",
              description="authorization service",
              openapi_url=f"{config.API_V1_URL}/openapi.json")




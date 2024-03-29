from fastapi import FastAPI

from app.api.setup import setup
from app.infrastructure.db.factory import create_pool

from .config_reader import config


def crate_app():
    return FastAPI(
        title="AuthService",
        description="authorization service_2",
        openapi_url=f"{config.API_V1_URL}/openapi.json",
    )


def init_app():
    current_app: FastAPI = crate_app()
    pool = create_pool()
    setup(current_app, pool)
    return current_app


app = init_app()

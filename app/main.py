from fastapi import FastAPI
from .config_reader import config
from app import depends
from app.db.engine import create_pool


def crate_app():
    return FastAPI(
        title="AuthService",
        description="authorization service",
        openapi_url=f"{config.API_V1_URL}/openapi.json",
    )


def init_app():
    app: FastAPI = crate_app()
    pool = create_pool()
    depends.setup(app, pool)
    return app


if __name__ == "__main__":
    import uvicorn

    app = init_app()
    uvicorn.run(app, host="0.0.0.0", port=9090)

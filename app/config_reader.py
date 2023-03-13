
from typing import Optional, Any
from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_URL: str = "/api/v1"

    POSTGRES_USER: str = Field(default="admin")
    POSTGRES_PASSWORD: str = Field(default="qwerty123")
    POSTGRES_DB: str = Field(default="auth_service")
    POSTGRES_HOST: str = Field(default="db")
    POSTGRES_PORT: str = Field(default="5432")

    POSTGRES_URL: Optional[PostgresDsn] = None

    TTL_ACCESS_TOKEN: int = Field(default=30)
    TTL_REFRESH_TOKEN: int = Field(default=60)

    TTL_CODE_ACTIVATE: int = Field(default=30)

    @validator("POSTGRES_URL", pre=True)
    def assemble_celery_dburi(cls, v: Optional[str], values: [str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=f"{values.get('POSTGRES_PORT') or ''}",
        )


    class Config:
        env_file = './.env_dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()


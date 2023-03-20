from typing import Optional, Any, Dict
from pydantic import BaseModel, BaseSettings, Field, PostgresDsn, RedisDsn, validator


class Email(BaseModel):
    provider: str
    host: str
    port: int
    login: str
    password: str
    use_tls: bool

    template_path: str


class Settings(BaseSettings):
    email: Email

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
    def assemble_postgres_uri(cls, v: Optional[str], values: [str, Any]) -> Any:
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

    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)

    REDIS_URL: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=str(values.get("REDIS_PORT")),
            path="/0",
        )

    class Config:
        env_file = "./dev.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Settings()

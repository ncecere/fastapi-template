from dotenv import load_dotenv
from functools import cached_property
from typing import Literal

from pydantic import AnyHttpUrl, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")

class Settings(BaseSettings):
    # CORE SETTINGS
    # SECRET_KEY: str
    # ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PRD"] = "DEV"
    # SECURITY_BCRYPT_ROUNDS: int = 12
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    
    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = "App"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI Backend"
    
    # POSTGRESQL DEFAULT DATABASE
    DATABASE_HOSTNAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_DB: str

    @computed_field
    @cached_property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOSTNAME,
                port=self.DATABASE_PORT,
                path=self.DATABASE_DB,
            )
        )

    model_config = SettingsConfigDict(
        env_file=f".env", case_sensitive=True
    )

settings: Settings = Settings()  # type: ignore
from typing import Literal, Optional

from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None

    @model_validator(mode="after")
    def get_database_url(self):
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    TEST_DATABASE_URL: Optional[str] = None

    @model_validator(mode="after")
    def get_test_database_url(self):
        self.TEST_DATABASE_URL = (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:"
            f"{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:"
            f"{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )
        return self

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    LOG_LEVEL: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()

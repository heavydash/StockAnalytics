from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    JWT_SECRET_KEY: str
    JWT_LIFETIME: int   # в минутах
    JWT_ALGORITHM: str

    class Config:
        env_file = "../.env"


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

from functools import lru_cache
from typing import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env')
  PORT: int = 8000
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_HOST: str
  POSTGRES_PORT: str
  POSTGRES_DB: str
  DATABASE_URL: str
  SECRET_KEY: str
  ACCESS_TOKEN_DURATION_MINUTES: int
  REFRESH_TOKEN_DURATION_DAYS: int
  # Más simple que "Sequence[AnyHttpUrl]" y el linter no se queja
  CORS_ORIGINS: Sequence[str]
  SALT_ROUNDS: int
  PRODUCTION: bool


@lru_cache  # Para que no llame cada vez el mismo objeto, lo guarda en cache
def get_settings() -> Settings:
  return Settings()  # type: ignore


settings = get_settings()

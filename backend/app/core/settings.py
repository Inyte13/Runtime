from collections.abc import Sequence
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  PORT: int = 8000
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str
  POSTGRES_DB_TEST: str
  POSTGRES_PORT: str
  POSTGRES_HOST: str
  DATABASE_URL: str
  DATABASE_TEST_URL: str
  DATABASE_ADMIN_URL: str
  SECRET_KEY: str
  ACCESS_TOKEN_DURATION_MINUTES: int
  REFRESH_TOKEN_DURATION_DAYS: int
  # Más simple que "Sequence[AnyHttpUrl]" y el linter no se queja
  CORS_ORIGINS: Sequence[str]
  SALT_ROUNDS: int
  PRODUCTION: bool
  GOOGLE_CLIENT_ID: str
  GOOGLE_CLIENT_SECRET: str
  ADMIN_EMAILS: set[str]

  model_config = SettingsConfigDict(env_file='.env')


@lru_cache  # Para que no llame cada vez el mismo objeto, lo guarda en cache
def get_settings() -> Settings:
  return Settings()  # type: ignore


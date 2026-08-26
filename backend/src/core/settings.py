from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env', extra='ignore')
  docker_port: int
  cors_origins: list[str]


settings = Settings()  # type: ignore

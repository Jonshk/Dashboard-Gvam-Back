# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Para PostgreSQL
    db_host: str
    db_port: int = 5432       # <— valor por defecto si no se lee DB_PORT
    db_user: str
    db_password: str
    db_name: str

    # Para JWT
    jwt_secret: str
    jwt_algorithm: str
    jwt_exp_delta_seconds: int

    model_config = SettingsConfigDict(
      env_file_encoding="utf-8",
    )

settings = Settings()

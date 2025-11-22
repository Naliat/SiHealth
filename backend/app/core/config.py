# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_TITLE: str = "Farmácia API - SiHealth"
    API_V1_STR: str = "/api/v1"
    
    # O Pydantic lerá isso direto do .env
    DATABASE_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignora variáveis extras no .env se houverem
    )

settings = Settings()
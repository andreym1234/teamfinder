# src/core/config.py
import os
from dataclasses import dataclass

@dataclass
class Settings:
    telegram_bot_token: str
    database_url: str

def get_settings() -> Settings:
    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        database_url=os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/teamfinder"),
    )

settings = get_settings()

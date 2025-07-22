from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    FEEDBACK_CHAT_ID: str = Field(..., env="FEEDBACK_CHAT_ID")
    SUPPORT_CHAT_ID: str = Field(..., env="SUPPORT_CHAT_ID")
    ADMIN_IDS: str = Field(..., env="ADMIN_IDS")

    @property
    def admin_ids(self) -> List[int]:
        return [
            int(id_str.strip())
            for id_str in self.ADMIN_IDS.split(",")
            if id_str.strip()
        ]

    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

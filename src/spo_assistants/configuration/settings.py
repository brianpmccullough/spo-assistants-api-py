from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    azure_openai_endpoint: str
    azure_openai_api_key: SecretStr
    azure_openai_deployment: str
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_max_output_tokens: int = 2048
    chat_hmac_secret: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]

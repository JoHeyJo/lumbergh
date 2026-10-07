from pydantic import Field
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    AWS_REGION: str = Field(...)
    # bedrock_model_id: str
    tavily_api_key: str = Field(...)
    data_dir: Path = Path("data")


settings = Settings()

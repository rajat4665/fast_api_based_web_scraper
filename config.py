from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    num_pages: int = 1  # Default value, properly typed
    proxy: Optional[str] = None  # Default is None, properly typed as Optional
    api_token: str  # API token must be provided

    class Config:
        env_file = ".env"  # Specify that Pydantic should read from the .env file
        env_file_encoding = "utf-8"

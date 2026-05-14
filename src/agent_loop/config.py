from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str
    default_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
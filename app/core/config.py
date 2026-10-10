import os
from pydantic_settings import BaseSettings

# Yeh class hamare environment variables ko manage karti hai.
# Isse hume bar bar os.getenv nahi likhna padta.
class Settings(BaseSettings):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    class Config:
        env_file = ".env"

# settings object banate hain jisko baaki files mein use karenge
settings = Settings()

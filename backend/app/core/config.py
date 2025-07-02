import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./storage/app.db"
    
    # Google Gemini
    gemini_api_key: str
    
    # File Upload
    upload_max_size: int = 10485760  # 10MB
    upload_allowed_extensions: List[str] = ["pdf"]
    storage_path: str = "./storage"
    
    # Application
    environment: str = "development"
    debug: bool = True
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AI/ML
    embedding_model: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Ensure storage directories exist
Path(settings.storage_path).mkdir(exist_ok=True)
Path(f"{settings.storage_path}/uploads").mkdir(exist_ok=True)
Path(f"{settings.storage_path}/indexes").mkdir(exist_ok=True)
Path(f"{settings.storage_path}/temp").mkdir(exist_ok=True)
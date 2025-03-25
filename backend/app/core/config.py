import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Environment settings
    ENVIRONMENT: str = Field(default=os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = Field(default=os.getenv("DEBUG", "False") == "True")
    LOG_LEVEL: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))
    
    # API settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8001",   # FastAPI dev server
        "*"  # Allow all origins in development
    ]
    
    # LLM API Keys
    ANTHROPIC_API_KEY: str = Field(default=os.getenv("ANTHROPIC_API_KEY", ""))
    OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    
    # Case study file path
    CASE_STUDY_FILE: str = Field(default=os.getenv("CASE_STUDY_FILE", "data/case-study-inventory.csv"))
    
    # Vector database settings
    VECTOR_DB_PATH: str = "vectordb"
    
    # Model settings
    FAST_MODEL_NAME: str = "claude-3-haiku-20240307"
    DETAILED_MODEL_NAME: str = "claude-3-sonnet-20240229"
    
    # Use a different settings config to allow extra parameters
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Allow extra fields that are not in the model
    )

settings = Settings()
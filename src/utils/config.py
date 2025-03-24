"""Configuration utilities for the GivingTuesday Campaign Advisor."""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class ModelProvider(str, Enum):
    """Supported model providers."""
    
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    LOCAL = "local"
    HUGGINGFACE = "huggingface"


class ModelConfig(BaseModel):
    """Configuration for language models."""
    
    # API keys for different providers
    anthropic_api_key: Optional[str] = Field(default=os.getenv("ANTHROPIC_API_KEY"))
    openai_api_key: Optional[str] = Field(default=os.getenv("OPENAI_API_KEY"))
    
    # Provider selection
    reasoning_provider: ModelProvider = Field(
        default=ModelProvider.ANTHROPIC,
        description="Provider for reasoning model"
    )
    embedding_provider: ModelProvider = Field(
        default=ModelProvider.OPENAI,
        description="Provider for embedding model"
    )
    cost_effective_provider: ModelProvider = Field(
        default=ModelProvider.ANTHROPIC,
        description="Provider for cost-effective processing"
    )
    
    # High-quality reasoning model
    reasoning_model_name: str = Field(
        default="claude-3-7-sonnet-latest",
        description="Model ID for high-quality reasoning"
    )
    reasoning_model_temperature: float = Field(
        default=0.0,
        description="Temperature for reasoning model (0.0-1.0)"
    )
    
    # Cost-effective model
    cost_effective_model_name: str = Field(
        default="claude-3-5-haiku-latest",
        description="Model ID for cost-effective processing"
    )
    cost_effective_model_temperature: float = Field(
        default=0.0,
        description="Temperature for cost-effective model (0.0-1.0)"
    )
    
    # Embedding model
    embedding_model_name: str = Field(
        default="text-embedding-3-small",
        description="Model ID for text embeddings"
    )
    
    # Local model configuration
    local_model_path: Optional[str] = Field(
        default=os.getenv("LOCAL_MODEL_PATH"),
        description="Path to local model for cost-effective processing"
    )


class VectorDBConfig(BaseModel):
    """Configuration for vector database."""
    
    database_path: Path = Field(
        default=Path(os.getenv("VECTORDB_PATH", "./vectordb")),
        description="Path to vector database"
    )
    collection_name: str = Field(
        default="givingtuesday_campaigns",
        description="Collection name for vector database"
    )
    distance_func: str = Field(
        default="cosine",
        description="Distance function for similarity search"
    )


class AppConfig(BaseModel):
    """Application configuration."""
    
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )
    data_dir: Path = Field(
        default=Path("data"),
        description="Directory for data files"
    )
    case_study_file: Path = Field(
        default=Path(os.getenv("CASE_STUDY_FILE", "data/case-study-inventory.csv")),
        description="Path to case study CSV file"
    )
    models: ModelConfig = Field(
        default_factory=ModelConfig,
        description="Model configuration"
    )
    vectordb: VectorDBConfig = Field(
        default_factory=VectorDBConfig,
        description="Vector database configuration"
    )
    

# Create a singleton configuration object
config = AppConfig()
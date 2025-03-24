"""Tests for configuration utilities."""

import os
from pathlib import Path

import pytest

from src.utils.config import AppConfig, ModelConfig, VectorDBConfig


def test_model_config():
    """Test model configuration."""
    # Create a model config
    config = ModelConfig()
    
    # Check default values
    assert config.reasoning_model_name == "gpt-4o-mini"
    assert config.reasoning_model_temperature == 0.0
    assert config.embedding_model_name == "text-embedding-3-small"


def test_vector_db_config():
    """Test vector database configuration."""
    # Create a vector database config
    config = VectorDBConfig()
    
    # Check default values
    assert isinstance(config.database_path, Path)
    assert config.collection_name == "givingtuesday_campaigns"
    assert config.distance_func == "cosine"


def test_app_config():
    """Test application configuration."""
    # Create an application config
    config = AppConfig()
    
    # Check default values
    assert config.log_level == "INFO"
    assert isinstance(config.data_dir, Path)
    assert config.data_dir == Path("data")
    assert config.case_study_file == Path("data/case-study-inventory.csv")
    assert isinstance(config.models, ModelConfig)
    assert isinstance(config.vectordb, VectorDBConfig)

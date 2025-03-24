"""Factory functions for creating language models using LlamaIndex."""

from typing import Any, Dict, Optional, Union

from llama_index.core.base.llms.types import LLM
from llama_index.core.embeddings.base import BaseEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from src.utils.config import ModelProvider, config
from src.utils.logging import logger


def create_reasoning_model() -> LLM:
    """Create a high-quality reasoning model.
    
    Returns:
        Language model for high-quality reasoning.
    """
    provider = config.models.reasoning_provider
    model_name = config.models.reasoning_model_name
    temperature = config.models.reasoning_model_temperature
    
    logger.info(f"Creating reasoning model: {provider} / {model_name}")
    
    if provider == ModelProvider.ANTHROPIC:
        if not config.models.anthropic_api_key:
            raise ValueError("Anthropic API key is required for Anthropic models")
        
        return Anthropic(
            model=model_name,
            temperature=temperature,
            api_key=config.models.anthropic_api_key
        )
        
    elif provider == ModelProvider.OPENAI:
        if not config.models.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI models")
        
        return OpenAI(
            model=model_name,
            temperature=temperature,
            api_key=config.models.openai_api_key
        )
        
    else:
        raise ValueError(f"Unsupported provider for reasoning model: {provider}")


def create_cost_effective_model() -> LLM:
    """Create a cost-effective model for processing.
    
    Returns:
        Language model for cost-effective processing.
    """
    provider = config.models.cost_effective_provider
    model_name = config.models.cost_effective_model_name
    temperature = config.models.cost_effective_model_temperature
    
    logger.info(f"Creating cost-effective model: {provider} / {model_name}")
    
    if provider == ModelProvider.ANTHROPIC:
        if not config.models.anthropic_api_key:
            raise ValueError("Anthropic API key is required for Anthropic models")
        
        return Anthropic(
            model=model_name,
            temperature=temperature,
            api_key=config.models.anthropic_api_key
        )
        
    elif provider == ModelProvider.OPENAI:
        if not config.models.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI models")
        
        return OpenAI(
            model=model_name,
            temperature=temperature,
            api_key=config.models.openai_api_key
        )
        
    else:
        raise ValueError(f"Unsupported provider for cost-effective model: {provider}")


def create_embedding_model() -> BaseEmbedding:
    """Create an embedding model.
    
    Returns:
        Embedding model.
    """
    provider = config.models.embedding_provider
    model_name = config.models.embedding_model_name
    
    logger.info(f"Creating embedding model: {provider} / {model_name}")
    
    if provider == ModelProvider.OPENAI:
        if not config.models.openai_api_key:
            logger.warning("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError(
                "OpenAI API key is required for OpenAI embeddings. "
                "Please set the OPENAI_API_KEY environment variable in your .env file."
            )
        
        return OpenAIEmbedding(
            model_name=model_name,
            api_key=config.models.openai_api_key
        )
    
    else:
        raise ValueError(f"Unsupported provider for embedding model: {provider}")
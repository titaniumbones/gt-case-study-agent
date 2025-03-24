"""Factory functions for creating language models."""

from typing import Callable, Dict, Optional, Union

from langchain.chat_models.base import BaseChatModel
from langchain.embeddings.base import Embeddings
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain_core.language_models import BaseLLM
from langchain_core.language_models.llms import BaseLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.utils.config import ModelProvider, config
from src.utils.logging import logger


def create_reasoning_model() -> BaseChatModel:
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
        
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            anthropic_api_key=config.models.anthropic_api_key
        )
        
    elif provider == ModelProvider.OPENAI:
        if not config.models.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI models")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=config.models.openai_api_key
        )
        
    else:
        raise ValueError(f"Unsupported provider for reasoning model: {provider}")


def create_cost_effective_model() -> BaseChatModel:
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
        
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            anthropic_api_key=config.models.anthropic_api_key
        )
        
    elif provider == ModelProvider.OPENAI:
        if not config.models.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI models")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=config.models.openai_api_key
        )
        
    elif provider == ModelProvider.LOCAL:
        if not config.models.local_model_path:
            raise ValueError("Local model path is required for local models")
        
        return LlamaCpp(
            model_path=config.models.local_model_path,
            temperature=temperature,
            n_ctx=2048,
            verbose=False
        )
        
    else:
        raise ValueError(f"Unsupported provider for cost-effective model: {provider}")


def create_embedding_model() -> Embeddings:
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
        
        return OpenAIEmbeddings(
            model=model_name,
            openai_api_key=config.models.openai_api_key
        )
        
    elif provider == ModelProvider.HUGGINGFACE:
        return HuggingFaceEmbeddings(
            model_name=model_name
        )
        
    else:
        raise ValueError(f"Unsupported provider for embedding model: {provider}")
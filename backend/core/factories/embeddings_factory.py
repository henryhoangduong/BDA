import logging
from functools import lru_cache
from typing import Optional

from langchain.schema.embeddings import Embeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

from core.config import settings

logger = logging.getLogger(__name__)

SUPPORTED_PROVIDERS = {
    "openai": OpenAIEmbeddings,
    "huggingface": HuggingFaceEmbeddings,
    "cohere": CohereEmbeddings,
}


@lru_cache()
def get_embeddings(
    provider: Optional[str] = None, model_name: Optional[str] = None, **kwargs
) -> Embeddings:
    """
    Get an embedding model instance.
    Uses LRU cache to maintain single instance per configuration.

    Args:
        provider: The embedding provider (openai, huggingface, huggingface-bge, cohere)
        model_name: The specific model to use
        **kwargs: Additional configuration parameters

    Returns:
        Embeddings instance

    Examples:
        >>> embeddings = get_embeddings()  # Default OpenAI
        >>> embeddings = get_embeddings("huggingface", "sentence-transformers/all-mpnet-base-v2")
        >>> embeddings = get_embeddings("openai", dimensions=384)
    """

    # TODO: integrate litellm

    # Use settings if not explicitly provided
    provider = provider or settings.embedding.provider
    model_name = model_name or settings.embedding.model_name

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported embedding provider: {provider}. "
            f"Supported providers: {list(SUPPORTED_PROVIDERS.keys())}"
        )

    try:
        if provider == "openai":
            return OpenAIEmbeddings(
                model=model_name, **settings.embedding.additional_params, **kwargs
            )

        elif provider == "huggingface":
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": settings.embedding.device},
                **settings.embedding.additional_params,
                **kwargs,
            )

        elif provider == "ollama":
            return OllamaEmbeddings(
                model_name=model_name or "nomic-embed-text",
                **settings.embedding.additional_params,
                **kwargs,
            )

        elif provider == "cohere":
            return CohereEmbeddings(
                model=model_name or "embed-english-v3.0",
                **settings.embedding.additional_params,
                **kwargs,
            )

    except Exception as e:
        logger.error(f"Error creating embeddings for provider {provider}: {e}")
        raise


def get_embeddings():
    """Get embeddings model based on configuration"""
    if settings.embedding.provider == "huggingface":
        return HuggingFaceEmbeddings(
            model_name=settings.embedding.model_name,
            model_kwargs={"device": settings.embedding.device},
        )
    else:
        raise ValueError(
            f"Unsupported embedding provider: {settings.embedding.provider}"
        )

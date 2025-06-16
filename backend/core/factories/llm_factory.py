from functools import lru_cache
from typing import Optional

from langchain_community.llms import VLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from core.config import LLMConfig, settings


@lru_cache()
def get_llm(LLM: Optional[LLMConfig] = None):
    if settings.llm.provider == "openai":
        try:
            return ChatOpenAI(
                model_name=settings.llm.model_name,
                temperature=settings.llm.temperature,
                api_key=settings.llm.api_key,
                streaming=settings.llm.streaming,
            )
        except Exception as e:
            print(f"Error initializing LLM: {e}, openai is not supported")
            raise e

    elif settings.llm.provider == "ollama":
        print(f"Using Ollama model: {settings.llm.base_url}")
        return ChatOllama(
            model=settings.llm.model_name,
            temperature=settings.llm.temperature,
            base_url=settings.llm.base_url,
            streaming=settings.llm.streaming,
        )

    elif settings.llm.provider == "vllm":
        return VLLM(
            model=settings.llm.model_name,
            trust_remote_code=True,  # mandatory for hf models
            temperature=settings.llm.temperature,
            streaming=settings.llm.streaming,
        )
    elif settings.llm.provider == "google":
        return ChatGoogleGenerativeAI(
            model=settings.llm.model_name,
            temperature=settings.llm.temperature,
            model_kwargs={
                "streaming": settings.llm.streaming,
            }
        )
    elif settings.llm.provider == "anthropic":
        return """ChatAnthropic(
            model=settings.llm.model_name,
            temperature=settings.llm.temperature,
            api_key=settings.llm.api_key,
            streaming=settings.llm.streaming
        )"""

    raise ValueError(f"Unsupported LLM provider: {settings.LLM.provider}")

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from core.factories.vector_store_factory import VectorStoreFactory
from services.retrieval.factory import RetrieverFactory, RetrievalMethod
from services.auth.supabase_client import get_supabase_client
import logging
from typing import Dict, Union
logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, config: Dict[str, any] = None):
        self.store = VectorStoreFactory.get_vector_store()
        self.factory = RetrieverFactory
        self.default_retriever = self.factory.from_config(config)
        logger.info(
            f"Initialized retriever with default strategy: {type(self.default_retriever).__name__}"
        )

    def as_retriever(self, method: Union[str, RetrievalMethod] = None, **kwargs):
        if method:
            retriever = self.factory.get_retriever(
                method, vector_store=self.store)
            logger.debug(
                f"Creating LangChain retriever with strategy: {method}")
        else:
            # Use the default retriever
            retriever = self.default_retriever
            logger.debug(
                f"Creating LangChain retriever with default strategy: {type(retriever).__name__}"
            )

        # Return as a LangChain retriever
        return retriever.as_retriever(**kwargs)

    def as_ensemble_retriever(self):
        pass

    def retrieve(self, query: str, method: Union[str, RetrievalMethod] = None, **kwargs):
        supabase = get_supabase_client()
        user = supabase.auth.get_user()
        user_id = user.user.id
        if method:
            retriever = self.factory.get_retriever(
                method, vector_store=self.store)
            logger.debug(
                f"Using retrieval strategy '{method}' for query: {query[:50]}...")
        else:
            # Use the default retriever
            retriever = self.default_retriever
            logger.debug(
                f"Using default retrieval strategy for query: {query[:50]}...")
        if user_id is None:
            logger.warning(
                "retrieve() called without user_id - this is not secure for multi-tenant systems")
        if user_id:
            kwargs["user_id"] = user_id
        docs = retriever.retrieve(query, **kwargs)
        logger.debug(
            f"Retrieved {len(docs)} documents using {type(retriever).__name__}")
        return docs

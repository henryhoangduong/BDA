from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from langchain.schema import Document

from core.factories.vector_store_factory import VectorStoreFactory
from services.vector_store import VectorStoreService


class RetrievalMethod(str, Enum):

    DEFAULT = "default"
    ENSEMBLE = "ensemble"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    KEYWORD = "keyword"
    RERANKED = "reranked"


class BaseRetriever(ABC):
    def __init__(self, vector_store: Optional[VectorStoreService] = None):
        self.store = vector_store or VectorStoreFactory.get_vector_store()

    @abstractmethod
    def retrieve(self, query: str, user_id: str = None, **kwargs) -> List[Document]:
        pass

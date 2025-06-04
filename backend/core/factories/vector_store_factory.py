from core.config import settings
from core.factories.embeddings_factory import get_embeddings
from services.vector_store import PGVectorStore, VectorStoreService
from services.vector_store.vector_store_service import VectorStoreService


class VectorStoreFactory:
    _instance = None
    _initialized = None
    _vector_store = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialize_store()
            self._initialized = True

    def _initialize_store(self):
        embeddings = get_embeddings()
        if settings.vector_store.provider == "faiss":
            self._vector_store = self._initialize_faiss(embeddings)
        elif settings.vector_store.provider == "pgvector":
            self._vector_store = self._initialize_pgvector(embeddings)
        else:
            raise ValueError(
                f"Unsupported vector store provider: {settings.vector_store.provider}"
            )

    def _initialize_pgvector(self, embeddings):
        return PGVectorStore()

    @classmethod
    def get_vector_store(cls) -> VectorStoreService:
        return cls()._vector_store

    @classmethod
    def reset(cls):
        cls._initialized = None
        cls._instance = None

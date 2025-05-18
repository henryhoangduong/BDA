from services.vector_store_service import VectorStoreService


class VectorStoreFactory:
    _instance = None
    _initialized = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._vector_store = VectorStoreService()
            self._initialized = True

    @classmethod
    def get_vector_store(cls) -> VectorStoreService:
        return cls()._vector_store

    @classmethod
    def reset(cls):
        cls._initialized = None
        cls._instance = None

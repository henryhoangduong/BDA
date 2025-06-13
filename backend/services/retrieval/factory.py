import logging
from typing import Any, Dict, Union

from services.retrieval.base import BaseRetriever, RetrievalMethod
from services.vector_store.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)


class RetrieverFactory:
    @staticmethod
    def get_retriever(
        method: Union[str, RetrievalMethod], vector_store=None, **kwargs
    ) -> BaseRetriever:
        from services.retrieval.default import DefaultRetriever
        if isinstance(method, str):
            try:
                method = RetrievalMethod(method)
                logger.debug(
                    f"Converted string '{method}' to retrieval method enum")

            except ValueError:
                logger.warning(
                    f"Invalid retrieval method: '{method}', falling back to DEFAULT")
                method = RetrievalMethod.DEFAULT
        filtered_kwargs = {
            "vector_store": vector_store} if vector_store else {}

        logger.warning(
            "RerankedRetriever not implemented, falling back to DefaultRetriever")
        return DefaultRetriever(**filtered_kwargs)

    @staticmethod
    def from_config(config: Dict[str, Any] = None) -> BaseRetriever:
        if not config:
            from core.config import settings
            if hasattr(settings, "retrieval") and hasattr(settings.retrieval, "method"):
                method = settings.retrieval.method
                logger.info(
                    f"Creating retriever from config with method: {method}")
                params = {}
                if hasattr(settings.retrieval, "k"):
                    params["k"] = settings.retrieval.k
                if hasattr(settings.retrieval, "params"):
                    method_params = settings.retrieval.params
                    for key, value in method_params.items():
                        params[key] = value
                return RetrieverFactory.get_retriever(method, **params)
            logger.info("No retrieval config found, using default retriever")
            return RetrieverFactory.get_retriever(RetrievalMethod.DEFAULT)
        method = (
            config.pop("method", RetrievalMethod.DEFAULT)
            if isinstance(config, dict)
            else RetrievalMethod.DEFAULT
        )
        logger.info(f"Creating retriever with method: {method}")
        if isinstance(config, dict):
            return RetrieverFactory.get_retriever(method, **config)
        else:
            return RetrieverFactory.get_retriever(method)

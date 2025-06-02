from typing import List, cast

from fastapi import APIRouter, HTTPException

from core.factories.database_factory import get_database
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import SimbaDoc
from services.embeddings.embedding_service import EmbeddingService

embedding_route = APIRouter()

db = get_database()
store = VectorStoreFactory.get_vector_store()
embedding_service = EmbeddingService()


@embedding_route.post("/embed/documents")
async def embed_documents():
    """Embed all documents in the database into the vector store."""
    try:
        langchain_documents = embedding_service.embed_all_documents()
        return langchain_documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@embedding_route.post("/embed/document/{doc_id}")
async def embed_document(doc_id: str):
    """Embed a specific document into the vector store."""
    try:
        langchain_documents = embedding_service.embed_document(doc_id)
        return langchain_documents
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

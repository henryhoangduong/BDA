from typing import List, cast

from fastapi import APIRouter, HTTPException

from core.factories.database_factory import get_database
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import SimbaDoc

embedding_route = APIRouter()

db = get_database()
store = VectorStoreFactory.get_vector_store()


@embedding_route.post("/embed/document")
async def embed_document(doc_id: str):
    try:
        simbadoc: SimbaDoc = db.get_document(doc_id)
        langchain_documents = simbadoc.documents

        try:
            store.add_documents(langchain_documents)
            simbadoc.metadata.enabled = True
            db.update_document(doc_id, simbadoc)
            # kms.sync_with_store()

        except ValueError as ve:
            # If the error is about existing IDs, consider it a success
            if "Tried to add ids that already exist" in str(ve):
                return langchain_documents  # Return success response
            raise ve  # Re-raise if it's a different ValueError

        return langchain_documents

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import List, cast

from fastapi import APIRouter, HTTPException

from core.factories.database_factory import get_database
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import SimbaDoc
from services.dataset.dataset_service import generate_qa_from_chunks
dataset_route = APIRouter()

db = get_database()


@dataset_route.post("/dataset/create/doc/{doc_id}")
async def create_dataset(doc_id: str):
    try:
        document = db.get_document(doc_id)
        result = await generate_qa_from_chunks(document.documents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import asyncio
import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from core.config import settings
from core.factories.database_factory import get_database
from core.factories.storage_factory import StorageFactory
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import SimbaDoc
from services.ingestion.document_ingestion import DocumentIngestionService
from services.ingestion.file_handling import save_file_locally
from services.ingestion.loader import Loader

ingestion_service = DocumentIngestionService()
store = VectorStoreFactory.get_vector_store()
logger = logging.getLogger(__name__)
loader = Loader()
storage = StorageFactory.get_storage_provider()
ingestion = APIRouter()
db = get_database()


@ingestion.post("/ingestion")
async def ingest_document(
    files: List[UploadFile] = File(...),
    folder_path: str = Query(
        default="/", description="Folder path to store the document"
    ),
):
    """Ingest a document into the vector store"""
    try:
        # Process files concurrently using asyncio.gather
        async def process_file(file):
            simba_doc = await ingestion_service.ingest_document(file, folder_path)
            return simba_doc

        # Process all files concurrently
        response = await asyncio.gather(*[process_file(file) for file in files])
        db.insert_documents(response, user_id="1")

        return response

    except Exception as e:
        logger.error(f"Error in ingest_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@ingestion.get("/ingestion")
async def get_ingestion_documents():
    documents = db.get_all_documents(user_id="1")
    return documents


@ingestion.get("/ingestion/{uid}")
async def get_document(uid):
    document = db.get_document(uid)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {uid} not found")
    return document


@ingestion.put("/ingestion/update_document")
async def update_document(doc_id: str, simba_doc: SimbaDoc):
    try:
        success = db.update_document(doc_id, simba_doc)

        if not success:
            raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    except Exception as e:
        logger.error(f"Error in update_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@ingestion.delete("/ingestion")
async def delete(uids: List[str]):
    try:
        # Delete documents from vector store
        for uid in uids:
            simbadoc = db.get_document(uid)
            res = await storage.delete_file(f"{simbadoc.metadata.filename}")
            if simbadoc.metadata.enabled:
                for doc in simbadoc.documents:
                    try:
                        store.delete_documents([doc.id])
                    except Exception as e:
                        logger.error(
                            f"Error deleting document with id {doc.id} in vector store"
                        )
        # Delete documents from database
        db.delete_documents(uids)

        # kms.sync_with_store()
        return {"message": f"Documents {uids} deleted successfully"}
    except Exception as e:
        logger.error(f"Error in delete_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@ingestion.get("/loaders")
async def get_loaders():
    """Get supported document loaders"""
    return {
        "loaders": [
            loader_name.__name__ for loader_name in loader.SUPPORTED_EXTENSIONS.values()
        ]
    }


@ingestion.get("/upload-directory")
async def get_upload_directory():
    """Get upload directory path"""
    return {"path": str(settings.paths.upload_dir)}

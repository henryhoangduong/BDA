import asyncio
import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from core.config import settings
from core.factories.database_factory import get_database
from services.ingestion_service.document_ingestion_service import \
    DocumentIngestionService
from services.ingestion_service.file_handling import save_file_locally

ingestion_service = DocumentIngestionService()

logger = logging.getLogger(__name__)

ingestion=APIRouter()
db= get_database()

@ingestion.post("/ingestion")
async def ingest_document(
    files: List[UploadFile] = File(...),
    folder_path: str = Query(default="/",description="Folder path to store the document")
):
    try:
        store_path = Path(settings.paths.upload_dir)
        if folder_path != "/":
            store_path = store_path / folder_path.strip("/")
        async def process_file(file):
            await file.seek(0)
            await save_file_locally(file, store_path)
            await file.seek(0)
            simba_doc = await ingestion_service.ingest_document(file)
            return simba_doc
       # Process all files concurrently
        response = await asyncio.gather(*[process_file(file) for file in files])
        # # Insert into database
        db.insert_documents(response)
        return response

    except Exception as e:
        logger.error(f"Error in ingest_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@ingestion.get("/ingestion")
async def get_ingestion_documents():
    documents = db.get_all_documents()
    return documents


@ingestion.get("/ingestion/{uid}")
async def get_document(uid):
    document = db.get_document(id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {uid} not found")
    return document


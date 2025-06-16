import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import UploadFile
from langchain.schema import Document

from core.config import settings
from core.factories.database_factory import get_database
from core.factories.storage_factory import StorageFactory
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import MetadataType, SimbaDoc
from services.ingestion.loader import Loader
from services.splitting.splitter import Splitter
from services.storage.base import StorageProvider
from services.auth.supabase_client import get_supabase_client

from services.ingestion.file_handling import delete_file_locally
logger = logging.getLogger(__name__)
supabase = get_supabase_client()


class DocumentIngestionService:
    def __init__(self):
        self.vector_store = VectorStoreFactory.get_vector_store()
        self.database = get_database()
        self.loader = Loader()
        self.splitter = Splitter()
        self.storage: StorageProvider = StorageFactory.get_storage_provider()

    async def ingest_document(
        self, file: UploadFile, folder_path: str = "/"
    ) -> Document:
        try:
            from tasks.generate_summary import generate_summary_task

            file_path = Path(folder_path.strip("/")) / file.filename
            print("file_path: ", file_path)
            file_extension = f".{file.filename.split('.')[-1].lower()}"
            saved_local_path = await self.storage.save_file(file_path, file)
            saved_remote_path = await self.storage.get_public_url(file_path)
            file_size = saved_local_path.stat().st_size
            if file_size == 0:
                raise ValueError(f"File {saved_local_path} is empty")
            document = await self.loader.aload(file_path=str(saved_local_path))
            document = await asyncio.to_thread(self.splitter.split_document, document)
            for doc in document:
                doc.id = str(uuid.uuid4())
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
            metadata = MetadataType(
                filename=file.filename,
                type=file_extension,
                page_number=len(document),
                chunk_number=0,
                enabled=False,
                parsing_status="Unparsed",
                size=size_str,
                loader=self.loader.__name__,
                uploadedAt=datetime.now().isoformat(),
                file_path=saved_remote_path,
                parser=None,
            )

            simbadoc = SimbaDoc.from_documents(
                id=str(uuid.uuid4()), documents=document, metadata=metadata
            )
            generate_summary_task.delay(simbadoc.model_dump())
            return simbadoc
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            raise e

    async def delete_ingested_document(self, uid: str, delete_locally: bool = False) -> int:
        try:

            if delete_locally:
                doc = self.vector_store.get_document(uid)
                delete_file_locally(Path(doc.metadata.get("file_path")))

            self.vector_store.delete_documents([uid])

            return {"message": f"Document {uid} deleted successfully"}

        except Exception as e:
            logger.error(f"Error deleting document {uid}: {e}")
            raise e

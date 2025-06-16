from fastapi import APIRouter
from fastapi import Depends
from typing import Dict, Any
from api.middleware.auth import get_current_user
from services.auth.supabase_client import get_supabase_client
from core.factories.storage_factory import StorageFactory
from core.factories.vector_store_factory import VectorStoreFactory
from services.embeddings.embedding_service import EmbeddingService
from services.ingestion.document_ingestion import DocumentIngestionService
from core.factories.database_factory import get_database
import logging
logger = logging.getLogger(__name__)
document_route = APIRouter()

storage = StorageFactory.get_storage_provider()
db = get_database()
embedding_service = EmbeddingService()
store = VectorStoreFactory.get_vector_store()
kms = DocumentIngestionService()


@document_route.delete("/document/{uid}")
async def delete_file(uid: str, current_user: Dict[str, any] = Depends(get_current_user)):
    try:
        simbadoc = db.get_document(uid, user_id=current_user["id"])
        result = await embedding_service.delete_document(uid)

        if simbadoc and simbadoc.metadata.enabled:
            try:
                store.delete_documents(
                    [doc.id for doc in simbadoc.documents])
            except Exception as e:
                # Log the error but continue with deletion
                logger.warning(
                    f"Error deleting document {uid} from vector store: {str(e)}. Continuing with database deletion."
                )
        await storage.delete_file(simbadoc.metadata.filename)
        await db.delete_document(uid, current_user.get("id", None))
        return True
    except Exception as e:
        logger.error(f"Error deleting documet: {str(e)}")
        return False

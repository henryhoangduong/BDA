import logging
import os

import torch

from core.celery_config import \
    celery_app as celery  # Rename for backward compatibility
from core.factories.database_factory import get_database
from core.factories.vector_store_factory import VectorStoreFactory
from services.parser_service import ParserService

logger = logging.getLogger(__name__)

# Force CPU usage through environment variables
os.environ["PYTORCH_DEVICE"] = "cpu"
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Disable CUDA
os.environ["TORCH_DEVICE"] = "cpu"  # Force PyTorch to use CPU

# Ensure PyTorch is using CPU
if torch.cuda.is_available():
    torch.cuda.empty_cache()
torch.set_num_threads(1)  # Limit to single thread to avoid conflicts

parser_service = ParserService(device="cpu", force_cpu=True)
vector_store = VectorStoreFactory.get_vector_store()


@celery.task(name="parse_markitdown", bind=True)
def parse_markitdown_task(self, document_id: str):
    db = None
    try:
        # Get fresh database connection
        db = get_database()
        logger.info(
            f"[Task {self.request.id}] Fetching document with ID: {document_id}"
        )

        doc = db.get_document(document_id)
        if not doc:
            logger.error(f"[Task {self.request.id}] Document {document_id} not found")
            return {"status": "error", "error": "Document not found"}

        # Get parsed document from service
        parsed_doc = parser_service._parse_markitdown(doc)
        # Update with SimbaDoc instance
        db.update_document(document_id, parsed_doc)
        logger.info(
            f"[Task {self.request.id}] Successfully updated document {document_id}"
        )
        return {"status": "success", "document_id": document_id}

    except Exception as e:
        logger.error(f"[Task {self.request.id}] Parse failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}
    finally:
        if hasattr(db, "close"):
            db.close()


@celery.task(name="parse_docling")
def parse_docling_task(document_id: str):
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        db = get_database()
        original_doc = db.get_document(document_id)
        with torch.no_grad():  # Disable gradient computation
            parsed_simba_doc = parser_service.parse_document(original_doc, "docling")

        db.update_document(document_id, parsed_simba_doc)
        vector_store.add_documents(parsed_simba_doc.documents)
        print("---")
        print("adding documents to store : ", parsed_simba_doc.documents)
        print("---")

    except Exception as e:
        logger.error(f"Parse failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}
    finally:
        if hasattr(db, "close"):
            db.close()
        # Clean up any remaining GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

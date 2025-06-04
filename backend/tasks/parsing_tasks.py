import logging

import torch

from core.celery_config import celery_app as celery
from core.factories.database_factory import get_database
from services.parsing.docling_parser import DoclingParser
from services.embeddings.embedding_service import EmbeddingService
logger = logging.getLogger(__name__)


@celery.task(name="parse_docling")
def parse_docling_task(document_id: str):
    logger.info(f"Starting Docling parsing for document ID: {document_id}")
    try:
        parser = DoclingParser()
        db = get_database()
        embedding_service = EmbeddingService()

        original_doc = db.get_document(document_id)

        parsed_simba_doc = parser.parse(original_doc)

        embedding_service.embed_document(document_id)

        db.update_document(document_id, parsed_simba_doc)

        return {"status": "success", "document_id": parsed_simba_doc.id}
    except Exception as e:
        logger.error(f"Parse failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}
    finally:
        if hasattr(db, "close"):
            db.close()
        # Clean up any remaining GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

import logging

from core.celery_config import celery_app as celery
from core.factories.database_factory import get_database
from models.simbadoc import SimbaDoc
from services.ingestion.summary import summarize_document

logger = logging.getLogger(__name__)


@celery.task(name="generate_summary_task")
def generate_summary_task(simbadoc_dict: dict):

    try:
        simbadoc = SimbaDoc.model_validate(simbadoc_dict)
        logger.info(
            f"[SUMMARY] Processing document: id={simbadoc.id}, filename={getattr(simbadoc.metadata, 'filename', None)}, metadata={simbadoc.metadata}"
        )
        # Generate summary
        summary = summarize_document(simbadoc)
        logger.info(
            f"[SUMMARY] Generated summary for document {simbadoc.id}: {summary}"
        )

        # Attach summary to metadata (as attribute and dict for compatibility)
        setattr(simbadoc.metadata, "summary", summary)
        if hasattr(simbadoc.metadata, "__dict__"):
            simbadoc.metadata.__dict__["summary"] = summary

        # Update in database - only get db connection when needed
        db = get_database()
        db.update_document(simbadoc.id, simbadoc)
        logger.info(f"[SUMMARY] Summary saved for document {simbadoc.id}.")

        return {"status": "success", "document_id": simbadoc.id}
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}

import logging
import os

from celery.app.control import Inspect
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from core.config import settings
from core.factories.database_factory import get_database
from models.simbadoc import SimbaDoc
from services.parser_service import ParserService
from tasks.parsing_tasks import celery, parse_docling_task

logger = logging.getLogger(__name__)
parsing = APIRouter()

parser_service = ParserService()
db = get_database()


class ParseDocumentRequest(BaseModel):
    document_id: str
    parser: str


@parsing.get("/parsers")
async def get_parsers():
    """Get the list of parsers supported by the document ingestion service"""
    parsers = parser_service.get_parsers()
    return {"parsers": parsers}


@parsing.post("/parses")
async def parse_document(request: ParseDocumentRequest):
    try:
        logger.info(f"Received parse request: {request}")

        # Verify document exists first
        simbadoc: SimbaDoc = db.get_document(request.document_id)
        if not simbadoc:
            raise HTTPException(status_code=404, detail="Document not found")

        if request.parser == "docling":
            task = parse_docling_task.delay(request.document_id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported parser")

        return {"task_id": task.id, "status_url": f"parsing/tasks/{task.id}"}

    except Exception as e:
        logger.error(f"Error queuing parsing task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@parsing.get("/parsing/tasks")
async def get_all_tasks():
    """Get all Celery tasks (active, reserved, scheduled)"""
    try:
        i = Inspect(app=celery)
        tasks = {
            "active": i.active(),  # Currently executing tasks
            "reserved": i.reserved(),  # Tasks that have been claimed by workers
            "scheduled": i.scheduled(),  # Tasks scheduled for later execution
            "registered": i.registered(),  # All tasks registered in the worker
        }

        # Add task queue length if available
        try:
            stats = celery.control.inspect().stats()
            if stats:
                tasks["stats"] = stats
        except:
            pass

        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@parsing.get("/parsing/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Check status of a parsing task"""
    result = celery.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }

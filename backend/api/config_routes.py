import logging
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from api.middleware.auth import get_current_user
from core.config import Settings
from models.user import UserResponse

logger = logging.getLogger(__name__)

# Create router
config_router = APIRouter(
    prefix="/config",
    tags=["configuration"]
)

# Global settings instance
settings = Settings.load_from_yaml()


@config_router.get(
    "",
    response_model=Dict[str, Any],
    summary="Get current configuration",
    description="Retrieve the complete application configuration"
)
async def get_config(current_user: UserResponse = Depends(get_current_user)):
    try:
        return {
            "llm": settings.llm.model_dump(),
            "embedding": settings.embedding.model_dump(),
            "vector_store": settings.vector_store.model_dump(),
            "retrieval": settings.retrieval.model_dump(),
            "project": settings.project.model_dump(),
            "database": settings.database.model_dump(),
            "storage": settings.storage.model_dump(),
            "celery": settings.celery.model_dump()
        }
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve configuration"
        )

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from simba.api.middleware.auth import (get_current_user, require_role,
                                       require_tenant_access)

from models.api_key import APIKeyCreate, APIKeyInfo, APIKeyResponse
from services.auth.api_key_service import APIKeyService

logger = logging.getLogger(__name__)

api_key_router = APIRouter(
    prefix="/api/api-keys",
    tags=["api-keys"],
)

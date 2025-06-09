import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from models.api_key import APIKeyCreate, APIKeyResponse, APIKeyInfo
from services.auth.api_key_service import APIKeyService
from simba.api.middleware.auth import get_current_user, require_role, require_tenant_access

logger = logging.getLogger(__name__)

api_key_router = APIRouter(
    prefix="/api/api-keys",
    tags=["api-keys"],
)

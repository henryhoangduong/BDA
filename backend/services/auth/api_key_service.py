import hashlib
import json
import logging
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status

from database.postgres import PostgresDB
from services.auth.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


class APIKeyService:
    @staticmethod
    def _generate_key() -> str:
        pass

    @staticmethod
    def _hash_key(key: str) -> str:
        pass

    @classmethod
    def create_key(cls, user_id: UUID, key_data: APIKeyCreate) -> APIKeyResponse:
        pass

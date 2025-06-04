import logging
from typing import Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (APIKeyHeader, HTTPAuthorizationCredentials,
                              HTTPBearer)

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
tenant_id_header = APIKeyHeader(name="X-Tenant-Id", auto_error=False)


async def get_current_user(
    request: Request,
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        http_bearer),
    api_key: Optional[str] = Depends(api_key_header),
    tenant_id: Optional[str] = Depends(tenant_id_header),
):
    tenant_uuid = None
    try:
        tenant_uuid = UUID(tenant_id)
    except:
        logger.warning(f"Invalid tenant ID format: {tenant_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tenant ID format",
        )
    if api_key:
        try:
        except Exception as e:
            
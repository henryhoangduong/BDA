import logging
from typing import Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (APIKeyHeader, HTTPAuthorizationCredentials,
                              HTTPBearer)

from services.auth.role_service import RoleService
from services.auth.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
tenant_id_header = APIKeyHeader(name="X-Tenant-Id", auto_error=False)

logger = logging.getLogger(__name__)


async def get_current_user(
    request: Request,
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        http_bearer),
    api_key: Optional[str] = Depends(api_key_header),
    tenant_id: Optional[str] = Depends(tenant_id_header),
):

    if bearer_credentials:
        try:
            supabase = get_supabase_client()
            token = bearer_credentials.credentials

            user_response = supabase.auth.get_user(token)
            if not user_response:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user_data = {
                "id": user_response.user.id,
                "email": user_response.user.email,
                "auth_type": "jwt",
                "metadata": user_response.user.user_metadata or {},
            }
            logger.debug("User authenticated with bearer token")
            return user_data
        except Exception as e:
            logger.error(f"Bearer token authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    logger.warning("No authentication credentials provided")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer, APIKey"},
    )


def require_role(role: str):
    async def dependency(current_user: dict = Depends(get_current_user)):
        user_id = current_user.id
        try:
            # Check if user has the required role
            has_role = RoleService.has_role(user_id, role)

            if not has_role:
                logger.warning(
                    f"Access denied: User {user_id} does not have role {role}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: Role '{role}' required",
                )

            return current_user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Role check error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify role",
            )
    return dependency


def require_permission(permission: str):
    """Dependency for permission-based access control.

    Args:
        permission: Required permission

    Returns:
        callable: Dependency function
    """
    async def dependency(current_user: dict = Depends(get_current_user)):
        user_id = current_user.get("id")

        # For API keys with fixed permissions, we currently only support role-based checks
        # You might want to extend this to map roles to permissions for API keys
        if current_user.get("auth_type") == "api_key":
            logger.warning(
                f"Permission check for API key not supported, use role-based checks instead")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API keys currently only support role-based authorization",
            )

        try:
            # Check if user has the required permission
            has_permission = RoleService.has_permission(user_id, permission)

            if not has_permission:
                logger.warning(
                    f"Access denied: User {user_id} does not have permission {permission}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: Permission '{permission}' required",
                )

            return current_user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Permission check error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify permission",
            )

    return dependency

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
from models.api_key import APIKeyCreate, APIKeyResponse, APIKeyInfo
from services.roles.role_services import RoleService
from services.auth.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

supabase = get_supabase_client()


class APIKeyService:
    @staticmethod
    def _generate_key() -> str:
        raw_key = secrets.token_hex(APIKeyService.KEY_LENGTH)

        return raw_key

    @staticmethod
    def _hash_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    @classmethod
    def create_key(cls, user_id: UUID, key_data: APIKeyCreate) -> APIKeyResponse:
        try:
            logger.info(f"Creating API key for user: {user_id}")
            logger.info(f"Key data: {key_data.model_dump_json()}")
            raw_key = cls._generate_key()
            key_hash = cls._hash_key(raw_key)
            key_prefix = raw_key[:cls.PREFIX_LENGTH]
            role_service = RoleService()
            for role_name in key_data.roles:
                role = role_service.get_role_by_name(role_name)
                if not role:
                    logger.error(f"Role '{role_name}' does not exist")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Role '{role_name}' does not exist"
                    )
            insert_data = {
                "key": key_hash,
                "key_prefix": key_prefix,
                # Convert UUID to string to match auth.uid() format
                "user_id": str(user_id),
                "tenant_id": str(key_data.tenant_id) if key_data.tenant_id else None,
                "name": key_data.name,
                "roles": key_data.roles,
                "expires_at": key_data.expires_at.isoformat() if key_data.expires_at else None
            }
            try:
                result = supabase.table('api_keys').insert(
                    insert_data).execute()

                if not result.data:
                    logger.error("Failed to create API key through Supabase")
                    raise Exception("Failed to create API key")
                row = result.data[0]
                response = APIKeyResponse(
                    id=row['id'],
                    key=raw_key,
                    key_prefix=row['key_prefix'],
                    tenant_id=row['tenant_id'],
                    name=row['name'],
                    roles=row['roles'],
                    created_at=row['created_at'],
                    expires_at=row['expires_at']
                )
                logger.info(
                    f"API key created successfully with ID: {response.id}")
                return response
            except Exception as db_error:
                logger.error(
                    f"Database error during API key creation: {str(db_error)}")
                raise
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to create API key: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create API key: {str(e)}"
            )

    @staticmethod
    def get_keys(user_id: UUID, tenant_id: Optional[UUID] = None) -> List[APIKeyInfo]:
        try:
            logger.info(
                f"Getting API keys for user: {user_id}, tenant: {tenant_id}")
            query = supabase.table('api_keys').select(
                '*').eq('user_id', str(user_id))
            if tenant_id:
                query = query.eq('tenant_id', str(tenant_id))
            result = query.execute()
            if not result.data:
                logger.info(f"No API keys found for user {user_id}")
                return []
            api_keys = []
            for row in result.data:
                logger.info(
                    f"Processing API key: {row.get('id')} with prefix: {row.get('key_prefix')}")

                api_keys.append(APIKeyInfo(
                    id=row['id'],
                    key_prefix=row['key_prefix'],
                    tenant_id=row['tenant_id'],
                    name=row['name'],
                    roles=row['roles'],
                    created_at=row['created_at'],
                    last_used=row['last_used'],
                    is_active=row['is_active'],
                    expires_at=row['expires_at']
                ))

            logger.info(f"Returning {len(api_keys)} API keys")
            return api_keys
        except Exception as e:
            logger.error(f"Failed to get API keys: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch API keys: {str(e)}"
            )

    @staticmethod
    def get_tenant_keys(tenant_id: UUID) -> List[APIKeyInfo]:
        try:
            rows = PostgresDB.fetch_all("""
                SELECT id, key_prefix, tenant_id, name, roles, created_at, last_used, is_active, expires_at
                FROM api_keys
                WHERE tenant_id = %s
                ORDER BY created_at DESC
            """, (str(tenant_id),))
            api_keys = []
            for row in rows:
                # Parse the roles JSON if it's a string
                roles = row['roles']
                if isinstance(roles, str):
                    try:
                        roles = json.loads(roles)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse roles JSON: {roles}")
                        roles = []

                api_keys.append(APIKeyInfo(
                    id=row['id'],
                    key_prefix=row['key_prefix'],
                    tenant_id=row['tenant_id'],
                    name=row['name'],
                    roles=roles,
                    created_at=row['created_at'],
                    last_used=row['last_used'],
                    is_active=row['is_active'],
                    expires_at=row['expires_at']
                ))

            return api_keys
        except Exception as e:
            logger.error(f"Failed to get tenant API keys: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch tenant API keys"
            )

    @staticmethod
    def delete_key(user_id: UUID, key_id: UUID, tenant_id: Optional[UUID] = None) -> bool:
        try:
            query = """
                DELETE FROM api_keys
                WHERE id = %s AND user_id = %s
            """
            params = [str(key_id), str(user_id)]
            if tenant_id:
                query += " AND tenant_id = %s"
                params.append(str(tenant_id))
            result = PostgresDB.execute_query(query, tuple(params))

            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete API key: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete API key"
            )

    @staticmethod
    def delete_tenant_key(tenant_id: UUID, key_id: UUID) -> bool:
        try:
            result = PostgresDB.execute_query("""
                DELETE FROM api_keys
                WHERE id = %s AND tenant_id = %s
            """, (str(key_id), str(tenant_id)))

            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete tenant API key: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete tenant API key"
            )

    @staticmethod
    def deactivate_key(user_id: UUID, key_id: UUID, tenant_id: Optional[UUID] = None) -> bool:
        try:
            query = """
                UPDATE api_keys
                SET is_active = FALSE
                WHERE id = %s AND user_id = %s
            """
            params = [str(key_id), str(user_id)]

            if tenant_id:
                query += " AND tenant_id = %s"
                params.append(str(tenant_id))

            result = PostgresDB.execute_query(query, tuple(params))

            return result > 0
        except Exception as e:
            logger.error(f"Failed to deactivate API key: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to deactivate API key"
            )

    @staticmethod
    def validate_key(api_key: str, tenant_id: Optional[UUID] = None) -> Optional[Dict[str, Any]]:
        try:
            key_hash = APIKeyService._hash_key(api_key)
            query = """
                SELECT id, user_id, tenant_id, roles, is_active, expires_at
                FROM api_keys
                WHERE key = %s
            """
            params = [key_hash]
            if tenant_id:
                query += " AND tenant_id = %s"
                params.append(str(tenant_id))
            row = PostgresDB.fetch_one(query, tuple(params))
            if not row:
                logger.warning("API key not found")
                return None
            if not row['is_active']:
                logger.warning("API key is inactive")
                return None
            if row['expires_at'] and row['expires_at'] < datetime.now():
                logger.warning("API key is expired")
                return None
            PostgresDB.execute_query("""
                UPDATE api_keys
                SET last_used = NOW()
                WHERE id = %s
            """, (row['id'],))
            roles = row['roles']
            if isinstance(roles, str):
                try:
                    roles = json.loads(roles)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse roles JSON: {roles}")
                    roles = []
            return {
                "id": row['user_id'],
                "tenant_id": row['tenant_id'],
                "roles": roles,
                "metadata": {
                    "is_api_key": True,
                    "api_key_id": row['id']
                }
            }
        except Exception as e:
            logger.error(f"Failed to validate API key: {str(e)}")
            return None

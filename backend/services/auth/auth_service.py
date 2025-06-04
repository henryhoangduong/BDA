import logging
from typing import Any, Dict, Optional

from pydantic import EmailStr

from services.auth.role_service import RoleService
from services.auth.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def sign_up(
        email: str, password: str, user_metadat: Optional[Dict[str, Any]] = None
    ):
        user_metadata = user_metadata or {}
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": user_metadata},
                }
            )
            if hasattr(response, "error") and response.error:
                raise ValueError(f"Failed to sign up: {response.error.message}")
            logger.info(f"User signed up successfully: {email}")
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": response.user.created_at,
                "metadata": response.user.user_metadata,
            }
            try:
                role_service = RoleService()
                role = role_service.get_role_by_name("admin")
                if role:
                    role_service.assign_role_to_user(
                        user_id=user_data["id"], role_id=role.id
                    )
                    user_data["roles"] = [role]
                    user_data["permissions"] = role_service.get_role_permissions(
                        role.id
                    )
                    logger.info(f"Assigned default '{role.name}' role to user: {email}")
                else:
                    logger.error(
                        "No default roles ('user' or 'admin') found in the database"
                    )
                    raise ValueError(
                        "Failed to assign default role - no roles found in database"
                    )

            except Exception as e:
                logger.error(f"Failed to assign default role to user: {str(e)}")
                raise ValueError(f"Failed to assign default role: {str(e)}")

            return user_data
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to sign up: {str(e)}")
            raise ValueError(f"Sign up failed: {str(e)}")

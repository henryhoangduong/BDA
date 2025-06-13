import logging
from typing import Any, Dict, Optional

from pydantic import EmailStr

from services.auth.role_service import RoleService
from services.auth.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def sign_up(
        email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None
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
                raise ValueError(
                    f"Failed to sign up: {response.error.message}")
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
                    logger.info(
                        f"Assigned default '{role.name}' role to user: {email}")
                else:
                    logger.error(
                        "No default roles ('user' or 'admin') found in the database"
                    )
                    raise ValueError(
                        "Failed to assign default role - no roles found in database"
                    )

            except Exception as e:
                logger.error(
                    f"Failed to assign default role to user: {str(e)}")
                raise ValueError(f"Failed to assign default role: {str(e)}")

            return user_data
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to sign up: {str(e)}")
            raise ValueError(f"Sign up failed: {str(e)}")

    async def sign_in(email: str, password: str) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if hasattr(response, 'error') and response.error:
                raise ValueError(
                    f"Failed to sign in: {response.error.message}")
            logger.info(f"User signed in successfully: {email}")
            return {
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "created_at": response.user.created_at,
                    "metadata": response.user.user_metadata,
                },
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_at": response.session.expires_at
                }
            }
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to sign in: {str(e)}")
            raise ValueError(f"Sign in failed: {str(e)}")

    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, str]:
        """Refresh an authentication token.

        Args:
            refresh_token: Refresh token

        Returns:
            Dict with new access and refresh tokens

        Raises:
            ValueError: If token refresh fails
        """
        try:
            supabase = get_supabase_client()

            response = supabase.auth.refresh_session(refresh_token)

            if hasattr(response, 'error') and response.error:
                raise ValueError(
                    f"Failed to refresh token: {response.error.message}")

            logger.info("Token refreshed successfully")

            return {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            }
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            raise ValueError(f"Token refresh failed: {str(e)}")

    async def sign_out(access_token: Optional[str] = None) -> None:
        try:
            supabase = get_supabase_client()

            if access_token:
                # Sign out specific session
                response = supabase.auth.sign_out(access_token)
            else:
                # Sign out current session
                response = supabase.auth.sign_out()

            if hasattr(response, 'error') and response.error:
                raise ValueError(
                    f"Failed to sign out: {response.error.message}")

            logger.info("User signed out successfully")
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to sign out: {str(e)}")
            raise ValueError(f"Sign out failed: {str(e)}")

import logging
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException, status

from database.postgres import PostgresDB
from models.role import Permission, Role, UserRole

logger = logging.getLogger(__name__)


class RoleService:
    @staticmethod
    def get_user_roles(user_id: str) -> List[Role]:
        try:
            # Get roles for user with a JOIN query
            rows = PostgresDB.fetch_all("""
                SELECT r.id, r.name, r.description, r.created_at
                FROM roles r
                JOIN user_roles ur ON ur.role_id = r.id
                WHERE ur.user_id = %s
                ORDER BY r.name
            """, (user_id,))

            # Convert to Role objects
            roles = [
                Role(
                    id=row['id'],
                    name=row['name'],
                    description=row.get('description'),
                    created_at=row.get('created_at')
                )
                for row in rows
            ]

            return roles
        except Exception as e:
            logger.error(f"Failed to get user roles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user roles"
            )

import logging
from typing import List, Optional

from fastapi import HTTPException, status

from database.postgres import PostgresDB
from models.role import Permission, Role, UserRole

logger = logging.getLogger(__name__)


class RoleService:
    @staticmethod
    def get_roles() -> List[Role]:
        try:
            rows = PostgresDB.fetch_all(
                """SELECT id, name, description, created_at, FROM roles ORDER BY name"""
            )
            roles = [
                Role(
                    id=rows["id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]
            return rows
        except Exception as e:
            logger.error(f"Failed to get roles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch roles",
            )

    @staticmethod
    def get_role_by_name(role_name: str) -> Optional[Role]:
        try:
            row = PostgresDB.fetch_one(
                """SELECT * from roles where name = %s""", (role_name,)
            )
            if not row:
                return None

            return Role(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                created_at=row["created_at"],
            )
        except Exception as e:
            logger.error(f"Failed to get role by name: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch role",
            )

    @staticmethod
    def assign_role_to_user(user_id: str, role_id: int) -> UserRole:
        """Assign a role to a user.

        Args:
            user_id: User ID
            role_id: Role ID

        Returns:
            UserRole: Created user role
        """
        try:
            # Check if role exists using PostgresDB
            role = PostgresDB.fetch_one(
                "SELECT id FROM roles WHERE id = %s", (role_id,)
            )
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with ID {role_id} not found",
                )

            # Check if user already has this role using PostgresDB
            existing = PostgresDB.fetch_one(
                "SELECT user_id, role_id FROM user_roles WHERE user_id = %s AND role_id = %s",
                (user_id, role_id),
            )

            if existing:
                # User already has this role
                return UserRole(user_id=user_id, role_id=role_id)

            # Assign role to user using PostgresDB
            PostgresDB.execute_query(
                "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)",
                (user_id, role_id),
            )

            return UserRole(user_id=user_id, role_id=role_id)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to assign role to user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign role to user",
            )

    @staticmethod
    def get_role_permissions(role_id: int) -> List[Permission]:
        try:
            rows = PostgresDB.fetch_all(
                """
            SELECT p.id, p.name, p.description
            FROM permissions p
            JOIN role_permissions rp ON rp.permission_id = p.id
                WHERE rp.role_id = %s
                ORDER BY p.name
            """,
                (role_id,),
            )
            permissions = [
                Permission(
                    id=row["id"], name=row["name"], description=row["description"]
                )
                for row in rows
            ]
            return permissions
        except Exception as e:
            logger.error(f"Failed to get role permissions: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch role permissions",
            )

    @staticmethod
    def has_role(user_id: str, role_name: str):
        try:
            row = PostgresDB.fetch_one("""
                SELECT 1
                FROM roles r
                JOIN user_roles ur ON ur.role_id=r.id
                WHERE ur.user_id = %s AND r.name = %s
                LIMIT 1
                                       """)
            return row is not None
        except Exception as e:
            logger.error(f"Failed to check user role: {str(e)}")
            return False

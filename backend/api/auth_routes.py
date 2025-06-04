import logging
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

auth_router = APIRouter(
    prefix=f"/auth",
    tags=["auth"],
)
# Request/Response models


class SignUpRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    metadata: Optional[Dict] = Field(
        default=None, description="Additional user metadata"
    )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signUpRequest: SignUpRequest):
    try:
        pass
    except ValueError as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_router.post("/signin", status_code=status.HTTP_201_CREATED)
async def signin():
    pass

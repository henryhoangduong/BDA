import logging
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from services.auth.auth_service import AuthService

logger = logging.getLogger(__name__)

auth_router = APIRouter(
    prefix=f"/auth",
    tags=["auth"],
)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")


class SignInRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class SignUpRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    metadata: Optional[Dict] = Field(
        default=None, description="Additional user metadata"
    )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignUpRequest):
    try:
        user = await AuthService.sign_up(
            email=request.email,
            password=request.password,
            user_metadata=request.metadata
        )
        return user
    except ValueError as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_router.post("/signin", status_code=status.HTTP_201_CREATED)
async def signin(request: SignInRequest):
    try:
        result = await AuthService.sign_in(
            email=request.email,
            password=request.password
        )

        # Ensure the response has the format expected by the frontend
        if "user" not in result or "session" not in result:
            logger.error(f"Invalid auth response structure: {result}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid authentication response from server"
            )

        return result
    except ValueError as e:
        logger.error(f"Signin error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during signin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        tokens = await AuthService.refresh_token(refresh_token=request.refresh_token)
        return tokens
    except ValueError as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

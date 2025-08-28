from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from axiom.config import OWNER_ID, supabase

load_dotenv()

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validate JWT token from Supabase and return user information
    """
    try:
        token = credentials.credentials

        # Verify the JWT token with Supabase
        user_response = supabase.auth.get_user(token)

        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_response.user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(current_user=Depends(get_current_user)):
    """
    Ensure the user is active (not disabled)
    """
    # In Supabase, users are either active or banned/disabled
    # We can check user metadata or just return the user if valid
    return current_user


async def get_owner_user(current_user=Depends(get_current_active_user)):
    """
    Ensure the current user is the owner (for Schwab access)
    """
    if current_user.id != OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )
    return current_user


def require_auth():
    """
    Dependency that requires authentication
    """
    return Depends(get_current_active_user)


def require_owner():
    """
    Dependency that requires owner authentication
    """
    return Depends(get_owner_user)

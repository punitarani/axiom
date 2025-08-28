import base64
import json

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from axiom.config import supabase
from axiom.env import env

security = HTTPBearer()


async def get_current_user_from_cookies(request: Request):
    """
    Validate JWT token from Supabase SSR cookies.
    """
    try:
        # Get session cookie: sb-{SUPABASE_PROJECT_ID}-auth-token
        cookie_name = f"sb-{env.SUPABASE_PROJECT_ID}-auth-token"
        cookie_value = request.cookies.get(cookie_name)

        if not cookie_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication token found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Parse cookie value as JSON object
        if not cookie_value.startswith("base64-"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session cookie format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        base64_str = cookie_value[7:].strip()
        # Add padding if necessary
        missing_padding = len(base64_str) % 4
        if missing_padding:
            base64_str += "=" * (4 - missing_padding)

        decoded = base64.b64decode(base64_str).decode("utf-8")
        session_data = json.loads(decoded)

        if not isinstance(session_data, dict):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract tokens from the session object
        access_token = session_data.get("access_token")
        refresh_token = session_data.get("refresh_token")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No access token in session",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Set session in Supabase client
        if refresh_token:
            supabase.auth.set_session(
                access_token=access_token, refresh_token=refresh_token
            )

        # Always validate server-side for security
        user_response = supabase.auth.get_user(access_token)

        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_response.user

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validate JWT token from Supabase and return user information (Bearer token method)
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


async def get_current_active_user_from_cookies(request: Request):
    """
    Get active user from cookies
    """
    current_user = await get_current_user_from_cookies(request)
    return current_user


async def get_owner_user_from_cookies(request: Request):
    """
    Ensure the current user is the owner (for Schwab access) - from cookies
    """
    current_user = await get_current_active_user_from_cookies(request)
    if current_user.id != env.OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )
    return current_user


async def get_owner_user(current_user=Depends(get_current_active_user)):
    """
    Ensure the current user is the owner (for Schwab access)
    """
    if current_user.id != env.OWNER_ID:
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


def require_auth_cookies():
    """
    Dependency that requires authentication from cookies
    """
    return Depends(get_current_active_user_from_cookies)


def require_owner():
    """
    Dependency that requires owner authentication
    """
    return Depends(get_owner_user)


def require_owner_cookies():
    """
    Dependency that requires owner authentication from cookies
    """
    return Depends(get_owner_user_from_cookies)

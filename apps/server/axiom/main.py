import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.api.auth.schwab import router as schwab_auth_router
from axiom.auth import require_auth
from axiom.config import supabase
from axiom.db.client import get_db
from axiom.db.models.oauth import OAuthState
from axiom.env import env
from axiom.mdata.auth import SchwabAuthService

app = FastAPI(title="Axiom Server", version="0.1.0")

# Configure CORS to allow frontend connection with credentials (cookies)
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Include auth routers
app.include_router(schwab_auth_router, prefix="/api/auth")


@app.get("/")
async def root():
    return {"message": "Axiom Server API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/protected")
async def protected_route(current_user=require_auth()):
    """
    Example protected route that requires authentication
    """
    return {
        "message": "This is a protected route",
        "user": {"id": current_user.id, "email": current_user.email},
    }


@app.get("/user/profile")
async def get_user_profile(
    current_user=require_auth(), db: AsyncSession = Depends(get_db)
):
    """
    Get current user profile
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "email_confirmed_at": current_user.email_confirmed_at,
    }


@app.get("/user/me")
async def get_current_user_info(current_user=require_auth()):
    """
    Get current user info using header auth
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


@app.get("/connections/status")
async def get_connection_status(current_user=require_auth()):
    """
    Get status of all supported connections
    """
    schwab_auth_service = SchwabAuthService()

    connections = {}

    # Check Schwab connection (only for owner)
    if current_user.id == env.OWNER_ID:
        try:
            schwab_tokens = await schwab_auth_service.get_tokens_from_vault(
                current_user.id
            )
            connections["schwab"] = {
                "name": "Charles Schwab",
                "connected": bool(schwab_tokens),
                "available": True,
            }
        except Exception:
            connections["schwab"] = {
                "name": "Charles Schwab",
                "connected": False,
                "available": True,
            }
    else:
        connections["schwab"] = {
            "name": "Charles Schwab",
            "connected": False,
            "available": False,
            "reason": "Owner privileges required",
        }

    return {"connections": connections}


@app.post("/connect/schwab")
async def connect_schwab(
    current_user=require_auth(), db: AsyncSession = Depends(get_db)
):
    """
    Connect Schwab account - validates owner internally and returns auth URL
    """
    schwab_auth_service = SchwabAuthService()

    # Check if user is owner
    if current_user.id != env.OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )

    # Check if already connected
    tokens = await schwab_auth_service.get_tokens_from_vault(current_user.id)
    if tokens:
        return {"connected": True, "message": "Schwab account already connected"}

    # Generate auth URL
    auth_url, state = await schwab_auth_service.generate_auth_url(current_user.id, db)
    return {"connected": False, "auth_url": auth_url, "state": state}


@app.delete("/disconnect/schwab")
async def disconnect_schwab(current_user=require_auth()):
    """
    Disconnect Schwab account - validates owner internally
    """

    # Check if user is owner
    if current_user.id != env.OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )

    try:
        vault_key = f"schwab_tokens_{current_user.id}"
        supabase.postgrest.table("vault").delete().eq("id", vault_key).execute()
        return {"message": "Schwab account disconnected successfully"}
    except Exception as e:
        return {"error": f"Failed to disconnect: {str(e)}"}


@app.post("/reset/schwab")
async def reset_schwab_connection(
    current_user=require_auth(), db: AsyncSession = Depends(get_db)
):
    """
    Reset Schwab connection - clears all auth data including tokens and OAuth states
    """

    # Check if user is owner
    if current_user.id != env.OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )

    try:
        vault_key = f"schwab_tokens_{current_user.id}"

        # Clear tokens from vault
        supabase.postgrest.table("vault").delete().eq("id", vault_key).execute()

        # Clear any pending OAuth states for this user
        await db.execute(
            delete(OAuthState).where(OAuthState.user_id == current_user.id)
        )
        await db.commit()

        return {"message": "Schwab connection reset successfully"}
    except Exception as e:
        return {"error": f"Failed to reset connection: {str(e)}"}


@app.get("/openapi.json")
async def get_openapi():
    """
    Export OpenAPI schema for code generation
    """
    return app.openapi()


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

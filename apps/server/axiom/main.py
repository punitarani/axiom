import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.auth import require_auth, require_auth_cookies
from axiom.database import get_db
from axiom.schwab_auth import schwab_auth_service

app = FastAPI(title="Axiom Server", version="0.1.0")

# Configure CORS to allow frontend connection with credentials (cookies)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # This allows cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/connect/schwab")
async def connect_schwab(current_user=require_auth_cookies()):
    """
    Connect Schwab account - validates owner internally and returns auth URL
    """
    from axiom.config import OWNER_ID
    
    # Check if user is owner
    if current_user.id != OWNER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Owner privileges required.",
        )
    
    # Check if already connected
    tokens = await schwab_auth_service.get_tokens_from_vault(current_user.id)
    if tokens:
        return {
            "connected": True,
            "message": "Schwab account already connected"
        }
    
    # Generate auth URL
    auth_url, state = schwab_auth_service.generate_auth_url(current_user.id)
    return {
        "connected": False,
        "auth_url": auth_url,
        "state": state
    }


@app.get("/api/schwab/callback")
async def schwab_oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
):
    """
    Handle Schwab OAuth callback - validates state to identify user
    """
    try:
        # Get user ID from state validation
        user_id = await schwab_auth_service.get_user_id_from_state(state)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid or expired OAuth state")
            
        # Validate that user is owner
        from axiom.config import OWNER_ID
        if user_id != OWNER_ID:
            raise HTTPException(status_code=403, detail="Access denied. Owner privileges required.")
        
        # Exchange code for tokens
        tokens = await schwab_auth_service.exchange_code_for_tokens(
            code, state, user_id
        )
        
        # Store tokens in vault
        await schwab_auth_service.store_tokens_in_vault(user_id, tokens)
        
        # Redirect to frontend success page
        return RedirectResponse(url="http://localhost:3000/schwab/success")
        
    except HTTPException:
        raise
    except Exception as e:
        # Redirect to frontend error page
        return RedirectResponse(url=f"http://localhost:3000/schwab/error?message={str(e)}")


@app.delete("/disconnect/schwab")
async def disconnect_schwab(current_user=require_auth_cookies()):
    """
    Disconnect Schwab account - validates owner internally
    """
    from axiom.config import OWNER_ID, supabase
    
    # Check if user is owner
    if current_user.id != OWNER_ID:
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

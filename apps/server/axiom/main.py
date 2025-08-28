import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.auth import require_auth
from axiom.database import get_db

app = FastAPI(title="Axiom Server", version="0.1.0")

# Configure CORS to allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
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

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl, validator

load_dotenv()


class Environment(BaseModel):
    """Environment variables configuration with validation and type parsing."""

    # App URLs
    API_URL: HttpUrl = Field(
        default="http://localhost:8000", description="Backend API URL"
    )
    APP_URL: HttpUrl = Field(
        default="http://localhost:3000", description="Frontend app URL"
    )

    # Supabase Configuration
    SUPABASE_URL: HttpUrl = Field(..., description="Supabase project URL")
    SUPABASE_SERVICE_KEY: str = Field(
        ..., min_length=1, description="Supabase service key"
    )
    SUPABASE_ANON_KEY: str = Field(
        ..., min_length=1, description="Supabase anonymous key"
    )
    SUPABASE_JWT_SECRET: str = Field(
        ..., min_length=1, description="Supabase JWT secret"
    )
    SUPABASE_PROJECT_ID: str = Field(
        ..., min_length=1, description="Supabase project ID"
    )

    # Database Configuration
    DB_URL: str = Field(
        default="postgresql+asyncpg://user:pass@localhost/axiom",
        description="Database connection URL",
    )

    # Schwab OAuth Configuration
    SCHWAB_API_KEY: str = Field(..., min_length=1, description="Schwab API key")
    SCHWAB_APP_SECRET: str = Field(..., min_length=1, description="Schwab app secret")
    SCHWAB_CALLBACK_URL: Optional[str] = Field(
        default=None, description="Schwab OAuth callback URL"
    )

    # Access Control
    OWNER_ID: str = Field(
        ..., min_length=1, description="Owner user ID for access control"
    )

    # Environment Settings
    ENVIRONMENT: str = Field(default="development", description="Current environment")
    DEBUG: bool = Field(default=True, description="Enable debug mode")

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("SCHWAB_CALLBACK_URL", always=True)
    def set_schwab_callback_url(cls, v, values):
        """Auto-generate Schwab callback URL if not provided."""
        if v is None and "API_URL" in values:
            return f"{values['API_URL']}/api/auth/schwab/callback"
        return v

    @validator("DEBUG")
    def parse_debug(cls, v):
        """Parse DEBUG from string to boolean."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v

    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment is one of expected values."""
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    @property
    def origins(self) -> list[str]:
        """Generate CORS origins list."""
        app_origin = str(self.APP_URL).rstrip("/")
        origins = [app_origin]
        # Also allow 127.0.0.1 variant for local development convenience
        if app_origin.startswith("http://localhost:"):
            origins.append(app_origin.replace("localhost", "127.0.0.1", 1))
        return list(dict.fromkeys(origins))


def create_env() -> Environment:
    """Create and validate environment configuration."""
    try:
        return Environment(
            API_URL=os.getenv("API_URL", "http://localhost:8000"),
            APP_URL=os.getenv("APP_URL", "http://localhost:3000"),
            SUPABASE_URL=os.getenv("SUPABASE_URL"),
            SUPABASE_SERVICE_KEY=os.getenv("SUPABASE_SERVICE_KEY"),
            SUPABASE_ANON_KEY=os.getenv("SUPABASE_ANON_KEY"),
            SUPABASE_JWT_SECRET=os.getenv("SUPABASE_JWT_SECRET"),
            SUPABASE_PROJECT_ID=os.getenv("SUPABASE_PROJECT_ID"),
            DB_URL=os.getenv(
                "DB_URL", "postgresql+asyncpg://user:pass@localhost/axiom"
            ),
            SCHWAB_API_KEY=os.getenv("SCHWAB_API_KEY"),
            SCHWAB_APP_SECRET=os.getenv("SCHWAB_APP_SECRET"),
            SCHWAB_CALLBACK_URL=os.getenv("SCHWAB_CALLBACK_URL"),
            OWNER_ID=os.getenv("OWNER_ID"),
            ENVIRONMENT=os.getenv("ENVIRONMENT", "development"),
            DEBUG=os.getenv("DEBUG", "true"),
        )
    except Exception as e:
        print(f"❌ Environment validation failed: {e}")
        raise


# Global environment instance
env = create_env()

# Validate required configurations
if not all([env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY, env.SUPABASE_PROJECT_ID]):
    raise ValueError("❌ Missing required Supabase configuration")

if not all([env.SCHWAB_API_KEY, env.SCHWAB_APP_SECRET, env.OWNER_ID]):
    raise ValueError("❌ Missing required Schwab OAuth or OWNER_ID configuration")

print(f"✅ Environment loaded successfully ({env.ENVIRONMENT} mode)")

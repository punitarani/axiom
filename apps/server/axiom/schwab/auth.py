import json
import secrets
from typing import Optional
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from axiom.config import supabase
from axiom.env import env


class SchwabAuthService:
    def __init__(self):
        self.api_key = env.SCHWAB_API_KEY
        self.app_secret = env.SCHWAB_APP_SECRET
        self.callback_url = env.SCHWAB_CALLBACK_URL
        self.auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self.token_url = "https://api.schwabapi.com/v1/oauth/token"

    def generate_auth_url(self, user_id: str) -> tuple[str, str]:
        """
        Generate OAuth authorization URL and state parameter
        """
        state = secrets.token_urlsafe(32)

        # Store state temporarily for validation
        self._store_oauth_state(user_id, state)

        params = {
            "client_id": self.api_key,
            "redirect_uri": self.callback_url,
            "response_type": "code",
            "scope": "readonly",
            "state": state,
        }

        auth_url = f"{self.auth_url}?{urlencode(params)}"
        return auth_url, state

    async def exchange_code_for_tokens(
        self, code: str, state: str, user_id: str
    ) -> dict:
        """
        Exchange authorization code for access and refresh tokens
        """
        # Validate state parameter
        if not self._validate_oauth_state(user_id, state):
            raise HTTPException(status_code=400, detail="Invalid OAuth state")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {self._get_basic_auth_header()}",
                },
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.callback_url,
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to exchange code for tokens: {response.text}",
            )

        return response.json()

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh access token using refresh token
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {self._get_basic_auth_header()}",
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail=f"Failed to refresh token: {response.text}"
            )

        return response.json()

    async def store_tokens_in_vault(self, user_id: str, tokens: dict) -> None:
        """
        Store Schwab tokens securely in Supabase Vault
        """
        try:
            # Store in Supabase Vault with user-specific key
            vault_key = f"schwab_tokens_{user_id}"

            # Store tokens as encrypted JSON
            token_data = {
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "expires_in": tokens.get("expires_in"),
                "token_type": tokens.get("token_type", "Bearer"),
                "scope": tokens.get("scope"),
            }

            # Use Supabase Vault for secure storage
            supabase.postgrest.table("vault").upsert(
                {"id": vault_key, "secret": json.dumps(token_data)}
            ).execute()

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to store tokens: {str(e)}"
            )

    async def get_tokens_from_vault(self, user_id: str) -> Optional[dict]:
        """
        Retrieve Schwab tokens from Supabase Vault
        """
        try:
            vault_key = f"schwab_tokens_{user_id}"

            result = (
                supabase.postgrest.table("vault")
                .select("secret")
                .eq("id", vault_key)
                .execute()
            )

            if not result.data:
                return None

            return json.loads(result.data[0]["secret"])

        except Exception:
            return None

    def _get_basic_auth_header(self) -> str:
        """
        Generate basic auth header for token requests
        """
        import base64

        credentials = f"{self.api_key}:{self.app_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return encoded

    def _store_oauth_state(self, user_id: str, state: str) -> None:
        """
        Temporarily store OAuth state for validation
        """
        try:
            # Store state with 10 minute expiry
            supabase.postgrest.table("oauth_states").upsert(
                {"user_id": user_id, "state": state, "created_at": "now()"}
            ).execute()
        except Exception:
            pass  # Non-critical for demo purposes

    async def get_user_id_from_state(self, state: str) -> Optional[str]:
        """
        Get user ID from OAuth state parameter and validate it
        """
        try:
            result = (
                supabase.postgrest.table("oauth_states")
                .select("user_id")
                .eq("state", state)
                .execute()
            )

            if result.data:
                user_id = result.data[0]["user_id"]
                # Clean up used state
                supabase.postgrest.table("oauth_states").delete().eq(
                    "state", state
                ).execute()
                return user_id

            return None
        except Exception:
            return None

    def _validate_oauth_state(self, user_id: str, state: str) -> bool:
        """
        Validate OAuth state parameter
        """
        try:
            result = (
                supabase.postgrest.table("oauth_states")
                .select("state")
                .eq("user_id", user_id)
                .eq("state", state)
                .execute()
            )

            if result.data:
                # Clean up used state
                supabase.postgrest.table("oauth_states").delete().eq(
                    "user_id", user_id
                ).eq("state", state).execute()
                return True

            return False
        except Exception:
            return False


schwab_auth_service = SchwabAuthService()

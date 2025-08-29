import asyncio
import base64
import json
import secrets
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode

import httpx
import schwab
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.config import supabase
from axiom.db.models.oauth import OAuthState
from axiom.env import env


class SchwabAuthService:
    def __init__(self):
        self.api_key = env.SCHWAB_API_KEY
        self.app_secret = env.SCHWAB_APP_SECRET
        self.callback_url = env.SCHWAB_CALLBACK_URL

    async def generate_auth_url(
        self, user_id: str, db: AsyncSession
    ) -> tuple[str, str]:
        # Generate and store random state for validation
        state = secrets.token_urlsafe(32)
        await self._store_oauth_state(user_id, state, db)

        params = {
            "client_id": self.api_key,
            "redirect_uri": self.callback_url,
            "response_type": "code",
            "scope": "readonly",
            "state": state,
        }

        auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?{urlencode(params)}"
        return auth_url, state

    async def exchange_code_for_tokens(
        self, code: str, state: str, user_id: str
    ) -> dict:
        """
        Exchange authorization code for tokens using HTTP requests
        """
        async with httpx.AsyncClient() as client:
            auth_header = base64.b64encode(
                f"{self.api_key}:{self.app_secret}".encode()
            ).decode()

            response = await client.post(
                "https://api.schwabapi.com/v1/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {auth_header}",
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

    async def get_client_for_user(self, user_id: str) -> Optional[schwab.client.Client]:
        """
        Get authenticated schwab client for user
        """
        tokens = await self.get_tokens_from_vault(user_id)
        if not tokens:
            return None

        # Create client with stored tokens
        def token_read():
            return tokens

        def token_write(new_token):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.store_tokens_in_vault(user_id, new_token))
            loop.close()

        return schwab.auth.client_from_access_functions(
            api_key=self.api_key,
            app_secret=self.app_secret,
            token_read_func=token_read,
            token_write_func=token_write,
            asyncio=True,
        )

    async def store_tokens_in_vault(self, user_id: str, tokens: dict) -> None:
        """
        Store Schwab tokens securely in Supabase Vault
        """
        vault_name = f"schwab_tokens_{user_id}"
        secret_data = json.dumps(tokens)

        # Use Supabase Vault's create_secret function with correct parameter order
        supabase.postgrest.schema("vault").rpc(
            "create_secret",
            {
                "new_secret": secret_data,
                "new_name": vault_name,
                "new_description": f"Schwab OAuth tokens for user {user_id}",
                "new_key_id": None,
            },
        ).execute()

    async def get_tokens_from_vault(self, user_id: str) -> Optional[dict]:
        """
        Retrieve Schwab tokens from Supabase Vault
        """
        vault_name = f"schwab_tokens_{user_id}"

        # Query the decrypted_secrets view to get the token
        result = (
            supabase.postgrest.schema("vault")
            .table("decrypted_secrets")
            .select("decrypted_secret")
            .eq("name", vault_name)
            .execute()
        )

        if not result.data:
            return None

        return json.loads(result.data[0]["decrypted_secret"])

    async def _store_oauth_state(
        self, user_id: str, state: str, db: AsyncSession
    ) -> None:
        """
        Temporarily store OAuth state for validation
        """
        # Delete any existing state for this user to ensure uniqueness
        await db.execute(delete(OAuthState).where(OAuthState.user_id == user_id))

        # Store new state
        oauth_state = OAuthState(
            user_id=user_id,
            state=state,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        db.add(oauth_state)
        await db.commit()

    async def get_user_id_from_state(
        self, state: str, db: AsyncSession
    ) -> Optional[str]:
        """
        Get user ID from OAuth state parameter and validate it
        """
        async with db.begin():
            # Find the OAuth state
            result = await db.execute(
                select(OAuthState).where(OAuthState.state == state)
            )
            oauth_state = result.scalar_one_or_none()

            if oauth_state:
                user_id = oauth_state.user_id

                # Clean up used state
                await db.execute(delete(OAuthState).where(OAuthState.state == state))
                return user_id

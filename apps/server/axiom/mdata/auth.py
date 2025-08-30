import asyncio
import json
import secrets
import time
from datetime import datetime, timezone
from typing import Optional

from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client
from fastapi import HTTPException
from schwab.auth import TokenMetadata
from schwab.client import AsyncClient
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
        self._authorize_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self._token_endpoint = "https://api.schwabapi.com/v1/oauth/token"

    async def generate_auth_url(
        self, user_id: str, db: AsyncSession
    ) -> tuple[str, str]:
        # Generate and store random state for validation
        state = secrets.token_urlsafe(32)
        await self._store_oauth_state(user_id, state, db)

        # Use Authlib to create the authorization URL
        oauth = OAuth2Client(self.api_key, redirect_uri=self.callback_url)
        authorization_url, returned_state = oauth.create_authorization_url(
            self._authorize_url, state=state
        )

        # Prefer the state that Authlib returns (should match provided)
        return authorization_url, returned_state

    async def exchange_code_for_tokens(
        self, code: str, state: str, user_id: str
    ) -> dict:
        """
        Exchange authorization code for tokens using Authlib (OAuth2Client)
        and return the token in Authlib format (includes expires_at).
        """
        oauth = AsyncOAuth2Client(
            self.api_key, client_secret=self.app_secret, redirect_uri=self.callback_url
        )
        try:
            token = await oauth.fetch_token(
                self._token_endpoint,
                code=code,
                grant_type="authorization_code",
                client_id=self.api_key,
                auth=(self.api_key, self.app_secret),
                state=state,
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to exchange code for tokens: {e}"
            )

        # Authlib attaches an absolute expires_at; keep the dict as-is
        # Optionally compute a refresh_token_expires_at if provided as relative
        now_ts = int(time.time())
        rtei = token.get("refresh_token_expires_in")
        if isinstance(rtei, (int, float)) and "refresh_token_expires_at" not in token:
            token["refresh_token_expires_at"] = int(now_ts + int(rtei))

        return token

    async def get_client_for_user(self, user_id: str) -> Optional[AsyncClient]:
        """
        Get authenticated schwab client for user
        """
        tokens = await self.get_tokens_from_vault(user_id)
        if not tokens:
            return None

        def _write_wrapped_to_vault(wrapped_token: dict, *args, **kwargs) -> None:
            inner = (
                wrapped_token.get("token")
                if isinstance(wrapped_token, dict)
                else wrapped_token
            )
            if not isinstance(inner, dict):
                return
            try:
                running = asyncio.get_running_loop()
                running.create_task(self.store_tokens_in_vault(user_id, inner))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                try:
                    loop.run_until_complete(self.store_tokens_in_vault(user_id, inner))
                finally:
                    loop.close()

        token_metadata = TokenMetadata(
            tokens, int(time.time()), _write_wrapped_to_vault
        )

        async def update_token(token: dict, *args, **kwargs) -> None:
            token_metadata.token = token
            await self.store_tokens_in_vault(user_id, token)

        # Build an Authlib OAuth2 session with refresh support
        session = AsyncOAuth2Client(
            self.api_key,
            client_secret=self.app_secret,
            token=tokens,
            token_endpoint=self._token_endpoint,
            update_token=update_token,
            leeway=300,
        )

        # Create Schwab AsyncClient backed by the Authlib session
        client = AsyncClient(self.api_key, session)
        # Attach TokenMetadata so StreamClient can access the token
        # This is a hack but required for StreamClient to work
        setattr(client, "token_metadata", token_metadata)
        return client

    async def store_tokens_in_vault(self, user_id: str, tokens: dict) -> None:
        """
        Store Schwab tokens securely in Supabase Vault (Authlib format)
        """
        vault_name = f"schwab_tokens_{user_id}"
        if not isinstance(tokens, dict):
            raise ValueError("Invalid token format: expected dict")
        # Persist raw Authlib token dict as-is
        secret_data = json.dumps(tokens)

        # Ensure idempotency: delete existing by name, then create
        try:
            supabase.postgrest.schema("vault").from_("secrets").delete().eq(
                "name", vault_name
            ).execute()
        except Exception:
            pass

        # Use Supabase Vault's create_secret RPC
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
        Retrieve Schwab tokens from Supabase Vault (returns Authlib format)
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

        try:
            loaded = json.loads(result.data[0]["decrypted_secret"])
        except Exception:
            return None

        # If token is in legacy wrapped format, unwrap to Authlib format and migrate
        if isinstance(loaded, dict) and (
            "creation_timestamp" in loaded and "token" in loaded
        ):
            unwrapped = loaded.get("token") or {}
            if isinstance(unwrapped, dict):
                await self.store_tokens_in_vault(user_id, unwrapped)
                return unwrapped
            return None

        # Already in Authlib format
        return loaded if isinstance(loaded, dict) else None

    async def delete_tokens_from_vault(self, user_id: str) -> None:
        """Delete Schwab tokens for a user from Supabase Vault by name."""
        vault_name = f"schwab_tokens_{user_id}"
        try:
            supabase.postgrest.schema("vault").from_("secrets").delete().eq(
                "name", vault_name
            ).execute()
        except Exception:
            pass

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

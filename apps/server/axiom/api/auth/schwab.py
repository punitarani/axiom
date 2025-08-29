from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.db.client import get_db
from axiom.env import env
from axiom.mdata.auth import SchwabAuthService

router = APIRouter(prefix="/schwab", tags=["schwab-auth"])


@router.get("/callback")
async def schwab_oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
    session: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Schwab OAuth callback - validates state to identify user
    """
    schwab_auth_service = SchwabAuthService()

    try:
        # Get user ID from state validation
        user_id = await schwab_auth_service.get_user_id_from_state(state, db)
        if not user_id:
            raise HTTPException(
                status_code=400, detail="Invalid or expired OAuth state"
            )

        # Validate that user is owner
        if user_id != env.OWNER_ID:
            raise HTTPException(
                status_code=403, detail="Access denied. Owner privileges required."
            )

        # Exchange code for tokens
        tokens = await schwab_auth_service.exchange_code_for_tokens(
            code, state, user_id
        )

        # Store tokens in vault
        await schwab_auth_service.store_tokens_in_vault(user_id, tokens)

        # Redirect to frontend success page
        redirect_url = f"{env.APP_URL}/oauth/callback?success=true&connection=schwab"
        return RedirectResponse(url=redirect_url)

    except HTTPException:
        raise
    except Exception as e:
        # Redirect to frontend error page
        return RedirectResponse(
            url=f"{env.APP_URL}/oauth/callback?error={str(e)}&connection=schwab"
        )

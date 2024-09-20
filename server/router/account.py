"""server/router/account.py"""

from fastapi import APIRouter, HTTPException

from axiom.mdata.account import get_account_info
from axiom.schwab_models_account import Position

router = APIRouter(prefix="/account")


@router.get("/positions")
async def get_positions() -> list[Position]:
    try:
        account_info = await get_account_info()
        positions = account_info.securitiesAccount.root.positions
        if positions is None:
            return []
        return positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching account positions: {str(e)}")

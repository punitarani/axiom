"""server/router/account.py"""

from fastapi import APIRouter, Depends, HTTPException

from axiom.mdata.account import get_account_info, get_account_transactions
from axiom.schwab_models_account import Position, Transaction

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


@router.get("/transactions")
async def get_transactions() -> list[Transaction]:
    try:
        transactions = await get_account_transactions()
        if transactions is None:
            return []
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching account transactions: {str(e)}"
        )

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.db.models import Account, Transaction, TransactionType
from axiom.mdata.auth import SchwabAuthService


class AccountService:
    def __init__(self, auth: Optional[SchwabAuthService] = None):
        self.auth = auth or SchwabAuthService()

    async def ensure_account(
        self,
        db: AsyncSession,
        account_hash: str,
        account_number: str,
        nickname: Optional[str] = None,
    ) -> Account:
        result = await db.execute(
            select(Account).where(Account.account_hash == account_hash)
        )
        account = result.scalar_one_or_none()
        if account:
            return account
        account = Account(
            account_hash=account_hash, account_number=account_number, nickname=nickname
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account

    async def sync_transactions(
        self,
        db: AsyncSession,
        user_id: str,
        account_hash: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        symbol: Optional[str] = None,
        transaction_types: Optional[Iterable[TransactionType]] = None,
    ) -> int:
        client = await self.auth.get_client_for_user(user_id)
        if client is None:
            return 0

        params: dict = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if symbol:
            params["symbol"] = symbol
        if transaction_types:
            params["transaction_types"] = [t.value for t in transaction_types]

        resp = await client.get_transactions(account_hash, **params)
        resp.raise_for_status()
        data = resp.json() or []

        inserted = 0
        for item in data:
            provider_transaction_id = str(item.get("transactionId"))
            txn_type = TransactionType(item.get("type", "MEMORANDUM"))
            symbol_val = item.get("symbol")
            quantity = item.get("amount", None)
            price = item.get("price", None)
            amount = item.get("netAmount", None)
            fees = item.get("fees", None)
            entered = item.get("transactionDate") or item.get("enteredTime")
            txn_time = (
                datetime.fromisoformat(entered.replace("Z", "+00:00"))
                if isinstance(entered, str)
                else datetime.now(timezone.utc)
            )

            # Find account by hash
            result_acc = await db.execute(
                select(Account).where(Account.account_hash == account_hash)
            )
            account = result_acc.scalar_one_or_none()
            if account is None:
                continue

            existing = await db.execute(
                select(Transaction).where(
                    Transaction.provider == "schwab",
                    Transaction.provider_transaction_id == provider_transaction_id,
                )
            )
            if existing.scalar_one_or_none():
                continue

            txn = Transaction(
                account_id=account.id,
                provider="schwab",
                provider_transaction_id=provider_transaction_id,
                type=txn_type,
                symbol=symbol_val,
                quantity=quantity,
                price=price,
                amount=amount,
                fees=fees,
                transaction_time=txn_time,
            )
            db.add(txn)
            inserted += 1

        if inserted:
            await db.commit()
        return inserted

"""axiom/mdata/account.py"""

from axiom.schwab_client import get_schwab_client, sch_limiter
from axiom.schwab_models_account import Account, AccountNumberHash, Transaction
from axiom.store.cache import account_info_cache

# Hardcode the account idx to only support one account for now
ACCOUNT_IDX = 0

# Cache the account number hash as it doesn't change
account_number_hash: AccountNumberHash | None = None


async def get_account_hash() -> AccountNumberHash:
    """Get the account hash for the user."""
    global account_number_hash

    if account_number_hash is None:
        sch = get_schwab_client()

        async with sch_limiter:
            response = await sch.get_account_numbers()
            account_info = response.json()[ACCOUNT_IDX]
            account_number_hash = AccountNumberHash.model_validate(account_info)

    return account_number_hash


async def get_account_info() -> Account:
    """Get accounts information for the user."""

    # Check the cache first
    cached_account_data = account_info_cache.get(ACCOUNT_IDX)
    if cached_account_data is not None:
        return cached_account_data

    sch = get_schwab_client()

    async with sch_limiter:
        response = await sch.get_accounts(fields=sch.Account.Fields.POSITIONS)
        account_info = response.json()[ACCOUNT_IDX]
        account_data = Account.model_validate(account_info)

        # Cache the account info for 5 minutes
        account_info_cache.set(ACCOUNT_IDX, account_data, expire=300)

        return account_data


async def get_account_transactions() -> list[Transaction]:
    """Get the transactions for a given account."""
    sch = get_schwab_client()

    async with sch_limiter:
        account_number_hash = await get_account_hash()
        response = await sch.get_transactions(account_number_hash.hashValue)

        # Parse the Transaction objects
        transactions = [Transaction.model_validate(transaction) for transaction in response.json()]
        return transactions

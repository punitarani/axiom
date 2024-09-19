"""axiom/mdata/options.py"""

from schwab.client import Client

from axiom.schwab_client import get_schwab_client, sch_limiter
from axiom.schwab_models import OptionChain


async def get_options_chain(symbol: str) -> OptionChain:
    """Get the options chain for a given symbol."""

    sch = get_schwab_client()

    # Check the cache first
    async with sch_limiter:
        response = await sch.get_option_chain(
            symbol=symbol,
            contract_type=Client.Options.ContractType.ALL,
            strike_count=100,
            include_underlying_quote=True,
            strategy=Client.Options.Strategy.SINGLE,
        )
        data = response.json()

    return OptionChain.model_validate(data)

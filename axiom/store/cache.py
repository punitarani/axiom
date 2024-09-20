"""axiom/store/cache.py"""

import diskcache

from axiom.config import DATA_DIR

CACHE_DIR = DATA_DIR.joinpath("cache")

level_one_cache = diskcache.Cache(directory=CACHE_DIR.joinpath("level_one"))
daily_price_history_cache = diskcache.Cache(directory=CACHE_DIR.joinpath("daily_price_history"))
instrument_cache = diskcache.Cache(directory=CACHE_DIR.joinpath("instrument"))

# Account caches
account_info_cache = diskcache.Cache(directory=CACHE_DIR.joinpath("account_info"))

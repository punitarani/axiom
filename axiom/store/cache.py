"""axiom/store/cache.py"""

import diskcache

from axiom.config import DATA_DIR

level_one_cache = diskcache.Cache(directory=DATA_DIR.joinpath("cache/level_one"))

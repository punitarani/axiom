#! /usr/bin/env python3

from axiom.db.auth import get_schwab_token_from_db

token = get_schwab_token_from_db()
print(token)

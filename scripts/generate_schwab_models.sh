#!/usr/bin/env bash
datamodel-codegen  --input ./data/schwab-market-openapi.json --input-file-type openapi --output ./axiom/schwab_models_market.py --output-model-type pydantic_v2.BaseModel
datamodel-codegen  --input ./data/schwab-account-openapi.json --input-file-type openapi --output ./axiom/schwab_models_account.py --output-model-type pydantic_v2.BaseModel

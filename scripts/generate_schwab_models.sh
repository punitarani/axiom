#!/usr/bin/env bash
datamodel-codegen  --input ./data/schwab-openapi.json --input-file-type openapi --output ./axiom/schwab/models.py --output-model-type pydantic_v2.BaseModel

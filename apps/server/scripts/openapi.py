import json

from axiom.main import app

openapi_schema = app.openapi()

print("Generating OpenAPI schema...")
with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("OpenAPI schema generated successfully")

import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "../server/openapi.json",
  output: {
    path: "src/lib/api",
    format: "prettier",
    lint: "biome",
  },
  plugins: [
    "@hey-api/typescript",
    {
      name: "@hey-api/sdk",
      asClass: false,
    },
  ],
});

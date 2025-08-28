# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Turborepo monorepo with mixed language applications:

- **Root**: Turborepo workspace with Bun as package manager
- **apps/web**: Next.js 15 frontend application with TypeScript, Tailwind CSS, and shadcn/ui components
- **apps/server**: Python FastAPI backend server with poetry/uv dependency management

## Development Commands

### Root-level commands (using Turbo):
```bash
bun dev           # Start development servers for all apps
bun build         # Build all apps
bun lint          # Lint all apps
bun format        # Format all apps
bun typecheck     # Type check all apps
```

### Web app specific (apps/web):
```bash
# Development
bun dev           # Next.js dev server with Turbopack
bun build         # Production build with Turbopack
bun start         # Start production server

# Code quality
bun lint          # Biome linting with auto-fix
bun format        # Biome formatting
```

### Server app specific (apps/server):
```bash
# Development
bun dev           # Run Python server via poetry
# or directly: poetry run python main.py

# Code quality
bun lint          # Ruff linting with auto-fix
bun format        # Ruff formatting
# or directly: poetry run ruff check --fix . && poetry run ruff format .
```

## Architecture Overview

### Web Application
- **Framework**: Next.js 15 with React 19 and Turbopack
- **Styling**: Tailwind CSS v4 with shadcn/ui component library
- **UI Components**: Comprehensive Radix UI primitive library in `src/components/ui/`
- **Type Safety**: Full TypeScript with strict configuration
- **Linting**: Biome for linting and formatting (excludes generated UI components)

### Server Application
- **Framework**: FastAPI with WebSocket support
- **Dependencies**: schwab-py for trading functionality
- **Python Version**: Requires Python 3.13+
- **Dependency Management**: Uses uv/poetry hybrid approach
- **Code Quality**: Ruff for linting and formatting with 88-character line length

### Turborepo Configuration
- **Task Dependencies**: Build and format tasks have proper dependency chains
- **Dev Mode**: Persistent development servers with no caching
- **Workspace**: Configured for apps/* and packages/* (though packages/ not currently used)

## Important Notes

- **Package Manager**: This project uses Bun (v1.2.18) as specified in package.json
- **Node Version**: Requires Node.js 18+
- **UI Components**: The `src/components/ui/` directory contains generated shadcn/ui components and is excluded from Biome linting
- **Python Environment**: Server requires Python 3.13+ and uses FastAPI with WebSocket capabilities
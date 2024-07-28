# Makefile

# List of directories and files to format and lint
TARGETS = axiom/ notebooks/ server/ tests/

# Format code using isort and black
format:
	poetry run isort $(TARGETS)
	poetry run black $(TARGETS)

# Lint code using ruff
lint:
	poetry run ruff check $(TARGETS)

# Build the Docker image
build:
	DOCKER_BUILDKIT=1 docker buildx build --platform linux/amd64 -t punitarani/axiom --push .

# Display help message by default
.DEFAULT_GOAL := help
help:
	@echo "Available commands:"
	@echo "  make format      - Format code using isort and black"
	@echo "  make lint        - Lint code using ruff"
	@echo "  make build       - Build the Docker image"

# Declare the targets as phony
.PHONY: format lint build help

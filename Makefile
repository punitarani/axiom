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

# Display help message by default
.DEFAULT_GOAL := help
help:
	@echo "Available commands:"
	@echo "  make format      - Format code using isort and black"
	@echo "  make lint        - Lint code using ruff"

# Declare the targets as phony
.PHONY: format lint help

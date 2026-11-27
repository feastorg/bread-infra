# bread-infra task runner

set dotenv-load := false

# Default: show available recipes
default:
    @just --list

# Install the locked dependencies into .venv
setup:
    uv sync --locked

# Format code (mutates working tree — use locally)
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Verify formatting (non-mutating — use in CI)
fmt-check:
    uv run ruff format --check .

# Run linters
lint:
    uv run ruff check .

# Type-check
typecheck:
    uv run pyright

# Format + lint + type-check (non-mutating — safe for CI)
check: fmt-check lint typecheck

# Run tests
test:
    uv run python -m unittest discover tests

# Remove local environment and caches
clean:
    rm -rf .venv .ruff_cache .mypy_cache
    find . -type d -name __pycache__ -prune -exec rm -rf {} +

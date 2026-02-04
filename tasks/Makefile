.PHONY: all test run lint

### Default target(s)
all: run

### Perform static analysis
lint:
	uv run ruff check --select I --fix .
	uv run ruff format .
	uv run ruff check . --fix
	uv run ty check .

### Run the project
run: lint
	uv run fab git.ls

### Run unit tests
test: lint
	uv run pytest -s -v

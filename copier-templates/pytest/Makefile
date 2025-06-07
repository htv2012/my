.PHONY: test

### Perform unit tests
test:
	ruff check . --fix
	ruff format .
	pytest -s -vv

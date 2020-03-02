
.PHONY: init test test-cov lint format

CODE = pyfractals
TEST = poetry run pytest tests --verbosity=2 --showlocals --strict --cov=$(CODE)
TEST_FULL = poetry run pytest tests regression --verbosity=2 --showlocals --strict --cov=$(CODE)

init:
	poetry install
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(TEST) -k "$(k)"

test-cov:
	$(TEST_FULL) --cov-report=html

lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE) tests
	poetry run pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE) tests
	poetry run black --check $(CODE) tests

format:
	poetry run black $(CODE) tests

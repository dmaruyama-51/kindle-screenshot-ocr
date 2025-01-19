.PHONY: lint format

format:
	poetry run ruff format .

lint:
	poetry run ruff check . --fix

all: format lint 
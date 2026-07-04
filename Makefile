.PHONY: check lint test validate-examples converter-test

check: lint test validate-examples converter-test

lint:
	cd contracts/tools && uv run --with ruff ruff check .

test:
	cd contracts/tools && uv run --with pytest --with pytest-cov pytest --cov=pic_contracts --cov-report=term-missing

validate-examples:
	cd contracts/tools && uv run python -m pic_contracts.validate_examples ../../contracts

converter-test:
	uv run --directory converters/fixtures --with pytest --with pytest-cov pytest --cov=pic_fixture_converters --cov-report=term-missing

.PHONY: check audit audit-test paper-artifacts paper-artifacts-write lint test validate-examples converter-lint converter-test corpus-report-check harness-lint harness-test snap-runner-lint snap-runner-test nz-recon-lint nz-recon-test service-boundaries-lint service-boundaries-test docassemble-oia-clock-lint docassemble-oia-clock-test

check: audit audit-test paper-artifacts lint test validate-examples converter-lint converter-test corpus-report-check harness-lint harness-test snap-runner-lint snap-runner-test nz-recon-lint nz-recon-test service-boundaries-lint service-boundaries-test docassemble-oia-clock-lint docassemble-oia-clock-test

audit:
	PYTHONPATH=. uv run python -m tools.repo_audit

audit-test:
	PYTHONPATH=. uv run --with pytest --with pyyaml pytest tools/tests

paper-artifacts:
	PYTHONPATH=. uv run python -m tools.paper_artifacts --check

paper-artifacts-write:
	PYTHONPATH=. uv run python -m tools.paper_artifacts --write

lint:
	cd contracts/tools && uv run --with ruff ruff check .

test:
	cd contracts/tools && uv run --with pytest --with pytest-cov pytest --cov=pic_contracts --cov-report=term-missing

validate-examples:
	cd contracts/tools && uv run python -m pic_contracts.validate_examples ../../contracts

converter-lint:
	uv run --directory converters/fixtures --with ruff ruff check .

converter-test:
	uv run --directory converters/fixtures --with pytest --with pytest-cov pytest --cov=pic_fixture_converters --cov-report=term-missing

corpus-report-check:
	PYTHONPATH=converters/fixtures/src uv run --with PyYAML python -m pic_fixture_converters.corpus_report --check

harness-lint:
	PYTHONPATH=harness:contracts/tools/src uv run --with ruff ruff check harness

harness-test:
	PYTHONPATH=harness:contracts/tools/src uv run --with pytest --with jsonschema pytest harness/tests

snap-runner-lint:
	PYTHONPATH=studies/snap-divergence/runner/src:harness:contracts/tools/src uv run --with ruff ruff check studies/snap-divergence/runner/src studies/snap-divergence/runner/tests

snap-runner-test:
	PYTHONPATH=studies/snap-divergence/runner/src:harness:contracts/tools/src uv run --with pytest --with jsonschema pytest studies/snap-divergence/runner/tests

nz-recon-lint:
	PYTHONPATH=studies/nz-reconciliation/runner/src uv run --with ruff ruff check studies/nz-reconciliation/runner/src studies/nz-reconciliation/runner/tests

nz-recon-test:
	PYTHONPATH=studies/nz-reconciliation/runner/src uv run --with pytest --with pyyaml pytest studies/nz-reconciliation/runner/tests

service-boundaries-lint:
	PYTHONPATH=demos/service-boundaries/src:external/foi-o/src uv run --with ruff ruff check demos/service-boundaries/src demos/service-boundaries/tests

service-boundaries-test:
	PYTHONPATH=demos/service-boundaries/src:external/foi-o/src uv run --with pytest --with jsonschema pytest demos/service-boundaries/tests

docassemble-oia-clock-lint:
	PYTHONPATH=demos/docassemble-oia-clock/src:demos/service-boundaries/src:external/foi-o/src uv run --with ruff ruff check demos/docassemble-oia-clock/src demos/docassemble-oia-clock/tests

docassemble-oia-clock-test:
	PYTHONPATH=demos/docassemble-oia-clock/src:demos/service-boundaries/src:external/foi-o/src uv run --with pytest pytest demos/docassemble-oia-clock/tests

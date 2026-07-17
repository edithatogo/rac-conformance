.PHONY: check audit audit-test release-gates-check paper-artifacts paper-artifacts-write lint test validate-examples converter-lint converter-test corpus-report-check harness-lint harness-test snap-runner-lint snap-runner-test nz-recon-lint nz-recon-test service-boundaries-lint service-boundaries-test docassemble-oia-clock-lint docassemble-oia-clock-test v1-baseline v1-fuzz v1-mutation v1-reproducibility v1-rollback

AS_OF ?= $(shell date -u +%Y-%m-%d)

check: audit audit-test release-gates-check paper-artifacts lint test validate-examples converter-lint converter-test corpus-report-check harness-lint harness-test snap-runner-lint snap-runner-test nz-recon-lint nz-recon-test service-boundaries-lint service-boundaries-test docassemble-oia-clock-lint docassemble-oia-clock-test

audit:
	PYTHONPATH=. uv run python -m tools.repo_audit

audit-test:
	PYTHONPATH=. uv run --with pytest --with pyyaml --with jsonschema pytest tools/tests

release-gates-check:
	PYTHONPATH=. uv run python -m tools.release_gates conductor/v1-release-gates.json --as-of $(AS_OF)

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

v1-baseline:
	PYTHONPATH=contracts/tools/src uv run --with jsonschema python tools/v1_baseline.py --output docs/V1_VALIDATION_BASELINE.json

v1-fuzz:
	PYTHONPATH=contracts/tools/src uv run --with jsonschema python tools/v1_fuzz.py --output docs/V1_FUZZ_BASELINE.json

v1-mutation:
	PYTHONPATH=contracts/tools/src uv run --with jsonschema python tools/v1_mutation.py --output docs/V1_MUTATION_GATE.json

v1-reproducibility:
	uv run python tools/v1_reproducibility.py --output docs/V1_REPRODUCIBILITY.json

v1-rollback:
	PYTHONPATH=tools uv run python tools/v1_rollback_rehearsal.py --output docs/V1_ROLLBACK_REHEARSAL.json

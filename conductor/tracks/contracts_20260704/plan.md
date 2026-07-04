# Plan: contracts_20260704 — Policy Interchange Contracts v0.1

Read `spec.md` first. Follow `conductor/workflow.md` (TDD, one commit per task, `[HUMAN]` tasks are prepared-then-stopped).

## Phase 1 — Scaffolding and pic-semantics

> CHECKPOINT (2026-07-05): Phase 1 scaffold is installed under `contracts/tools` as `pic_contracts`, with root `make check` running lint, tests, and placeholder example validation. `pic-semantics/0.1.0` now has normative value-state/epistemic-status prose, reusable `$defs`, two valid examples, three invalid examples, and schema tests asserting intended rejection reasons. Validation passed with `PATH=$PWD/.venv/bin:$PATH make check`. Direct system `pip install -e contracts/tools` is blocked by this machine's externally managed Python; editable install was verified in repo-local `.venv`.

- [x] Task: Scaffold `contracts/` package
    - [x] Create `contracts/README.md` (one-page overview: the five contracts, ground rules from spec §Ground rules, links)
    - [x] Create `contracts/CONSUMERS.md` (table: contract, version, consumer, status; seed with foi-o/Track 2 as "intended")
    - [x] Create root `pyproject.toml` for package `pic_contracts` (src layout: `contracts/tools/src/pic_contracts/`), pytest + ruff config, `jsonschema` and `pyyaml` deps
    - [x] Create `Makefile` with `check: lint test validate-examples` targets (validate-examples may be a placeholder script until tools exist)
    - **Acceptance:** `pip install -e contracts/tools` succeeds; `make check` runs (may trivially pass)
- [x] Task: Write `pic-semantics` 0.1.0
    - [x] Write `contracts/pic-semantics/0.1.0/SPEC.md`: valueState enum + definitions, epistemicStatus enum, the propagation decision table for and/or/not/comparison/arithmetic/if per spec C1, data types, rounding declaration. Include a worked example table showing `unknown AND false = false`, `unknown + 5 = unknown`, `verified_stale < threshold = unknown-with-warning`
    - [x] Write `schema.json` exposing `$defs`: `valueState`, `epistemicStatus`, `dataType`, `rounding`, `valueObject` (`{value?, valueState, epistemicStatus?, currency?}`)
    - [x] Write tests: 2 valid + 3 invalid example JSON files instantiating `valueObject`; test that schema accepts/rejects correctly
    - **Acceptance:** pytest green; invalid examples each fail for the intended reason (assert on error path/message)
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — pic-crosswalk and pic-parameters

> CHECKPOINT (2026-07-05): Phase 2 added `pic-crosswalk/0.1.0` with row-set header, mapping methods, kind constraints, two valid examples, and invalid coverage for bad IDs, kinds, methods, and mappings without systems. `pic-parameters/0.1.0` now supports integer, boolean, string, decimal-string, and bracket schedule values, plus Python period validation for ordering/open-ended/overlap rules. Conductor review fixed decimal-string acceptance in the parameter schema. Validation passed with `PATH=$PWD/.venv/bin:$PATH make check`.

- [x] Task: Write `pic-crosswalk` 0.1.0
    - [x] Write tests first: valid row set; invalid: bad ID pattern, unknown `kind`, unknown `method`, mapping without `system`
    - [x] `SPEC.md` + `schema.json` per spec C2 (row array file with header block `{conformsTo, jurisdictionScope, provenance}`)
    - [x] Valid examples: one 3-row `us-snap` sample (mark all mappings `ai-proposed`), one 3-row `nz-oia` sample
    - **Acceptance:** pytest green; examples validate via schema in CI test
- [x] Task: Write `pic-parameters` 0.1.0
    - [x] Write tests first: overlapping periods rejected; unordered periods rejected; float value rejected; bracket schedule accepted; open-ended `to: null` accepted
    - [x] `SPEC.md` + `schema.json` per spec C3, importing `$defs` from pic-semantics
    - [x] Valid examples: a simple threshold parameter with two historical periods + sourceRefs; a bracketed schedule parameter
    - [x] Implement period-consistency validation in Python (schema can't express non-overlap): function `validate_parameter_periods(doc) -> list[Error]`
    - **Acceptance:** pytest green incl. period-logic unit tests
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — pic-fixtures and pic-traces

> CHECKPOINT (2026-07-05): Phase 3 added `pic-fixtures/0.1.0` with file-level provenance, value-state-aware inputs, expected tolerances, two valid examples, and invalid coverage for float money, missing curator, and bad tolerance. `pic-traces/0.1.0` now covers scalar case-level traces, vectorized-engine deferral, step kind constraints, three invalid examples, and `trace_equivalence` output/path/semantic levels. Validation passed with `PATH=$PWD/.venv/bin:$PATH make check`. Conductor review found no further fixes.

- [x] Task: Write `pic-fixtures` 0.1.0
    - [x] Write tests first: case with float money rejected; case missing `provenance.curator` rejected; `valueState`-only input (no value) accepted for `not_provided`; tolerance parsing
    - [x] `SPEC.md` + `schema.json` per spec C4
    - [x] Valid examples: 2 fixture files (one plain, one exercising `not_provided` and `verified_stale` inputs)
    - **Acceptance:** pytest green
- [x] Task: Write `pic-traces` 0.1.0
    - [x] Write tests first: step with unknown `kind` rejected; trace without `conformsTo` rejected; equivalence functions (see next) unit-tested with equal/output-only-equal/path-different trace pairs
    - [x] `SPEC.md` + `schema.json` per spec C5, including the normative "Vectorized engines" deferral section and the three equivalence levels
    - [x] Implement `trace_equivalence(a, b) -> {output: bool, path: bool, semantic: bool, diffs: [...]}` in `pic_contracts.traces`
    - **Acceptance:** pytest green; equivalence function returns correct levels on constructed pairs
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4 — Reference tooling

> CHECKPOINT (2026-07-05): Phase 4 replaced the scaffold placeholders with `pic-validate`, directory referential-integrity checks, `pic-diff`, a valid/invalid example-corpus gate, and GitHub Actions CI. Required integrity failures are tested: unknown fixture ID, unknown trace parameter, and crosswalk/fixture type mismatch. Local validation passed with `PATH=$PWD/.venv/bin:$PATH make check`, including coverage >=80% (observed 88.55%) and example corpus validation. Workflow YAML parsed locally; no `actionlint`/`yamllint` binary was installed.

- [x] Task: Implement `pic-validate`
    - [x] Tests first: detects each contract type; validates valid/invalid corpus; directory mode runs referential-integrity checks and catches the three cases in spec §Acceptance 3
    - [x] Implement type detection (`conformsTo` field, fallback sniffing), schema validation, and cross-file integrity checks (fixture input IDs ∈ crosswalk; trace parameterVersions ∈ parameters; dataType consistency)
    - [x] CLI entry point `pic-validate` (argparse; exit 1 on failure; human-readable + `--json` output)
    - **Acceptance:** `pic-validate contracts/examples/nz-oia-clocks/` exits 0 once Phase 5 exists; unit tests green meanwhile on synthetic dirs
- [x] Task: Implement `pic-diff`
    - [x] Tests first: value change, new period, removed parameter, unchanged — all reported correctly
    - [x] Implement Markdown + JSON diff output
    - **Acceptance:** pytest green; sample diff committed under `contracts/examples/diffs/`
- [x] Task: Wire CI
    - [x] GitHub Actions workflow: ruff, pytest with coverage gate ≥80% on tools, `pic-validate` over all `examples/valid` (expect pass) and `examples/invalid` (expect fail)
    - [x] Make `make check` run the same gate locally
    - **Acceptance:** workflow file lints (yamllint or actionlint if available); `make check` green locally
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5 — Worked example: nz-oia-clocks

- [x] Task: Build `contracts/examples/nz-oia-clocks/`
    - [x] Draft crosswalk (3 rows), parameters (2: 20-working-day limit with source ref to OIA 1982 s 15; holiday-calendar reference parameter), 5 fixtures per spec (mark ALL fixtures `method: ai-proposed`), 1 sample trace
    - [x] Validate with `pic-validate` (directory mode)
    - [x] Cross-check consistency with foi-o's working-day semantics: read https://github.com/edithatogo/foi-o README/schemas if network available; if not, add `> BLOCKED` note and proceed — Track 2 will reconcile
    - **Acceptance:** `pic-validate contracts/examples/nz-oia-clocks/` exits 0
- [ ] Task: [HUMAN] Fixture review
    - [ ] Dylan verifies the 5 fixtures against the OIA text/Ombudsman guidance, flips `method` to `human-approved`, fills `interpreterOfRecord`
    > HUMAN-GATE (2026-07-05): Candidate fixtures and `FIXTURE_REVIEW.md` are prepared. Agent must stop here; Dylan must verify dates/interpretation, promote method, and fill interpreter-of-record before release housekeeping or archive.
- [ ] Task: Release housekeeping
    - [ ] CHANGELOGs for all five contracts at 0.1.0; update `contracts/CONSUMERS.md`; update root README repo-map row for `contracts/` from "to be built" to "v0.1"
    - **Acceptance:** `make check` green; `git log` shows one commit per task
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Notes for implementing agents

- Do NOT invent an expression language anywhere in this track. Fixtures test inputs→outputs; how an engine computes is its business.
- Do NOT add `@context`, RDF, SHACL, or any external-standard mapping. That is a deliberate scope decision (views/06 §8), not an oversight.
- If jsonschema draft 2020-12 features are missing in the environment, pin `jsonschema>=4.18`.
- Schema `$id`s use `https://github.com/edithatogo/rulesandprocesses/contracts/<name>/<version>/schema.json` (repo-relative resolution in tools; do not fetch over network).

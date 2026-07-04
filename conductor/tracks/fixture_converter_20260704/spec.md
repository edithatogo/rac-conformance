# Spec: OpenFisca ↔ PolicyEngine test fixture converter

## Purpose

The least political, highest-utility interchange artifact: both ecosystems keep tests as YAML, in similar-but-diverged dialects. A deterministic converter (OpenFisca tests ↔ PIC fixtures ↔ PolicyEngine tests) enables cross-validation and migration in both directions and *proves* pic-fixtures is a normalization of real formats rather than an invention. This is the pitch to maintainers: "your existing tests, portable."

## Format facts to verify first (agents: confirm against current repos, do not trust from memory)

- OpenFisca test YAML: `name`, `period`, `absolute_error_margin`/`relative_error_margin`, `input:`/`output:` maps keyed by variable name, optional entity structure (`persons`, `households`, …), possibly multiple documents per file. Check `openfisca-core` test loader for the authoritative field set.
- PolicyEngine test YAML (policyengine-core lineage): same ancestry, diverged details — check `policyengine-core` `test_...` runner for current field names, entity key conventions, and period handling.
- PIC fixture: `contracts/pic-fixtures/0.1.0/` (Track 1).

## Deliverables

1. `converters/fixtures/` Python package `pic_fixture_converters`:
   - `openfisca_to_pic(path|doc) -> [FixtureFile]`, `pic_to_openfisca(...)`, `policyengine_to_pic(...)`, `pic_to_policyengine(...)`.
   - **Supported-subset manifest** (`SUPPORTED.md`): exactly which constructs convert; everything else is **rejected loudly** (`UnsupportedConstructError` naming the construct and file/line) — never silently dropped. Initial subset: scalar inputs/outputs, single- and multi-entity cases, absolute error margins, periods (year/month/eternity), enum/boolean/decimal values.
   - Variable names pass through unchanged by default; optional `--crosswalk <pic-crosswalk file>` remaps to PIC IDs. Without a crosswalk, generated PIC fixtures carry `"idScheme": "native:openfisca:<country_package>"` — honest about un-mapped identity.
   - Converted fixtures carry provenance `method: mechanical` and cite the source file+commit.
2. Round-trip guarantee: for the supported subset, `openfisca -> pic -> openfisca` and `policyengine -> pic -> policyengine` are canonically equal (after YAML normalization). Cross-engine conversion (`openfisca -> pic -> policyengine`) is only claimed valid when a crosswalk covers all IDs.
3. Corpus tests: vendor a small sample of real test files (≥10 each from an OpenFisca country package and policyengine-us, license-checked, with source commit noted) under `converters/fixtures/corpus/`; CI converts the corpus and reports supported/unsupported statistics.
4. `external/openfisca/SUBMISSION.md` and `external/policyengine/SUBMISSION.md`: draft upstream issue proposing the converter as a maintained tool (or doc link), including the corpus statistics as evidence.

## Acceptance criteria

1. Round-trip tests green on the whole supported subset; ≥3 rejection tests for unsupported constructs.
2. Corpus report: ≥80% of sampled real test files convert cleanly (if below, the honest number is still the deliverable — adjust SUPPORTED.md, don't force conversions).
3. `pic-validate` passes on every converted fixture.
4. Coverage ≥80%.

## Out of scope

Formula/expression conversion (none — fixtures are input/output only); parameter conversion (a natural follow-up, spec it only after this lands); reform/simulation tests; performance work.

## Dependencies

Track 1 phases 1–4. Network access to clone `openfisca-core`, one OpenFisca country package (recommend `openfisca-france` or `openfisca-aotearoa` for the NZ tie-in), `policyengine-core`, `policyengine-us`.

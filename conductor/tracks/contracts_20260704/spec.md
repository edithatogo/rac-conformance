# Spec: Policy Interchange Contracts (PIC) v0.1

## Purpose

Define five small, independent, versioned artifact contracts that let policy rules engines and process pipelines exchange semantics, values, tests, and audit data **without adopting each other's runtime**. These contracts are the "standards within this repo" that all external tracks point back to.

Design authority: `views/06_fable5_independent_review.md` §5, §8, §10; `views/07` §5.

## Ground rules (normative for this track)

1. Plain JSON is canonical. YAML accepted at import boundaries only. No `@context` or JSON-LD requirement anywhere in v0.1 (optional overlay may be added in a later minor version).
2. Each contract versions independently (semver). Directory layout: `contracts/<name>/<semver>/` containing `SPEC.md`, `schema.json`, `examples/valid/*.json`, `examples/invalid/*.json`, `CHANGELOG.md`.
3. Money and precise quantities are decimal **strings** (`"40000.00"`), never floats. Dates are ISO 8601 strings. Every date-bearing contract states its timezone/calendar convention field.
4. IDs: lowercase, dot-separated, jurisdiction/package-scoped, pattern `^[a-z0-9_-]+(/[a-z0-9_-]+)*(\.[a-z0-9_]+)+$` refined per contract; e.g. `nz-oia/parameter.working_day_limit`, `us-snap/variable.net_income`. No global registry, no URIs required.
5. **No mapping without a consumer**: the schemas define shapes; they never enumerate external standards.

## The five contracts

### C1 `pic-semantics` (0.1.0) — value-state and typing semantics

The shared vocabulary all other contracts import. Contents:

- **Value states** (merges RaCX missingness taxonomy with foi-o epistemic status). Enum `valueState`:
  `known` | `zero` (explicitly zero, distinct from unknown) | `false` (explicit boolean false) | `unknown` | `not_provided` | `not_applicable` | `provided_unverified` | `verified_stale` | `conflicting`.
  Plus `epistemicStatus`: `observed` | `inferred` | `asserted` | `certified` | `unknown` (foi-o-compatible).
- **Propagation rules** (normative prose + decision table): how each state propagates through `and`, `or`, `not`, comparisons, arithmetic, and conditionals. Default: three-valued-logic style — `unknown AND false = false`, `unknown AND true = unknown`, arithmetic with any non-`known`/`zero` operand yields `unknown`; engines MAY declare stricter behavior in their runner manifest.
- **Data types**: `boolean`, `integer`, `decimal`, `money` (requires `currency`), `string`, `date`, `enum` (requires `allowedValues`), `duration_working_days`, `duration_calendar_days`.
- **Rounding declaration**: `{mode: half_up|half_even|floor|ceil, scale: int}`.
- Deliverable is mostly `SPEC.md` prose + a small `semantics.schema.json` for the reusable `$defs` other schemas `$ref`.

### C2 `pic-crosswalk` (0.1.0) — concept/variable/parameter crosswalk tables

- A crosswalk file maps IDs across systems. Row shape:
  ```json
  {
    "id": "us-snap/variable.net_income",
    "label": "SNAP net monthly income",
    "kind": "variable",
    "dataType": "money",
    "period": "month",
    "mappings": [
      {"system": "policyengine-us", "ref": "snap_net_income", "method": "human-approved", "notes": ""},
      {"system": "atlanta-fed-prd", "ref": "NetIncome.SNAP", "method": "ai-proposed", "notes": "verify countable-income def"}
    ],
    "sourceRefs": ["7 CFR 273.10(e)"],
    "definition": "Gross income minus allowable deductions per 7 CFR 273.9(d)."
  }
  ```
- `method` ∈ `human-approved` | `ai-proposed` | `mechanical` (derived by deterministic tooling). Consumers MUST be able to filter by method.
- `kind` ∈ `concept` | `variable` | `parameter` | `decision` | `evidence` | `process_step`.

### C3 `pic-parameters` (0.1.0) — temporal parameters

- Modeled as a normalization of OpenFisca/PolicyEngine YAML parameter conventions (design constraint: an exporter from either engine must be mechanical).
- Shape: `{id, label, unit|currency, values: [{from, to|null, value, sourceRefs[], instrument?}], calendar: {timezone, convention}, rounding?}`. Values are non-overlapping, ordered; `to: null` = open-ended; supersession is expressed by a new value period, never by mutating an old one.
- MUST support `value` types: decimal-string, integer, boolean, enum string, and **schedule tables** (`{brackets: [{threshold, rate|amount}]}`) since real tax/benefit parameters are bracketed.

### C4 `pic-fixtures` (0.1.0) — engine-neutral test fixtures

- Designed as a normalization of OpenFisca YAML tests and PolicyEngine YAML tests (Track 3 is the proof).
- Case shape:
  ```json
  {
    "caseId": "us-snap/fixture.3person-earned-income-01",
    "description": "...",
    "period": "2026-01",
    "entities": {"household": {...}, "people": [...]},
    "inputs": {"us-snap/variable.gross_income": {"value": "2100.00", "valueState": "known"}},
    "expected": {"us-snap/variable.snap_allotment": {"value": "358.00", "tolerance": "1.00"}},
    "provenance": {"curator": "…", "method": "human", "source": "USDA FNS worked example p.12", "interpreterOfRecord": "…", "disclaimer": "Interpretation, not law."},
    "sourceRefs": ["7 CFR 273.10"]
  }
  ```
- Inputs use `valueState`-aware value objects so fixtures can test missingness behavior — this is the differentiating feature versus both engines' native test formats.
- `tolerance` is a decimal string; omitted means exact.
- Fixture files carry a top-level `provenance` block; per-case blocks override.

### C5 `pic-traces` (0.1.0) — decision traces

- **Scope: scalar/case-level calculations only.** A `## Vectorized engines` section states that batch derivation (per-case re-execution, sampling, computation-tree projection) is explicitly deferred and points at Track 4 for the PolicyEngine computation-tree investigation.
- Trace shape: `{caseId, packageRef: {id, version}, engine: {name, version, adapter?}, timestamp, inputs: {id: valueObject}, outputs: {id: valueObject}, steps: [step], conformsTo: "pic-traces/0.1.0"}`.
- Step shape (constrained, unlike the RaCX skeleton): `{stepId, kind: decision|process|evidence_check|notice, refs: {decision?|processStep?}, inputsUsed: [id], parameterVersions: [{id, effectiveFrom}], result: valueObject, sourceRefs: [string]}`.
- Trace equivalence (normative): two traces are *output-equivalent* (same outputs within tolerance), *path-equivalent* (same ordered `stepId`+`parameterVersions`), or *semantically equivalent* (path-equivalent AND same `sourceRefs` per step). Conformance reports MUST state which level they claim.

## Reference tooling (in `contracts/tools/`)

- `pic-validate <file>`: detects contract type (by `conformsTo` or schema sniffing), validates against schema, then runs **referential-integrity checks** across a directory: fixture input IDs exist in crosswalk; trace parameterVersions exist in parameter files; crosswalk `dataType` matches parameter/fixture usage.
- `pic-diff <paramfileA> <paramfileB>`: temporal parameter diff report (value changes, period changes, missing IDs) in Markdown + JSON.
- Python package name: `pic_contracts`. CLI via `pyproject.toml` entry points. No third-party deps beyond `jsonschema` (+ `pyyaml` for import boundaries).

## Worked example package

`contracts/examples/nz-oia-clocks/` — a miniature real-world package used by Track 2: 3 crosswalk rows (OIA working-day limit, extension, transfer), 2 temporal parameters (20 working days; NZ public holiday calendar reference), 5 fixtures (including one `not_provided` and one `verified_stale` case), 1 sample trace. Values must come from the Official Information Act 1982 ss 15, 15A (verify text; mark fixtures `ai-proposed` until human-approved).

## Acceptance criteria (track-level)

1. All five contracts exist under `contracts/` with SPEC, schema, ≥2 valid and ≥3 invalid examples each, all validated in CI.
2. `pic-validate` passes on the worked example and fails with useful messages on every invalid example (asserted in tests).
3. Referential-integrity checks catch: fixture referencing unknown variable ID; trace referencing unknown parameter; type mismatch between crosswalk and fixture.
4. `pytest` coverage ≥80% on `contracts/tools/`.
5. `make check` runs the whole gate in one command.
6. `contracts/CONSUMERS.md` exists listing foi-o (Track 2) as intended first consumer.

## Out of scope

Expression language of any kind; JSON-LD contexts; process/case modeling beyond the trace `step.kind` enum; DMN/BPMN/XState/JSON Logic exports; simulation/population metadata (revisit only via Track 5 needs).

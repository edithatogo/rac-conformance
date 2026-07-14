# Tech Stack

## This repository

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12+ | Matches OpenFisca, PolicyEngine, and foi-o's control plane; lowest friction for upstream PRs |
| Packaging | `pyproject.toml` + `uv` (fallback: pip) | Matches foi-o conventions |
| Schemas | JSON Schema draft 2020-12 | Already used by RaCX skeleton and foi-o; tooling ubiquitous |
| Validation | `jsonschema` (Draft202012Validator) | Present in skeleton |
| Data wrangling (studies) | `polars` or `pandas`, `pyarrow` | Divergence-study reports |
| Decimal money | `decimal.Decimal` serialized as strings | Contract requirement; never binary floats |
| Tests | `pytest` | Standard |
| Lint/format | `ruff` | Matches foi-o |
| CI | GitHub Actions | Validate contracts, run reference validator on examples, run tests |
| Serialization | Plain JSON (canonical), YAML accepted at import boundaries | OpenFisca/PolicyEngine test/parameter files are YAML |
| JSON-LD | **Optional overlay only** — deferred; no `@context` required by any contract in v0.1 | Review decision (views/06 §5) |
| Optional process adapter | Camunda 8 BPMN + official Camunda Process Test, Java 17+ test module | v1 portability evidence only; exact versions must be pinned by `camunda_portability_20260714`; never a PIC core dependency |

## External surfaces this project writes against

| Target | Stack | Notes for agents |
|---|---|---|
| `edithatogo/foi-o` | Python 3.12 + Mojo/MAX kernels, Pydantic, JSON Schema, SKOS/SHACL, `uv`, `pixi` | Follow its repo conventions exactly; Python fallback semantics are its compatibility contract |
| `PolicyEngine/policyengine-us` (+ `-core`, `-uk`) | Python, vectorized NumPy, YAML parameters/tests | Tests live as YAML; computation tree exists internally; validation vs TAXSIM via `policyengine-taxsim` |
| PolicyEngine **Axiom** | Dylan has direct access; treat as Python | Validation harness target |
| OpenFisca (`openfisca-core`, country packages) | Python, YAML parameters and YAML tests, Web API with `/trace` | Fixture converter target |
| Atlanta Fed Policy Rules Database | **R** + RData parameters | Divergence study requires an R runner (`Rscript`) or a Python re-implementation of their published functions — see Track 5 spec for the decision |
| Alaveteli | Ruby on Rails | Track 6 contributions are data/spec-level (state taxonomies), not Ruby code, unless trivial |
| Camunda 8 | BPMN, optional DMN/FEEL, job workers/connectors, Camunda Process Test | Optional adapter only. Keep substantive deterministic rules behind typed service/worker boundaries and human judgement in user tasks. Do not use token simulation or AI judge assertions as conformance evidence. |

## Environment assumptions for agents

- macOS/Linux shell, `git`, `python3.12+`, `pip`/`uv` available.
- Network access to PyPI and GitHub is required for Tracks 3–5; if absent (e.g. restricted sandbox), do documentation-and-schema tasks only and record the blockage in the track plan.
- R (`Rscript`) needed only for Track 5 phase 2+; absence is a recorded blocker, not an improvisation license.

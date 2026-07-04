# STATUS: design notebook — superseded

**This directory is the RaCX repository skeleton as conceived by ChatGPT (2026-07-04). It is retained as a design notebook and is not the active line of development.**

Superseded by:

- `../views/06_fable5_independent_review.md` — independent review identifying what to keep/drop
- `../views/07_fable5_reassessment_and_pivot.md` — the evidence-first re-scoping
- `../conductor/tracks/` — the active specs and plans

## What was carried forward (and where)

| RaCX element | Disposition | Now lives in |
|---|---|---|
| Missingness taxonomy (8 states) | **Kept — promoted to headline** | Track 1: `contracts/` semantics spec (merged with foi-o's epistemic status) |
| Temporal parameter model | Kept | Track 1: parameters contract |
| Test fixture format | Kept, redesigned as normalization of OpenFisca/PolicyEngine YAML tests | Tracks 1, 3 |
| Trace contract | Kept, with explicit scalar-only scope pending a vectorized story | Tracks 1, 4 |
| Concept IDs / sidecar mappings | Kept as crosswalk tables (Level 0) | Track 1 |
| Source references (AKN URIs) | Kept | Track 1 |
| Typed rule/process bindings | Kept, demonstrated concretely instead of specified abstractly | Track 2 (foi-o OIA module) |
| Adoption ladder | Kept, extended with Level 0 | `../views/07`, Track 4 |
| "No runtime AI decisions", AI governance | Kept | Root `README.md`, `../conductor/workflow.md` |
| JSON-LD canonical lifecycle package | **Deferred** — optional overlay, revisit only after Tracks 1–5 have external adopters | — |
| "Superset" framing and 15-standard mapping tables | **Dropped** — replaced by "no mapping without a consumer" rule | — |
| `racx-expression-v0.1` | **Dropped** — do not invent an expression language; adopt an existing subset if ever needed | — |
| Evidence-confidence model as mandatory core | Deferred to the foi-o demonstration | Track 2 |
| RaCX-Process / RaCX-Case / RaCX-Simulation profiles | Deferred | — |
| DMN/BPMN/XState/JSON Logic/LegalRuleML/SHACL/OWL/CMMN exports | Dropped from scope | — |

## Known defects in this skeleton (do not build on without fixing)

Recorded so no agent mistakes this for a working reference implementation:

1. `racx-expression-v0.1` is referenced but never normatively specified.
2. `src/racx_validator/expression.py`: no `or`, no arithmetic; digit-string `Decimal` coercion via `replace('.','',1).isdigit()` mangles negatives/exponents; KeyError on missing inputs (no missingness semantics despite the spec's taxonomy).
3. `validate.py` validates only the manifest; seven of nine schemas are never loaded; no referential-integrity checks; no negative tests.
4. `trace.schema.json` `steps` is an unconstrained array; no batch/vectorized representation.
5. JSON-LD contexts point at `racx.example.org` and are not published.
6. Example manifest declares five profiles for a three-variable toy.

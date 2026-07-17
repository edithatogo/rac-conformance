# OpenFisca upstream implementation status

**Updated:** 2026-07-17
**Actor:** agent session (edithatogo / fork-based PRs)  
**Scope:** openfisca-core issues #1380 and #1381 only (not openfisca-aotearoa)

## Summary

| Issue | Topic | Status | PR / next step |
| --- | --- | --- | --- |
| [#1380](https://github.com/openfisca/openfisca-core/issues/1380) | Missingness vs zero | **PR opened** | https://github.com/openfisca/openfisca-core/pull/1382 |
| [#1381](https://github.com/openfisca/openfisca-core/issues/1381) | YAML converter | **Waiting on maintainers** (tooling stays external) | Issue comment; no core PR yet |

## #1380 — missingness vs zero

### PR

- **URL:** https://github.com/openfisca/openfisca-core/pull/1382
- **Branch:** `edithatogo:feat/distinguish-missing-input-from-default`
- **Fork:** https://github.com/edithatogo/openfisca-core
- **Local checkout:** `.external-repos/openfisca-core` (tracks `fork` + `upstream`)

### Implementation (minimal, non-breaking)

Calculation semantics are **unchanged**. Callers can now inspect whether a value was user-provided:

| API | Location | Meaning |
| --- | --- | --- |
| `Holder.is_input(period)` | `openfisca_core/holders/holder.py` | `True` if set via `set_input` |
| `Holder.get_value_state(period)` | same | `"explicit"` or `"default"` |
| `Simulation.is_input(name, period)` | `openfisca_core/simulations/simulation.py` | thin wrapper |
| `Simulation.get_value_state(name, period)` | same | thin wrapper |

Tracking details:

- Values recorded only on the `set_input` path (including `set_input_divide_by_period` / `set_input_dispatch_by_period` and custom `variable.set_input` helpers) via a short-lived `_recording_user_input` flag and optional `_set(..., as_input=True)`.
- `put_in_cache` (formula results) does **not** mark input.
- `delete_arrays` clears matching tracked periods (same `period.contains` rule as storage delete).
- Version bump: `44.7.0` → `44.8.0` (minor; new helpers) + `CHANGELOG.md`.

### Tests

Added in `tests/core/test_holders.py`:

1. Omitted salary vs explicit zero: same `calculate` result; different `get_value_state`.
2. Calculated / cached variables are not reported as inputs.
3. Yearly salary input via period casting marks monthly periods as explicit.
4. `delete_arrays` clears input tracking.

Local verification (Python 3.12, `openfisca-country-template`):

```text
pytest tests/core/test_holders.py  →  23 passed
```

### Issue thread

- Comment linking PR: https://github.com/openfisca/openfisca-core/issues/1380#issuecomment-4920657773

### Evidence (pre-existing)

- `external/openfisca/MISSINGNESS_CASES.md`
- `external/openfisca/SUBMISSION_missingness.md`

## #1381 — YAML converter

### Decision for this session

**No openfisca-core PR** for converter code. The issue already frames the preferred first step as an external tool, with a focused PR only if maintainers want docs or in-repo tooling.

### External implementation (already in this monorepo)

| Artifact | Path |
| --- | --- |
| Converter package | `converters/fixtures/src/pic_fixture_converters/` |
| Supported subset | `converters/fixtures/SUPPORTED.md` |
| Format notes | `converters/fixtures/FORMATS.md` |
| Corpus + report | `converters/fixtures/corpus/` |
| Issue draft | `external/openfisca/SUBMISSION.md` |

Corpus (from issue): 10/10 selected openfisca-france YAML files convert under the v0.1 subset.

### Issue thread

- Comment offering docs-only vs in-repo options: https://github.com/openfisca/openfisca-core/issues/1381#issuecomment-4920657868

### Blocker

- **Maintainer preference** between (1) docs pointer only and (2) in-repo tool. Until that, landing converter code or advertising PIC-branded intermediate formats in openfisca-core would be premature.

## Permissions / process notes

- GitHub auth: `edithatogo` with `repo` scope; fork push and upstream PR creation succeeded.
- OpenFisca Aotearoa was **not** modified (separate track).
- Prior local commits on `.external-repos/openfisca-core` master (conductor scaffolding + incomplete `_set`-based input tracking) were **not** pushed; the PR is a clean branch from `upstream/master` with a corrected implementation (cache no longer marked as input).

## Blockers / follow-ups

1. **#1380:** Awaiting OpenFisca review / CI on PR #1382. Possible review feedback on API naming (`get_value_state` vs alternatives) or docs site coverage.
2. **#1381:** Awaiting maintainer direction; then open a docs PR or tooling PR accordingly.
3. Optional: mirror the same provenance API idea for PolicyEngine if not already covered by that track.

## Independent-validation outreach

On 2026-07-17, following explicit human authorization, the RaC Conformance
project posted one bounded validation request on OpenFisca issue #1380:

https://github.com/openfisca/openfisca-core/issues/1380#issuecomment-4998515274

The request is limited to a maintainer-selected missingness case or read-only
trace projection. It does not request PIC adoption, a code merge, or a change
to OpenFisca calculation semantics. The response window is 14 days with at
most one follow-up. Silence will be recorded as `unresponsive` and will not
count toward v1 independent adoption.

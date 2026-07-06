# Axiom RuleSpec NZ Coverage Plan

Status: Phase 1 candidate audit, 2026-07-06.

This plan selects source-backed RuleSpec NZ slices for the Axiom validation expansion. The goal is to prefer modules with companion tests, clear official source anchors, and non-trivial output behavior. Anything without source support remains smoke-only or deferred.

## Selected slices

| Rank | RuleSpec NZ module(s) | Why selected | Companion evidence | Source assertions |
|---|---|---|---|---|
| 1 | `nz/statutes/kiwisaver/contributions.yaml` | Clean official-source path, explicit rate progression, contribution caps, and deterministic numeric outputs that exercise the harness without relying on policyengine-only oracles. | `tests/test_kiwisaver_contributions.py`; `nz/statutes/kiwisaver/contributions.test.yaml` | KiwiSaver Act 2006 ss 64, 101B, and schedule 1; Taxation (Budget Measures) Act 2025; IRD KiwiSaver contribution guidance. |
| 2 | `nz/statutes/new_zealand_superannuation/core.yaml` and `nz/statutes/new_zealand_superannuation/special_rates.yaml` | Official-source module pair with age thresholds, residence tests, and rate outputs that are deterministic enough for adapter and trace validation. | `tests/test_nz_superannuation_manifest.py`; `nz/statutes/new_zealand_superannuation/core.test.yaml` | New Zealand Superannuation and Retirement Income Act 2001; MSD NZ Super rates. |

## Reserve slice

| Module(s) | Why reserve only for now | Companion evidence | Source assertions |
|---|---|---|---|
| `nz/statutes/social_security/main_benefits/entitlement.yaml` and `nz/statutes/social_security/main_benefits/rates.yaml` | Source-backed and useful, but broader than the first two slices and better kept as a follow-on slice after the smaller rate/rate-cap cases are wired. | `tests/test_social_security_main_benefits_manifest.py`; `nz/statutes/social_security/main_benefits/entitlement.test.yaml`; `nz/statutes/social_security/main_benefits/rates.test.yaml` | Social Security Act 2018; Social Security Regulations 2018; MSD Jobseeker Support rates. |

## Rejected for this phase

| Module(s) | Reason not selected |
|---|---|
| `nz/statutes/gst/rate.yaml` | Already covered by the existing smoke fixture set; not an expansion candidate for this phase. |
| `nz/regulations/acc/earners_levy.yaml` | Already covered by the existing smoke fixture set; not an expansion candidate for this phase. |
| `nz/statutes/income_tax/schedule_1/individual_income_tax.yaml` | Already covered by the existing smoke fixture set; not an expansion candidate for this phase. |
| `nz/statutes/social_security/*` deferred surfaces such as `student_allowance`, `citizenship_and_immigration`, `rates_rebates`, `parental_leave`, and `housing_restructuring_and_social_housing` | The source-map and manifest evidence mark these as deferred or missing; they do not yet have the same companion-test confidence as the selected slices. |

## Source support matrix

| Slice | Disposition | Support status |
|---|---|---|
| Existing smoke slices: `nz/statutes/gst/rate.yaml`, `nz/regulations/acc/earners_levy.yaml`, `nz/statutes/income_tax/schedule_1/individual_income_tax.yaml` | Smoke-only baseline | Keep as deterministic smoke comparisons, not validation goldens. |
| Selected KiwiSaver and NZ Superannuation slices | Validation candidates | Source-backed through primary acts plus companion tests. |
| Reserve social-security slice | Follow-on candidate | Source-backed, but broader than the first validation pass. |
| Deferred social-security surfaces | Not selected | Missing or incomplete source/support confidence; remain out of validation scope. |

## Source Assertion Rules

- A slice is eligible only when there is an official source route or a companion test corpus that can be cited deterministically.
- A slice with no source-backed companion evidence remains smoke-only and must not be promoted into the validation set.
- PolicyEngine/OpenFisca oracle material is supporting evidence only; it is never treated as canonical law.
- Selection should preserve oracle independence and keep `canonical_law: false` wherever the oracle is used as a comparison source rather than the legal source of truth.

## Next Step

Implement the adapter tests and fixtures only for the selected slices in the next phase, then keep the reserve slice available if the first two cases validate cleanly.

## Handoff status

This plan is staged under `external/axiom/` so it can be copied into a submission packet when the Axiom track reaches its human review gate. The companion `SUBMISSION.md` captures the target repo, scope, and current upstream boundary.

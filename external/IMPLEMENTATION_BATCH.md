# Upstream implementation batch (2026-07-09)

Prioritized blockers and proposals implemented as fork PRs / compile fixes.

## Priority 1 — Blocker: rulespec-nz KiwiSaver compile

| Item | URL |
|---|---|
| Issue | https://github.com/TheAxiomFoundation/rulespec-nz/issues/79 |
| PR | https://github.com/TheAxiomFoundation/rulespec-nz/pull/80 |
| Local compile | Verified with axiom-rules-engine (3 derived outputs) |
| Remaining | CI `guard-generated` requires signed `.axiom/encoding-manifests` (maintainer key) |

## Priority 2 — openfisca-aotearoa coverage

| Item | URL |
|---|---|
| Issue | https://github.com/BetterRules/openfisca-aotearoa/issues/199 |
| PR | https://github.com/BetterRules/openfisca-aotearoa/pull/200 |
| Content | 2025–2026 tax brackets, schedule tax before credits, ACC earners levy, KiwiSaver min rates + tests |

## PolicyEngine

| Issue | PR |
|---|---|
| #512 trace | https://github.com/PolicyEngine/policyengine-core/pull/515 |
| #513 missingness | https://github.com/PolicyEngine/policyengine-core/pull/516 |
| #514 YAML docs | https://github.com/PolicyEngine/policyengine-core/pull/517 |

## OpenFisca core

| Issue | PR |
|---|---|
| #1380 missingness | https://github.com/openfisca/openfisca-core/pull/1382 |
| #1381 YAML converter | External tool only (issue comment) |

## Already merged

- foi-o OIA rules: https://github.com/edithatogo/foi-o/pull/20

## Alaveteli

| Item | URL |
|---|---|
| Issue | https://github.com/mysociety/alaveteli/issues/9355 |
| PR | https://github.com/mysociety/alaveteli/pull/9356 |
| Content | Docs + process_clock_metadata theme hook + state roles |


## Live dual-engine re-run (2026-07-09)

Local suite (`python -m nz_reconciliation.run_live_suite` on Python 3.11 + OF PR branch):

- **10/17 numeric agreements** (all schedule income tax; standard ACC earners levy; standard KiwiSaver min contributions)
- Remaining gaps: self-employed ACC / weekly purchase / invoice exempt; Crown KS parameter case
- OF PR #200 follow-up: clamp KiwiSaver base at zero (negative earnings)

Evidence: `studies/nz-reconciliation/results/LIVE_DUAL_ENGINE_REPORT.md`

# openfisca-aotearoa implementation status — NZ reconciliation coverage

**Date:** 2026-07-09  
**Upstream issue:** https://github.com/BetterRules/openfisca-aotearoa/issues/199  
**Pull request:** https://github.com/BetterRules/openfisca-aotearoa/pull/200  
**Head fork/branch:** `edithatogo/openfisca-aotearoa-br` @ `feat/199-income-tax-acc-kiwisaver`  
**Local checkout:** `.external-repos/openfisca-aotearoa` (tracks BetterRules via ServiceInnovationLab redirect)

## Goal

Close the engine coverage gap that blocked numeric NZ reconciliation between RuleSpec and openfisca-aotearoa for:

1. Schedule individual income tax (before credits) for current tax years  
2. ACC earners' levy (standard employee)  
3. KiwiSaver minimum contribution rates (optional thin surface)

## Implemented in PR #200

### Income tax

| Item | Detail |
|---|---|
| Parameter | `parameters/taxes/income_tax/individual_income_tax_rate.yaml` |
| Instants | 2021-04-01 (39% top rate); 2024-04-01 (transitional IRD bands); 2025-04-01+ (current brackets) |
| Variables | `income_tax__schedule_1_tax_before_credits`, alias `income_tax__income_tax_before_credits` |
| Formula | Marginal scale on `income_tax__taxable_income`; non-positive → 0 |
| Tests | `tests/income_tax/schedule_1_tax_before_credits.yaml` |

2026 expected (IRD from 1 Apr 2025): $15,600 → $1,638; $53,500 → $8,270.50; $180,000 → $49,277.50; $200,000 → $57,077.50.

### ACC earners' levy

| Item | Detail |
|---|---|
| Parameters | `parameters/acc/earners_levy/{rate_including_gst,maximum_earnings,maximum_levy_payable}.yaml` |
| 2026-04 rates | 1.75% including GST; max earnings $156,641; max levy $2,741.22 |
| Variables | `acc__earnings_for_earners_levy` (input), `acc__earners_levy_including_gst`, alias `acc__earners_levy` |
| Formula | `rate × min(max(earnings, 0), maximum_earnings)` |
| Tests | `tests/acc/earners_levy.yaml` |
| Out of scope | Self-employed minimum earnings formula; work account / industry levies |

Sources (verified online 2026-07-09):  
https://www.ird.govt.nz/income-tax/income-tax-for-individuals/acc-clients-and-carers/acc-earners-levy-rates

### KiwiSaver

| Item | Detail |
|---|---|
| Parameters | `parameters/kiwisaver/{employee,employer}_minimum_contribution_rate.yaml` |
| Rates | 3% from 2013-04-01; **3.5% from 2026-04-01**; 4% from 2028-04-01 |
| Variables | `kiwisaver__gross_salary_or_wages`, `kiwisaver__employee_minimum_contribution`, `kiwisaver__employer_minimum_contribution` |
| Tests | `tests/kiwisaver/minimum_contributions.yaml` |
| Out of scope | Eligibility, holidays, ESCT, Crown contribution, opted-up rates |

Sources (verified online 2026-07-09):  
https://www.ird.govt.nz/kiwisaver-changes

### Period convention

`YEAR` formulas resolve parameters at **1 April** of the calendar year of `period.start` (`period.start.offset(3, "month")`), matching NZ tax/levy years when simulations use calendar-year periods (e.g. `period: 2026` → `2026-04-01`).

## Test results

Environment: **Python 3.11.15**, `openfisca-core==41.5.7` (package pin `>=41.4.5,<42`), editable install of country package.

```text
openfisca test --country-package openfisca_aotearoa \
  openfisca_aotearoa/tests/income_tax/schedule_1_tax_before_credits.yaml \
  openfisca_aotearoa/tests/acc/earners_levy.yaml \
  openfisca_aotearoa/tests/kiwisaver/minimum_contributions.yaml \
  openfisca_aotearoa/tests/individual_income_tax_rate.yaml
# 20 passed

openfisca test --country-package openfisca_aotearoa openfisca_aotearoa/tests
# 326 passed, 1 error (pre-existing test_api.py: openfisca serve binary path in this env)
```

## Dependency / runtime blockers (unchanged by this PR)

| Constraint | Status |
|---|---|
| `openfisca-core` 41.x + pendulum 2.x on modern Python (3.13/3.14) | Build/install failure — use Python 3.11 for this package pin |
| `openfisca-core` 44.x + country package | Previously observed metaclass conflict; not required for these features |
| Core version bump | **Not** included; not necessary for tax/levy/KiwiSaver parameters |

## Verification policy

- Statute/rate values read from IRD public pages and legislation.govt.nz links recorded in parameter `metadata.reference` / variable `reference`.  
- No invented statute text.  
- No runtime AI decisions.  
- Self-employed ACC and full KiwiSaver machinery intentionally not invented beyond published minimum rates.

## Next steps

1. Maintainer review of PR #200.  
2. After merge: re-run `studies/nz-reconciliation` Phase 2 against updated package for numeric comparison on income tax + ACC standard levy cases.  
3. Optional follow-ups (separate issues): self-employed ACC minimum levy; KiwiSaver Crown/ESCT; mid-year prorating documentation.

## Files touched (PR)

- `openfisca_aotearoa/parameters/taxes/income_tax/individual_income_tax_rate.yaml`
- `openfisca_aotearoa/parameters/acc/earners_levy/*.yaml`
- `openfisca_aotearoa/parameters/kiwisaver/*.yaml`
- `openfisca_aotearoa/variables/acts/income_tax/individual.py`
- `openfisca_aotearoa/variables/acts/acc/earners_levy.py`
- `openfisca_aotearoa/variables/acts/kiwisaver/contributions.py`
- `openfisca_aotearoa/tests/income_tax/schedule_1_tax_before_credits.yaml`
- `openfisca_aotearoa/tests/acc/earners_levy.yaml`
- `openfisca_aotearoa/tests/kiwisaver/minimum_contributions.yaml`
- `CHANGELOG.md` (Unreleased section)

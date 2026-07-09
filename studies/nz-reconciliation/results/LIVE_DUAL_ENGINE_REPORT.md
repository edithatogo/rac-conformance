# NZ reconciliation — live dual-engine report

Cases: **17**
Numeric agreements (≤$0.02): **10**
RuleSpec oracle ok: **17**
OpenFisca live ok: **10**

## Agreements

- `nz-recon/income_tax.first_bracket_upper_bound` (income_tax)
- `nz-recon/income_tax.second_bracket_upper_bound` (income_tax)
- `nz-recon/income_tax.fourth_bracket_upper_bound` (income_tax)
- `nz-recon/income_tax.top_bracket_income` (income_tax)
- `nz-recon/income_tax.nonpositive_taxable_income` (income_tax)
- `nz-recon/acc_earners_levy.standard_2026_earnings_below_cap` (acc_earners_levy)
- `nz-recon/acc_earners_levy.standard_2026_earnings_above_cap` (acc_earners_levy)
- `nz-recon/acc_earners_levy.standard_negative_earnings` (acc_earners_levy)
- `nz-recon/kiwisaver.employee_and_employer_minimum_rates_2026` (kiwisaver)
- `nz-recon/kiwisaver.negative_salary_does_not_create_contributions` (kiwisaver)

## Non-agreements / gaps

- `nz-recon/acc_earners_levy.low_self_employed_minimum_levy_2026`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/acc_earners_levy.low_self_employed_threshold_not_met`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/acc_earners_levy.weekly_compensation_purchase_2026`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/acc_earners_levy.weekly_compensation_purchase_not_made`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/acc_earners_levy.self_employed_invoice_exempt_amount_applies`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/acc_earners_levy.self_employed_invoice_exempt_amount_exceeded`: `engine_gap` (rs=ok, of=engine_gap, diff=None)
- `nz-recon/kiwisaver.government_contribution_cap_from_threshold`: `engine_gap` (rs=ok, of=engine_gap, diff=None)

## Engines

- RuleSpec: companion-test oracles (KiwiSaver compile fixed in local checkout; upstream PR https://github.com/TheAxiomFoundation/rulespec-nz/pull/80).
- OpenFisca Aotearoa: live sim on PR branch https://github.com/BetterRules/openfisca-aotearoa/pull/200 (Python 3.11 + openfisca-core 41.x).

## Evidence

- `results/rulespec-candidate-results.jsonl`
- `results/openfisca-aotearoa-live-results.jsonl`
- `results/comparison-live-results.jsonl`

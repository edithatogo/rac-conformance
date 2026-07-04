# PolicyEngine-US SNAP Reconnaissance

Track: `divergence_study_20260704` phase 1

Date: 2026-07-05

## Source And Version

Repository: `PolicyEngine/policyengine-us`

Local clone path: `.external-repos/policyengine-us`

Pinned commit inspected: `fc64cef64ab55c3c48309c7fb304c35e5f3c9184`

Installed version inspected in the local editable venv:

- `policyengine-us==1.755.5`

Primary permalinks:

- Package version and license classifier: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/pyproject.toml#L1-L13>
- README note on household calculations vs managed microsimulation bundle: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/README.md#L7-L18>
- SNAP final allotment variable: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/snap.py#L4-L35>
- SNAP normal allotment: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/snap_normal_allotment.py#L4-L23>
- SNAP eligibility: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/eligibility/is_snap_eligible.py#L4-L36>
- SNAP categorical eligibility: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/eligibility/meets_snap_categorical_eligibility.py#L4-L17>
- TANF non-cash eligibility used for SNAP BBCE: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/hhs/tanf/non_cash/is_tanf_non_cash_eligible.py#L4-L15>
- TANF non-cash gross income limit by state: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/parameters/gov/hhs/tanf/non_cash/income_limit/gross.yaml#L1-L147>
- TANF non-cash asset limit by state: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/parameters/gov/hhs/tanf/non_cash/asset_limit.yaml#L1-L132>
- SNAP utility allowance choice: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/income/deductions/shelter/snap_utility_allowance_type.py#L4-L39>
- SNAP utility region mapping: <https://github.com/PolicyEngine/policyengine-us/blob/fc64cef64ab55c3c48309c7fb304c35e5f3c9184/policyengine_us/variables/gov/usda/snap/snap_utility_region.py#L4-L203>

## Calculation Entry Points

For household-level study fixtures, use `policyengine_us.Simulation(situation=..., trace=True)` and calculate:

- `snap`: final monthly SNAP amount for an SPM unit.
- `is_snap_eligible`: eligibility boolean.
- Optional trace diagnostics from Track 4's `harness/policyengine_trace` projection.

Relevant variables:

- `snap`: adds `snap_normal_allotment`, `snap_emergency_allotment`, and `dc_snap_temporary_local_benefit`; in dataset simulations it multiplies by take-up, but for household situations it returns the value directly.
- `snap_normal_allotment`: `max(snap_min_allotment, snap_max_allotment - snap_expected_contribution)` and is defined only for eligible units.
- `snap_expected_contribution`: floors `snap_net_income` and multiplies by the expected contribution parameter.
- `snap_max_allotment`: uses SNAP region and `snap_unit_size`.
- `is_snap_eligible`: requires normal income/asset eligibility or categorical eligibility, plus eligible-person, work-requirements, and immigration checks.
- `snap_unit_size`: subtracts ineligible students, immigration-ineligible members, and work-requirement-ineligible members from `spm_unit_size`.

## Parameter And State-Option Surface

SNAP parameter files are under:

- `policyengine_us/parameters/gov/usda/snap/`

Core SNAP parameters for this study:

- `income/limit/gross.yaml`: federal gross-income limit, `1.3` from `2005-01-01`.
- `income/limit/net.yaml`: net-income limit, `1.0` from `2005-01-01`.
- `asset_test/limit.yaml`: standard and elderly/disabled asset limits.
- `asset_test/sources.yaml`: countable liquid assets are `bank_account_assets`, `stock_assets`, and `bond_assets`.
- `categorical_eligibility.yaml`: categorical programs are `ssi`, `is_tanf_non_cash_eligible`, and `tanf`.
- `income/deductions/allowed.yaml`: standard, earned income, dependent care, child support, excess medical, and excess shelter deductions.
- `income/deductions/standard.yaml`: standard deduction by SNAP region and household size.
- `income/deductions/excess_shelter_expense/cap.yaml`: shelter cap by SNAP region.
- `income/deductions/utility/always_standard.yaml`: state list for automatic Standard Utility Allowance.
- `income/deductions/utility/standard/main.yaml`, `limited/main.yaml`, and `single/*`: utility allowance dollar amounts.
- `max_allotment.yaml`, `min_allotment/*`: allotment parameters.

Broad-Based Categorical Eligibility is not encoded as a single SNAP table. It is represented through TANF non-cash eligibility:

- `policyengine_us/variables/gov/hhs/tanf/non_cash/is_tanf_non_cash_eligible.py`
- `policyengine_us/parameters/gov/hhs/tanf/non_cash/income_limit/gross.yaml`
- `policyengine_us/parameters/gov/hhs/tanf/non_cash/asset_limit.yaml`
- `policyengine_us/parameters/gov/hhs/tanf/non_cash/income_limit/net_applies/non_hheod.yaml`
- `policyengine_us/parameters/gov/hhs/tanf/non_cash/income_limit/net_applies/hheod.yaml`

Observed 2026-01-01 candidate-state values from `CountryTaxBenefitSystem().parameters("2026-01-01")`:

| State | TANF non-cash gross limit | TANF non-cash asset limit | Net test applies, non-HHEOD | Net test applies, HHEOD | Always SUA |
|---|---:|---:|---|---|---|
| CA | 2.00 | inf | True | True | True |
| TX | 1.65 | 5000 | False | False | False |
| PA | 2.00 | inf | False | False | True |
| MS | -inf | -inf | False | False | False |
| KS | -inf | -inf | False | False | False |
| GA | 1.30 | inf | False | False | False |

Interpretation:

- `-inf` marks non-BBCE or impossible TANF non-cash eligibility in PolicyEngine's parameterization.
- `inf` marks no TANF non-cash asset cap.
- `CA` is a likely asymmetry state because PolicyEngine applies the TANF non-cash net-income test for both non-HHEOD and HHEOD cases, while PRD carries a `BBCE_State` and SNAP net-test waiver columns separately.
- `PA` is useful because both systems model a Heat-and-Eat/SUA-style surface; PolicyEngine represents always-SUA through `gov.usda.snap.income.deductions.utility.always_standard`.
- `MS` and `KS` are useful non-BBCE states; in PolicyEngine their TANF non-cash gross and asset limits are `-inf`.

## Unit And Period Semantics

PolicyEngine `snap` is a monthly SPM-unit variable. The PRD direct SNAP function returns annual `snapValue`. The comparison runner must normalize PRD annual values by 12 or choose a monthly PRD wrapper if one is later found.

PolicyEngine uses entity structure (`people`, `spm_units`, `tax_units`, `households`) rather than PRD's fixed `agePerson1`...`agePerson12` fields. The crosswalk must therefore define unit composition explicitly and treat PRD fixed slots as an adapter shape, not as the fixture source of truth.

## Known Modeling Asymmetries To Carry Forward

- PolicyEngine gross and net SNAP income limits are federal SNAP parameters; BBCE is mediated through TANF non-cash eligibility. PRD exposes `BBCE_State`, `GrossIncomeEligibilityFPL`, SNAP net-test waiver columns, and asset columns directly in `snapData`.
- PolicyEngine's `snap` includes emergency allotments and DC-specific local supplements as separate added variables. Fixture scope should use post-emergency periods and avoid DC in Phase 1 unless intentionally testing local supplements.
- PolicyEngine has explicit immigration, student, and work-requirement eligibility surfaces in `is_snap_eligible`; PRD's current `function.snapBenefit` surface inspected here does not expose equivalent member-level checks in the same direct way.
- PolicyEngine utility allowance logic distinguishes Standard, Limited, Individual, and None based on utility bills, state always-SUA status, and utility regions. PRD uses `HCSUA`, `HCSUAValue`, `BasicLimitedUtilityAllowance`, and `HeatandEatState`.
- PolicyEngine handles Alaska and New York utility subregions through county mapping. Avoid AK/NY in the first scope unless county-level fixtures are deliberately included.

## Commands Run

```bash
git -C .external-repos/policyengine-us rev-parse HEAD
rg -n "snap|categorical|utility|asset" .external-repos/policyengine-us/policyengine_us/variables/gov/usda/snap .external-repos/policyengine-us/policyengine_us/parameters/gov/usda/snap
. .venv-policyengine/bin/activate
python - <<'PY'
from policyengine_us import CountryTaxBenefitSystem
system = CountryTaxBenefitSystem()
p = system.parameters("2026-01-01")
for state in ["CA", "TX", "PA", "MS", "KS", "GA"]:
    bbce = p.gov.hhs.tanf.non_cash
    snap = p.gov.usda.snap
    print(state, bbce.income_limit.gross[state], bbce.asset_limit[state],
          bbce.income_limit.net_applies.non_hheod[state],
          bbce.income_limit.net_applies.hheod[state],
          snap.income.deductions.utility.always_standard[state])
PY
```

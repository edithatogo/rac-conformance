# Atlanta Fed PRD SNAP Reconnaissance

Track: `divergence_study_20260704` phase 1

Date: 2026-07-05

## Source And Version

Repository: `Research-Division/policy-rules-database`

Local clone path: `.external-repos/policy-rules-database`

Pinned commit inspected: `1d8e8674563a7653ec707d18956faa14b016bc5b`

Primary permalinks:

- README overview and use terms: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/README.md#L1-L19>
- License file: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/LICENSE#L1-L20>
- Citation file: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/CITATION.cff#L1-L8>
- Top-level runner: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/applyBenefitsCalculator.R#L13-L33>
- SNAP function: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/functions/benefits_functions.R#L577-L708>
- Food/housing orchestration: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/functions/BenefitsCalculator_functions.R#L1762-L1871>
- Update schedule for SNAP: <https://github.com/Research-Division/policy-rules-database/blob/1d8e8674563a7653ec707d18956faa14b016bc5b/PRD_Update_Schedule.md#L48-L57>

## License And Citation

The README states that PRD use terms are GNU GPL v3.0 and that alternative licensing arrangements require contacting the listed Atlanta Fed address. The repository includes a GPL-3.0 `LICENSE`.

`CITATION.cff` gives:

- Title: `Policy Rules Database`
- Author: `Federal Reserve Bank of Atlanta`
- URL: `https://github.com/Research-Division/policy-rules-database`
- Version field: `x.x.x`

Use in this study is source inspection and local execution for comparative research. Any derivative PRD wrapper code in this repository must preserve license notices and avoid vendoring PRD source into this repo unless a later license review approves it.

## Runtime Entry Points

The public user path is:

1. Edit a project YAML file under `projects/`.
2. Run `applyBenefitsCalculator.R`.
3. The script loads:
   - `prd_parameters/expenses.rdata`
   - `prd_parameters/benefit.parameters.rdata`
   - `prd_parameters/tables.rdata`
   - `prd_parameters/parameters.defaults.rdata`
4. It sources:
   - `libraries.R`
   - `functions/benefits_functions.R`
   - `functions/expense_functions.R`
   - `functions/BenefitsCalculator_functions.R`
   - `functions/TANF.R`
   - `functions/CCDF.R`
5. It calls `function.createData(inputs)`, then expense/default-benefit blocks, then `BenefitsCalculator.FoodandHousing(...)`.

For the study runner, the narrow SNAP call path should be:

- Load `prd_parameters/benefit.parameters.rdata` to get `snapData`.
- Load `prd_parameters/tables.rdata` to get `table.statemap` and FPL/support tables used by `function.createData` or local input preparation.
- Source `libraries.R`, `functions/benefits_functions.R`, and the minimal upstream functions needed for input construction.
- Prefer calling `function.snapBenefit(data)` directly once the wrapper can construct the expected PRD data frame columns.
- Use `BenefitsCalculator.FoodandHousing(data, APPLY_SNAP=TRUE, ...)` only when the fixture intentionally exercises interaction with housing assistance or food expense caps, because it limits `value.snap` by `exp.food` and applies take-up.

## SNAP Function Details

SNAP is implemented in `functions/benefits_functions.R` as `function.snapBenefit(data)`.

Observed algorithm surface:

- Extends future rule years by copying the latest available `snapData` rows when the input `ruleYear` exceeds the parameter max.
- Joins `data` to `snapData` by `ruleYear`, `stateFIPS`, and `famsize`.
- Computes gross income from earned income, gifts, child support, investment income, TANF, SSI, and SSDI.
- Computes elderly, disabled, and child counts from fixed `agePerson1`...`agePerson12` and `disability1`...`disability12` columns.
- Computes the earned-income deduction as `0.2 * income`.
- Computes utility deductions from `netexp.utilities`, `HeatandEatState`, `HCSUA`, and `HCSUAValue`.
- Computes medical deductions for elderly/disabled members, then adjusted income.
- Computes net income with a shelter cap for households without elderly/disabled members and uncapped excess shelter for households with elderly/disabled members.
- Applies state-specific New York and New Hampshire overrides after loading baseline parameter values.
- Applies categorical eligibility through TANF and all-family SSI receipt.
- Applies gross-income, net-income, and asset-test failures.
- Returns annual `snapValue`, rounded to dollars.

Important orchestration asymmetry:

- `function.snapBenefit(data)` returns an annual value.
- `BenefitsCalculator.FoodandHousing(..., APPLY_SNAP=TRUE)` sets `value.snap` to `rowMins(function.snapBenefit(data), data$exp.food)` and then applies optional take-up.
- PolicyEngine's `snap` variable is normally a monthly SNAP amount for a SNAP/SPM unit. The study runner must normalize annual/monthly units explicitly before comparing.

## Parameter Files And Objects

The SNAP parameter source is `prd_parameters/benefit.parameters.rdata`, object `snapData`.

Observed with:

```r
load("prd_parameters/benefit.parameters.rdata")
load("prd_parameters/tables.rdata")
```

`snapData` dimensions:

- Rows: `9810`
- Columns: `34`

`snapData` columns:

```text
programName, stateName, stateFIPS, AKorHI, famsize, ruleYear, BBCE_State,
AssetTestFed_nonelddis, AssetTestFed_Elder_Dis,
AssetTest_Elder_Dis_over200FPL, AssetTest_Elder_Dis_under200FPL,
AssetTest_nonelddis, NetIncomeEligibilityFPL,
NetIncomeEligibility_nonelddis, NetIncomeEligibility_Elder_Dis,
GrossIncomeEligibilityFPL, GrossIncomeEligibility, FPL_prioryear,
FPL_currentyear, FPL, WorkRequirements, MedicalExpenseDeductionFloor,
StandardDeduction, MaxShelterDeduction, MaxBenefit, MinBenefit,
ListofCountableAssets, ListofTypeofDeductions,
WaiveNetIncomeTest_nonelddis, WaiveNetIncomeTest_Elder_Dis, HCSUAValue,
BasicLimitedUtilityAllowance, HCSUA, HeatandEatState
```

Rule years present:

```text
2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
2022, 2023, 2024, 2025, 2026
```

Jurisdiction coverage for latest year (`2026`):

- `51` jurisdictions: all states plus District of Columbia.
- State FIPS present: `1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56`.

Supporting table source:

- `prd_parameters/tables.rdata`, object `table.statemap`, maps `stateName`, `stateFIPS`, and `stateAbbrev`.

## State Option Modeling Surface

The latest-year `snapData` rows include state-option columns needed for the first divergence hypotheses:

- `BBCE_State`
- `GrossIncomeEligibilityFPL`
- `WaiveNetIncomeTest_nonelddis`
- `WaiveNetIncomeTest_Elder_Dis`
- `AssetTest_nonelddis`
- `AssetTest_Elder_Dis_over200FPL`
- `AssetTest_Elder_Dis_under200FPL`
- `HCSUA`
- `HCSUAValue`
- `HeatandEatState`

Examples from latest year (`2026`, `famsize == 1`):

| State | FIPS | BBCE | Gross FPL | Net test non-elder/disabled waived | Asset test non-elder/disabled | HCSUA | Heat and Eat |
|---|---:|---|---:|---|---:|---|---|
| California | 6 | Yes | 2.00 | No | 999999 | Mandatory | No |
| Georgia | 13 | Yes | 1.30 | Yes | 999999 | Mandatory | No |
| Texas | 48 | Yes | 1.65 | Yes | 5000 | Mandatory | No |
| Pennsylvania | 42 | Yes | 2.00 | Yes | 999999 | Mandatory | Yes |
| Mississippi | 28 | No | 1.30 | No | 3000 | Mandatory | No |
| Kansas | 20 | No | 1.30 | No | 3000 | Mandatory | No |

Candidate scope states should include at least:

- `CA`: high BBCE threshold but net-income test not waived in PRD.
- `TX`: BBCE with 165% gross threshold and a non-infinite asset test.
- `PA`: BBCE with Heat and Eat.
- `MS` or `KS`: non-BBCE comparison state.
- `GA`: PRD marks BBCE `Yes` but still uses 130% gross FPL, useful for checking how both engines represent limited categorical eligibility.

Final state choice depends on PolicyEngine reconnaissance.

## Known Modeling Asymmetries To Carry Forward

- PRD returns annual `snapValue`; PolicyEngine SNAP outputs are usually monthly.
- PRD's food/housing block caps `value.snap` at `exp.food`; the direct `function.snapBenefit` does not. The comparison should use the direct function for legal allotment unless testing the calculator's net-resource framing.
- PRD uses fixed maximum family/person slots (`agePerson1`...`agePerson12`), while PolicyEngine models persons/groups directly.
- PRD folds TANF/SSI categorical eligibility into SNAP from other calculated benefit values; fixtures that set these benefits to zero or nonzero must do so intentionally.
- PRD appears to encode BBCE and related state options as parameter columns plus some in-code overrides for New York and New Hampshire.
- PRD copies latest SNAP parameters forward for input years beyond its parameter max. The study should avoid future-year copying by locking to an explicit covered year.

## Commands Run

```bash
git clone https://github.com/Research-Division/policy-rules-database.git .external-repos/policy-rules-database
git -C .external-repos/policy-rules-database rev-parse HEAD
Rscript --version
Rscript - <<'RS'
repo <- ".external-repos/policy-rules-database"
load(file.path(repo, "prd_parameters", "benefit.parameters.rdata"))
load(file.path(repo, "prd_parameters", "tables.rdata"))
cat("snapData_rows", nrow(snapData), "cols", ncol(snapData), "\n")
cat("ruleYears", paste(sort(unique(snapData$ruleYear)), collapse=", "), "\n")
cat("state_count", length(unique(snapData$stateFIPS[snapData$ruleYear == max(snapData$ruleYear)])), "\n")
RS
```

R runtime:

```text
Rscript (R) version 4.6.0 (2026-04-24)
```

# SNAP Divergence Study Scope

Track: `divergence_study_20260704` phase 1

Date: 2026-07-05

## Locked Scope

Program: Supplemental Nutrition Assistance Program (SNAP)

Systems:

- PolicyEngine-US `1.755.5`, commit `fc64cef64ab55c3c48309c7fb304c35e5f3c9184`
- Atlanta Fed Policy Rules Database, commit `1d8e8674563a7653ec707d18956faa14b016bc5b`

Policy period:

- Primary comparison month: `2026-01`
- PolicyEngine period: `2026-01`
- PRD rule year: `2026`

Rationale:

- PRD `snapData` includes explicit `ruleYear == 2026` rows for all 50 states plus DC.
- PolicyEngine-US has FY2026 SNAP parameters effective from `2025-10-01` for allotments and deductions, so `2026-01` avoids partial fiscal-year transition ambiguity.
- January avoids mid-year or emergency-allotment historical artifacts and keeps the first fixture set focused on regular SNAP eligibility and allotment mechanics.

Comparison outputs:

- Eligibility: PolicyEngine `is_snap_eligible` vs PRD implied eligibility `function.snapBenefit(data) > 0`, with caveats below.
- Allotment: PolicyEngine monthly `snap` vs PRD annual `snapValue / 12`, using direct `function.snapBenefit(data)` rather than `BenefitsCalculator.FoodandHousing` for the legal allotment comparison.

The first implementation must keep the unit normalization explicit in every per-case JSON result.

## States

| State | FIPS | Included for | Initial expected-divergence hypotheses |
|---|---:|---|---|
| California | 6 | BBCE high threshold; always-SUA in PolicyEngine; PRD BBCE with net-test fields | PolicyEngine applies TANF non-cash net tests for CA BBCE in both HHEOD and non-HHEOD parameter surfaces; PRD carries SNAP net-test waiver columns separately. |
| Texas | 48 | BBCE with 165% gross threshold and finite asset limit | Both systems expose a finite asset limit for BBCE-like eligibility, but asset definitions and vehicle treatment are likely adapter-sensitive. |
| Pennsylvania | 42 | BBCE at 200%, Heat-and-Eat / always-SUA surface | Both systems indicate a state utility/SUA shortcut, but PRD uses `HeatandEatState`/`HCSUA` while PolicyEngine uses `always_standard` plus utility allowance variables. |
| Mississippi | 28 | Non-BBCE comparison state | PolicyEngine represents non-BBCE through `-inf` TANF non-cash gross/asset limits; PRD marks `BBCE_State == No` for 2026. Baseline federal gross/net/asset tests should be easier to compare. |
| Georgia | 13 | PRD BBCE flag with 130% gross threshold; PolicyEngine TANF non-cash gross 130% | Useful limited-BBCE / categorical-eligibility edge state because state-option semantics may look superficially equivalent but differ in net/asset handling and categorical trigger conditions. |

Deferred states:

- `KS`: strong non-BBCE comparator, but Mississippi already fills the non-BBCE slot. Keep KS as reserve if Mississippi fixture sources are weak.
- `AK`, `HI`: different allotment/poverty regions add useful later coverage but increase first-pass parameter normalization complexity.
- `NY`: both systems include special-case logic; defer until the basic runner and crosswalk are stable.
- `DC`: PolicyEngine has DC-specific local SNAP supplement variables; defer to avoid local-benefit contamination of the federal SNAP comparison.

## Fixture Class Plan

Target after human approval: at least 40 approved fixtures across the five states.

Candidate distribution:

- 8 baseline low-income eligible cases, one or two per state.
- 8 gross-income threshold cases around 130%, 165%, and 200% FPL.
- 8 net-income / shelter deduction cases around the 100% FPL net test and shelter cap.
- 8 asset-test cases, concentrated in TX, MS, and GA.
- 8 utility allowance / Heat-and-Eat cases, concentrated in PA, CA, TX, and MS.
- Additional reserve candidates for elderly/disabled medical and uncapped shelter treatment.

Fixtures are not golden until Dylan promotes them. AI-proposed cases must remain in `fixtures/candidates/` with `method: ai-proposed` until human approval.

## Known Modeling Asymmetries

These are not bugs by themselves. They are hypotheses and adapter risks to investigate.

1. Period and unit:
   - PolicyEngine `snap` is monthly.
   - PRD direct `function.snapBenefit` returns annual dollars rounded to whole dollars.
   - Comparison will normalize PRD by dividing by 12 and retain both raw and normalized values.

2. Eligibility output:
   - PolicyEngine exposes `is_snap_eligible`.
   - PRD does not return an explicit eligibility boolean from `function.snapBenefit`; eligibility must initially be inferred from `snapValue > 0`.
   - Minimum benefit and food-expense caps can make this inference unsafe if using the high-level food/housing block, so Phase 3 must call the direct SNAP function for the primary comparison.

3. BBCE representation:
   - PRD `snapData` has `BBCE_State`, gross FPL, net-test waiver, and asset-test columns.
   - PolicyEngine represents BBCE through TANF non-cash eligibility (`is_tanf_non_cash_eligible`) included in SNAP categorical eligibility.
   - Crosswalk rows for BBCE must cite both the PRD `snapData` columns and the PolicyEngine `gov.hhs.tanf.non_cash` parameters.

4. Asset definitions:
   - PRD uses `totalassets` and state-specific `AssetTest_*` columns after its input construction.
   - PolicyEngine `snap_assets` adds `bank_account_assets`, `stock_assets`, and `bond_assets`.
   - Vehicle treatment in Texas is explicitly mentioned in PolicyEngine TANF non-cash parameters and may require fixture exclusion or a separate adapter field.

5. Utility allowances:
   - PRD uses `HCSUA`, `HCSUAValue`, `BasicLimitedUtilityAllowance`, and `HeatandEatState`.
   - PolicyEngine computes utility allowance type from utility bills, always-SUA state parameters, and state/substate utility regions.
   - First fixtures should specify utility expenses explicitly and record which allowance is expected.

6. Household composition:
   - PRD expects fixed person slots up to 12.
   - PolicyEngine uses entity membership.
   - The fixture source of truth must describe people and units, with separate adapters for PRD slots and PolicyEngine entity maps.

7. Other eligibility dimensions:
   - PolicyEngine includes immigration, student, and work-requirement eligibility in `is_snap_eligible`.
   - The first fixture set should use citizens/non-students/work-requirement-exempt or work-requirement-passing adults unless the fixture specifically tests those dimensions.

## Required Follow-Up Before Phase 2 Completion

- Draft crosswalk rows must explicitly map annual/monthly money units.
- Candidate fixtures must cite primary or state-policy manual sources; AI boundary cases remain candidates only.
- No fixture should be called approved unless Dylan promotes it after checking the code/parameter definitions.
- Phase 3 PRD runner must call the real R code with `Rscript`; no Python reimplementation of PRD rules is permitted.

## Evidence Files

- `studies/snap-divergence/PRD_NOTES.md`
- `studies/snap-divergence/PE_NOTES.md`

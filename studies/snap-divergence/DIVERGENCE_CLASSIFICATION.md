# SNAP Divergence Draft Classification

This is a draft classification over candidate fixtures. It is not a final claim until fixtures are promoted and each case receives source-level investigation logs.

## Summary

- Divergences classified: 15
- Remaining unclassified divergences: 0

## Counts

| Classification | Count |
|---|---:|
| deduction handling | 3 |
| parameter vintage | 3 |
| rounding | 1 |
| state-option modeling | 8 |

## Cases

| Case | Classification | Detail |
|---|---|---|
| `us-snap/fixture.ga_bbce_165_boundary` | state-option modeling | Georgia divergence candidate: limited BBCE/gross-limit surface differs across engines; PRD carries BBCE_State with 130 percent gross FPL while PolicyEngine routes through TANF non-cash eligibility. |
| `us-snap/fixture.ga_gross_130_above` | state-option modeling | Georgia divergence candidate: limited BBCE/gross-limit surface differs across engines; PRD carries BBCE_State with 130 percent gross FPL while PolicyEngine routes through TANF non-cash eligibility. |
| `us-snap/fixture.ga_gross_130_below` | state-option modeling | Georgia divergence candidate: limited BBCE/gross-limit surface differs across engines; PRD carries BBCE_State with 130 percent gross FPL while PolicyEngine routes through TANF non-cash eligibility. |
| `us-snap/fixture.ms_asset_above_limit` | state-option modeling | Asset-test divergence candidate: PRD zeros the case at the finite asset surface while PolicyEngine still returns a positive SNAP amount. Check PRD totalassets/AssetTest columns against PolicyEngine snap_assets and TANF non-cash asset parameters. |
| `us-snap/fixture.ms_bbce_165_boundary` | parameter vintage | Mississippi non-BBCE divergence candidate: compare federal gross/net/asset thresholds and PRD 2026 snapData values against PolicyEngine FY2026 SNAP parameters. |
| `us-snap/fixture.ms_gross_130_above` | parameter vintage | Mississippi non-BBCE divergence candidate: compare federal gross/net/asset thresholds and PRD 2026 snapData values against PolicyEngine FY2026 SNAP parameters. |
| `us-snap/fixture.ms_gross_130_below` | parameter vintage | Mississippi non-BBCE divergence candidate: compare federal gross/net/asset thresholds and PRD 2026 snapData values against PolicyEngine FY2026 SNAP parameters. |
| `us-snap/fixture.ms_utility_allowance_phone_only` | rounding | Mississippi phone-only utility divergence candidate: small non-decision-relevant allotment difference, likely annual/monthly rounding or limited utility allowance handling. |
| `us-snap/fixture.pa_bbce_165_boundary` | deduction handling | Pennsylvania divergence candidate: uniform offset on gross-threshold cases suggests Heat-and-Eat/SUA or utility-deduction handling rather than eligibility flip. |
| `us-snap/fixture.pa_gross_130_above` | deduction handling | Pennsylvania divergence candidate: uniform offset on gross-threshold cases suggests Heat-and-Eat/SUA or utility-deduction handling rather than eligibility flip. |
| `us-snap/fixture.pa_gross_130_below` | deduction handling | Pennsylvania divergence candidate: uniform offset on gross-threshold cases suggests Heat-and-Eat/SUA or utility-deduction handling rather than eligibility flip. |
| `us-snap/fixture.tx_asset_above_limit` | state-option modeling | Asset-test divergence candidate: PRD zeros the case at the finite asset surface while PolicyEngine still returns a positive SNAP amount. Check PRD totalassets/AssetTest columns against PolicyEngine snap_assets and TANF non-cash asset parameters. |
| `us-snap/fixture.tx_bbce_165_boundary` | state-option modeling | Texas divergence candidate: BBCE gross threshold and finite asset-limit surface differ between PRD snapData and PolicyEngine TANF non-cash eligibility parameters. |
| `us-snap/fixture.tx_gross_130_above` | state-option modeling | Texas divergence candidate: BBCE gross threshold and finite asset-limit surface differ between PRD snapData and PolicyEngine TANF non-cash eligibility parameters. |
| `us-snap/fixture.tx_gross_130_below` | state-option modeling | Texas divergence candidate: BBCE gross threshold and finite asset-limit surface differ between PRD snapData and PolicyEngine TANF non-cash eligibility parameters. |

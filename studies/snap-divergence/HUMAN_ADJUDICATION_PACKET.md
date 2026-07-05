# SNAP Divergence Human Adjudication Packet

Track: `divergence_study_20260704`

Status: prepared for Dylan review on 2026-07-06.

This packet is for legal/source-of-truth adjudication. The agent has source-level classified the 15 held divergences, but has not decided which engine is legally correct and has not labeled any divergence as a confirmed bug.

## Inputs

- Source-level classification: `studies/snap-divergence/DIVERGENCE_CLASSIFICATION.md`
- Source triangulation pack: `studies/snap-divergence/SOURCE_TRIANGULATION.md`
- Machine-readable classified rows: `studies/snap-divergence/results/classified-candidate-divergences.jsonl`
- Held-case comparison evidence: `studies/snap-divergence/fixtures/FIXTURE_PROMOTION_REVIEW.md`
- PRD notes: `studies/snap-divergence/PRD_NOTES.md`
- PolicyEngine notes: `studies/snap-divergence/PE_NOTES.md`

## Current Classification Summary

| Classification | Cases | Decision-relevant | Human question |
|---|---:|---:|---|
| state-option modeling | 8 | 8 | Is either engine encoding the applicable FY2026 state option incorrectly, or are these acceptable modeling-scope differences? |
| deduction handling | 4 | 3 | Is the PRD or PolicyEngine utility/SUA/Heat-and-Eat treatment the legally correct surface for the fixture assumptions? |
| parameter vintage | 3 | 3 | Which parameter source should control Mississippi FY2026 non-BBCE gross/net/asset treatment? |

## Case Groups

### Georgia limited-BBCE/gross cases

Cases:

- `us-snap/fixture.ga_bbce_165_boundary`
- `us-snap/fixture.ga_gross_130_above`
- `us-snap/fixture.ga_gross_130_below`

Agent classification: `state-option modeling`.

Adjudication needed:

- Confirm whether Georgia FY2026 should be treated as BBCE with a 130% gross-FPL limit for the fixture assumptions.
- Decide whether the observed PRD/PolicyEngine differences are expected scope differences or a bug in one engine's state-option encoding.

### Texas BBCE and asset cases

Cases:

- `us-snap/fixture.tx_asset_above_limit`
- `us-snap/fixture.tx_bbce_165_boundary`
- `us-snap/fixture.tx_gross_130_above`
- `us-snap/fixture.tx_gross_130_below`

Agent classification: `state-option modeling`.

Adjudication needed:

- Confirm Texas FY2026 BBCE gross limit and $5,000 asset surface, including vehicle assumptions.
- Decide whether the direct PRD SNAP asset/gross gates or PolicyEngine TANF non-cash categorical route better matches the fixture assumptions.

### Mississippi non-BBCE cases

Cases:

- `us-snap/fixture.ms_asset_above_limit`
- `us-snap/fixture.ms_bbce_165_boundary`
- `us-snap/fixture.ms_gross_130_above`
- `us-snap/fixture.ms_gross_130_below`

Agent classifications: `state-option modeling` for the asset-above case; `parameter vintage` for the gross/BBCE cases.

Adjudication needed:

- Confirm Mississippi FY2026 non-BBCE status and applicable gross/net/asset thresholds.
- Decide whether the PRD finite asset/gross surface or PolicyEngine normal SNAP/TANF-disabled surface should control.

### Pennsylvania Heat-and-Eat/SUA cases

Cases:

- `us-snap/fixture.pa_bbce_165_boundary`
- `us-snap/fixture.pa_gross_130_above`
- `us-snap/fixture.pa_gross_130_below`

Agent classification: `deduction handling`.

Adjudication needed:

- Confirm whether Pennsylvania FY2026 Heat-and-Eat/SUA should route these fixture households to the PRD HCSUA value, PolicyEngine's PA standard utility allowance, or a more specific assumption.
- Decide whether the uniform monthly offset is a parameter-source mismatch, an adapter assumption issue, or a bug.

### Mississippi phone-only utility case

Case:

- `us-snap/fixture.ms_utility_allowance_phone_only`

Agent classification: `deduction handling`; non-decision-relevant.

Adjudication needed:

- Confirm whether the fixture should be treated as phone-only, generic utilities-positive, or heating/cooling utility for both engines.
- Decide whether this case should remain a held divergence, become an approved fixture with a clarified utility input, or be excluded from bug claims.

## Required Human Output

For each group, record one of:

- `confirmed_bug_policyengine`
- `confirmed_bug_prd`
- `expected_modeling_difference`
- `fixture_adapter_issue`
- `needs_more_source_review`

Only `confirmed_bug_policyengine` or `confirmed_bug_prd` should feed upstream issue drafts.

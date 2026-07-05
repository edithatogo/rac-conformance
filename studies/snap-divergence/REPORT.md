# SNAP Divergence Draft Report

This draft is generated from candidate fixtures. It is not a final finding report until fixtures are promoted and divergences are classified.

## Summary

| Metric | Value |
|---|---:|
| Total cases | 65 |
| Agreements | 50 |
| Divergences | 15 |
| Decision-relevant divergences | 14 |
| Unclassified divergences | 15 |

## Divergences

| Case | PolicyEngine allotment | PRD allotment | Difference | Decision-relevant | Classification |
|---|---:|---:|---:|---|---|
| `us-snap/fixture.ga_bbce_165_boundary` | 142.0999755859375 | 0 | 142.0999755859375 | true | unclassified |
| `us-snap/fixture.ga_gross_130_above` | 304.0999755859375 | 0 | 304.0999755859375 | true | unclassified |
| `us-snap/fixture.ga_gross_130_below` | 376.0999755859375 | 298.4167 | 77.6832755859375 | true | unclassified |
| `us-snap/fixture.ms_asset_above_limit` | 546 | 0 | 546 | true | unclassified |
| `us-snap/fixture.ms_bbce_165_boundary` | 142.0999755859375 | 0 | 142.0999755859375 | true | unclassified |
| `us-snap/fixture.ms_gross_130_above` | 304.0999755859375 | 0 | 304.0999755859375 | true | unclassified |
| `us-snap/fixture.ms_gross_130_below` | 376.0999755859375 | 269.5 | 106.5999755859375 | true | unclassified |
| `us-snap/fixture.ms_utility_allowance_phone_only` | 295.8999938964844 | 292.5 | 3.3999938964844 | false | unclassified |
| `us-snap/fixture.pa_bbce_165_boundary` | 142.0999755859375 | 176.5833 | 34.4833244140625 | true | unclassified |
| `us-snap/fixture.pa_gross_130_above` | 304.0999755859375 | 338.5833 | 34.4833244140625 | true | unclassified |
| `us-snap/fixture.pa_gross_130_below` | 376.0999755859375 | 410.5833 | 34.4833244140625 | true | unclassified |
| `us-snap/fixture.tx_asset_above_limit` | 546 | 0 | 546 | true | unclassified |
| `us-snap/fixture.tx_bbce_165_boundary` | 142.0999755859375 | 76.75 | 65.3499755859375 | true | unclassified |
| `us-snap/fixture.tx_gross_130_above` | 304.0999755859375 | 238.75 | 65.3499755859375 | true | unclassified |
| `us-snap/fixture.tx_gross_130_below` | 376.0999755859375 | 310.75 | 65.3499755859375 | true | unclassified |

## Evidence

- PolicyEngine candidate outputs: `studies/snap-divergence/results/policyengine-candidate-results.jsonl`
- PRD candidate outputs: `studies/snap-divergence/results/prd-candidate-results.jsonl`
- Machine-readable comparison rows: `studies/snap-divergence/results/comparison-candidate-results.jsonl`

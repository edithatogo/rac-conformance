# PRD Runner Evidence

Track: `divergence_study_20260704`

Python adapter: `studies/snap-divergence/runner/src/snap_divergence/prd_runner.py`

R bridge: `studies/snap-divergence/runner/R/prd_snap_runner.R`

Pinned engine:

- Atlanta Fed Policy Rules Database commit: `1d8e8674563a7653ec707d18956faa14b016bc5b`
- R runtime: `Rscript 4.6.0`
- Direct PRD entry point: `function.snapBenefit(data)`

## Dependency Boundary

The bridge does not source PRD `libraries.R`, because that file installs and loads the full application stack. The runner loads only the packages needed by `function.snapBenefit`: `dplyr`, `jsonlite`, and `matrixStats`, then sources PRD `functions/benefits_functions.R`.

## Candidate Run

Command:

```sh
PYTHONPATH=studies/snap-divergence/runner/src:harness:contracts/tools/src \
  python -m snap_divergence.prd_runner \
  --output studies/snap-divergence/results/prd-candidate-results.jsonl
```

Result:

- 65 candidate fixtures executed.
- Output file: `studies/snap-divergence/results/prd-candidate-results.jsonl`
- First case: `us-snap/fixture.ca_baseline_single_very_low_income`, allotment `298`.
- Last case: `us-snap/fixture.ga_utility_allowance_phone_only`, allotment `295.9167`.

The PRD direct function returns annual `snapValue`; the adapter normalizes the comparison allotment to monthly dollars by dividing by 12 and preserves the annual raw output.

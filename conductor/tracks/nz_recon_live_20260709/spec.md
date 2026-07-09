# Spec: NZ reconciliation live dual-engine re-run

## Goal
Produce numeric cross-engine agreements for cases where both engines expose comparable surfaces, using:

- RuleSpec companion oracles (and local KiwiSaver compile patch)
- Live OpenFisca Aotearoa simulations on the feat/199 branch (PR #200)

## Acceptance
- `python -m nz_reconciliation.run_live_suite` exits 0
- Report lists agreements and remaining intentional gaps (self-employed ACC, Crown KiwiSaver)
- Unit tests still pass under `make nz-recon-test`

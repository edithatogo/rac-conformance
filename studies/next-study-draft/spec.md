# Spec: NZ RuleSpec vs OpenFisca Aotearoa Reconciliation

## Overview
Reconcile the NZ tax/benefit calculation logic of `rulespec-nz` against `openfisca-aotearoa` using the PIC validation harness.

## Scope
- Compare personal income tax calculations, ACC earner levies, and KiwiSaver contributions.
- Target at least 15 cross-engine test cases.

## Acceptance Criteria
- Full verification suite runs cleanly via `make check`.
- Discovered divergence reports are compiled and published under `studies/nz-reconciliation/results/`.

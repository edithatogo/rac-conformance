# Plan

GitHub issue: https://github.com/edithatogo/rac-conformance/issues/33

> REVIEW (2026-07-14): Local review passed. `CITATION.cff` and `.zenodo.json`
> agree, the mirror manifest preserves the pending-human-deposit boundary, and
> the FOI programme evidence test passes. No Zenodo deposit or DOI verification
> is claimed; the remaining items stay blocked on the human publication gate.

- [x] Add `.zenodo.json` and register the repository in the paper mirror manifest. (CFF/Zenodo metadata validated locally)
- [ ] [HUMAN] Publish and verify the evidence release in Zenodo.
> BLOCKED (2026-07-14): Requires Dylan to publish the tagged evidence release
> in GitHub/Zenodo and verify the resulting version DOI. The configured remote
> does not currently advertise `refs/tags/v0.2.0`; agents must not infer a
> release SHA, claim a deposit, or replace the pending DOI gate.
- [ ] Replace the pending DOI gate in the manuscript ledger.
> BLOCKED (2026-07-14): Depends on the verified Zenodo version DOI from the
> human publication step above.

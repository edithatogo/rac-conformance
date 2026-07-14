# Plan

GitHub issue: https://github.com/edithatogo/rac-conformance/issues/33

> REVIEW (2026-07-14): Local review passed. `CITATION.cff` and `.zenodo.json`
> agree, the mirror manifest preserves the pending-human-deposit boundary, and
> the FOI programme evidence test passes. No Zenodo deposit or DOI verification
> is claimed; the remaining items stay blocked on the human publication gate.

> RELEASE VERIFIED (2026-07-14): GitHub release `v0.2.0` is published from
> `main` at commit `35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5`. Zenodo deposit and
> DOI verification remain human-gated; no DOI is inferred from the GitHub
> release.

- [x] Add `.zenodo.json` and register the repository in the paper mirror manifest. (CFF/Zenodo metadata validated locally)
- [ ] [HUMAN] Deposit the verified GitHub release in Zenodo and verify the
      resulting version and concept DOIs.
> BLOCKED (2026-07-14): Requires authenticated maintainer Zenodo access. The
> GitHub release/tag prerequisite is complete; agents must not claim a deposit
> or replace the pending DOI gate without a resolving Zenodo record.
- [ ] Replace the pending DOI gate in the manuscript ledger.
> BLOCKED (2026-07-14): Depends on the verified Zenodo version DOI from the
> human publication step above.

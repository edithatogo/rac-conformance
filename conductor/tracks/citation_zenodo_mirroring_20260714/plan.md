# Plan

GitHub issue: https://github.com/edithatogo/rac-conformance/issues/33

> REVIEW (2026-07-14): Local review passed. `CITATION.cff` and `.zenodo.json`
> agree, the mirror manifest preserves the pending-human-deposit boundary, and
> the FOI programme evidence test passes. No Zenodo deposit or DOI verification
> was claimed at that checkpoint; the publication gate is now reconciled below.

> RELEASE VERIFIED (2026-07-14): GitHub release `v0.2.0` is published from
> `main` at commit `35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5`. Zenodo deposit and
> DOI verification remained human-gated at that checkpoint; no DOI was inferred
> from the GitHub release.

- [x] Add `.zenodo.json` and register the repository in the paper mirror manifest. (CFF/Zenodo metadata validated locally)
- [x] [HUMAN] Deposit the verified GitHub release in Zenodo and verify the
      resulting version and concept DOIs.
- [x] Replace the pending DOI gate in the manuscript ledger.

> CHECKPOINT (2026-07-15): Zenodo record `21360138` publishes `v0.8.1` at
> version DOI `10.5281/zenodo.21360138` and concept DOI
> `10.5281/zenodo.21360137`. Public metadata identifies the GitHub repository,
> MIT license, and author ORCID `0000-0002-9775-0603`; the GitHub release
> resolves to commit `d24ae6f9f2d9488052969f633d91eff4a9a47f58`.

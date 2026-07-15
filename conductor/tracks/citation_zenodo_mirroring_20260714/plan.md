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
- [ ] [HUMAN] Deposit the verified GitHub release in Zenodo and verify the
      resulting version and concept DOIs.
      - **PREPARATION COMPLETE (2026-07-15):** `papers/zenodo/RAC_CONFORMANCE_V0.2.0_ARCHIVE.json` records the verified release commit and GitHub archive SHA-256.
- [ ] Replace the pending DOI gate in the manuscript ledger.

> EVIDENCE CORRECTION (2026-07-15): Zenodo record `21360138` is the FOI-O
> `v0.8.1` release and does not satisfy this track's RaC Conformance evidence-
> release deposit gate. RaC Conformance `v0.2.0` is published at commit
> `35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5`, but the programme manifest and
> citation ledger correctly retain `pending_human_deposit`; live Zenodo searches
> by repository URL and title returned no RaC Conformance record.

> BLOCKED (2026-07-15): Publishing the RaC Conformance `v0.2.0` release in
> Zenodo and verifying its version and concept DOIs require the human deposit
> gate. No DOI will be inferred from FOI-O or another programme repository.

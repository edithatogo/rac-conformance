# RaC Conformance Zenodo submission checklist

Human publication gate for `citation_zenodo_mirroring_20260714` and GitHub
issue #33. This is a preparation artifact, not evidence that a deposit exists.

## Before publishing

> Verification (2026-07-14): the configured `rac-conformance` remote does not
> currently advertise `refs/tags/v0.2.0`. The maintainer must create or publish
> that immutable release before Zenodo deposition; no release SHA is inferred
> locally.

1. Create or verify the GitHub release/tag matching `CITATION.cff` version
   `0.2.0` and confirm the release archive contains the contracts, harnesses,
   studies, FOI programme quality register, and manuscript evidence ledger.
2. Upload the release to the linked Zenodo repository using `.zenodo.json`.
3. Confirm the Zenodo metadata title, creator ORCID, Apache-2.0 license, and
   `isIdenticalTo` GitHub identifier match `CITATION.cff`.

## After publishing

Record all of the following in `papers/zenodo/foi-programme-mirror-manifest.json`
and `papers/CITATION_LEDGER.md`:

- version DOI and concept DOI;
- deposited version and Git tag/SHA;
- Zenodo landing-page URL;
- checksum or archive digest for the evidence bundle;
- date verified by the human maintainer.

Only after the version DOI resolves to the tagged release may the manuscript
ledger replace `pending_human_deposit` for `rac-conformance`.

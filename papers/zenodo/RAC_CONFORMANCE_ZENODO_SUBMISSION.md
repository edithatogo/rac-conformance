# RaC Conformance Zenodo submission checklist

Human publication gate for `citation_zenodo_mirroring_20260714` and GitHub
issue #33. This file is preparation evidence, not proof of a Zenodo deposit.

## Verified release input

- GitHub release/tag: `v0.2.0`
- Main commit: `35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5`
- Release: https://github.com/edithatogo/rac-conformance/releases/tag/v0.2.0
- GitHub source archive SHA-256: `07743bb7e4be3749f89564d8cb0184372a76d26af426181ccdcd3115e8d667ff`
- Locally reproducible `git archive` SHA-256: `3077044a38d1f2fcabf60d473c3875de4e1de09717f10fbe76582eff13939c11`

The GitHub archive digest is the deposit identity to verify. The local archive
digest is retained as a reproducibility cross-check; GitHub and local gzip
archives are not expected to be byte-identical.

## Human publication steps

1. Deposit the GitHub release in Zenodo using the repository `.zenodo.json`.
2. Verify the title, creator ORCID, Apache-2.0 license, and repository link.
3. Record the version DOI and concept DOI in the mirror manifest. Record the
   landing page, release SHA, archive digest, and verification date in the
   citation ledger.
4. Replace `pending_human_deposit` with `verified_published_version` only after
   the version DOI resolves to this exact release.

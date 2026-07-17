# v1 Security, Licensing, and Claims Review

Review scope: current `codex/rac-v1-integration` working branch and the
unpublished candidate from commit `4206608baa37c4844cb4aee4a629797df9479ff9`.

## Verified locally

- `make check` passes, including repository audit and all declared local test,
  lint, example, converter, harness, study, and demo gates.
- `docs/V1_THREAT_MODEL.md` and `docs/V1_RISK_REGISTER.json` enumerate trust
  boundaries, threat classes, owners, controls, verification, and release
  dispositions.
- `docs/V1_VALIDATION_BASELINE.json` and `docs/V1_FUZZ_BASELINE.json` record
  bounded validation measurements and deterministic synthetic mutations.
- `docs/V1_SUPPLY_CHAIN_EVIDENCE.md`, `docs/V1_HOSTED_GOVERNANCE.md`, and
  `docs/V1_SBOM.json` record local workflow/dependency audits, lockfiles, SBOM
  evidence, hosted branch protection, secret-scanning status, and remaining
  signing/environment limitations.
- GitHub Actions workflows use read-only contents permissions and immutable
  action references in the reviewed files.
- The candidate contains Apache-2.0 licensing metadata, `CITATION.cff`,
  `.zenodo.json`, `SECURITY.md`, dependency lock data, SBOM, checksums, and
  provenance.
- `docs/V1_SCOPE.md` excludes legal, clinical, funding, standards-body, and
  broad portability claims; candidate fixtures and AI-proposed mappings remain
  non-normative.

## Automated hardening update (2026-07-17)

The engineering-hardening track's contributor-controlled evidence is now
complete for the current mainline: hosted cross-platform qualification,
hostile-input and property tests, deterministic mutation testing, SBOM,
reproducibility, and rollback rehearsal are recorded. This does not close the
release gate: hosted artifact attestations, signing, live rollback evidence,
external source rights, and human residual-risk approval remain open.

## Not locally certifiable

- External source rights, protected release environments, commit signatures,
  and artifact attestations remain open.
- FOI-O evidence, independent adoption, human mapping certification, health
  case selection, and publication authorization remain open.
- Human approval is still required for release promotion, signing, package
  publication, DOI deposition, and announcements.

## Release disposition

`blocked`: no unresolved high/critical risk may be silently waived. This packet
is evidence for review, not a security certification or release authorization.

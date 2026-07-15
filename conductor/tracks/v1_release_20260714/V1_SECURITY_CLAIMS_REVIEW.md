# v1 Security, Licensing, and Claims Review

Candidate commit: `0c4a83b55208bae59592af017c6e0f66194ec8bb`

## Verified locally

- `make check` passes, including repository audit and all declared local test,
  lint, example, converter, harness, study, and demo gates.
- GitHub Actions workflows use read-only contents permissions and immutable
  action references in the reviewed files.
- The candidate contains Apache-2.0 licensing metadata, `CITATION.cff`,
  `.zenodo.json`, `SECURITY.md`, dependency lock data, SBOM, checksums, and
  provenance.
- `docs/V1_SCOPE.md` excludes legal, clinical, funding, standards-body, and
  broad portability claims; candidate fixtures and AI-proposed mappings remain
  non-normative.

## Not locally certifiable

- Live dependency advisories, GitHub branch-protection status, hosted Actions
  results for this exact commit, secret-scanning results, and external source
  rights were not independently rechecked in this workspace.
- The engineering-hardening track still contains unchecked threat-model,
  hostile-input, mutation, supply-chain, and platform-qualification tasks.
- Human approval is still required for release promotion, signing, package
  publication, DOI deposition, and announcements.

## Release disposition

`blocked`: no unresolved high/critical risk may be silently waived. This packet
is evidence for review, not a security certification or release authorization.

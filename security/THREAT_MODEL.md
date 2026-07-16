# v1 Threat Model

Scope: local validators, converters, harnesses, study runners, generated
reports, CI, release artifacts, and staged external packets. The repository
does not execute untrusted code or accept live personal data.

| Boundary | Untrusted input | Threats | Required control | Evidence |
| --- | --- | --- | --- | --- |
| File -> JSON parser | checked-in or submitted artifact | oversized/deep/bomb input | byte, depth, and string bounds | `pic_contracts.safety` tests |
| JSON -> schema validator | malformed records and references | crash, misleading diagnostics, authority leakage | schema plus semantic validation | `make check` |
| Archive/path -> converter | fixture archives and paths | traversal, symlink escape, resource exhaustion | isolated temp root and path policy | converter hostile-input tests |
| URL/source -> mapping | official-source metadata | stale, spoofed, confidential inference | immutable URL/revision, status, effective date, human gate | source manifests |
| Process -> report | generated traces/results | injection, false claims, accidental sensitive output | escaped serialization and claims audit | release audit |
| Workflow -> repository | pull request and action inputs | token misuse, dependency compromise | least privilege, pinned actions, dependency review, CodeQL | `.github/workflows/` |
| Release -> consumer | packages and manifests | tampering, provenance spoofing, rollback failure | checksums, SBOM, provenance, restore rehearsal | v1 release packet |

## Release disposition

High/critical findings must be fixed or remain release-blocking. Human approval
is required for residual risk, signing, promotion of candidates, and external
publication. This document does not certify third-party services or policy
content.

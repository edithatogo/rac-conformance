# v1 Supply-Chain Evidence

Observed: 2026-07-17 from current `origin/main`.

## Local evidence

| Check | Result | Evidence or limitation |
| --- | --- | --- |
| Workflow action pinning | pass | Every `uses:` reference in `.github/workflows/` uses an immutable commit SHA. |
| Workflow permissions | pass | Workflows declare least-privilege top-level permissions; CodeQL separately requests `security-events: write` for its required upload. |
| Workflow security audit | pass | `uvx zizmor .github/workflows` reported no findings; 10 informational findings are suppressed by existing configuration. |
| Dependency vulnerability audit | pass with limitation | `pip-audit` found no known vulnerabilities in the contract-tool environment. The local editable `pic-contracts` package is not present on PyPI and was not auditable as a distribution. |
| Dependency locking | pass | `contracts/tools/uv.lock` and `converters/fixtures/uv.lock` are tracked. |
| SBOM | pass | `docs/V1_SBOM.json` is a CycloneDX JSON inventory generated with reproducible output. |
| Secret scanning | hosted pass | GitHub API verification on 2026-07-16 reports secret scanning and push protection enabled; validity checks and non-provider patterns remain disabled. |
| Branch protection | hosted pass with limitation | Main requires all recorded CI/security/v1 matrix checks and conversation resolution; no approving review or code-owner review is currently required. Admin enforcement, linear history, no force-push, and no deletion are enabled. |
| Release environment protection | not reverified | Release-environment reviewers, bypass, and protected-branch deployment settings require a live release-time check; artifact-attestation execution and commit signatures remain open. |

## Release disposition

The local and main-branch controls are suitable for continued engineering, but
the v1 release remains blocked until signing, artifact attestations, and the
remaining human/external gates are verified. A clean CI run must not be
represented as proof of independent adoption or release authorization. Details
of the hosted observation are in
`docs/V1_HOSTED_GOVERNANCE.md`.

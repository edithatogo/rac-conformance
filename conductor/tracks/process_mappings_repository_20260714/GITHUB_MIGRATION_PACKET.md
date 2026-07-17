# Process-mappings GitHub Migration Packet

Status: **staged migration; public remote exists and hosted verification passed**.
human approval was recorded before repository creation; canonical cutover still
requires a separate closeout decision.

This packet is prepared from `rac-conformance` issue [#50](https://github.com/edithatogo/rac-conformance/issues/50) and the dependent parent issues [#39](https://github.com/edithatogo/rac-conformance/issues/39), [#40](https://github.com/edithatogo/rac-conformance/issues/40), [#41](https://github.com/edithatogo/rac-conformance/issues/41), [#42](https://github.com/edithatogo/rac-conformance/issues/42), and [#43](https://github.com/edithatogo/rac-conformance/issues/43). The public remote exists; canonical parent cutover remains open.

## Proposed repository

| Field | Proposal | State before approval |
|---|---|---|
| Owner | `edithatogo` | proposed |
| Name | `process-mappings` | proposed |
| URL | `https://github.com/edithatogo/process-mappings` | public remote exists; not yet canonical |
| Visibility | Public, subject to source-rights review | proposed |
| License | Apache-2.0, retaining source-specific rights notices | prepared in `LICENSE_BOUNDARY.md` |
| Initial version | `0.1.0-incubation` or equivalent pre-1.0 release | human decision |
| Canonical source | Future remote only after cutover | current source is this subtree |
| Project | GitHub Project 19 | add/link only after repository creation |

## Files prepared

- `.github/CODEOWNERS`: `@edithatogo` owns all paths.
- `.github/PULL_REQUEST_TEMPLATE.md`: provenance, loss, contract, and boundary checks.
- `.github/ISSUE_TEMPLATE/profile.yml`: profile intake with named consumer and primary sources.
- `.github/ISSUE_TEMPLATE/bug.yml`: reproducible defect/provenance intake.
- `SECURITY.md`: security-reporting boundary with no false contact address.
- `ci/check.sh` and `.github/workflows/standalone-check.yml`: dependency-free extracted-tree check.
- `schemas/contract-consumption.json`: immutable PIC and upstream input ledger.

## Required repository settings after approval

1. Create `edithatogo/process-mappings` with the approved visibility and Apache-2.0 license.
2. Populate it from the filtered subtree commit in `EXTRACTION_REHEARSAL.json`; preserve the six-commit filtered history and record the migration commit.
3. Configure `main` as the default branch, require pull requests, require the CODEOWNERS review, require conversation resolution, and require the standalone check.
4. Enable dependency/security features supported by the repository plan, with least-privilege workflow permissions and immutable action references.
5. Link the repository issues to Project 19 and create destination issues only after approving the mapping below.
6. Set the canonical URL and release policy, then verify a clean clone and hosted CI before any parent cutover.

## Parent-to-destination issue map

| Parent issue | Destination issue proposal | Scope | Migration rule |
|---|---|---|---|
| `rac-conformance#50` | `process-mappings#1` | extraction governance and canonical cutover | preserve backlink; close parent only after cutover |
| `rac-conformance#40` | `process-mappings#2` | profile implementation consumer surface | parent remains normative-contract owner |
| `rac-conformance#41` | `process-mappings#3` | adverse-incident/open-disclosure profile | human/source gate remains explicit |
| `rac-conformance#42` | `process-mappings#4` | health-technology pathways | source authority stays with named regulators/payers |
| `rac-conformance#43` | `process-mappings#5` | optional Camunda adapter | adapter cannot redefine PIC |

These are destination proposals, not created issues. No issue is migrated by
an agent. Existing parent issue history remains authoritative until the human
cutover decision and authenticated migration.

## Rollback and single-source rule

- Before cutover, `subrepos/process-mappings/` is the only writable source.
- After cutover, the extracted remote becomes the single writable canonical source.
- The parent subtree must be removed or changed to a documented read-only pointer in the same approved closeout.
- If hosted checks, history, rights, or governance verification fails, do not close the parent; delete or quarantine the remote and return to the parent subtree using the immutable rehearsal commit.
- A release tag is not evidence of canonical cutover until the source-of-truth and hosted-control checks are complete.

## Human decision checklist

- [x] Approve repository creation and public visibility.
- [x] Approve proposed owner, CODEOWNERS, branch protection, and security posture.
- [x] Approve issue/project mapping and destination issue creation.
- [ ] Approve initial versioning and release policy.
- [x] Approve the migration commit from `EXTRACTION_REHEARSAL.json`.
- [ ] Approve canonical cutover only after hosted CI and clean-clone verification.

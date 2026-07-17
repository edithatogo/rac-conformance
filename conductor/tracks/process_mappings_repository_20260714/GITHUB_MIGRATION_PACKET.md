# Process-mappings GitHub Migration Packet

Status: **staged migration; public remote exists and hosted verification passed**.
The packet records analyst approval before repository creation (legacy
compatibility phrase: human approval); canonical cutover still
requires a separate closeout decision.

This packet is prepared from `rac-conformance` issue [#50](https://github.com/edithatogo/rac-conformance/issues/50) and the dependent parent issues [#39](https://github.com/edithatogo/rac-conformance/issues/39), [#40](https://github.com/edithatogo/rac-conformance/issues/40), [#41](https://github.com/edithatogo/rac-conformance/issues/41), [#42](https://github.com/edithatogo/rac-conformance/issues/42), and [#43](https://github.com/edithatogo/rac-conformance/issues/43). The public remote exists; canonical parent cutover remains open.

## Proposed repository

| Field | Proposal | State before approval |
|---|---|---|
| Owner | `edithatogo` | verified |
| Name | `process-mappings` | verified |
| URL | `https://github.com/edithatogo/process-mappings` | public remote exists; not yet canonical |
| Visibility | Public, subject to ongoing source-rights review | verified |
| License | Apache-2.0, retaining source-specific rights notices | verified in destination |
| Initial version | `0.1.0-incubation` or equivalent pre-1.0 release | analyst decision remains |
| Canonical source | Future remote only after cutover | parent subtree remains authoritative |
| Project | Project 19 and Project 14 | destination issue #1 linked |

## Files prepared

- `.github/CODEOWNERS`: `@edithatogo` owns all paths.
- `.github/PULL_REQUEST_TEMPLATE.md`: provenance, loss, contract, and boundary checks.
- `.github/ISSUE_TEMPLATE/profile.yml`: profile intake with named consumer and primary sources.
- `.github/ISSUE_TEMPLATE/bug.yml`: reproducible defect/provenance intake.
- `SECURITY.md`: security-reporting boundary with no false contact address.
- `ci/check.sh` and `.github/workflows/standalone-check.yml`: dependency-free extracted-tree check.
- `schemas/contract-consumption.json`: immutable PIC and upstream input ledger.

## Hosted controls verified

1. `edithatogo/process-mappings` is public, uses `main`, and is licensed Apache-2.0.
2. The destination contains the filtered history and immutable migration commit
   `d0257c1a99068262ea257643f3d6bdb57f2baee6`.
3. `main` requires pull requests, one CODEOWNER approval, conversation
   resolution, and the standalone `check` status.
4. Dependency review, secret scanning, push protection, and least-privilege
   workflow settings are enabled where supported.
5. Destination issue #1 is linked to Projects 19 and 14.
6. A clean clone, `git fsck --full`, standalone verification, and hosted CI
   passed.

Canonical URL ownership and release policy remain subject to the separate
cutover decision below.

## Parent-to-destination issue map

| Parent issue | Destination issue proposal | Scope | Migration rule |
|---|---|---|---|
| `rac-conformance#50` | `process-mappings#1` | extraction governance and canonical cutover | linked; keep parent open until cutover |
| `rac-conformance#40` | `process-mappings#2` | profile implementation consumer surface | parent remains normative-contract owner |
| `rac-conformance#41` | `process-mappings#3` | adverse-incident/open-disclosure profile | analyst/source gate remains explicit |
| `rac-conformance#42` | `process-mappings#4` | health-technology pathways | source authority stays with named regulators/payers |
| `rac-conformance#43` | `process-mappings#5` | optional Camunda adapter | adapter cannot redefine PIC |

Issue #1 is the created destination governance issue. Issues #2-#5 remain
proposals and are deliberately not created until named consumers and profile
scope require them. Existing parent issue history remains authoritative until
the analyst cutover decision.

## Evidence register for analyst review

The entries below are repository-local evidence. A rehearsal or prepared
destination file does not prove a hosted setting exists.

| Evidence ID | Claim or decision supported | Evidence | Limitation |
|---|---|---|---|
| `PM-LOCAL-01` | The incubator has defined ownership boundaries. | [`spec.md`](./spec.md), [`plan.md`](./plan.md) | Repository-local; recheck the working tree at review. |
| `PM-LOCAL-02` | Filtered extraction and rollback were rehearsed. | [`EXTRACTION_REHEARSAL.json`](./EXTRACTION_REHEARSAL.json) | Does not prove remote or hosted controls. |
| `PM-LOCAL-03` | Destination governance files were prepared. | [`subrepos/process-mappings/.github`](../../../subrepos/process-mappings/.github), [`SECURITY.md`](../../../subrepos/process-mappings/SECURITY.md), [`ci/check.sh`](../../../subrepos/process-mappings/ci/check.sh) | Prepared files only; no hosted execution is claimed. |
| `PM-EXTERNAL-01` | Hosted repository and Project 19 state are current. | Authenticated GitHub export/settings capture | Must be collected and pinned by the analyst; this packet cannot substitute for it. |

Record the export or settings page, retrieval date, account/owner, and stable
URL or digest before relying on a hosted fact.

## Rollback and single-source rule

- Before cutover, `subrepos/process-mappings/` is the only writable source.
- After cutover, the extracted remote becomes the single writable canonical source.
- The parent subtree must be removed or changed to a documented read-only pointer in the same approved closeout.
- If hosted checks, history, rights, or governance verification fails, do not close the parent; delete or quarantine the remote and return to the parent subtree using the immutable rehearsal commit.
- A release tag is not evidence of canonical cutover until the source-of-truth and hosted-control checks are complete.

## Analyst decision checklist

- [x] Approve repository creation and public visibility.
- [x] Approve proposed owner, CODEOWNERS, branch protection, and security posture.
- [x] Approve issue/project mapping and destination issue creation.
- [ ] Approve initial versioning and release policy; see `VERSIONING_DECISION_PACKET.md`.
- [x] Approve the migration commit from `EXTRACTION_REHEARSAL.json`.
- [ ] Approve canonical cutover only after consumer migration, hosted CI, and clean-clone verification.

An agent must not create a remote, migrate issues, configure hosted settings, or
make the extracted copy canonical while a required analyst decision is blank.

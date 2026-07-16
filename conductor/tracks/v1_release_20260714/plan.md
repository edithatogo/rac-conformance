# Implementation Plan

GitHub issue: [#46](https://github.com/edithatogo/rac-conformance/issues/46). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39)-[#45](https://github.com/edithatogo/rac-conformance/issues/45) and all applicable existing external, publication, citation, and human gates.

## Phase 1 - Release Candidate Freeze

- [ ] Task: Audit all v1 gates and dependency evidence
    - [ ] Validate the machine-readable gate manifest and every linked artifact.
    - [ ] Recheck external URLs, hosted checks, human certifications, and evidence freshness.
    - [ ] Block release for any missing, stale, conflicting, or self-certified required gate.
    - **Acceptance:** the gate report is deterministic and has no unknown required status.
    - Evidence: `release/v1/gates.json` and `tools/v1_release_audit.py`; the report explicitly remains non-releasable.
    > BLOCKED (2026-07-16): External URL freshness, hosted checks, human certifications, and upstream gates cannot be verified or completed from this local repository.
- [ ] Task: Freeze normative surface and migration set
    - [ ] Freeze schemas, CLIs, canonicalization, identifiers, diagnostics, and compatibility promises.
    - [ ] Generate migrations from every supported 0.x version.
    - [ ] Move nonqualifying features to experimental or a later 1.x roadmap.
    - **Acceptance:** freeze diff and exclusions are explicit and reviewed.
- [ ] Task: Build release candidate from clean environments
    - [ ] Produce packages, source archives, SBOMs, checksums, provenance, and compatibility reports.
    - [ ] Compare reproducible builds and run all supported-platform matrices.
    - **Acceptance:** all release artifacts derive from the reviewed release commit.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Release Candidate Freeze' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): The release audit is deterministic and reports nine
> explicit gates. It correctly returns `releasable: false`; no release freeze
> or v1.0 publication is claimed.

## Phase 2 - Qualification

- [ ] Task: Run full consumer and domain qualification
    - [ ] Run FOI-O, rules-heavy, adverse-incident, health-technology, Camunda, and independent-consumer suites.
    - [ ] Verify no candidate or uncertified fixture is counted as golden evidence.
    - [ ] Resolve contributor-controlled defects through regression-first fixes.
    - **Acceptance:** the frozen compatibility matrix is green or release remains blocked.
- [ ] Task: Review security, licensing, documentation, and claims
    - [ ] Recheck threat-model disposition, dependency advisories, licenses, source rights, and sensitive-data scans.
    - [ ] Match every README/release-note capability claim to evidence and scope limits.
    - **Acceptance:** no unresolved high/critical risk or unsupported capability claim remains.
- [ ] Task: [HUMAN] Approve v1.0 release candidate
    - [ ] Present complete gate, risk, compatibility, consumer, source, and publication-boundary packet.
    - [ ] Dylan approves release, requires fixes, or continues 0.x.
    - **Acceptance:** authorization is explicit and tied to an exact commit/artifact set.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Qualification' (Protocol in workflow.md)

## Phase 3 - Publication and Verification

- [ ] Task: [HUMAN] Publish and sign approved v1.0 artifacts
    - [ ] Create signed tag/release and publish packages only as authorized.
    - [ ] Perform DOI/Zenodo and announcement actions only under their separate approvals.
    - **Acceptance:** every destination confirms the expected immutable artifact and metadata.
- [ ] Task: Verify published release and rollback readiness
    - [ ] Install from public distribution surfaces in clean environments.
    - [ ] Verify signatures/checksums/provenance, CLI behavior, schemas, and compatibility examples.
    - [ ] Trigger rollback procedure for integrity or release-blocking compatibility failure.
    - **Acceptance:** public artifacts match reviewed artifacts byte-for-byte where promised.
- [ ] Task: Close release ledger and create 1.x follow-up roadmap
    - [ ] Record final evidence, known limitations, maintenance dates, and deferred work.
    - [ ] Close Project 19 items only at their true terminal state.
    - [ ] Archive tracks after review and post-release verification.
    - **Acceptance:** local, GitHub, package, release, citation, and consumer status agree.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Publication and Verification' (Protocol in workflow.md)

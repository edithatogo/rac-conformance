# Implementation Plan

GitHub issue: [#46](https://github.com/edithatogo/rac-conformance/issues/46). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39)-[#45](https://github.com/edithatogo/rac-conformance/issues/45) and all applicable existing external, publication, citation, and human gates.

## Phase 1 - Release Candidate Freeze

- [x] Task: Audit all v1 gates and dependency evidence
    - [x] Validate the machine-readable gate manifest and every linked artifact.
    - [x] Recheck external URLs, hosted checks, human certifications, and evidence freshness.
    - [x] Block release for any missing, stale, conflicting, or self-certified required gate.
    - **Acceptance:** the gate report is deterministic and has no unknown required status.
    - **Evidence:** `tools/v1_release_audit.py`, `tools/tests/test_v1_release_audit.py`, and `V1_RELEASE_GATE_AUDIT.json` produce a deterministic blocked/ready decision. External URL, hosted-check, and human-certification verification is explicitly recorded as `not-performed` when it cannot be proven locally.
- [x] Task: Freeze normative surface and migration set
    - [x] Freeze schemas, CLIs, canonicalization, identifiers, diagnostics, and compatibility promises.
    - [x] Generate migrations from every supported 0.x version.
    - [x] Move nonqualifying features to experimental or a later 1.x roadmap.
    - **Acceptance:** freeze diff and exclusions are explicit and reviewed.
    - **Evidence:** `V1_NORMATIVE_FREEZE.md` records the exact freeze base, supported package versions, migration posture, exclusions, and post-freeze change rule; contract documentation was corrected to match the `pic-traces/0.2.0` schema.
- [x] Task: Build release candidate from clean environments
    - [x] Produce packages, source archives, SBOMs, checksums, provenance, and compatibility reports.
    - [x] Compare reproducible builds and run all supported-platform matrices.
    - **Acceptance:** all release artifacts derive from the reviewed release commit.
    - **Evidence:** `release-candidate/current/` contains the prior unpublished package/source artifacts, SBOM, checksums, provenance, compatibility report, and candidate manifest generated from clean commit `4206608`. The latest hosted qualification ran against `0442ffd` and was merged to current `main` as `680dbd7`; two clean source/package builds had identical SHA-256 digests, local `make check` passed, and hosted qualification passed. The candidate remains unpublished and unsigned; rebuild from the final reviewed tree is required before promotion.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Release Candidate Freeze' (Protocol in workflow.md)
    - **CHECKPOINT:** Gate audit is deterministic and blocked for four declared external/human gates. Normative scope is frozen, package metadata is buildable, and a reproducible `v1.0.0-rc.1` candidate has passed clean `make check`. Qualification, human certification, publication, and final release remain deferred.

> EVIDENCE RECONCILIATION (2026-07-17): Hosted v1 qualification run
> `29578650877` passed all four Ubuntu/macOS and Python 3.12/3.13 jobs for
> commit `0442ffdf`, now represented on `main` by merge commit `680dbd7`.
> The packet records the distinction between tested PR content and a future
> release-candidate rebuild; no stale candidate is treated as current.

## Phase 2 - Qualification

- [ ] Task: Run full consumer and domain qualification
    - [ ] Run FOI-O, rules-heavy, adverse-incident, health-technology, Camunda, and independent-consumer suites.
    - [ ] Verify no candidate or uncertified fixture is counted as golden evidence.
    - [ ] Resolve contributor-controlled defects through regression-first fixes.
    - **Acceptance:** the frozen compatibility matrix is green or release remains blocked.
    - **Evidence:** `V1_QUALIFICATION_MATRIX.md` records all local suites as passing where runnable and preserves external, candidate-only, and independent-adoption blockers.
    - **BLOCKED (2026-07-15):** FOI-O release evidence, independent consumer evidence, and human selection/certification for pending profiles are unavailable; v1 remains blocked.
- [ ] Task: Review security, licensing, documentation, and claims
    - [ ] Recheck threat-model disposition, dependency advisories, licenses, source rights, and sensitive-data scans.
    - [ ] Match every README/release-note capability claim to evidence and scope limits.
    - **Acceptance:** no unresolved high/critical risk or unsupported capability claim remains.
    - **Evidence:** `V1_SECURITY_CLAIMS_REVIEW.md` records local checks and the remaining hosted-attestation, signing, rights, external-evidence, and human-authorization limits.
    - **BLOCKED (2026-07-17):** automated engineering-hardening evidence is complete, but external/live security evidence, hosted attestations, signing, and residual-risk certification remain open.
    - Current evidence refresh: `V1_SECURITY_CLAIMS_REVIEW.md` now references the current hardening threat model, validation baselines, SBOM, and supply-chain audit rather than the historical candidate artifact set.
- [ ] Task: [HUMAN] Approve v1.0 release candidate
    - [ ] Present complete gate, risk, compatibility, consumer, source, and publication-boundary packet.
    - [ ] Dylan approves release, requires fixes, or continues 0.x.
    - **Acceptance:** authorization is explicit and tied to an exact commit/artifact set.
    - **Packet:** `V1_RELEASE_AUTHORIZATION_PACKET.md` is prepared; no release authorization or publication action has been taken.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Qualification' (Protocol in workflow.md)
    - **BLOCKED (2026-07-17):** The qualification matrix and security review preserve unresolved FOI-O evidence, independent adoption, live-check, Project 14 verification, paper submission, Zenodo, signing, and human-certification gates. Do not promote, sign, publish, or archive v1.0 until those gates change state.

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

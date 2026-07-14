# Implementation Plan

GitHub issue: [edithatogo/foi-process#7](https://github.com/edithatogo/foi-process/issues/7).

Repository boundary: foi-process is a deterministic FOI event/replay/OCEL
implementation and evidence consumer. FOI-O owns FOI semantics;
`rac-conformance` owns PIC contracts; the proposed process-mappings repository
owns generic source-backed profiles and adapters.

## Phase 1 - Upstream Citation and Release Readiness

- [ ] Task: Prepare citation metadata in foi-process
    - [ ] Add and validate `CITATION.cff` against repository identity, authorship, license, and release metadata.
    - [ ] Document the integration-consumer boundary without claiming normative FOI or PIC ownership.
    - **Acceptance:** citation validation passes and metadata matches the repository's actual release target.
    - > BLOCKED (2026-07-14): Upstream repository work is tracked in issue #7; no `CITATION.cff` is present in the current release surface.
- [ ] Task: [HUMAN] Authorize and publish an immutable foi-process release
    - [ ] Review the release commit, changelog, citation metadata, and version.
    - [ ] Publish the approved tag and record immutable commit/tag evidence.
    - **Acceptance:** a public immutable release exists and its tag resolves to the approved commit.
    - > BLOCKED (2026-07-14): No version tag exists; release publication requires upstream maintainer authorization.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Upstream Citation and Release Readiness' (Protocol in workflow.md)

## Phase 2 - Programme Mirror and Preservation Evidence

- [ ] Task: Add the released repository to programme citation ledgers
    - [ ] Pin the released foi-process tag and commit in the FOI programme mirror manifest.
    - [ ] Record its implementation-consumer and operational-evidence role.
    - [ ] Verify that references do not make foi-process a runtime dependency or semantic authority.
    - **Acceptance:** mirror and citation checks resolve to the immutable upstream release.
- [ ] Task: [HUMAN] Enable and verify Zenodo preservation
    - [ ] Enable the repository in Zenodo and publish preservation for the approved release.
    - [ ] Verify version and concept DOI metadata against the GitHub release and `CITATION.cff`.
    - **Acceptance:** DOI records resolve publicly and all mirrored identifiers agree.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Programme Mirror and Preservation Evidence' (Protocol in workflow.md)

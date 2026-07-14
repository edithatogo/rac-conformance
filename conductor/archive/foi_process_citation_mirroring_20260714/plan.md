# Implementation Plan

GitHub issue: [edithatogo/foi-process#7](https://github.com/edithatogo/foi-process/issues/7).

Repository boundary: foi-process is a deterministic FOI event/replay/OCEL
implementation and evidence consumer. FOI-O owns FOI semantics;
`rac-conformance` owns PIC contracts; the proposed process-mappings repository
owns generic source-backed profiles and adapters.

## Phase 1 - Upstream Citation and Release Readiness

- [x] Task: Prepare citation metadata in foi-process
    - [x] Add and validate `CITATION.cff` against repository identity, authorship, license, and release metadata.
    - [x] Document the integration-consumer boundary without claiming normative FOI or PIC ownership.
    - **Acceptance:** citation validation passes and metadata matches the repository's actual release target.
- [x] Task: [HUMAN] Authorize and publish an immutable foi-process release
    - [x] Review the release commit, changelog, citation metadata, and version.
    - [x] Publish the approved tag and record immutable commit/tag evidence.
    - **Acceptance:** a public immutable release exists and its tag resolves to the approved commit.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Upstream Citation and Release Readiness' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): Upstream release `v0.1.0` is public and resolves to
> commit `2e635115f61e24d2e109d868119024a5591cce00`. `CITATION.cff` records the
> repository, Apache-2.0 license, version `0.1.0`, and release date. Hosted
> `contracts`, `dependency-policy`, `feature-matrix`, and both Rust checks passed.

## Phase 2 - Programme Mirror and Preservation Evidence

- [x] Task: Add the released repository to programme citation ledgers
    - [x] Pin the released foi-process tag and commit in the FOI programme mirror manifest.
    - [x] Record its implementation-consumer and operational-evidence role.
    - [x] Verify that references do not make foi-process a runtime dependency or semantic authority.
    - **Acceptance:** mirror and citation checks resolve to the immutable upstream release.
- [x] Task: [HUMAN] Enable and verify Zenodo preservation
    - [x] Enable the repository in Zenodo and publish preservation for the approved release.
    - [x] Verify version and concept DOI metadata against the GitHub release and `CITATION.cff`.
    - **Acceptance:** DOI records resolve publicly and all mirrored identifiers agree.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Programme Mirror and Preservation Evidence' (Protocol in workflow.md)

> CHECKPOINT (2026-07-15): Zenodo record `21359526` publishes `v0.1.0` at
> version DOI `10.5281/zenodo.21359526` and concept DOI
> `10.5281/zenodo.21359525`. Public metadata identifies the GitHub repository,
> Apache-2.0 license, and author ORCID `0000-0002-9775-0603`; the GitHub release
> resolves to commit `2e635115f61e24d2e109d868119024a5591cce00`. The programme
> citation validator passes with the release commit pinned in the manifest.

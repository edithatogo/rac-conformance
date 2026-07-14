# Implementation Plan

GitHub issue: [#50](https://github.com/edithatogo/rac-conformance/issues/50).
Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39)
Phase 1 and establishes the implementation home required by
[#40](https://github.com/edithatogo/rac-conformance/issues/40).

## Phase 1 - Incubator Boundary and Scaffold

> CHECKPOINT (2026-07-14): The tracked, non-canonical incubator now defines
> standalone product, safety, source, licensing, repository, and Conductor boundaries and
> contains explicit empty homes for the three initial profiles and Camunda
> adapter. It contains no nested Git repository, substantive mapping, runtime
> dependency, or remote/canonical claim. `make check` passed. Contract
> consumption and extraction remain deferred to later phases and human gates.

- [x] Task: Establish the tracked incubator boundary
    - [x] Add standalone product, repository-boundary, status, safety, and source-governance documents.
    - [x] State that the subtree is non-canonical, contains no nested `.git`, and cannot be published independently before cutover.
    - [x] Define `rac-conformance`, `foi-o`, `foi-process`, and `process-mappings` responsibilities.
    - **Acceptance:** an implementer can determine where every normative, semantic, execution, evidence, and mapping artifact belongs.
- [x] Task: Scaffold domain and adapter homes
    - [x] Create explicit homes for FOI compatibility, adverse incidents/open disclosure, health-technology pathways, and Camunda adapters.
    - [x] Add source, schema-reference, and test boundaries without claiming mappings are implemented.
    - [x] Prohibit real health data, inferred confidential facts, and AI-certified controlling evidence.
    - **Acceptance:** the scaffold is empty of substantive mappings but ready for independently reviewable track outputs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Incubator Boundary and Scaffold' (Protocol in workflow.md)

## Phase 2 - Parent Integration and Contract Discipline

- [x] Task: Wire parent roadmap and repository boundaries
    - [x] Insert this track between the v1 foundation and process-profile implementation.
    - [x] Add `foi-process` as a current implementation/evidence consumer and the incubator as a provisional repository home.
    - [x] Update tracks #40-#43 with exact normative and implementation paths.
    - **Acceptance:** local and GitHub dependency graphs agree and no existing repository is repurposed ambiguously.
- [ ] Task: Define released-contract consumption and compatibility tests
    - [ ] Pin the process-profile contract version or commit consumed from `rac-conformance`.
    - [ ] Validate profiles against upstream schemas without copying normative definitions.
    - [ ] Add compatibility-matrix and provenance checks for FOI-O and foi-process inputs.
    - **Acceptance:** drift is detected deterministically and cannot silently fork PIC or FOI semantics.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Parent Integration and Contract Discipline' (Protocol in workflow.md)

## Phase 3 - Extraction Rehearsal and Governance Packet

- [ ] Task: Build and test the extraction procedure
    - [ ] Preserve subtree history and verify file, commit, and license integrity.
    - [ ] Rehearse standalone CI, local installation, links, provenance checks, and dependency updates in a temporary local repository.
    - [ ] Define rollback and prevent simultaneous writable parent and extracted copies.
    - **Acceptance:** the rehearsal is reproducible and produces an auditable evidence report without creating a remote.
- [ ] Task: Prepare GitHub repository and migration packet
    - [ ] Draft repository description, topics, license, CODEOWNERS, issue/PR templates, security policy, branch protection, required checks, and Project 19 linkage.
    - [ ] Map parent issues/subissues to destination issues without losing cross-references.
    - [ ] Record owner, canonical URL, archive/reference behavior, release policy, and initial versioning proposal.
    - **Acceptance:** all authenticated or human actions are itemized and no remote-side fact is invented.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Extraction Rehearsal and Governance Packet' (Protocol in workflow.md)

## Phase 4 - Human Cutover and Parent Closeout

- [ ] Task: [HUMAN] Approve repository creation and canonical cutover
    - [ ] Review extraction evidence, ownership, visibility, governance, security, issue migration, and rollback plan.
    - [ ] Approve, defer, or reject creation of `edithatogo/process-mappings`.
    - **Acceptance:** the decision and any conditions are recorded before remote creation or canonical-home changes.
- [ ] Task: Execute approved extraction and verify hosted controls
    - [ ] Create and populate the remote only after approval, then configure approved protections and Project linkage.
    - [ ] Run required hosted checks and independently clone/test the extracted repository.
    - [ ] Record immutable migration commit and source-tree provenance.
    - **Acceptance:** the approved remote is reproducible, protected, and green; otherwise rollback is executed.
- [ ] Task: Close the parent incubator without dual ownership
    - [ ] Remove the writable subtree or replace it with an intentional read-only reference after all parent consumers use the canonical remote.
    - [ ] Update roadmap, issues, links, source manifests, and repository-boundary documentation.
    - [ ] Verify no automation writes to the retired location.
    - **Acceptance:** exactly one canonical writable source remains and parent checks pass.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Human Cutover and Parent Closeout' (Protocol in workflow.md)

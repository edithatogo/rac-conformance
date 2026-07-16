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

> CHECKPOINT (2026-07-15): The incubator now consumes the merged
> `pic-process-profile/0.1.0` contract through a full commit and schema digest
> pin. A deterministic validator checks the pinned schema, candidate source
> manifest, local FOI-O/foi-process evidence paths, and valid contract examples;
> drift fails `make check`. No normative schema is copied and no remote
> repository is created. Phase 3 extraction rehearsal remains pending.

- [x] Task: Wire parent roadmap and repository boundaries
    - [x] Insert this track between the v1 foundation and process-profile implementation.
    - [x] Add `foi-process` as a current implementation/evidence consumer and the incubator as a provisional repository home.
    - [x] Update tracks #40-#43 with exact normative and implementation paths.
    - **Acceptance:** local and GitHub dependency graphs agree and no existing repository is repurposed ambiguously.
- [x] Task: Define released-contract consumption and compatibility tests
    - [x] Pin the process-profile contract version or commit consumed from `rac-conformance`.
    - [x] Validate profiles against upstream schemas without copying normative definitions.
    - [x] Add compatibility-matrix and provenance checks for FOI-O and foi-process inputs.
    - Evidence: `subrepos/process-mappings/contracts/consumption.json`,
      `contracts/tools/src/pic_contracts/process_mappings_consumption.py`, and
      `contracts/tools/tests/test_process_mappings_consumption.py`.
    - **Acceptance:** drift is detected deterministically and cannot silently fork PIC or FOI semantics.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Parent Integration and Contract Discipline' (Protocol in workflow.md)

## Phase 3 - Extraction Rehearsal and Governance Packet

> CHECKPOINT (2026-07-15): The extraction procedure now produces an auditable
> local report covering tracked-tree provenance, license transfer, temporary
> standalone Git commit and clone, link and source-manifest checks, rollback,
> and the explicit no-remote boundary. The migration packet drafts destination
> metadata, issue cross-references, hosted controls, versioning, and cutover
> conditions without inventing remote state. Remote creation and canonical
> cutover remain human-gated.

- [x] Task: Build and test the extraction procedure
    - [x] Preserve subtree history and verify file, commit, and license integrity.
    - [x] Rehearse standalone CI, local installation, links, provenance checks, and dependency updates in a temporary local repository.
    - [x] Define rollback and prevent simultaneous writable parent and extracted copies.
    - Evidence: `tools/process_mappings_rehearsal.py`,
      `tools/tests/test_process_mappings_rehearsal.py`, and
      `subrepos/process-mappings/migration/REHEARSAL_REPORT.json`.
    - **Acceptance:** the rehearsal is reproducible and produces an auditable evidence report without creating a remote.
- [x] Task: Prepare GitHub repository and migration packet
    - [x] Draft repository description, topics, license, CODEOWNERS, issue/PR templates, security policy, branch protection, required checks, and Project 19 linkage.
    - [x] Map parent issues/subissues to destination issues without losing cross-references.
    - [x] Record owner, canonical URL, archive/reference behavior, release policy, and initial versioning proposal.
    - Evidence: `subrepos/process-mappings/migration/GITHUB_MIGRATION_PACKET.md`.
    - **Acceptance:** all authenticated or human actions are itemized and no remote-side fact is invented.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Extraction Rehearsal and Governance Packet' (Protocol in workflow.md)

## Phase 4 - Deferred Cutover and Parent Closeout

> CHECKPOINT (2026-07-16): The human decision is to defer creation of
> `edithatogo/process-mappings`. The structured subrepo remains the sole
> writable source, and the migration packet plus extraction rehearsal are
> retained for reconsideration when a second mature domain or independent
> consumer justifies a separate release lifecycle. No remote, destination
> issues, redirects, or hosted settings were created. Parent checks remain the
> active verification gate.
>
> Review (2026-07-16): Found and fixed one extracted-clone portability defect
> where `STATUS.md` linked to a parent-only decision file. The local decision
> mirror in `subrepos/process-mappings/migration/` now makes the subtree
> link-complete. Focused rehearsal tests and full `make check` pass.

- [x] Task: [HUMAN] Record decision to defer repository creation and canonical cutover
    - [x] Review extraction evidence, ownership, visibility, governance, security, issue migration, and rollback plan.
    - [x] Defer creation of `edithatogo/process-mappings` until the reconsideration triggers in `migration/DEFERRED_CUTOVER_DECISION.md` are met.
    - Prepared source portability evidence: `subrepos/process-mappings/profiles/foi/SOURCE_REFERENCE_PORTABILITY.json` pins the four current FOI-O references and records byte equality without certifying legal or semantic authority.
    - **Acceptance:** the decision and its reconsideration conditions are recorded before any remote-side action.
- [x] Task: [DEFERRED] Execute extraction and verify hosted controls
    - [x] No remote or hosted control is created while the cutover is deferred.
    - [x] Preserve the extraction rehearsal and rollback evidence for future reconsideration.
    - **Acceptance:** no remote-side action occurs and the parent remains the sole writable source.
- [x] Task: Retain the parent incubator as the sole writable source
    - [x] Keep `subrepos/process-mappings/` as the maintained implementation home.
    - [x] State that future changes must land through `rac-conformance` until a new cutover decision.
    - [x] Preserve the future migration packet without creating destination issues or redirects.
    - **Acceptance:** exactly one writable source remains and parent checks continue to pass.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Deferred Cutover and Parent Closeout' (Protocol in workflow.md)

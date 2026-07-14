# Implementation Plan

GitHub issue: [#39](https://github.com/edithatogo/rac-conformance/issues/39).

## Phase 1 - Product Boundary

- [ ] Task: Define v1 normative and optional surfaces
    - [ ] Inventory every public schema, CLI, library, generated artifact, study interface, and adapter.
    - [ ] Classify each as core, optional profile, jurisdiction profile, adapter, experimental, or internal.
    - [ ] Record explicit v1 non-goals and prohibited claims.
    - **Acceptance:** every public surface has one owner, stability class, and support posture.
- [ ] Task: Define conformance levels and evidence semantics
    - [ ] Separate syntactic, semantic, execution, trace, source, and independently certified conformance.
    - [ ] Define pass, fail, blocked, exception, and not-applicable states.
    - [ ] Prohibit legal, clinical, funding, and standards-body claims from conformance badges.
    - **Acceptance:** each level has deterministic tests and required evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Product Boundary' (Protocol in workflow.md)

## Phase 2 - Lifecycle Policies

- [ ] Task: Publish compatibility and migration policy
    - [ ] Define SemVer treatment for each PIC contract and the aggregate toolkit.
    - [ ] Define canonical serialization, identifier stability, and CLI compatibility promises.
    - [ ] Define deprecation notice periods and migration-artifact requirements.
    - **Acceptance:** representative compatible and breaking changes are classified by tests.
- [ ] Task: Publish support, maintenance, and security policy
    - [ ] Define supported Python/platform versions and maintenance windows.
    - [ ] Define vulnerability intake, embargo, patch, and end-of-support behavior.
    - [ ] Define maintainer succession and release authority.
    - **Acceptance:** policies have named owners and observable response targets.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lifecycle Policies' (Protocol in workflow.md)

## Phase 3 - Release Gate Control Plane

- [ ] Task: Write release-gate manifest tests
    - [ ] Add invalid cases for missing evidence, self-certified adoption, stale evidence, and ambiguous gate status.
    - [ ] Add valid blocked and fully satisfied examples.
    - **Acceptance:** tests fail before validator implementation.
- [ ] Task: Implement machine-readable v1 gate manifest and validator
    - [ ] Record gate owner, dependencies, evidence URLs/digests, observation time, and status.
    - [ ] Produce a deterministic human-readable report.
    - [ ] Integrate validation into `make check`.
    - **Acceptance:** local success cannot convert external or human gates to pass.
- [ ] Task: Reconcile existing programme gates
    - [ ] Link FOI-O release, external adoption, papers, Zenodo, and governance items without duplicating their source-of-truth plans.
    - [ ] Update Project 19 from the local manifest.
    - **Acceptance:** no existing gate is silently weakened or counted twice.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Release Gate Control Plane' (Protocol in workflow.md)

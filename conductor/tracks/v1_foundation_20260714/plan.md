# Implementation Plan

GitHub issue: [#39](https://github.com/edithatogo/rac-conformance/issues/39).

## Phase 1 - Product Boundary

- [x] Task: Define v1 normative and optional surfaces
    - [x] Inventory every public schema, CLI, library, generated artifact, study interface, and adapter.
    - [x] Classify each as core, optional profile, jurisdiction profile, adapter, experimental, or internal.
    - [x] Record explicit v1 non-goals and prohibited claims.
    - **Acceptance:** every public surface has one owner, stability class, and support posture.
    - **Evidence:** `docs/V1_SCOPE.md` inventories the current contracts, tools, profiles, adapters, studies, demos, generated artifacts, and internal materials, with explicit v1 non-goals and prohibited claims.
- [x] Task: Define conformance levels and evidence semantics
    - [x] Separate syntactic, semantic, execution, trace, source, and independently certified conformance.
    - [x] Define pass, fail, blocked, exception, and not-applicable states.
    - [x] Prohibit legal, clinical, funding, and standards-body claims from conformance badges.
    - **Acceptance:** each level has deterministic tests and required evidence.
    - **Evidence:** `docs/V1_CONFORMANCE.md` defines the six cumulative levels, five machine-readable evidence states, independence requirements, required evidence, and prohibited claims.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Product Boundary' (Protocol in workflow.md)
    - **Review:** Phase 1 review found and fixed stale unchecked sub-items in this plan; no scope or implementation defect remained.

> CHECKPOINT (2026-07-15): `docs/V1_SCOPE.md` classifies the current public and internal surfaces, assigns owners and support postures, and records v1 non-goals. `docs/V1_CONFORMANCE.md` defines cumulative syntactic, semantic, execution, trace, source, and independently certified levels plus deterministic evidence states. Full `make check` passed after both documentation tasks. External adoption, source certification, human certification, and publication gates remain separate and are not claimed by this phase.

## Phase 2 - Lifecycle Policies

- [x] Task: Publish compatibility and migration policy
    - [x] Define SemVer treatment for each PIC contract and the aggregate toolkit.
    - [x] Define canonical serialization, identifier stability, and CLI compatibility promises.
    - [x] Define deprecation notice periods and migration-artifact requirements.
    - **Acceptance:** representative compatible and breaking changes are classified by tests.
    - **Evidence:** `docs/V1_COMPATIBILITY.md` defines independent package versioning, serialization and identifier stability, CLI compatibility, deprecation periods, and migration artifacts.
- [x] Task: Publish support, maintenance, and security policy
    - [x] Define supported Python/platform versions and maintenance windows.
    - [x] Define vulnerability intake, embargo, patch, and end-of-support behavior.
    - [x] Define maintainer succession and release authority.
    - **Acceptance:** policies have named owners and observable response targets.
    - **Evidence:** `docs/V1_SUPPORT_SECURITY.md` defines the tested baseline, maintenance window, private vulnerability intake, response targets, patch workflow, and succession rules.
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

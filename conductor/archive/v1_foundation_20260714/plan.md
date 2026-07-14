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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lifecycle Policies' (Protocol in workflow.md)
    - **Review:** Phase 2 review found no policy contradiction after splitting the two task commits; compatibility and support evidence are explicit and repository-local.

> CHECKPOINT (2026-07-15): `docs/V1_COMPATIBILITY.md` preserves independently versioned PIC contracts, canonical serialization, identifier stability, CLI behavior, deprecation periods, and migration evidence. `docs/V1_SUPPORT_SECURITY.md` records the tested support baseline, maintenance window, vulnerability response targets, and succession controls. Full `make check` passed after each policy task. External security reports, release deposits, and independent certifications remain external or human-gated.

## Phase 3 - Release Gate Control Plane

- [x] Task: Write release-gate manifest tests
    - [x] Add invalid cases for missing evidence, self-certified adoption, stale evidence, and ambiguous gate status.
    - [x] Add valid blocked and fully satisfied examples.
    - **Acceptance:** tests fail before validator implementation.
    - **Evidence:** `tools/tests/test_release_gates.py` and its six JSON fixtures define the required red/green corpus; the targeted test run failed before `tools.release_gates` existed.
- [x] Task: Implement machine-readable v1 gate manifest and validator
    - [x] Record gate owner, dependencies, evidence URLs/digests, observation time, and status.
    - [x] Produce a deterministic human-readable report.
    - [x] Integrate validation into `make check`.
    - **Acceptance:** local success cannot convert external or human gates to pass.
    - **Evidence:** `conductor/v1-release-gates.json` is validated by `tools/release_gates.py` and the `release-gates-check` Make target; the manifest retains external and human gates as `blocked`.
- [x] Task: Reconcile existing programme gates
    - [x] Link FOI-O release, external adoption, papers, Zenodo, and governance items without duplicating their source-of-truth plans.
    - [x] Update Project 19 from the local manifest.
    - **Acceptance:** no existing gate is silently weakened or counted twice.
    - **Evidence:** `conductor/v1-release-gates.json` links gate records to FOI-O #27, RaC #23/#31/#33/#30, and leaves their source-of-truth statuses authoritative; Track #39 is In Progress in Project 19.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Release Gate Control Plane' (Protocol in workflow.md)
    - **Review:** Phase 3 review found no gate-state weakening or duplicate source-of-truth ownership; the manifest validator was added to `make check` and retains blocked external/human gates.

> CHECKPOINT (2026-07-15): The release-gate corpus covers invalid missing evidence, self-certified adoption, stale evidence, and ambiguous status, plus valid blocked and fully satisfied manifests. `tools/release_gates.py` produces deterministic reports and `conductor/v1-release-gates.json` records FOI-O, adoption, papers, Zenodo, and governance dependencies with source issue links. Full `make check` passed, and Track #39 is In Progress in Project 19. External deposits, independent adoption, and FOI-O evidence remain blocked rather than locally certified.

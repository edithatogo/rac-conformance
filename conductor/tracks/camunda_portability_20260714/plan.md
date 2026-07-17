# Implementation Plan

GitHub issue: [#43](https://github.com/edithatogo/rac-conformance/issues/43). Depends on [#40](https://github.com/edithatogo/rac-conformance/issues/40) and one certified demonstrator from [#41](https://github.com/edithatogo/rac-conformance/issues/41) or [#42](https://github.com/edithatogo/rac-conformance/issues/42).

Implementation home: `subrepos/process-mappings/adapters/camunda/` during the
repository incubation governed by
[#50](https://github.com/edithatogo/rac-conformance/issues/50).

## Phase 1 - Architecture and Reproducibility

- [x] Task: Record Camunda adapter architecture decision
    - [x] Verify current official BPMN, connector/job-worker, Process Test, clock, audit, and migration capabilities.
    - [x] Choose the smallest supported local runtime and exact version.
    - [x] Define rule-worker, human-task, trace, error, credential, and data boundaries.
    - **Acceptance:** the decision explains why Camunda is optional and identifies unsupported assumptions.
    - **Evidence:** `ARCHITECTURE_DECISION.md` and `VERSION_LOCK.json` select an optional Java 17, Camunda 8.9.12, Maven, and Testcontainers boundary; unsupported assumptions and core isolation are explicit.
- [x] Task: Scaffold reproducible adapter test module
    - [x] Create the module under `subrepos/process-mappings/adapters/camunda/` without adding Java, Docker, or Camunda dependencies to PIC core.
    - [x] Pin Java/build/Testcontainers/Camunda dependencies and container images.
    - [x] Add offline-friendly dependency and image documentation.
    - [x] Add a smoke test and CI job that can be disabled only with an explicit environment reason.
    - **Acceptance:** clean setup and teardown leave no committed runtime state.
    - **Evidence:** the isolated Maven module, committed BPMN, smoke test, version lock, and `.github/workflows/camunda-adapter.yml` passed the hosted adapter jobs recorded by commits `de49562` and `541a63f`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Architecture and Reproducibility' (Protocol in workflow.md)
    - **CHECKPOINT (2026-07-15):** Architecture and the reproducible optional scaffold are implemented. PIC core remains Camunda-independent.

## Phase 2 - Executable Mapping

- [ ] Task: Write BPMN and adapter contract tests
    - [ ] Assert stable element IDs, variable schemas, correlation IDs, task kinds, and error contracts.
    - [ ] Add negative tests for rule duplication, missing human task, unbounded retry, and untyped variables.
    - [ ] Add controlled-clock timer cases.
    - **Acceptance:** tests fail before model/worker implementation.
- [x] Task: Implement BPMN process and deterministic rule boundary
    - [x] Map one certified demonstrator to BPMN with expected-result gateways and technical-error boundaries.
    - [x] Invoke the PIC/rule service by job worker or REST connector.
    - [x] Keep clinical/legal/funding judgement in explicit user tasks.
    - **Acceptance:** normal and exception paths execute deterministically.
    - **Evidence:** `PicRuleWorkerBoundary`, the BPMN model, contract tests, and worker tests implement the bounded deterministic worker slice recorded by commit `624506f`.
- [ ] Task: Implement normalized trace projection
    - [ ] Map Camunda process, element, task, incident, timer, and operation events to PIC trace records.
    - [ ] Exclude secrets and sensitive variables.
    - [ ] Emit explicit representational-loss records.
    - **Acceptance:** repeated runs produce canonical-equal normalized traces.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Executable Mapping' (Protocol in workflow.md)

> DEFERRED CHECKPOINT (2026-07-17): The architecture, isolated scaffold, and
> deterministic worker boundary are retained as implemented evidence.
> Controlled-clock contract execution, normalized trace projection, migration,
> workload experiments, reconciliation, and packaging remain deferred under
> `conductor/DEFERRED_ROADMAP.md` until the certified-demonstrator and named
> portability-question re-entry conditions are met.

## Phase 3 - Lifecycle and Operational Evidence

- [ ] Task: Test versioning and active-instance migration
    - [ ] Define compatible, migration-required, and unsupported model changes.
    - [ ] Test active wait-state migration and audit-history preservation as supported.
    - [ ] Fail safely for unsupported migration plans.
    - **Acceptance:** no migration success is claimed from model deployment alone.
- [ ] Task: Add deterministic workload experiments
    - [ ] Separate conformance scenarios from seeded queue, delay, retry, and SLA experiments.
    - [ ] Record seed, workload, runtime, environment, and non-generalisation caveats.
    - [ ] Do not convert operational simulation into legal or policy correctness evidence.
    - **Acceptance:** results are reproducible and clearly labeled non-normative.
- [ ] Task: Reconcile Camunda and native demonstrator traces
    - [ ] Compare normalized traces and classify expected platform differences, adapter defects, profile gaps, and unresolved cases.
    - [ ] Feed justified profile gaps back through normal contract change control.
    - **Acceptance:** no profile change is made solely to hide an adapter defect.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Lifecycle and Operational Evidence' (Protocol in workflow.md)

## Phase 4 - Review and Packaging

- [ ] Task: Run security, license, portability, and full CI review
    - [ ] Scan dependencies/images, verify licenses, run process tests, and run `make check`.
    - [ ] Verify core installation and tests remain Camunda-independent.
    - **Acceptance:** all required checks pass or exact external runtime blockers are documented.
- [ ] Task: Publish adapter guide and evidence packet
    - [ ] Document supported scope, setup, mappings, test coverage, trace loss, migration limits, and teardown.
    - [ ] Include generated diagrams only as non-normative views of committed BPMN.
    - **Acceptance:** another implementer can reproduce the experiment without undocumented services.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Review and Packaging' (Protocol in workflow.md)

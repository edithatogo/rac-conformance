# Implementation Plan

Depends on: `repo_boundaries_20260706` Phase 2 and `adoption_closure_20260706` Phase 1.

## Phase 1 - Demo Architecture

- [x] Task: Confirm demo surfaces
    - [x] Re-read `external/docassemble/ASSESSMENT.md` and `external/civiform/ASSESSMENT.md`.
    - [x] Select exact local paths for demo artifacts.
    - [x] Define request/response JSON examples.
    - **Acceptance:** `demos/service-boundaries/DESIGN.md` defines both demos and their limits.
- [x] Task: Write schema/tests first
    - [x] Add request/response validation tests.
    - [x] Add trace-presence tests.
    - **Acceptance:** tests fail before implementation.

> CHECKPOINT (2026-07-07): The service-boundary design now names exact Docassemble-style and CiviForm-style demo artifacts under `demos/service-boundaries/`, and the committed examples define both request and response payloads.
> The shared demo helper exercises the staged OIA rules module, and the new tests cover request validation, response shape, and trace presence.
> `make check` passed, while the actual README instructions, privacy review, and outreach packet remain deferred to later phases.

- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Demo Architecture' (Protocol in workflow.md)

## Phase 2 - OIA/Docassemble Demo

- [ ] Task: Implement Docassemble-style OIA invocation demo
    - [ ] Build a small local runner using the staged OIA rules module.
    - [ ] Include representative interview input and rule result output.
    - [ ] Add README instructions.
    - **Acceptance:** demo test calculates expected OIA deadline and emits trace fields.
- [ ] Task: Validate no process coupling regression
    - [ ] Confirm the rules module does not import unrelated `foi-o` process code.
    - [ ] Run relevant OIA tests and `pic-validate`.
    - **Acceptance:** import isolation and validation pass.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - OIA/Docassemble Demo' (Protocol in workflow.md)

## Phase 3 - CiviForm-Style Service Mock

- [ ] Task: Implement HTTP or CLI service-boundary mock
    - [ ] Accept a JSON application payload.
    - [ ] Call a PIC-tested rule function.
    - [ ] Return a PIC-shaped result and trace summary.
    - **Acceptance:** integration test covers valid and invalid requests.
- [ ] Task: Document CiviForm path
    - [ ] State what a real CiviForm integration would require.
    - [ ] Record whether Java/plugin work is justified.
    - **Acceptance:** README prevents overclaiming production readiness.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - CiviForm-Style Service Mock' (Protocol in workflow.md)

## Phase 4 - CI And External Packaging

- [ ] Task: Privacy/security review
    - [ ] Confirm no real applicant/requester data is committed.
    - [ ] Confirm no secrets, tokens, or live service credentials are required.
    - [ ] Confirm tests mock external calls.
    - [ ] Confirm trace outputs are minimal and do not leak unnecessary private inputs.
    - **Acceptance:** review checklist is committed and all items pass or are blocked.
- [ ] Task: Add checks to `make check`
    - [ ] Include demo tests without requiring external services.
    - [ ] Keep fixtures deterministic.
    - **Acceptance:** `make check` passes locally.
- [ ] Task: Prepare outreach/update packet
    - [ ] Draft update for DBN/Docassemble/CiviForm only if demo is credible.
    - [ ] Mark sending/posting as `[HUMAN]`.
    - **Acceptance:** packet is staged or explicitly deferred.
- [ ] Task: Push branch and monitor GitHub Actions
    - [ ] Push after local green checks.
    - [ ] Apply fixes for failing Actions.
    - **Acceptance:** branch Actions pass or exact blocker is recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - CI And External Packaging' (Protocol in workflow.md)

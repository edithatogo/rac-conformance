# Implementation Plan

Depends on: `repo_boundaries_20260706` Phase 1. Use `conductor/edithatogo-repo-boundaries.md` before touching any external repo.

## Phase 1 - Adoption Inventory

- [ ] Task: Build adoption ledger
    - [ ] Read every `external/*/SUBMISSION*.md`, `external/dbn/LOG.md`, and archived plan checkpoint that mentions upstream submission.
    - [ ] Create `external/ADOPTION_STATUS.md` with target, artifact, status, URL, CI state, owner, and next action columns.
    - [ ] Mark unknown external status as `needs_verification`, not complete.
    - **Acceptance:** every staged external artifact has one ledger row.
- [ ] Task: Verify live external state
    - [ ] Use GitHub CLI/API for issue/PR state where available.
    - [ ] Check DBN log and any available mailbox/thread evidence only when the relevant connector/tool is available and authorized.
    - [ ] Record exact URLs or "not found / not accessible".
    - **Acceptance:** no row remains uninspected unless access is blocked and logged.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Adoption Inventory' (Protocol in workflow.md)

## Phase 2 - Patch-Ready External Bundles

- [ ] Task: Prepare `foi-o` PR bundle
    - [ ] Confirm local `foi-o` branch status before editing.
    - [ ] Apply the staged OIA rules module into the `foi-o` checkout or refresh the patch bundle, respecting existing user changes.
    - [ ] Run `foi-o` tests relevant to the rules module.
    - [ ] Commit in the external repo only if changes are authorized and scoped.
    - **Acceptance:** PR-ready branch or patch bundle exists; CI/test command output is logged.
- [ ] Task: Prepare PolicyEngine/OpenFisca issue and PR follow-through
    - [ ] Verify whether trace, missingness, and converter submissions are already open.
    - [ ] If not open, prepare final issue/PR text and mark `[HUMAN]` submission gate.
    - [ ] If open, monitor responses and apply requested documentation/code fixes in this repo or external repo as appropriate.
    - **Acceptance:** every PolicyEngine/OpenFisca artifact has live URL, human gate, or blocked reason.
- [ ] Task: Prepare Alaveteli follow-through
    - [ ] Verify whether the Alaveteli state-taxonomy discussion/issue exists.
    - [ ] If not, prepare final discussion text and mark `[HUMAN]` submission gate.
    - [ ] If open, record response and next action.
    - **Acceptance:** Alaveteli status is not ambiguous.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Patch-Ready External Bundles' (Protocol in workflow.md)

## Phase 3 - CI, Review, And Merge Closure

- [ ] Task: Monitor active PRs and GitHub Actions
    - [ ] For every live PR, record latest commit SHA, required checks, pass/fail state, and reviewer state.
    - [ ] Apply fixes for failing checks where the agent has push authority.
    - [ ] Commit each fix with the external repo's conventions.
    - **Acceptance:** all agent-addressable CI failures are fixed or precisely blocked.
- [ ] Task: [HUMAN] Merge or maintainer-response gate
    - [ ] Present merge-ready PRs and external-response queue to Dylan.
    - [ ] Record which PRs Dylan merges, which require maintainer review, and which are intentionally deferred.
    - **Acceptance:** no PR is represented as merged without URL evidence.
- [ ] Task: Update adoption ledger and README summary
    - [ ] Refresh `external/ADOPTION_STATUS.md`.
    - [ ] Add a short status pointer in `README.md` or `conductor/tracks.md` if appropriate.
    - **Acceptance:** repo-local documentation matches live external state.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - CI, Review, And Merge Closure' (Protocol in workflow.md)

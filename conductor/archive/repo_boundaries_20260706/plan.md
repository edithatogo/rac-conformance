# Implementation Plan

## Phase 1 - Boundary Catalog

- [x] Task: Verify repository inventory
    - [x] Read `gh repo list edithatogo --limit 200` output or equivalent GitHub source.
    - [x] Cross-check local checkouts under `/Volumes/PortableSSD/GitHub` for relevant working copies.
    - [x] Record any inaccessible private/ambiguous repos as unknown rather than inferring scope.
    - **Acceptance:** inventory evidence is summarized in the checkpoint.
- [x] Task: Finalize `conductor/edithatogo-repo-boundaries.md`
    - [x] Confirm each repo is assigned to exactly one boundary class.
    - [x] Add entry conditions for all potentially relevant repos.
    - [x] Add hard boundary rules for external PR/merge authority.
    - **Acceptance:** document has current, potential, not-relevant, and external-target sections.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Boundary Catalog' (Protocol in workflow.md)


## Phase 2 - Enforcement Hooks

- [x] Task: Add boundary references to roadmap tracks
    - [x] Update active track specs to cite `conductor/edithatogo-repo-boundaries.md` where cross-repo work is planned.
    - [x] Ensure each spec names the allowed target repositories and excludes unrelated repos.
    - **Acceptance:** no active spec has an unbounded "search all repos" instruction.
- [x] Task: Add lightweight lint or review checklist
    - [x] Prefer a markdown checklist if code would be overkill.
    - [x] If code is added, write tests first and include it in `make check`.
    - **Acceptance:** future track reviews have an explicit repo-boundary check.
- [x] Task: Verify GitHub planning boundaries
    - [x] Read `conductor/github-planning.md`.
    - [x] Confirm GitHub issues/project items point back to local track paths.
    - [x] Confirm no GitHub issue asks agents to edit an out-of-scope repo without a boundary update.
    - **Acceptance:** GitHub mirror cannot bypass repo-boundary rules.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Enforcement Hooks' (Protocol in workflow.md)

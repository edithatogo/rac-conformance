# Implementation Plan

## Phase 1 - Boundary Catalog

- [ ] Task: Verify repository inventory
    - [ ] Read `gh repo list edithatogo --limit 200` output or equivalent GitHub source.
    - [ ] Cross-check local checkouts under `/Volumes/PortableSSD/GitHub` for relevant working copies.
    - [ ] Record any inaccessible private/ambiguous repos as unknown rather than inferring scope.
    - **Acceptance:** inventory evidence is summarized in the checkpoint.
- [ ] Task: Finalize `conductor/edithatogo-repo-boundaries.md`
    - [ ] Confirm each repo is assigned to exactly one boundary class.
    - [ ] Add entry conditions for all potentially relevant repos.
    - [ ] Add hard boundary rules for external PR/merge authority.
    - **Acceptance:** document has current, potential, not-relevant, and external-target sections.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Boundary Catalog' (Protocol in workflow.md)

## Phase 2 - Enforcement Hooks

- [ ] Task: Add boundary references to roadmap tracks
    - [ ] Update active track specs to cite `conductor/edithatogo-repo-boundaries.md` where cross-repo work is planned.
    - [ ] Ensure each spec names the allowed target repositories and excludes unrelated repos.
    - **Acceptance:** no active spec has an unbounded "search all repos" instruction.
- [ ] Task: Add lightweight lint or review checklist
    - [ ] Prefer a markdown checklist if code would be overkill.
    - [ ] If code is added, write tests first and include it in `make check`.
    - **Acceptance:** future track reviews have an explicit repo-boundary check.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Enforcement Hooks' (Protocol in workflow.md)

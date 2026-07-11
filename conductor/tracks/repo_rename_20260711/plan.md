# Plan: repo_rename_20260711

## Phase 1 - Inventory and migration contract

- [ ] Task: Classify every old repository URL as canonical-current or persistent-historical
    - [ ] Add a machine-readable/link-audit allowlist for intentionally retained schema IDs
    - [ ] Add regression tests for canonical current URLs and retained historical IDs
- [ ] Task: Conductor - Automated Review and Checkpoint 'Inventory and migration contract' (Protocol in workflow.md)

## Phase 2 - Rename and local migration

- [ ] Task: Rename the GitHub repository and update local remotes
- [ ] Task: Update current repository metadata, documentation, papers, and operational links
- [ ] Task: Conductor - Automated Review and Checkpoint 'Rename and local migration' (Protocol in workflow.md)

## Phase 3 - External verification

- [ ] Task: Verify redirects, clone/fetch, issue links, Projects, and all GitHub Actions
- [ ] Task: Record downstream links that rely on GitHub redirects and need optional future cleanup
- [ ] Task: Conductor - Automated Review and Checkpoint 'External verification' (Protocol in workflow.md)

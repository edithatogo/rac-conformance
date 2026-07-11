# Plan: repo_rename_20260711

## Phase 1 - Inventory and migration contract

- [x] Task: Classify every old repository URL as canonical-current or persistent-historical
    - [x] Add a machine-readable/link-audit allowlist for intentionally retained schema IDs
    - [x] Add regression tests for canonical current URLs and retained historical IDs
- [x] Task: Conductor - Automated Review and Checkpoint 'Inventory and migration contract' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Current links use `rac-conformance`; published schema IDs and the identity policy are the only intentional legacy references. Redirects resolve to the new repository, `git ls-remote origin HEAD` succeeds, and the new-repository Actions runs are green. The audit initially caught its own legacy rule and an issue-template URL; both were corrected.

## Phase 2 - Rename and local migration

- [x] Task: Rename the GitHub repository and update local remotes
- [x] Task: Update current repository metadata, documentation, papers, and operational links
- [x] Task: Conductor - Automated Review and Checkpoint 'Rename and local migration' (Protocol in workflow.md)

## Phase 3 - External verification

- [x] Task: Verify redirects, clone/fetch, issue links, Projects, and all GitHub Actions
- [x] Task: Record downstream links that rely on GitHub redirects and need optional future cleanup
- [x] Task: Conductor - Automated Review and Checkpoint 'External verification' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Both old and new public URLs return 200 at the canonical new URL; local remote and `ls-remote` use `rac-conformance`; Quality, CodeQL, and prior Contracts runs pass. GitHub issue/project links resolve after the rename. Historical external links may continue through GitHub redirects.

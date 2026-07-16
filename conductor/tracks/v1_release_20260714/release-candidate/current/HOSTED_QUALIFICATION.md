# v1 Hosted Qualification Evidence

Status: automated qualification passed; human residual-risk and release
certification remain open.

## Qualification run

- Workflow: [v1 Qualification run 29476769764](https://github.com/edithatogo/rac-conformance/actions/runs/29476769764)
- Pull request: [#91](https://github.com/edithatogo/rac-conformance/pull/91)
- Tested source commit: `04ef0f918f8d356309fc453ddb4cf204af0319a0`
- Event: `pull_request`
- Result: `success`
- Retention: artifacts expire 2026-10-14 unless preserved by a release process.

## Matrix results

| Runner | Python | Result | Artifact |
| --- | --- | --- | --- |
| `ubuntu-latest` | 3.12 | pass | `v1-qualification-ubuntu-latest-py3.12` (artifact `8366853373`) |
| `ubuntu-latest` | 3.13 | pass | `v1-qualification-ubuntu-latest-py3.13` (artifact `8366853478`) |
| `macos-latest` | 3.12 | pass | `v1-qualification-macos-latest-py3.12` (artifact `8366855095`) |
| `macos-latest` | 3.13 | pass | `v1-qualification-macos-latest-py3.13` (artifact `8366853449`) |

Each matrix job passed `make check`, generated the validation baseline, fuzz,
mutation, reproducibility, and rollback reports, and uploaded all five JSON
artifacts.

The final documentation-bearing PR revision was independently rerun with the
same matrix:

- Workflow: [v1 Qualification run 29476864216](https://github.com/edithatogo/rac-conformance/actions/runs/29476864216)
- Tested source commit: `307b7d767d070b36a272ef78a5aaaef0d8326ae7`
- Result: `success`
- Artifacts: Ubuntu/Python 3.12 `8366887820`, Ubuntu/Python 3.13 `8366889878`,
  macOS/Python 3.12 `8366890389`, macOS/Python 3.13 `8366891290`
- Artifact expiry: 2026-10-14

## Companion hosted controls

The same pull request commit also passed:

- [Quality run 29476769786](https://github.com/edithatogo/rac-conformance/actions/runs/29476769786), including full check, workflow lint, and workflow security;
- [Contracts run 29476769773](https://github.com/edithatogo/rac-conformance/actions/runs/29476769773);
- [Dependency Review run 29476769769](https://github.com/edithatogo/rac-conformance/actions/runs/29476769769); and
- [CodeQL run 29476769781](https://github.com/edithatogo/rac-conformance/actions/runs/29476769781).

These results prove the stated automated checks for this pull-request commit.
They do not prove branch-protection configuration, secret-scanning settings,
protected environments, artifact signing, independent adoption, human source
certification, or v1 release authorization.

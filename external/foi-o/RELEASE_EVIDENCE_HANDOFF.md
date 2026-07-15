# FOI-O v0.8.1 release-evidence handoff

Status: candidate remediation only. This file is not an upstream release,
evidence bundle, or publication claim.

## Verified release input

- Repository: <https://github.com/edithatogo/foi-o>
- Tag: `v0.8.1`
- Commit: [`d24ae6f9f2d9488052969f633d91eff4a9a47f58`](https://github.com/edithatogo/foi-o/commit/d24ae6f9f2d9488052969f633d91eff4a9a47f58)
- Zenodo version DOI: [`10.5281/zenodo.21360138`](https://doi.org/10.5281/zenodo.21360138)
- Zenodo concept DOI: [`10.5281/zenodo.21360137`](https://doi.org/10.5281/zenodo.21360137)
- Evidence-bundle gate: <https://github.com/edithatogo/foi-o/issues/27>

## Immutable-tag validation

The tag was checked in a clean detached worktree with:

```bash
uv sync --extra dev --extra rdf
uv run pytest -q
```

Before remediation, the result was `278 passed, 2 skipped, 2 failed`. The
failures were stale inventory values in the coverage matrix and generated
maturation summary, not an unverified empirical result.

## Candidate remediation

Detached candidate commit `995dbd27530bbe2ab97bd10d0e6c2812baf00758` updates:

- `docs/24-schema-ontology-coverage-matrix.md`: documentation count `52` and
  Python test-module count `53`;
- `examples/maturation-summary.ontology-maturation.json`: regenerated from the
  tagged repository tree.

The candidate was then rechecked with the same environment and produced
`280 passed, 2 skipped`. It has not been pushed to `foi-o` and does not replace
the upstream tag.

## Still required for #27

The upstream release-evidence bundle must still include and substantiate the
release tag/SHA, contract versions, capabilities, migrations, tests, fixtures,
provenance, empirical results, exceptions, and limitations. The FOI-O plan
still marks extraction-contract, consumer-contract, independent fixture,
source-triangulation, empirical adjudication, and evidence-bundle tasks as
open. This handoff does not certify any of those unfinished gates.

## Human boundary

Dylan must decide whether to apply and review the candidate in the FOI-O
repository, publish a corrected immutable release, and generate the accepted
evidence bundle. No upstream branch, PR, release, dataset, or paper action is
performed by this handoff.

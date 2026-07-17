# Independent-validation handoff packet

This directory is a local analyst handoff surface. It contains status
snapshots and review instructions only; it is not an upstream branch, an
outreach channel, an adoption ledger, or an evidence result.

## Source of truth

- The reusable implementer kit and result schema are under
  [`independent/kit/`](../../independent/kit/).
- The canonical local adoption ledger is
  [`independent/STATUS_LEDGER.json`](../../independent/STATUS_LEDGER.json).
- The active track and analyst gates are in
  [`conductor/tracks/v1_independent_validation_20260714/`](../../conductor/tracks/v1_independent_validation_20260714/).
- The dated upstream snapshot is [`UPSTREAM_STATUS_20260717.md`](UPSTREAM_STATUS_20260717.md).

Do not create a second qualifying-consumer record in this directory. Update
the canonical ledger only when independently supplied, reproducible evidence
has passed the verifier and the required acknowledgement is durable.

## Fail-closed review rule

An analyst must leave a target `blocked` unless all of the following are
available and independently checkable:

1. A public or embargoed implementation identity with an immutable revision.
2. A corpus digest and oracle description generated outside the maintainer
   repository.
3. Reproducible result files, not a screenshot, narrative, issue, paper, or
   local rehearsal.
4. Environment and test details sufficient to rerun the result.
5. A result accepted by `tools/independent_validation.py` and an explicit
   external acknowledgement.

Missing, stale, conflicting, or unverifiable evidence is an evidence failure,
not permission to continue. Record the exception and stop the adoption claim.
Do not infer FOI-O facts from a release tag, DOI, issue comment, local
candidate, or paper draft.

## Analyst boundary

This packet does not authorize contacting maintainers, submitting issues or
PRs, promoting fixtures, publishing a paper, or certifying v1. Those actions
remain analyst-gated in the active track.

# Deferred Canonical Cutover Decision

Decision date: 2026-07-16
Decision source: Dylan's instruction to proceed with retaining the process-mappings work as a subrepo and defer extraction.

## Decision

Do **not** create `edithatogo/process-mappings` at this stage. Retain
`subrepos/process-mappings/` inside `rac-conformance` as the sole writable,
non-canonical incubator.

This is a deferral of repository creation, not a rejection of the process-
mappings design. The subtree remains structured for later extraction with its
own boundaries, profiles, optional adapters, provenance ledger, standalone
check, and extraction rehearsal.

## Rationale

- `rac-conformance` remains the appropriate coordination and contract home
  while the profiles are candidate or human-gated material.
- `foi-o` and `foi-process` already provide the FOI semantic and implementation
  boundaries; a new repository would add governance and release overhead before
  a second mature domain consumer exists.
- `fyi-archive` remains the immutable source corpus, not a mapping repository.
- A future neutral repository becomes justified when at least one additional
  domain profile has a named consumer, stable source/provenance artifacts, and
  a release lifecycle independent of `rac-conformance`.

## Reconsideration triggers

Reopen extraction only when all of these are true:

1. A second domain profile, such as adverse incidents or health technology, has
   a named consumer and a reviewed profile artifact.
2. At least one independent consumer needs the mappings outside the parent
   repository.
3. The mapping artifacts require an independent release cadence or governance
   surface.
4. A new cutover packet is approved, including hosted controls and issue
   migration conditions.

Until then, all changes must land through `rac-conformance`; no destination
   issue, remote, redirect, or canonical-home claim should be created.

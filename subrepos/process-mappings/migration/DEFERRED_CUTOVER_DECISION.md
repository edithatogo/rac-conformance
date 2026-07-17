# Staged Canonical Cutover

Decision date: 2026-07-17
Status: public remote created and independently verified; retain the parent subtree as authoritative until the final canonical-cutover conditions pass.

The process-mappings work remains an ordinary tracked subrepo inside
`rac-conformance` for the moment. The public destination is populated at
`d0257c1a99068262ea257643f3d6bdb57f2baee6`, but it is not yet the canonical
writable source. This prevents dual ownership while parent consumers and links
are updated.

Reconsider extraction only when a second domain profile has a named consumer,
an independent consumer needs the mappings, and the mapping artifacts require
their own release or governance lifecycle. The full decision record and human
provenance are maintained in the parent Conductor track:
`conductor/archive/process_mappings_repository_20260714/migration/DEFERRED_CUTOVER_DECISION.md`.

Until final cutover, changes land through `rac-conformance`; the destination
repository, issue #1, hosted controls, and migration evidence are preparation
for canonical ownership, not a claim that the cutover is complete.

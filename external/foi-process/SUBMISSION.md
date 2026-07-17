# Staged foi-process evidence

This directory is a read-only evidence snapshot staged for the
`core_model_demonstrator_20260717` track. It is not a change to
`edithatogo/foi-process` and must not be pushed there by this repository.

## Provenance

- Source repository: `https://github.com/edithatogo/foi-process`
- Source revision: `f67a351` (`citation: add release metadata`)
- Source paths: `examples/generated/conformance-trace.json`,
  `examples/generated/replay-snapshot.json`, and
  `schemas/portable/conformance-trace.schema.json`
- Source schema for process events was observed at
  `schemas/portable/process-event.schema.json` with SHA-256
  `5e758674cbd1cbbd01a1b3c72d5dea6efe00bd06962893801c62222934a1c37f`.

The copied bytes are hashed in
`conductor/tracks/core_model_demonstrator_20260717/FOI_DEMONSTRATOR_CHAIN.json`.
The generated trace declares `assertion_status: inferred` and an indicative
deadline. It is execution/evidence input, not a legal conclusion or a PIC
fixture promotion.

## Boundary

`foi-process` remains implementation-authoritative for its event, replay, and
OCEL representations. This snapshot is used only to test provenance and
representational loss at the PIC process-profile boundary.

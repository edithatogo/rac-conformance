# Process Profile Design

## Authority model

`sourceAssertions` are evidence records, not an inference engine. `authority`
describes the kind of source; `sourceType` describes whether the source is
official primary, official secondary, secondary, or a runtime record; and
`reviewStatus` records whether a human or official source has certified it.
Only `official_primary` or `human-approved` assertions may be marked
`controlling`, and every controlling assertion must have `effectiveFrom`.
Agent-proposed and secondary-only assertions remain non-controlling.

## Time model

- `applicableAt`: when the process definition applies.
- `occurredAt`: when an event happened in the process.
- `observedAt`: when the event or profile was recorded or retrieved.
- `effectiveFrom`/`effectiveTo`: the source assertion's validity interval.

The deterministic validator rejects observed events recorded before occurrence,
profiles observed before applicability, and reversed source intervals.

Timers are declarations of a timing obligation, not an executable clock. A
timer must reference a known start event, and its calendar or working-day
semantics must be resolved by a released PIC parameter or deterministic rule
invocation. This keeps platform adapters from silently changing statutory or
policy timing.

## Projection boundary

An adapter projects platform records into states, events, tasks, evidence, and
traces. It must retain stable IDs where available and record loss in a trace's
`lossNotes`. `equivalenceClaim` is limited to `output`, `path`, `semantic`, or
`none`; the profile does not imply that platform execution is losslessly
equivalent merely because it can be serialized.

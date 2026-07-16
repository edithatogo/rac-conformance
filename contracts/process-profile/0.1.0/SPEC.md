# pic-process-profile 0.1.0

`pic-process-profile` is a small, platform-neutral description of an
administrative process and its evidence-bearing execution. It is an
interchange and conformance contract, not a workflow engine or ontology.

## Semantics

- `states` and `transitions` describe the process definition.
- `actors` identify people, roles, organizations, and systems participating in
  the process. Authority for a role or system is linked through source
  assertions rather than inferred from its label.
- `timers` identify calendar, working-day, deadline, and relative timing
  obligations. They reference a start event and carry a human-readable
  duration; calendar arithmetic remains in the relevant PIC parameter or rule
  contract.
- `events` describe execution records. `observed_event`, `derived_state`,
  `proposed_action`, `certified_human_decision`, and `executed_action` are
  deliberately distinct; a proposal is never a certification.
- `tasks` distinguish human work from deterministic rule work. A human task
  may record a certified decision event, while a deterministic rule task must
  reference a `ruleInvocation`.
- All process times are explicit: `applicableAt` is when the definition is
  applicable, `occurredAt` is when an event happened, and `observedAt` is when
  the record was observed. The validator rejects impossible ordering and
  missing effective dates for controlling assertions.
- `sourceAssertions` identify authority and review state. An assertion is
  controlling only when it is an official primary source or has been approved
  by a human. Agent-proposed and secondary-only assertions remain evidence,
  never certification.
- `traces` link normalized process events to released PIC traces. Adapters may
  lose platform detail, but must state the equivalence claim and loss notes.

The profile contains identifiers and references, not embedded legal, clinical,
funding, or expression-language decisions. Domain profiles and jurisdiction
overlays remain source-backed consumer artifacts under the incubator.

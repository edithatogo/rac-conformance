# PIC Process Profile

Status: Draft | Consumed-by: FOI-O compatibility baseline, health demonstrators, Camunda adapter

## Overview

Define the smallest platform-neutral contract needed to describe and verify how
administrative processes invoke deterministic rules and produce auditable traces.
The contract must be implementable without FOI-O, BPMN, Camunda, or a new
ontology.

Depends on: `v1_foundation_20260714` Phase 1 and the incubation boundary in
`process_mappings_repository_20260714`.

Normative schemas, validators, and conformance tests remain under
`contracts/process-profile/` and `contracts/tools/` in `rac-conformance`.
Source-backed domain profiles and compatibility datasets live under
`subrepos/process-mappings/profiles/` during incubation and move only through
the approved repository cutover.

## Functional Requirements

1. Represent stable process, state, event, transition, actor/authority, timer,
   human-task, rule-invocation, evidence-reference, exception, and trace IDs.
2. Distinguish observed events, derived state, proposed actions, certified human
   decisions, and executed actions.
3. Represent applicable time, observation time, source effective date, and
   process-definition version.
4. Link to existing PIC parameters, fixtures, traces, and semantics by identifier.
5. Define a source-assertion ledger with authority and review status.
6. Define deterministic projection into and out of platform traces without
   claiming lossless equivalence.
7. Map FOI-O as the baseline consumer and publish documented loss or exceptions.
8. Consume foi-process traces or OCEL projections only as pinned implementation
   evidence; FOI-O remains authoritative for FOI semantics.

## Non-Functional Requirements

- JSON Schema 2020-12 and canonical JSON remain normative.
- No embedded expression language, global ontology, runtime AI, or executable
  clinical/legal judgement.
- Human tasks must remain distinguishable from deterministic rule tasks.
- Every schema change has valid and invalid examples and >=80% tool coverage.

## Acceptance Criteria

- Two independent implementations could produce comparable process traces from
  the contract without sharing runtime code.
- FOI-O examples validate without making PIC a FOI-O runtime dependency.
- Negative tests reject missing authority, ambiguous time, unreviewed controlling
  assertions, and attempts to label AI output as certified human judgement.
- `make check` passes.

## Out of Scope

- General-purpose BPMN replacement.
- Clinical decision support.
- Automatic legal interpretation.
- Cross-standard mapping without an executable consumer.

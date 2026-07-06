# Service Boundary Demonstrations

## Overview

Docassemble and CiviForm assessments exist, but no runnable demo exists yet. This track builds minimal demonstrations that a process/application system can call a PIC-tested rules module over a stable boundary and show traceable outputs.

## Functional Requirements

1. Build a Docassemble-style demo package or executable mock that asks for an OIA receipt date and calls the staged OIA rules module.
2. Build a CiviForm-style HTTP service mock that accepts a simple application payload and returns a PIC-shaped rule result.
3. Include traces/explanations in outputs.
4. Document integration boundaries and what is real vs mocked.
5. Avoid storing or processing real personal data.

## Non-Functional Requirements

- Prefer small, local, testable demos over production infrastructure.
- No runtime AI decisions.
- Use typed request/response schemas and JSON examples.
- Keep CiviForm integration as a mock/service-boundary proof unless a real CiviForm plugin path is selected.

## Acceptance Criteria

- Demo requests and responses are committed.
- Unit/integration tests verify request validation, rule invocation, and trace output.
- `make check` passes.
- Demo README names exact limitations and next upstream path.

## Out Of Scope

- Production deployment.
- Real applicant data.
- Full CiviForm plugin development unless a later track explicitly chooses it.

# Camunda 8 Process Portability Demonstrator

Status: Draft | Consumed-by: v1 portability evidence

## Overview

Implement Camunda 8 as one optional process-platform adapter. BPMN orchestrates;
deterministic rule services decide only source-backed machine-decidable matters;
human tasks retain legal, clinical, ethical, and funding judgement. PIC remains
the platform-neutral contract and Camunda is neither normative nor required.

Depends on: `pic_process_profile_20260714` and one certified process demonstrator.

## Functional Requirements

1. Record an architecture decision selecting a pinned supported Camunda 8 test
   runtime and official Camunda Process Test integration.
2. Map stable PIC process IDs to BPMN elements without using display names as IDs.
3. Invoke deterministic PIC/rule behavior through a job worker or REST boundary;
   do not duplicate substantive rules in BPMN gateways or DMN tables.
4. Implement user tasks, timers, messages, expected outcomes, technical errors,
   retries, incidents, and escalation paths as appropriate to the demonstrator.
5. Project Camunda execution records into normalized PIC traces and report loss.
6. Test process-definition versioning and supported active-instance migration.
7. Provide deterministic scenario replay and separately labeled seeded operational
   workload experiments.

## Non-Functional Requirements

- Pin Camunda, Java, container, and plugin versions with checksums or lockfiles.
- Use Java 17+ and JUnit 5 if official Camunda Process Test remains the selected
  stable test surface; document any alternative.
- No AI judge assertions, runtime LLMs, or token simulation as conformance proof.
- Avoid committing runtime state, credentials, proprietary images, or generated
  reports that cannot be reproduced.
- Keep the adapter isolated under `demos/camunda/` or another approved boundary.

## Acceptance Criteria

- A clean environment can execute the pinned tests and produce the same normalized
  traces for deterministic scenarios.
- Timer tests use controlled time and do not wait on wall-clock delays.
- Process coverage includes normal, exception, human-task, timer, retry/incident,
  and migration behavior relevant to the selected demonstrator.
- Trace differences are explained rather than hidden by platform-specific fields.
- Core PIC validation remains usable without Java, Docker, or Camunda.

## Out of Scope

- Production Camunda deployment or procurement recommendation.
- Treating token simulation as runtime evidence.
- Automating human legal, clinical, disclosure, or funding decisions.
- Making BPMN, DMN, FEEL, or Camunda extensions part of PIC core.

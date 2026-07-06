# PIC v0.2 Consumer-Driven Revision

## Overview

PIC v0.1 exists and validates. PIC v0.2 must not be a speculative standardization push. It may only add or change contract surface based on concrete consumer feedback from `foi-o`, PolicyEngine/Axiom, OpenFisca, DBN, Alaveteli, Docassemble, CiviForm, or another approved consumer.

## Functional Requirements

1. Create `contracts/FEEDBACK.md` with one row per consumer request or adoption friction point.
2. Classify every proposed change as:
   - required for active consumer;
   - optional convenience;
   - rejected as premature standardization;
   - deferred pending evidence.
3. Draft v0.2 changes only for required active-consumer needs.
4. Preserve independent versioning for each PIC contract.
5. Include migration notes and compatibility examples for any breaking change.
6. Keep JSON-LD, external-standard crosswalks, expression languages, and ontologies out of v0.2 unless a named consumer requires them and a working converter exists.

## Non-Functional Requirements

- Restrict repository modifications strictly per `conductor/edithatogo-repo-boundaries.md`.
- Use TDD for schema and validator changes.
- Maintain >=80% coverage for `contracts/tools`.
- Keep examples small and source-backed.
- Money and precise decimals remain strings.

## Acceptance Criteria

- `contracts/FEEDBACK.md` exists and cites real artifacts or URLs.
- Any v0.2 schema has valid/invalid examples and tests.
- `pic-validate` validates all v0.1 examples and any v0.2 examples.
- `contracts/CONSUMERS.md` distinguishes active consumers from potential consumers.
- `make check` and GitHub Actions pass.

## Out Of Scope

- Creating a general ontology.
- Publishing a standard without adoption evidence.
- Adding converters for standards that have no consumer in this repo.

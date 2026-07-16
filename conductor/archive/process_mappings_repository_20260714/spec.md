# Process Mappings Repository Incubation and Extraction

Status: Draft | GitHub issue: [#50](https://github.com/edithatogo/rac-conformance/issues/50)

## Overview

Establish a domain-neutral home for source-backed process profiles, jurisdiction
overlays, synthetic candidate scenarios, and optional platform adapters. The
work begins as an ordinary tracked subtree at `subrepos/process-mappings/` so
the boundary can be tested before a new remote is created. Extraction to
`edithatogo/process-mappings` requires an explicit human cutover decision.

Depends on: `v1_foundation_20260714` Phase 1. Establishes the implementation
home used by `pic_process_profile_20260714` and its demonstrators.

## Repository Responsibilities

| Repository | Owns | Does not own |
|---|---|---|
| `rac-conformance` | Normative PIC contracts, schemas, validators, conformance harnesses, qualification, and v1 release evidence. | Domain source packs or platform implementations as canonical products. |
| `process-mappings` | Source-backed process profiles, jurisdiction overlays, mapping evidence, synthetic candidate scenarios, and optional platform adapters. | PIC normative semantics, legal certification, or production workflow operations. |
| `foi-o` | FOI ontology, legal semantics, and jurisdiction profiles. | Generic process-profile contracts or runtime process mining. |
| `foi-process` | Deterministic FOI event/replay/OCEL/process-intelligence implementation and operational evidence. | Generic mappings, canonical FOI legal semantics, or PIC normative contracts. |

## Functional Requirements

1. Provide standalone product, safety, source, licensing, contribution, test,
   and Conductor boundaries before domain mappings are implemented.
2. Reference PIC contracts by released version or pinned commit; never copy and
   silently fork normative schemas.
3. Accept FOI-O semantic exports and foi-process execution evidence through
   versioned, documented adapters with provenance and explicit loss records.
4. Keep all AI-drafted mappings and scenarios as `agent-proposed` candidates
   until a human certifies controlling assertions and promotion.
5. Preserve authority, jurisdiction, effective date, retrieval date, source
   status, rights, digest, interpretation state, and reviewer state.
6. Rehearse extraction with history, license, CI, issue/project migration,
   redirects, dependency updates, rollback, and integrity evidence.
7. Maintain exactly one writable canonical copy after extraction.

## Non-Functional Requirements

- No runtime AI decisions, patient-level data, confidential deliberative
  evidence, or agent-certified controlling assertions.
- Platform adapters remain optional and cannot redefine the neutral profile.
- The incubator is an ordinary tracked subtree, not a Git submodule or nested
  Git repository.
- No remote repository is created and no canonical-home claim is made before
  the `[HUMAN]` cutover gate.
- Extraction must preserve Apache-2.0 compatibility, provenance, and a
  reproducible verification path.

## Acceptance Criteria

- `subrepos/process-mappings/` clearly identifies itself as non-canonical and
  names every owning repository boundary.
- Tracks #40-#43 name exact normative and implementation paths.
- FOI compatibility treats `foi-o` as semantic authority and `foi-process` as
  an implementation/evidence consumer.
- A clean extraction rehearsal proves history, tests, links, issue migration,
  and rollback without creating a second writable source of truth.
- The human cutover packet records the proposed owner, visibility, repository
  settings, branch protection, project linkage, migration commit, and rollback.

## Out of Scope

- Creating the GitHub remote before human approval.
- Moving PIC normative contracts out of `rac-conformance`.
- Replacing FOI-O or foi-process.
- Publishing source mappings as legal, clinical, regulatory, or funding advice.
- Production Camunda deployment or operational incident management.

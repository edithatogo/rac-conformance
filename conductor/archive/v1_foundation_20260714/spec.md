# v1 Foundation and Governance

Status: Draft | Consumed-by: all v1 roadmap tracks

## Overview

Turn the evidence-first programme into a bounded v1 product contract before
additional domain and platform work expands the surface. This track defines what
1.0 guarantees and what remains experimental; it does not declare 1.0 complete.

## Functional Requirements

1. Define core, optional profile, jurisdiction-profile, adapter, and experimental
   artifact classes.
2. Publish v1 entry, release-candidate, and general-availability gates.
3. Define compatibility, support, deprecation, migration, and vulnerability
   response policies.
4. Define independent-consumer and independent-oracle requirements.
5. Define conformance levels without implying legal, clinical, or funding
   authority.
6. Create a machine-readable release-gate manifest validated in CI.
7. Reconcile the v1 roadmap with existing FOI-O, Axiom/OpenFisca, external
   adoption, paper, Zenodo, and human-certification gates.

## Non-Functional Requirements

- Preserve independent semantic versioning for PIC contracts.
- Do not make a platform adapter or domain profile a core runtime dependency.
- Use precise, testable RFC 2119 requirements for normative commitments.
- Keep repository-local proof distinct from external adoption and publication.

## Acceptance Criteria

- The v1 scope and non-goals are unambiguous.
- A validator can report each release gate as pass, fail, blocked, or not
  applicable with evidence links.
- Compatibility and deprecation policies cover every public contract and CLI.
- `make check` passes and Project 19 matches the local track state.

## Out of Scope

- Implementing new process profiles or adapters.
- Claiming standards-body endorsement.
- Releasing 1.0.
- Treating papers, citations, or repository ownership as independent adoption.

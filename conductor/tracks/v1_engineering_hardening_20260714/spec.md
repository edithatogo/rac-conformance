# v1 Engineering and Supply-Chain Hardening

Status: Draft | Consumed-by: v1 release candidate

## Overview

Establish production-quality evidence for consuming untrusted interchange
artifacts and distributing the validator/toolkit. This work proves bounded
reliability; it does not claim that validated policy content is correct.

Depends on: `v1_foundation_20260714` and stable process-profile schemas.

## Functional Requirements

1. Threat-model parsers, schemas, converters, source retrieval, plugins/adapters,
   generated reports, CI, releases, and external artifact ingestion.
2. Add property, fuzz, hostile-input, mutation, and resource-limit tests based on
   the threat model.
3. Define measurable time, memory, artifact-size, and diagnostic-quality budgets.
4. Test supported OS/Python/runtime and old-to-new contract compatibility.
5. Produce locked dependencies, SBOMs, artifact checksums, provenance evidence,
   and reproducible-build comparisons.
6. Harden release automation with least privilege, pinned actions, protected
   environments, and attestations where supported.
7. Establish backup/restore and release rollback rehearsals for published
   artifacts and compatibility metadata.

## Non-Functional Requirements

- Security tests must be deterministic and safe for CI.
- Fuzz corpora must contain no sensitive or restricted data.
- Mutation thresholds apply only where a stable, meaningful test oracle exists.
- Hosted GitHub evidence must be recorded separately from local test results.
- Signing and protected release approval remain human or platform gates.

## Acceptance Criteria

- All high/critical threat-model findings are fixed or explicitly release-blocking.
- Supported-platform and compatibility matrices are green.
- Performance budgets pass on a documented reference environment.
- Build outputs are reproducible within documented platform limits.
- SBOM, checksums, provenance, rollback, and vulnerability response evidence are
  included in the release candidate.

## Out of Scope

- Certifying third-party policy content.
- Penetration testing third-party services.
- Unsupported platform guarantees.
- Eliminating every transitive dependency regardless of risk.

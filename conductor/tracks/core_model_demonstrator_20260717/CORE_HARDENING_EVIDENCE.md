# Core Hardening Evidence

Date: 2026-07-17  
Scope: local qualification of the PIC contracts, process profile, and FOI
demonstrator evidence chain

## Evidence matrix

| Area | Evidence | Local result | Boundary |
| --- | --- | --- | --- |
| Threat model and risk register | `security/THREAT_MODEL.md`, `security/RISK_REGISTER.json` | Present; trust boundaries and fail-closed controls recorded | Third-party service and hosted release controls remain external |
| Hostile input and resource limits | `contracts/tools/src/pic_contracts/safety.py`, `contracts/tools/tests/test_safety.py` | Pass under bounded parser and path policies | No claim of arbitrary unbounded input safety |
| Property and deterministic tests | `contracts/tools/tests/test_hardening_properties.py`, process-profile and chain tests | Pass | Seeded local corpus, not an external fuzz campaign |
| Mutation gate | `docs/V1_MUTATION_GATE.json`, `tools/v1_mutation.py` | 3/3 declared mutations killed; 0 equivalent accepted | Mutation scope is the declared validator set |
| SBOM and dependency evidence | `security/SBOM.spdx.json`, lockfiles, dependency-review workflow | Present and hosted dependency review passes | Local SPDX packet is not a hosted attestation |
| Reproducibility | `docs/V1_REPRODUCIBILITY.json` | Two clean source archives byte-identical | Hosted provenance and package signing are absent |
| Rollback rehearsal | `security/ROLLBACK_REHEARSAL.md` | Tabletop procedure present | No public release has existed, so no live yank was performed |
| Cross-platform CI | PR checks on the focused core changes | Ubuntu/macOS Python 3.12/3.13, CodeQL, workflow and dependency checks pass | Hosted artifact attestations, signing, and live rollback remain deferred |

## Qualification statement

The local core implementation is hardened enough to proceed to human review of
the bounded FOI demonstrator. This packet does not qualify v1.0, certify third-
party adoption, or authorize publication. Those gates remain in
`conductor/DEFERRED_ROADMAP.md`.

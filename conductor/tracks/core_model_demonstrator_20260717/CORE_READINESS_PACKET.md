# Core Demonstrator Readiness Packet

Status: core implementation ready for human demonstrator certification  
Date: 2026-07-17  
Track: `core_model_demonstrator_20260717`

## What is complete

The repository now provides a bounded, deterministic core model demonstrator:

1. Released PIC contract schemas and valid/invalid corpora are audited and
   validated.
2. `pic-process-profile/0.1.0` has named consumer coverage, fail-closed source
   authority rules, explicit time semantics, and order-independent trace
   normalization.
3. The FOI-O candidate profile, FOI-O PIC trace, and staged `foi-process`
   execution/replay evidence are linked by a pinned chain manifest.
4. Local hostile-input, property, mutation, SBOM, reproducibility, rollback,
   and cross-platform CI evidence is recorded.
5. Human certification is explicitly bounded to compatibility and
   representational loss. No legal conclusion, universal portability claim,
   fixture promotion, or canonical process-mappings cutover is made.

## Evidence index

| Claim | Evidence |
| --- | --- |
| Contract corpus is reproducible | [CORE_CONTRACT_AUDIT.md](CORE_CONTRACT_AUDIT.md) |
| Process profile is implementable and platform-neutral | [PROCESS_PROFILE_CLOSURE_AUDIT.md](PROCESS_PROFILE_CLOSURE_AUDIT.md) |
| FOI source/profile/execution chain is pinned | [FOI_DEMONSTRATOR_CHAIN.json](FOI_DEMONSTRATOR_CHAIN.json), [FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md](FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md) |
| Local hardening is qualified | [CORE_HARDENING_EVIDENCE.md](CORE_HARDENING_EVIDENCE.md) |
| Deferred work and re-entry conditions are visible | [DEFERRED_ROADMAP.md](../../DEFERRED_ROADMAP.md) |

## Remaining gates

### Human gate

Dylan must review [FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md](FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md)
and record one of `certified-bounded`, `rejected`, or `changes-requested`. This is the only
remaining decision for the bounded demonstrator itself.

### External or deferred gates

The following are intentionally not prerequisites for this core packet and
remain deferred: health-pathway breadth, Camunda portability, canonical
process-mappings cutover, independent external validation/adoption, hosted
attestations and signing, v1.0 release qualification, papers, Zenodo, and
upstream FOI-O publication/governance.

## Qualification boundary

This packet establishes readiness to make the bounded demonstrator decision.
It is not a v1.0 release authorization, a publication authorization, or an
assertion that the model has been independently adopted or validated.

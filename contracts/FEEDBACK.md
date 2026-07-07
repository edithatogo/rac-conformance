# PIC Consumer Feedback Ledger

This ledger inventories all concrete feedback, friction points, and feature requests from active consumers of the Policy Interchange Contracts (PIC).

## Proposal Status Summary

| Proposal ID | Consumer | Source / Evidence | Description | Status | Urgency |
|:---|:---|:---|:---|:---|:---|
| `PIC-REQ-001` | `foi-o` | `external/foi-o/rules/` | Decouple calendar parameters and exclusion limits from engine code. | **approved** | High |
| `PIC-REQ-002` | `PolicyEngine`, `OpenFisca` | `external/*/SUBMISSION_missingness.md` | Distinguish omitted variables from explicit zeros in traces (`valueState` / `is_input`). | **approved** | High |
| `PIC-REQ-003` | `DBN` | `external/dbn/EMAIL.md` | Standardize decimal string formats for financial precision. | **approved** | Medium |
| `PIC-REQ-004` | `Alaveteli` | `external/alaveteli/SUBMISSION.md` | Expose request-state taxonomy hooks for statutory-clock mapping. | **deferred** | Medium (No active PIC consumer yet) |
| `PIC-REQ-005` | None (Speculative) | General suggestion | Introduce JSON-LD and semantic web schemas. | **rejected** | Low (No consumer) |
| `PIC-REQ-006` | None (Speculative) | General suggestion | Add expression evaluation DSL. | **deferred** | Low (No active use case) |

## Classifications

### PIC-REQ-001: Calendar exclusion customization
- **Source:** `foi-o` integration (statutory clock deadline rules).
- **Resolution:** Approved for PIC v0.2. Allow schemas to represent holiday parameters explicitly.

### PIC-REQ-002: Missingness indicator in trace/execution context
- **Source:** PolicyEngine and OpenFisca missingness findings.
- **Resolution:** Approved for PIC v0.2. Expose `valueState` (either `explicit` or `default`) on input traces.

### PIC-REQ-003: String-based decimals for financial values
- **Source:** DBN cross-engine comparison harness.
- **Resolution:** Approved. Keep string representation for money to prevent float errors.

### PIC-REQ-004: Alaveteli request-state hooks
- **Source:** Alaveteli request-state taxonomy proposal.
- **Resolution:** Deferred until there is a named consumer that needs the hook in PIC v0.2. The proposal is useful evidence, but it does not justify a schema change by itself.

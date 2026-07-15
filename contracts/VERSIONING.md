# Policy Interchange Contracts (PIC) Versioning Policy

PIC packages are independently versioned and matched against active consumer requirements. 

## Semantic Versioning Rules

- **Patch (`0.x.y` -> `0.x.y+1`):** Non-breaking clarifications, comments, or documentation additions to a schema.
- **Minor (`0.x.y` -> `0.x+1.0`):** Backward-compatible additions (e.g. new optional fields).
- **Major (`1.x.y` -> `2.0.0`):** Breaking changes to schema structures.

## PIC v0.2 Scope & Schema Version Upgrades

Based on active consumer requirements, the following packages are upgraded to `v0.2`:

1.  **`pic-traces` (Upgrade to `0.2.0`):**
    *   **Requirement:** Distinguish omitted from explicit zero values (`PIC-REQ-002`).
    *   **Change:** Require the shared `valueState` field on input trace nodes
        and add optional `valueOrigin` (`"explicit"` or `"default"`) to
        distinguish explicit and defaulted inputs. `valueState` retains the
        shared semantic enum from `pic-semantics/0.1.0`.
2.  **`pic-parameters` (Upgrade to `0.2.0`):**
    *   **Requirement:** Decouple calendar configurations (`PIC-REQ-001`).
    *   **Change:** Add support for declaring explicit holiday exclusions array.

All other contracts (`pic-semantics`, `pic-crosswalk`, `pic-fixtures`) remain at `v0.1` as no consumer feedback requires changes.

The Alaveteli request-state proposal is tracked in `contracts/FEEDBACK.md` as deferred evidence; it does not upgrade any PIC package until a named consumer requires it.

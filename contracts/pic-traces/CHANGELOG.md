# CHANGELOG: pic-traces

## 0.2.0 (2026-07-06)


- Require the shared `valueState` field on input trace nodes and add optional
  `valueOrigin` (enum: `["explicit", "default"]`) to distinguish explicit
  and defaulted inputs.
- Update validator support to validate v0.2.0 trace formats.

## 0.1.0 (2026-07-06)

- Initial release of Policy Interchange Contracts (PIC) decision-trace schema.
- Supported case-level decision step traces.
- Standardized trace equivalence verification levels: output, path, and semantic.

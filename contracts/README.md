# Policy Interchange Contracts

Policy Interchange Contracts (PIC) are small, versioned JSON artifact contracts for exchanging policy concepts, parameters, fixtures, traces, and value semantics without adopting another project's runtime.

## Contracts

| Contract | Version | Purpose |
|---|---:|---|
| `pic-semantics` | `0.1.0` | Shared value-state, epistemic-status, data-type, and rounding definitions. |
| `pic-crosswalk` | `0.1.0` | Concept, variable, parameter, evidence, decision, and process-step mappings across concrete systems. |
| `pic-parameters` | `0.1.0` | Time-versioned parameter values, including bracket schedules, with source references. |
| `pic-fixtures` | `0.1.0` | Engine-neutral test fixtures with value-state-aware inputs and expected outputs. |
| `pic-traces` | `0.1.0` | Case-level decision traces and trace-equivalence claims. |
| `pic-foio-compatibility` | `0.1.0` | Content-addressed FOI-O release, jurisdiction, legislation, archive/Hugging Face, NLP, and governance handshake. |

## Ground Rules

- Plain JSON is canonical. YAML is accepted only at import boundaries.
- Money and precise decimals are strings, never binary floats.
- IDs are package-scoped and lowercase; no global registry or URI registry is required.
- Golden fixtures are human-curated. AI-proposed candidates stay marked as `ai-proposed`.
- No JSON-LD context, external-standard crosswalk, expression language, or runtime AI decision belongs in v0.1.

## Tooling

The reference tooling lives in `contracts/tools` as the `pic_contracts` Python package:

- `pic-validate` validates schemas and package-level referential integrity.
- `pic-diff` compares temporal parameter files.

Run the full local gate from the repository root:

```sh
make check
```

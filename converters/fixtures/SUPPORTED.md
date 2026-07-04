# Supported Subset v0.1

Status: Draft | Consumed-by: `fixture_converter_20260704`

This document defines the initial deterministic conversion subset for:

- OpenFisca YAML tests -> PIC fixtures -> OpenFisca YAML tests.
- PolicyEngine YAML tests -> PIC fixtures -> PolicyEngine YAML tests.
- Cross-engine YAML conversion only when every variable id is covered by a supplied PIC crosswalk.

The converter MUST reject unsupported constructs loudly with `UnsupportedConstructError`, naming the construct and source file context. It MUST NOT silently drop fields.

## Top-Level YAML Fields

| Field | OpenFisca | PolicyEngine | v0.1 decision | Reason |
|---|---|---|---|---|
| `name` | Accepted | Accepted | Convertible | Becomes case description and stable case-id seed. |
| `period` | Accepted | Accepted | Convertible | Required by PIC case; missing source period is rejected. |
| `input` | Accepted | Accepted | Convertible for scalar and supported entity maps | Fixture inputs are the core converter surface. |
| `output` | Required at runtime | Required at runtime | Convertible for scalar and supported entity maps | Fixture expected values are the core converter surface. |
| `absolute_error_margin` | Accepted scalar or per-variable map | Accepted scalar | Convertible | Maps to PIC `expected[*].tolerance` as decimal string. |
| `relative_error_margin` | Accepted | Accepted | Rejected | PIC v0.1 fixtures have absolute `tolerance`, not relative tolerance. |
| `description` | Accepted | Accepted | Convertible | Preserved in PIC description/provenance notes where present. |
| `keywords` | Accepted for filtering | Accepted for filtering | Rejected | Runner selection metadata, not fixture semantics. |
| `ignore_variables` | Accepted option/filtering metadata | Accepted option/filtering metadata | Rejected | Can change tested outputs; not semantically portable. |
| `only_variables` | Accepted option/filtering metadata | Accepted option/filtering metadata | Rejected | Can change tested outputs; not semantically portable. |
| `reforms` | Accepted | Accepted | Rejected | Reform code paths are engine-specific. |
| `extensions` | Accepted | Accepted | Rejected | Extension loading is engine-specific. |
| `parameters` | Accepted by OpenFisca | Not accepted | Rejected | Parameter conversion is out of scope. |
| dotted `input` keys | Ordinary variable names in OpenFisca | Inline parameter reforms in PolicyEngine | Rejected for PolicyEngine | Parameter conversion is out of scope. |
| `max_spiral_loops` | Accepted by OpenFisca | Not accepted | Rejected | Simulation-control metadata, not fixture semantics. |

## Value Shapes

| Shape | v0.1 decision | Notes |
|---|---|---|
| Boolean scalar | Convertible | PIC value type is boolean. |
| Integer scalar | Convertible | PIC value type is integer. |
| Decimal/numeric scalar | Convertible | Serialized into PIC as a decimal string. |
| String scalar | Convertible | Includes enum-like values. |
| Date-like string | Convertible as string | PIC fixture schema does not require a date type marker inside values. |
| Per-period mapping, e.g. `variable: {2024: 1}` | Convertible | Flattened to an id suffix containing the requested period and reconstructed on round-trip. |
| Single entity mapping | Convertible when unambiguous | Preserved in case `entities` and flattened value ids. |
| Plural entity mapping keyed by instance id | Convertible when leaves are scalar or per-period maps | Preserved in `entities` and flattened value ids. |
| Lists/arrays | Rejected | Shape is ambiguous without model metadata. |
| Null | Rejected | PIC `not_provided` has explicit value-state semantics; native YAML null needs manual interpretation. |
| Expressions as strings, e.g. `-(7934.0 - 330.0)` | Rejected | Engine runner may evaluate; converter will not execute expressions. |

## Identity Mapping

Without a crosswalk, variable names pass through as native names under a generated PIC id:

- OpenFisca: `native/openfisca/<variable_name>.value`
- PolicyEngine: `native/policyengine/<variable_name>.value`

The generated PIC fixture file records the native identity scheme in provenance notes. With a crosswalk, every input and expected output variable MUST map to a PIC id. Missing mappings are rejected.

## Round-Trip Guarantees

The supported subset guarantees canonical equality for:

- `openfisca -> pic -> openfisca`
- `policyengine -> pic -> policyengine`

Canonical equality means YAML documents are parsed, unsupported fields are absent, scalar values are normalized, keys are sorted where ordering is not semantic, and resulting data structures compare equal. Comments and original formatting are not preserved.

Cross-engine conversion is supported only when a supplied crosswalk covers every variable id. Otherwise the converter rejects with the first unmapped name.

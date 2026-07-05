# Axiom public interface notes

Track: `engine_contributions_20260704` phase 3 C-C
Status: public-source interface discovery, not Dylan review
Reviewed on: 2026-07-06

## Purpose

These notes record what can be learned from Axiom's public site and official
repositories about the surface a validation harness can target. They do not
replace Dylan's review of the actual generated-model artifact used in Axiom's
private or applied workflow.

## Sources searched

- Axiom documentation index: https://axiom-foundation.org/docs
- Axiom technical stack: https://axiom-foundation.org/stack
- Axiom Rules Engine repository: https://github.com/TheAxiomFoundation/axiom-rules-engine
- RuleSpec engine README: https://github.com/TheAxiomFoundation/axiom-rules-engine/blob/main/README.md
- RuleSpec format notes: https://github.com/TheAxiomFoundation/axiom-rules-engine/blob/main/docs/rulespec.md
- Python wrapper: https://github.com/TheAxiomFoundation/axiom-rules-engine/tree/main/python/axiom_rules_engine
- RuleSpec schemas: https://github.com/TheAxiomFoundation/axiom-rules-engine/tree/main/schemas
- New Zealand RuleSpec corpus: https://github.com/TheAxiomFoundation/rulespec-nz
  at `3c6436b2ecf82dd7a7f7810a406a2695a64af33a`

## Public interface recovered

### Artifact shape

Axiom's public executable rule artifact is RuleSpec. The site describes RuleSpec
as the computation layer between source/claims and runtime execution, and the
stack page describes the post-encoding path as tested `.yaml` RuleSpec files,
companion `.yaml.test` cases, deterministic verification, runtime execution, and
public inspection.

The engine README and RuleSpec docs identify the accepted authoring/interchange
shape:

- RuleSpec modules declare `format: rulespec/v1` or a schema starting with
  `axiom.rules`.
- Direct `ProgramSpec` YAML is internal runtime IR, not the authoring target.
- Jurisdiction RuleSpec corpora use repo-backed legal IDs; public requests use
  durable legal IDs for inputs, relations, and outputs.
- Checked-in companion test files use the `rulespec-test.v1.schema.json` shape.
- Repeated execution can use a compiled artifact JSON produced by the engine.

### Compile and execute

The public command-line flow is:

```bash
cargo run -- compile \
  --program /path/to/rulespec.yaml \
  --output /tmp/model.compiled.json

cargo run -- run-compiled --artifact /tmp/model.compiled.json < request.json
```

The public Python wrapper mirrors the CLI:

- `AxiomRulesEngine.compile(program_path=..., output_path=...)`
- `AxiomRulesEngine.run_compiled(mode=..., artifact_path=..., dataset=..., queries=...)`
- `AxiomRulesEngine.run(mode=..., program=..., dataset=..., queries=...)`
- `AxiomRulesEngine.execute(...)` and `execute_compiled(...)` for request-model calls

### Execution request model

The public request model is deterministic and data-shaped:

- `mode`: `explain` or `fast`
- `dataset.inputs[]`: durable input name, entity, entity ID, interval, scalar
  value
- `dataset.relations[]`: durable relation name, tuple, interval
- `queries[]`: entity ID, period, requested durable output IDs, optional
  assessment date

Scalar values support `bool`, `integer`, `decimal`, `text`, and `date`. Decimal
values are represented as strings in the public request examples, which matches
this repository's no-floats-for-money rule.

### Execution response and traces

The public response model contains:

- `metadata`: requested mode, actual mode, and optional fallback reason
- `results[]`: one result per query
- `outputs`: output values keyed by requested durable IDs
- `trace`: derived trace nodes when running in `explain` mode

Trace nodes carry scalar or judgment outputs, optional source/source URL,
dependencies, and the durable ID where available. RuleSpec's rounding docs also
state that explain-mode traces expose the applied rounding mode and
`pre_rounding_value` when rounding changes a value.

### Discovery and validation helpers

The engine repository exposes JSON schemas for RuleSpec modules, companion test
cases, and compiled artifacts. The README also documents concept discovery and
validation commands:

```bash
axiom concepts search "adjusted gross income" --root /path/to/rulespec-us --json
axiom concepts show us:statutes/26/1401#self_employment_tax --root /path/to/rulespec-us --json
axiom concepts validate us:statutes/26/62#adjusted_gross_income --root /path/to/rulespec-us --json
axiom concepts list --namespace us:statutes/26 --root /path/to/rulespec-us --json
```

### Concrete public corpus: `rulespec-nz`

Dylan's suggested repository is a concrete public Axiom RuleSpec corpus:
`TheAxiomFoundation/rulespec-nz`. Its README describes it as the full-country
Aotearoa New Zealand RuleSpec workspace for tax, transfers, social insurance,
student support, family assistance, housing support, and related eligibility
surfaces.

Remote inspection of `main` resolved commit
`3c6436b2ecf82dd7a7f7810a406a2695a64af33a`. The tree contains executable
RuleSpec modules and companion tests under:

- `nz/statutes/`
- `nz/regulations/`
- `nz/policies/`
- `data/oracles/`

Sample module/test pair:

- `nz/statutes/gst/rate.yaml` declares `format: rulespec/v1` and durable
  outputs such as `nz:statutes/gst/rate#gst_standard_rate`.
- `nz/statutes/gst/rate.test.yaml` uses companion-test inputs and outputs keyed
  by the same durable IDs.

The oracle index also names comparison references for PolicyEngine NZ, Treasury
IncomeExplorer/EMTR, `nztaxmicrosim`, and `openfisca-aotearoa`. That makes
`rulespec-nz` a better first public integration target than an abstract stub,
provided Dylan confirms the intended module and comparison reference.

## Harness implication

A generic public prototype does not need to guess Axiom internals. It can target
the public RuleSpec runtime contract:

1. Accept either a RuleSpec module path or a precompiled artifact path.
2. If given RuleSpec, compile it to a temporary artifact through
   `axiom-rules-engine`.
3. Convert PIC fixture inputs into `Dataset` inputs and relations keyed by
   durable Axiom IDs from a reviewed crosswalk.
4. Query expected output IDs in `explain` mode.
5. Normalize outputs and traces into this repository's PIC-shaped divergence
   report.

This still leaves a human-specific gate: Dylan must confirm whether the actual
Axiom-generated model he wants tested is exposed as a RuleSpec file, a compiled
artifact, a checked-in jurisdiction repo path, or an app-specific wrapper around
the public runtime.

If Dylan selects `rulespec-nz` as the model under test, the adapter can treat the
repository checkout as the RuleSpec repo root and compile/query specific
`nz:...` modules through the public `axiom-rules-engine` path.

## Remaining unknowns for Dylan

- Which generated artifact should be treated as the model under test?
- Is the artifact a RuleSpec file, a compiled artifact, or a wrapper service?
- If `rulespec-nz` is the target, which module/test pair should be the first
  harness slice?
- Which jurisdiction repo roots and imports are required for the SNAP or tax
  overlap cases?
- Which durable output IDs should be compared to PolicyEngine and TAXSIM?
- Are Axiom explain traces available directly from the generated artifact, or
  only after compiling/running through `axiom-rules-engine`?

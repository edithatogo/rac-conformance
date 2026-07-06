# Axiom RuleSpec Validation Expansion

## Overview

The first roadmap produced a working Axiom harness and live RuleSpec NZ smoke evidence for GST, ACC earners levy, and individual income tax. This track turns that into a repeatable validation suite with clear oracle independence, source assertions, and CI integration.

## Functional Requirements

1. Expand `external/axiom` fixtures beyond the three smoke cases only where there is a source-backed or independent companion test.
2. Add deterministic PIC-to-RuleSpec mappings for each new slice.
3. Run against pinned `rulespec-nz` and `axiom-rules-engine` commits.
4. Generate machine-readable and human-readable reports under `external/axiom/results/`.
5. Add regression tests for adapter mappings and report summaries.
6. Prepare upstream feedback or PRs for Axiom/RuleSpec maintainers where the harness reveals a useful integration gap.

## Non-Functional Requirements

- Restrict repository modifications strictly per `conductor/edithatogo-repo-boundaries.md`.
- No runtime AI decisions.
- No inferred mappings at runtime.
- All money/decimal values remain strings in PIC fixtures.
- Do not certify legal correctness from RuleSpec output alone.


## Acceptance Criteria

- At least 10 RuleSpec NZ cases run through the harness, or a documented source/coverage blocker explains why not.
- Harness reports show exact matches, mismatches, and adapter failures deterministically.
- `make check` passes.
- Axiom upstream feedback is staged or submitted with URL/log evidence.

## Out Of Scope

- Rewriting RuleSpec.
- Treating RuleSpec NZ as authoritative law without source assertions.
- Adding broad ontology or JSON-LD layers.

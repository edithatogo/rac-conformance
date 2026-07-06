# Next Comparative Study Selection

## Overview

The SNAP study proved the harness pattern. This track chooses the next comparative study based on external demand and feasibility, then prepares scope, sources, and track plans for implementation.

## Functional Requirements

1. Build a candidate matrix for:
   - EITC/CTC three-way: PolicyEngine, TAXSIM, PSL Tax-Calculator.
   - Additional SNAP/benefits state-option slices guided by DBN or PolicyEngine/PRD feedback.
   - UK PolicyEngine-UK vs UKMOD if access permits.
   - France OpenFisca-France vs LexImpact if language/source burden is justified.
   - Aotearoa/NZ RuleSpec vs independent statutory calculator slices where source evidence exists.
2. Score each candidate on:
   - public-interest relevance;
   - open-source/runtime access;
   - independent oracle availability;
   - source assertion burden;
   - likelihood of maintainer adoption;
   - novelty relative to existing validation work.
3. Select one primary and one reserve study.
4. Draft conductor-ready specs/plans for the selected study, but do not start implementation until approved.

## Non-Functional Requirements

- Prefer maintainable, source-backed studies over impressive breadth.
- Do not duplicate active external work unless the repo adds a clear missing layer.
- Treat PRD/PolicyEngine's own MOU as a coordination signal, not competition.

## Acceptance Criteria

- `studies/NEXT_STUDY_SELECTION.md` exists with scoring and recommendation.
- Selected study has a draft `spec.md` and `plan.md` or a documented decision not to proceed.
- External dependencies, licenses, and source-access blockers are identified before implementation.
- `make check` passes.

## Out Of Scope

- Running the full next study.
- Creating golden fixtures without human approval.
- Starting a new standardization effort.

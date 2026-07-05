# SNAP Triangulation Adjudication Rules

Status: deterministic resolver rules for Track 5 Phase 4.

The resolver reduces human adjudication by deriving proposed dispositions from source assertions, fixture assumptions, and engine outputs. It does not call AI at runtime and does not submit upstream issues.

## Inputs

- `SOURCE_ASSERTIONS.json`: machine-readable source assertions encoded as a PIC-valid artifact.
- `fixtures/candidates/snap-fy2026-candidates.json`: fixture assumptions for the 15 held divergences.
- `results/classified-candidate-divergences.jsonl`: source-level engine classification and output evidence.

## Dispositions

- `confirmed_bug_policyengine`: controlling official or human-approved source assertions determine expected eligibility; PRD matches and PolicyEngine does not.
- `confirmed_bug_prd`: controlling official or human-approved source assertions determine expected eligibility; PolicyEngine matches and PRD does not.
- `expected_modeling_difference`: eligibility is source-resolved but the remaining mismatch is allotment-only and no controlling source identifies a wrong engine.
- `fixture_adapter_issue`: fixture semantics are too coarse for a direct bug claim, usually around utility-surface encoding.
- `needs_more_source_review`: official sources are blocked, conflicting, missing effective dates, secondary-only, or the fixture assumption is underspecified.

## Fail-Closed Rules

- Confirmed-bug labels require a controlling source assertion from an official primary source or a human-approved assertion.
- Secondary-only evidence cannot support a confirmed-bug label.
- Blocked official sources force `needs_more_source_review`.
- Conflicting primary assertions force `needs_more_source_review`.
- Missing effective-date metadata on controlling assertions forces `needs_more_source_review`.
- Underspecified fixture state, period, fixture class, or required input surface forces `needs_more_source_review`.

## Human Review Boundary

Dylan reviews only:

- resolver exceptions;
- source assertions that are blocked, contested, or promoted to human-approved status;
- any proposed upstream issue that depends on a confirmed-bug disposition.

The resolver output is therefore a triage artifact, not a substitute for upstream issue review.

# Spec: OIA statutory rules extraction + typed process→rule coupling (foi-o)

## Purpose

Demonstrate the rules/process coupling thesis on real data with a real consumer, and give the PIC contracts their first consumer. foi-o (https://github.com/edithatogo/foi-o) already models OIA *process* (events, states, clocks, certification boundaries) with statutory calculations embedded as bespoke Mojo/Python kernels. This track extracts those calculations into a **declarative rules module** with PIC-format parameters, fixtures, and traces, invoked by process events through a **typed interface**.

Why this matters (views/07 §4): OIA is process-heavy/rules-light — the mirror image of tax-benefit law. Instantiating the same artifact contracts here and in Track 4/5's tax-benefit work is the empirical form of the original "superset" claim.

## Target rules (statutory calculations to extract)

All references to the Official Information Act 1982 (NZ). **Agents MUST verify section numbers and current text against legislation.govt.nz before encoding; cite the consolidated version date in every sourceRef.**

| Rule ID (proposed) | Statute (verify) | Calculation |
|---|---|---|
| `nz-oia/decision.response_deadline` | s 15(1) | 20 working days from day after receipt; "working day" per s 2 definition (excludes weekends, listed holidays, and the Dec 25–Jan 15 period per current text) |
| `nz-oia/decision.extension_validity` | s 15A | Extension permitted grounds (large quantity / consultations / substantial collation); notice must be given within original time limit; extended period must be reasonable |
| `nz-oia/decision.transfer_deadline` | s 14 | Transfer promptly and in any case within 10 working days |
| `nz-oia/decision.deemed_refusal` | s 28(4)/(5) area | Failure to respond within time limit reviewable as refusal |
| `nz-oia/decision.urgency_flag` | s 12(3) | Requester may ask for urgency; affects process routing only (discretion point, NOT computable) |

The urgency rule is deliberately included as a **discretion point** to demonstrate the "typed, non-computable" pattern: it produces a `HumanDecisionRequired` marker with required-reasons metadata, never a computed outcome.

## Deliverables

Staged in this repo under `external/foi-o/` as a patch-ready tree; upstream submission is `[HUMAN]`.

### D1 `rules/` module for foi-o

- `rules/parameters/*.json` — PIC pic-parameters format: working-day limit (20), transfer limit (10), holiday-period definition parameter, each with sourceRefs and effective-date periods (statutory amendments = new periods).
- `rules/decisions/*.py` — pure Python functions (no I/O, no Mojo dependency; foi-o may later port to Mojo kernels — Python is its declared compatibility contract): `response_deadline(received_date, calendar) -> date`, `extension_valid(grounds, notice_date, original_deadline) -> ValueObject`, etc. Each function returns a PIC `valueObject` and a trace `step`.
- `rules/fixtures/*.json` — PIC pic-fixtures: golden cases curated from Ombudsman guidance and worked examples (candidates drafted by agent; promotion `[HUMAN]`). MUST include: receipt on a Friday before a holiday; receipt during the Dec–Jan shutdown period; an extension notified after the original deadline (invalid); a `not_provided` receipt date (valueState propagation).
- `rules/traces/` — sample traces emitted by running fixtures through the module.

### D2 Typed invocation interface

A small spec + implementation: `ProcessEventContext -> RuleInvocation -> RuleResult`.

```python
@dataclass
class RuleInvocation:
    decision_id: str          # "nz-oia/decision.response_deadline"
    inputs: dict[str, ValueObject]
    parameter_set: str        # parameter file version/date requested
    invoked_by: str           # foi-o event id — process knows the rule; rule never knows the process
@dataclass
class RuleResult:
    outputs: dict[str, ValueObject]
    trace_step: dict          # PIC trace step
    discretion_required: DiscretionPoint | None
```

Coupling rules (normative): the rules module has **zero imports from foi-o process code**; foi-o's event pipeline calls it through this interface only; evidence/verification state enters as `valueState`/`epistemicStatus` on inputs; results with `discretion_required` are routed to foi-o's human-certification boundary, never auto-applied.

### D3 Conformance in foi-o CI

A runner (`pytest` module) that loads the PIC fixtures, runs them through the rules module, compares against expected outputs, and validates emitted traces with `pic-validate`. Reconcile against foi-o's existing working-day kernels: **both implementations must agree on all fixtures** (differential test inside one repo — the smallest possible divergence study).

### D4 `SUBMISSION.md`

Draft PR description for foi-o: motivation (statutory calculations become declaratively testable and independently versioned; process pipeline decoupled from rule changes), file map, how it fits foi-o's Mojo-first direction (Python fallback contract), and a one-line note that fixture/parameter formats follow the PIC contracts (link) — format as footnote, not headline.

## Acceptance criteria

1. All target rules implemented as pure functions with ≥90% branch coverage (small module; go higher than the default 80%).
2. Differential agreement: new rules module vs existing foi-o working-day logic on every fixture (or documented, human-reviewed divergence — which would itself be a finding).
3. `pic-validate` passes on parameters, fixtures, and emitted traces.
4. The urgency discretion point produces `DiscretionPoint` and no computed outcome; test asserts it cannot be auto-certified.
5. `SUBMISSION.md` complete; upstream submission prepared but not sent (that is `[HUMAN]`).

## Out of scope

Withholding-grounds logic (s 6/s 9 public-interest balancing — pure discretion, encode nothing); charging calculations (defer to a follow-up once guidance sources are verified); any change to foi-o's certification boundary; MCP surfaces.

## Dependencies

Track 1 phases 1–3 (needs pic-semantics, pic-parameters, pic-fixtures, pic-traces schemas). Network access to read foi-o source; if unavailable, implement against foi-o's README-documented conventions and mark reconciliation tasks BLOCKED.

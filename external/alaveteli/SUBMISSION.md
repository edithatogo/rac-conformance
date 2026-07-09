**Status (2026-07-09): submitted + minimal PR.**  
Issue: https://github.com/mysociety/alaveteli/issues/9355  
PR: https://github.com/mysociety/alaveteli/pull/9356  
Implementation notes: `external/alaveteli/IMPLEMENTATION_STATUS.md`

# Alaveteli Upstream Proposal: Request State Taxonomy Mapping

**Track:** `community_20260704` (Phase 2)  
**Proposed By:** `foi-o` Project  
**Date:** July 2026

## Objective
Propose a documented request-state taxonomy with statutory-clock metadata hooks to Alaveteli/mySociety based on our experience normalising Alaveteli states in the `foi-o` processing engine.

## Context
Alaveteli request states (e.g. `waiting_response`, `gone_postal`, `successful`) represent user-facing status observations. However, for statutory compliance, audit, and legal-clock automation (such as OIA deadline calculations), these must map to cautious process-lifecycle states.

## State Mapping Table

| Alaveteli Source State | `foi-o` Normalised RequestState | Confidence | Mapping Description / Notes |
|---|---|---:|---|
| `waiting_response` | `RECEIVED` | 0.74 | Request is submitted and awaiting agency response; legal clock is active (receipt is Day 0). |
| `waiting_clarification` | `AWAITING_CLARIFICATION` | 0.78 | Clock may be paused or request restarted under s 15(1A) OIA pending clarification. |
| `gone_postal` | `SEARCHING` | 0.48 | Request handled offline; exact process state is inferred. |
| `internal_review` | `INTERNAL_REVIEW_REQUESTED` | 0.82 | Appeal stage; internal agency review is underway. |
| `error_message` | `UNKNOWN` | 0.20 | Platform-level error, not a legal state. |
| `requires_admin` | `UNKNOWN` | 0.20 | Moderation queue, not a legal state. |
| `successful` | `RELEASED_IN_FULL` | 0.55 | Platform reports success; legal status is full release. |
| `partially_successful` | `RELEASED_IN_PART` | 0.58 | Release in part with partial withholding/refusal. |
| `rejected` | `REFUSED` | 0.58 | Refusal of request; requires statutory grounds. |
| `not_held` | `NO_DOCUMENTS_FOUND` | 0.62 | Exemption or refusal under s 18(g) (information not held). |
| `information_not_held` | `NO_DOCUMENTS_FOUND` | 0.62 | Same as above. |
| `user_withdrawn` | `WITHDRAWN` | 0.75 | Request withdrawn by user; clock stops. |
| `not_foi` | `CLOSED` | 0.45 | Non-FOI request; platform closing. |

## Proposal
We propose that Alaveteli introduce structural hooks allowing local deployments (like FYI.org.nz) to expose metadata for these mappings, enabling downstream compliance tools (like `foi-o`) to automate statutory timelines without parsing free-text message threads.

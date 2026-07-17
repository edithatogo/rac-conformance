# FOI Demonstrator Analyst Decision Packet

**Review posture:** analyst-facing preparation only. This packet does not
certify a demonstrator, promote a candidate, change a machine-facing gate, or
authorize publication.

**Review base:** `54d6c93` (`pic-process-profile: reconcile certification
checkpoint`). Re-pin the evidence below to the commit under review before
recording a decision.

## Decision boundary

Review only whether the evidence supports a bounded compatibility demonstrator
for the following shared concepts:

- request timing and working-day deadline calculation;
- source and evidence references; and
- explicit analyst-review/discretion boundaries.

The decision must not be read as a finding of legal correctness, FOI-O
authority, production readiness, profile equivalence, universal portability,
independent adoption, or canonical `process-mappings` cutover. The candidate
profile remains a candidate until an analyst decision is recorded in the owning
track materials.

## Exact evidence index

| ID | Evidence link | Pin | Analyst use |
| --- | --- | --- | --- |
| E1 | [`contracts/process-profile/0.1.0/schema.json`](../../../contracts/process-profile/0.1.0/schema.json) | `cad9bd4b41da6745ee3ee8bd6ec46b68cd3160e368ecbfda6ee8e4fd84dffa77` | Confirm the profile contract and validation boundary. |
| E2 | [`contracts/process-profile/CONSUMER_INVENTORY.md`](../../../contracts/process-profile/CONSUMER_INVENTORY.md) | Re-pin at review | Check that claimed profile concepts have named consumers. |
| E3 | [`subrepos/process-mappings/profiles/foi/CANDIDATE_REVIEW.md`](../../../subrepos/process-mappings/profiles/foi/CANDIDATE_REVIEW.md) | Re-pin at review | Review the candidate status, losses, and non-authority language. |
| E4 | [`subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json`](../../../subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json) | `ba49100cd3599acc141208baaddf70c6822bbdbc96288d105eedf208e4731f5b` | Inspect candidate mappings and explicit loss notes. |
| E5 | [`external/foi-o/rules/SOURCES.md`](../../../external/foi-o/rules/SOURCES.md) | `0d565fecaed0d26beefac4a5574fd54a71db383be609e464389dbddbdb1a874f` | Check source authority, ambiguity notes, and analyst-review limits. |
| E6 | [`external/foi-o/rules/crosswalk.json`](../../../external/foi-o/rules/crosswalk.json) | `767849385b9ecc3f19763be0a14560f096fdaab984cc20dfae97d13c3c003a3f` | Compare source concepts with the staged PIC vocabulary. |
| E7 | [`external/foi-o/rules/traces/friday_before_public_holiday_response-trace.json`](../../../external/foi-o/rules/traces/friday_before_public_holiday_response-trace.json) | `2c7f157a59fcbea12f176a03dff9bbd1b00f42c559a0a621f287299f2eff7bd3` | Inspect one deterministic trace example; do not infer profile equivalence. |
| E8 | [`conductor/tracks/pic_process_profile_20260714/MAPPING_REVIEW_MATRIX.md`](../pic_process_profile_20260714/MAPPING_REVIEW_MATRIX.md) | `655ea3ce3b7e040433d1a42d8bf1845436177639aa6be49cc807720a3ae72bbc` | Review unresolved analyst questions and mapping exclusions. |

**Evidence gap:** no `external/foi-process/` execution/replay snapshot is
present in this branch. Do not treat a path from another branch or a narrative
reference as execution evidence; request the exact revision, file paths, and
digests if that evidence is required for the decision.

## Analyst checklist

- [ ] The shared-concept slice is narrow enough to avoid an interoperability
      or legal-authority claim.
- [ ] FOI-O remains the semantic authority and PIC remains a compatibility
      projection.
- [ ] Candidate mappings, trace identity, ontology loss, and discretion points
      are described without silently filling gaps.
- [ ] The unavailable execution/replay evidence is recorded as a blocker or
      explicitly excluded from this decision.
- [ ] No fixture or candidate is promoted as part of this review.

## Decision record for analyst completion

- Decision: `pending | bounded-compatible | changes-requested | rejected`
- Analyst: `______________________________`
- Date: `__________________`
- Evidence pins reviewed: `______________________________`
- Required changes or rationale: `______________________________`

This section is intentionally blank. An agent must not complete it.

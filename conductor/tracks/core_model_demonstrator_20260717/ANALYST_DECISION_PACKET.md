# FOI Demonstrator Analyst Decision Packet

**Review posture:** analyst decision recorded. This packet certifies only the
bounded demonstrator described below; it does not promote a candidate or
authorize publication.

**Evidence snapshot base:** `7fc0d50`. Record the final reviewed commit with
the decision; the evidence files below are pinned by digest.

## Decision boundary

Review only whether the evidence supports a bounded compatibility demonstrator
for the following shared concepts:

- request timing and working-day deadline calculation;
- source and evidence references; and
- explicit analyst-review/discretion boundaries.

The decision must not be read as a finding of legal correctness, FOI-O
authority, production readiness, profile equivalence, universal portability,
independent adoption, or canonical `process-mappings` cutover. The candidate
profile remains compatibility-certified but unpromoted. This review does not
reopen that certification or authorize canonical cutover.

## Exact evidence index

| ID | Evidence link | Pin | Analyst use |
| --- | --- | --- | --- |
| E1 | [`contracts/process-profile/0.1.0/schema.json`](../../../contracts/process-profile/0.1.0/schema.json) | `cad9bd4b41da6745ee3ee8bd6ec46b68cd3160e368ecbfda6ee8e4fd84dffa77` | Confirm the profile contract and validation boundary. |
| E2 | [`contracts/process-profile/CONSUMER_INVENTORY.md`](../../../contracts/process-profile/CONSUMER_INVENTORY.md) | `4c6ac13ba58202a7a6d801f0229cbea63ffd95dc55ace10e5dc437abc4b20297` | Check that claimed profile concepts have named consumers. |
| E3 | [`subrepos/process-mappings/profiles/foi/CANDIDATE_REVIEW.md`](../../../subrepos/process-mappings/profiles/foi/CANDIDATE_REVIEW.md) | `77327b22f411b33cbae355f22a0ad8064fbeea23517aa9cf06853db49dc3ad3a` | Confirm the previously certified candidate status, losses, and non-authority language. |
| E4 | [`subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json`](../../../subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json) | `ba49100cd3599acc141208baaddf70c6822bbdbc96288d105eedf208e4731f5b` | Inspect candidate mappings and explicit loss notes. |
| E5 | [`external/foi-o/rules/SOURCES.md`](../../../external/foi-o/rules/SOURCES.md) | `57f64e2f02d225302f048584cb600ba89bf67d1e80012ebfc03f304a3f314c95` | Check source authority, ambiguity notes, and analyst-review limits. |
| E6 | [`external/foi-o/rules/crosswalk.json`](../../../external/foi-o/rules/crosswalk.json) | `767849385b9ecc3f19763be0a14560f096fdaab984cc20dfae97d13c3c003a3f` | Compare source concepts with the staged PIC vocabulary. |
| E7 | [`external/foi-o/rules/traces/friday_before_public_holiday_response-trace.json`](../../../external/foi-o/rules/traces/friday_before_public_holiday_response-trace.json) | `2c7f157a59fcbea12f176a03dff9bbd1b00f42c559a0a621f287299f2eff7bd3` | Inspect one deterministic trace example; do not infer profile equivalence. |
| E8 | [`conductor/archive/pic_process_profile_20260714/CERTIFICATION_RECORD.json`](../../archive/pic_process_profile_20260714/CERTIFICATION_RECORD.json) | `4f6d6fbb1226938c0e501255670e65c659653a801168a1ffcc5d3cb81d6cb8bc` | Confirm the exact profile was already certified for compatibility and remains unpromoted. |
| E9 | [`external/foi-process/examples/generated/conformance-trace.json`](../../../external/foi-process/examples/generated/conformance-trace.json) | `8686db42aca8a89fece56e4139a262712e313beb57b7596ae9120adb0942b812` | Inspect the staged deterministic execution trace from `foi-process` revision `f67a351`. |
| E10 | [`external/foi-process/examples/generated/replay-snapshot.json`](../../../external/foi-process/examples/generated/replay-snapshot.json) | `5a69ba0d0fee1f62200dac0ab2039950b7c98cf7223143424eff338bc3ca2fa1` | Inspect replay evidence without treating its schema as equivalent to PIC traces. |
| E11 | [`FOI_DEMONSTRATOR_CHAIN.json`](FOI_DEMONSTRATOR_CHAIN.json) | `95b9c88765bd3629110a7149c97b860d0dccbe9791bc5b28fcd030749cc395ae` | Review the complete digest-pinned chain, losses, non-claims, and `none` equivalence claim. |

The `foi-process` execution and replay snapshots are staged evidence, not an
upstream release or independent result. Their distinct schema and case identity
are recorded as representational losses in `FOI_DEMONSTRATOR_CHAIN.json`.

## Analyst checklist

- [x] The shared-concept slice is narrow enough to avoid an interoperability
      or legal-authority claim.
- [x] FOI-O remains the semantic authority and PIC remains a compatibility
      projection.
- [x] Candidate mappings, trace identity, ontology loss, and discretion points
      are described without silently filling gaps.
- [x] The execution/replay evidence and its distinct schema are accepted or
      rejected within the bounded shared-concept comparison.
- [x] No fixture or candidate is promoted as part of this review.

## Decision record for analyst completion

- Decision: `bounded-compatible`
- Analyst: `Dylan`
- Date: `2026-07-18`
- Reviewed commit: `8343ad5f9dbc1d980ddf49018f2f6f4f6d181dde`
- Evidence pins reviewed: `E1-E11`
- Rationale: The digest-pinned chain supports the bounded shared-concept
  demonstrator with the declared representational losses and non-claims. It
  does not establish legal correctness, trace equivalence, production
  readiness, independent adoption, candidate promotion, or canonical cutover.

# PIC Process Profile Human Certification Packet

## Decision requested

Review the FOI-O candidate mapping and either certify the mapping for a
promoted profile, reject it, or request changes. This packet does not ask the
reviewer to certify legal meaning on behalf of FOI-O; `edithatogo/foi-o` remains
the semantic authority.

## Candidate

- Artifact: `subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json`
- Review notes: `subrepos/process-mappings/profiles/foi/CANDIDATE_REVIEW.md`
- Source spine: `external/foi-o/rules/SOURCES.md`
- Execution evidence: `external/foi-o/rules/traces/`
- Contract: `contracts/process-profile/0.1.0/`
- Machine-readable record: `CERTIFICATION_RECORD.json` (now `certified`).
- Row-level review aid: `MAPPING_REVIEW_MATRIX.md`.
- Candidate revision: `7990b4f`; the record pins the candidate SHA-256 and the
  `pic-process-profile/0.1.0` schema SHA-256.

## Review questions

1. Are `RequestObserved`, `TransferAssessed`, `TransferNotified`,
   `DeadlineCalculated`, `ExtensionAssessed`, `ExtensionNotified`,
   `OverdueFlagged`, and `DecisionCommunicated` the appropriate FOI-O event
   vocabulary for this compatibility candidate?
2. Does the candidate correctly distinguish observed events, executed actions,
   and derived deadline/overdue signals?
3. Is the reviewability state correctly non-terminal and explicitly prevented
   from being treated as an Ombudsman outcome, legal refusal conclusion, or
   certified human decision?
4. Are the source assertion, effective date, authority classification, actor
   links, and working-day timer appropriate?
5. Are the expanded loss notes complete, including FOI-O payload fields,
   ontology hierarchy, discretion, and reasonableness judgments?
6. Should this remain a candidate, or may it be promoted into a certified
   profile artifact after these questions are answered?

The row-level questions and explicit non-claims are listed in
`MAPPING_REVIEW_MATRIX.md`.

## Certification record

Complete this section by hand. An agent must not fill it in.

The machine-readable record must be updated by the human reviewer after the
decision. Its candidate and contract SHA-256 values must remain unchanged.

- Decision: `pending | certified | rejected | changes-requested`
- Reviewer: `______________________________`
- Date: `__________________`
- Evidence or change request: `______________________________`

## Decision log

- Decision 1, event vocabulary and non-terminal state semantics: **approved by
  Dylan on 2026-07-16**.
- Decision 2, event-kind distinctions: **approved by Dylan on 2026-07-16**.
- Decision 3, reviewability boundary: **approved by Dylan on 2026-07-16**.
- Decision 4, source/actor/timer integrity: **approved by Dylan on 2026-07-16**.
- Decision 5, loss notes and non-claims: **approved by Dylan on 2026-07-16**.
- Overall disposition: **certified by Dylan on 2026-07-16** for PIC
  compatibility; candidate retained pending #50 repository cutover.

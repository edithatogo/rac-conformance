# Medicine Regulatory and Payer Pathways

Status: Draft | Consumed-by: PIC process-profile comparative study, future platform adapter

## Overview

Model the evidence-to-access lifecycle across market authorisation, health
technology assessment, funding recommendation, pricing/listing, individual
access, implementation, and post-market monitoring. The study preserves the
different mandates of Medsafe and Pharmac; TGA, PBAC/PBS, and MSAC/MBS; MHRA and
NICE; and FDA and US payers.

The first executable comparison is deliberately narrower than the full matrix:
one publicly documented medicine/indication, two regulator-to-funder jurisdiction
pairs, and an optional Australian codependent service/technology branch. The
specific case requires human approval after a source-readiness assessment.

Depends on: `pic_process_profile_20260714` Phase 2.

Implementation home: source manifests, authority matrices, candidate mappings,
and synthetic comparison scenarios live under
`subrepos/process-mappings/profiles/health-technology/`. Normative PIC schemas
and conformance behavior remain in `rac-conformance`.

## Functional Requirements

1. Create an authority/function matrix for NZ, Australia, UK, and US pathways.
2. Separate marketing authorisation from reimbursement and service funding.
3. Represent submission, validation, evidence request, technical review,
   committee advice, consultation, decision, pricing/listing, restrictions,
   reconsideration/appeal, implementation, exception, and post-market states
   where supported by controlling sources.
4. Model parallel and conditional pathways; do not assume authorisation always
   precedes HTA work or that positive advice guarantees listing or access.
5. Represent confidential/commercial evidence as unavailable with an explicit
   epistemic state, never inferred from public summaries.
6. Select a comparison case using source completeness, public decision records,
   comparable indication, temporal alignment, and licensing criteria.
7. Produce deterministic candidate fixtures and traces with independent review.
8. Consume the optional adverse-incident post-market safety handoff only where an
   official source supports monitoring or reassessment. Consumption must preserve
   privacy purpose, provenance, uncertainty, and human decision ownership.

## Non-Functional Requirements

- Use official regulator, HTA, payer, legislation, and published decision sources.
- No clinical recommendation, reimbursement recommendation, price inference, or
  patient-level access decision.
- Money and thresholds use decimal strings.
- Preserve public, confidential, redacted, unavailable, and not-applicable states.
- Treat MBS/MSAC as a service and technology pathway, not a medicine regulator or
  PBS substitute.

## Acceptance Criteria

- The authority matrix correctly distinguishes regulator, HTA adviser, payer,
  minister/delegate, listing body, and post-market actor.
- At least two jurisdiction slices run through the same process-profile harness
  while preserving documented differences.
- Tests reject false equivalence, jurisdiction leakage, stale decisions,
  confidential-data inference, and unsupported causal claims.
- Cross-domain tests reject patient-level incident data and any inference that a
  safety signal determines regulatory, funding, restriction, or access outcomes.
- Every promoted fixture has a human-certified source spine.
- `make check` passes.

## Out of Scope

- Exhaustive mapping of every pathway or expedited programme.
- Ranking agencies or medicines.
- Reconstructing confidential economic models, prices, or committee deliberation.
- Generalising one product/indication result to an agency's complete process.
- Treating FDA as a payer or MBS as a medicine-listing authority.

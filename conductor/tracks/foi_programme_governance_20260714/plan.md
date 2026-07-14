# Plan: Freedom of Information programme governance

## Phase 1: Umbrella definition

- [ ] Task: Update Project 14 title documentation, description, repository roles,
      inclusion filters, and status semantics.
- [ ] Task: Add navigation anchors for every in-scope repository and dedicated Project.
- [ ] Task: Define FOI-only filters for multi-purpose repositories.
- [ ] Task: Conductor - User Manual Verification 'Umbrella definition' (Protocol in workflow.md)

## Phase 2: Item synchronization

- [ ] Task: Add current FOI programme issues to Project 14 without removing
      their dedicated Project membership.
- [ ] Task: Add dependency and jurisdiction metadata where Project fields support it.
- [ ] Task: Verify issue state and Project status against local Conductor plans.
- [ ] Task: Conductor - User Manual Verification 'Item synchronization' (Protocol in workflow.md)

## Phase 3: Durable governance

- [ ] Task: Document or implement a repeatable item-level sync with FOI-only allowlists.
- [ ] Task: Add drift checks for missing, stale, or unrelated Project 14 items.
- [ ] Task: Run repository quality gates and Conductor review.
- [ ] Task: Archive only after live Project evidence is recorded.
- [ ] Task: Conductor - User Manual Verification 'Durable governance' (Protocol in workflow.md)

## Phase 4: FOI-O to PIC compatibility profile

- [x] Task: Specify a machine-readable release-handshake manifest that pins
      FOI-O, PIC, legislation, archive, Hugging Face dataset, NLP pipeline,
      jurisdiction-profile, and calendar versions and content digests.
- [x] Task: Define a lossless governance crosswalk that keeps FOI-O epistemic,
      review, extraction, and certification axes separate from PIC `valueState`.
- [ ] Task: Extend or wrap PIC fixtures, parameters, and traces with common
      jurisdiction, applicable-time, observation-time, and evidence-reference
      metadata without creating a FOI-O runtime dependency on PIC.
- [x] Task: Write valid examples and at least three negative examples covering
      digest mismatch, cross-jurisdiction leakage, and incompatible legislative
      or calendar versions before implementing schema validation.
- [ ] Task: Implement offline validation and a release compatibility matrix,
      then exercise both repositories against pinned published artifacts rather
      than checkout-relative paths.
- [ ] Task: Require independent-oracle review before generated FOI-O candidates
      can be promoted to PIC golden fixtures or approved crosswalk rows.
- [ ] Task: Produce a machine-readable release-evidence bundle for the papers
      track, including immutable Hugging Face dataset coordinates for derived
      `fyi-archive` outputs.
- [ ] Task: Conductor - User Manual Verification 'FOI-O to PIC compatibility profile' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): The optional compatibility manifest, lossless governance
> boundary, two valid examples, three negative examples, validator registration,
> and candidate compatibility matrix are present and tested locally. PIC wrapping,
> independent-oracle promotion, immutable release evidence, and human verification
> remain open.

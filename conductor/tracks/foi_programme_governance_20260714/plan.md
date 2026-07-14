# Plan: Freedom of Information programme governance

## Phase 1: Umbrella definition

- [x] Task: Update Project 14 title documentation, description, repository roles,
      inclusion filters, and status semantics.
- [x] Task: Add navigation anchors for every in-scope repository and dedicated Project.
- [x] Task: Define FOI-only filters for multi-purpose repositories.
- [ ] Task: Conductor - User Manual Verification 'Umbrella definition' (Protocol in workflow.md)

> BLOCKED (2026-07-14): Manual verification requires Dylan to confirm the
> live Project 14 title, scope, repository boundaries, and navigation anchors.

> CHECKPOINT (2026-07-14): Live Project 14 documentation at
> `https://github.com/users/edithatogo/projects/14` already contains the
> approved title, all seven repository roles and boundaries, FOI-only scope
> rules, status semantics, and navigation anchors for dedicated boards.

## Phase 2: Item synchronization

- [x] Task: Add current FOI programme issues to Project 14 without removing
      their dedicated Project membership.
- [x] Task: Add dependency and jurisdiction metadata where Project fields support it.
- [x] Task: Verify issue state and Project status against local Conductor plans.
- [ ] Task: Conductor - User Manual Verification 'Item synchronization' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): Project 14 contains the current FOI-O #23/#24,
> rac-conformance #30, fyi-archive #187/#188, nlp-policy-nz #100/#101, and
> legislation #62 items; the paper release gate rac-conformance #31 was added.
> Their current Project status is `Todo`, matching the local plans. Project 14
> now provides jurisdiction, repository role, dependency, evidence status,
> human gate, and delivery status fields; all 18 allowlisted items have values.

## Phase 3: Durable governance

- [x] Task: Document or implement a repeatable item-level sync with FOI-only allowlists.
- [x] Task: Add drift checks for missing, stale, or unrelated Project 14 items.
- [x] Task: Run repository quality gates and Conductor review.
- [ ] Task: Archive only after live Project evidence is recorded.
- [ ] Task: Conductor - User Manual Verification 'Durable governance' (Protocol in workflow.md)

> CHECKPOINT (2026-07-15): Added `project14-allowlist.json` and
> `tools/validate_project14_allowlist.py`. Against the live Project 14 export,
> the checker initially found all 18 required items and 67 extra historical
> items. The historical items were removed from Project 14 only, preserving
> their source issues and dedicated-project memberships. The live board now
> passes the exact allowlist with zero missing, extra, or stale items.

> REVIEW (2026-07-15): Added stale-status detection and four passing unit tests.
> Full `make check` passed after the checker integration.

## Phase 4: FOI-O to PIC compatibility profile

- [x] Task: Specify a machine-readable release-handshake manifest that pins
      FOI-O, PIC, legislation, archive, Hugging Face dataset, NLP pipeline,
      jurisdiction-profile, and calendar versions and content digests.
- [x] Task: Define a lossless governance crosswalk that keeps FOI-O epistemic,
      review, extraction, and certification axes separate from PIC `valueState`.
- [x] Task: Extend or wrap PIC fixtures, parameters, and traces with common
      jurisdiction, applicable-time, observation-time, and evidence-reference
      metadata without creating a FOI-O runtime dependency on PIC.
- [x] Task: Write valid examples and at least three negative examples covering
      digest mismatch, cross-jurisdiction leakage, and incompatible legislative
      or calendar versions before implementing schema validation.
- [ ] Task: Implement offline validation and a release compatibility matrix,
      then exercise both repositories against pinned published artifacts rather
      than checkout-relative paths.

> BLOCKED (2026-07-14): `pic-foio-check`, content-addressed offline bundle
> validation, and a fail-closed compatibility matrix are implemented. The live
> exercise cannot pass until `edithatogo/foi-o` publishes a V2 release: the
> existing `v0.8.0` tag lacks the V2 manifest/codebook/capability/migration
> artifacts, and no GitHub release or release PR currently exists.
- [x] Task: Require independent-oracle review before generated FOI-O candidates
      can be promoted to PIC golden fixtures or approved crosswalk rows.
- [x] Task: Produce a machine-readable release-evidence bundle for the papers
      track, including immutable Hugging Face dataset coordinates for derived
      `fyi-archive` outputs.
- [ ] Task: Conductor - User Manual Verification 'FOI-O to PIC compatibility profile' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): The optional compatibility manifest, lossless governance
> boundary, two valid examples, three negative examples, validator registration,
> PIC artifact wrappers, fail-closed oracle promotion, offline bundle checks, and
> a machine-readable papers handoff are present and tested locally. The live
> published-artifact exercise, independent human review, and manual verification
> remain open.

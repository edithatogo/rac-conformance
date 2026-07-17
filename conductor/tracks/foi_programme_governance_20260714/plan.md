# Plan: Freedom of Information programme governance

> ANALYST AUDIT (2026-07-17): Existing Project 14 checkpoints and approval
> notes are retained as dated historical records. This audit performed no live
> Project verification and does not refresh, archive, or mark the governance
> track complete. Use `HUMAN_VERIFICATION_PACKET.md` to record current evidence
> and analyst decisions before relying on hosted status.

## Phase 1: Umbrella definition

- [x] Task: Update Project 14 title documentation, description, repository roles,
      inclusion filters, and status semantics.
- [x] Task: Add navigation anchors for every in-scope repository and dedicated Project.
- [x] Task: Define FOI-only filters for multi-purpose repositories.
- [ ] Task: Conductor - User Manual Verification 'Umbrella definition' (Protocol in workflow.md)

> BLOCKED (2026-07-14): Manual verification requires Dylan to confirm the
> live Project 14 title, scope, repository boundaries, and navigation anchors.
> Prepared review surface: `HUMAN_VERIFICATION_PACKET.md` section 1.

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

> CHECKPOINT (2026-07-15): Live Project 14 contains the current FOI-O #23/#24,
> rac-conformance #30, fyi-archive #187/#188, nlp-policy-nz #100/#101, and
> legislation #62 items; the paper release gate rac-conformance #31 was added.
> Completed delivery items nlp-policy-nz #100/#101 and rac-conformance #36 are
> explicitly overridden to `Done`; all other allowlisted items are `Todo`.
> Project 14 provides jurisdiction, repository role, dependency, evidence
> status, human gate, and delivery status fields; all 19 allowlisted items have
> values.
> Prepared review surface: `HUMAN_VERIFICATION_PACKET.md` section 2.

## Phase 3: Durable governance

- [x] Task: Document or implement a repeatable item-level sync with FOI-only allowlists.
- [x] Task: Add drift checks for missing, stale, or unrelated Project 14 items.
- [x] Task: Run repository quality gates and Conductor review.
- [x] Task: Archive only after live Project evidence is recorded.
- [ ] Task: Conductor - User Manual Verification 'Durable governance' (Protocol in workflow.md)

> CHECKPOINT (2026-07-15): Added `project14-allowlist.json` and
> `tools/validate_project14_allowlist.py`. Against the live Project 14 export,
> the checker initially found all 18 required items and 67 extra historical
> items. The historical items were removed from Project 14 only, preserving
> their source issues and dedicated-project memberships. Delivery PR #36 was
> subsequently added as the nineteenth required item. A fresh export found the
> completed NLP issues #100/#101 still expected as `Todo`; their explicit
> `Done` overrides now make the exact allowlist pass with zero missing, extra,
> or stale items.
> Prepared review surface: `HUMAN_VERIFICATION_PACKET.md` section 3.

> REVIEW (2026-07-14): Added stale-status detection and four passing unit tests.
> Full `make check` passed after the checker integration.

> REVIEW (2026-07-14): Phase 4 review closed fail-open validation edges:
> malformed timestamps now report deterministic errors, publication/review URIs
> must be content-addressed, and offline bundles validate each wrapped artifact
> against its complete PIC schema rather than trusting `conformsTo` alone.

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
> Prepared boundary review: `HUMAN_VERIFICATION_PACKET.md` section 4.

> FINAL REVIEW (2026-07-14): Full `make check` passed after remediation:
> repository audit, 11 tools tests, 46 contract tests at 87.20% coverage,
> schema corpus validation, 25 converter tests, 20 harness tests, 33 SNAP
> tests, 16 NZ reconciliation tests, 6 service-boundary tests, and 2
> Docassemble tests. No repo-owned correctness blocker remains.

> PR REVIEW FIX (2026-07-14): Hardened bitemporal comparison for mixed
> offset-naive/aware inputs, normalized equivalent ISO-8601 instants, and split
> missing-profile diagnostics from independent jurisdiction/version mismatches.
> Fourteen focused compatibility tests pass.

> DELIVERY CHECKPOINT (2026-07-14): PR #36 merged after all hosted checks and
> review threads passed. Project 14 records it as `Done`, with human gate
> satisfied and delivery status done. The drift checker now supports per-item
> status overrides and fails on missing values in any of the six programme
> metadata fields.

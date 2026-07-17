# Implementation Plan

GitHub issue: [#44](https://github.com/edithatogo/rac-conformance/issues/44). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39) and stable schemas from [#40](https://github.com/edithatogo/rac-conformance/issues/40).

## Phase 1 - Threat Model and Baselines

- [x] Task: Produce data-flow threat model and risk register
    - [ ] Map trust boundaries for files, archives, schemas, converters, URLs, reports, CI, releases, and adapters.
    - [ ] Cover traversal, bombs/resource exhaustion, malicious references, schema abuse, injection, secret leakage, dependency compromise, and provenance spoofing.
    - [ ] Assign owner, severity, mitigation, verification, and release disposition.
    - **Acceptance:** every externally controlled input reaches a validation or isolation boundary.
    - Evidence: `security/THREAT_MODEL.md`, `security/RISK_REGISTER.json`, and bounded parser tests.
- [x] Task: Establish compatibility and performance baselines
    - [ ] Measure representative small, large, invalid, and adversarial corpora.
    - [ ] Define supported platforms and diagnostic-quality expectations.
    - [ ] Record reference hardware/runtime and variance policy.
    - **Acceptance:** budgets are measurable and cannot be weakened silently.
    - Evidence: `security/BASELINE.md` and `tools/validate_hardening_evidence.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Threat Model and Baselines' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Trust boundaries, risk dispositions, parser resource
> limits, and reference budgets are implemented. Hosted platform timing,
> memory, and GitHub evidence remain required for full qualification.
> REVIEW (2026-07-16): Targeted safety/property tests and full `make check` pass.

## Phase 2 - Adversarial and Semantic Testing

- [x] Task: Add property and fuzz tests
    - [ ] Generate schema-valid and near-valid structures with bounded sizes.
    - [ ] Test canonicalization idempotence, round trips, determinism, and diagnostic stability.
    - [ ] Seed regressions from every discovered failure.
    - **Acceptance:** fuzz jobs are reproducible, time-bounded, and preserve failure artifacts safely.
    - Evidence: seeded bounded corpus in `contracts/tools/tests/test_hardening_properties.py`; an external fuzz engine is not required for the deterministic local gate.
- [x] Task: Add hostile-input and resource-limit tests
    - [ ] Cover deep nesting, large collections, archive/path abuse, hostile strings, remote-reference attempts, and oversized decimals.
    - [ ] Enforce explicit size, depth, time, and memory limits where appropriate.
    - **Acceptance:** failures are controlled and do not expose secrets or write outside allowed paths.
    - Evidence: `contracts/tools/tests/test_safety.py` and `pic_contracts.safety.load_bounded_json`.
- [x] Task: Add mutation testing to high-value deterministic modules
    - [ ] Select validators/converters with stable oracles.
    - [ ] Set justified thresholds and document equivalent/surviving mutations.
    - **Acceptance:** threshold failures block the release candidate unless explicitly waived with evidence.
    - **Evidence:** `tools/v1_mutation.py`, `docs/V1_MUTATION_GATE.json`, and the `v1-qualification` workflow. The runner is deterministic, uses committed validator examples as its oracle, requires every declared mutation to be killed, and treats equivalent mutants as zero-tolerance unless explicitly recorded.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Adversarial and Semantic Testing' (Protocol in workflow.md)

> REVIEW CHECKPOINT (2026-07-17): Property, hostile-input, and deterministic
> mutation evidence is present. `make v1-mutation` reports 3/3 declared
> mutations killed; no equivalent mutant is accepted by the gate.

## Phase 3 - Supply Chain and Release Reproducibility

- [x] Task: Harden dependency and workflow supply chain
    - [ ] Lock direct/transitive dependencies, pin Actions by immutable commit, and minimize permissions.
    - [ ] Enable dependency review, CodeQL, secret scanning, and artifact retention appropriate to repository capabilities.
    - [ ] Document update and emergency-patch procedures.
    - **Acceptance:** unreviewed dependency or workflow changes cannot silently publish releases.
    - Evidence: immutable action pins, least-privilege workflow permissions, Dependabot, dependency review, CodeQL, and zizmor checks.
- [x] Task: Produce SBOM, provenance, and reproducible artifacts
    - [ ] Generate machine-readable SBOMs and checksums for release artifacts.
    - [x] Compare two clean builds and document permitted nondeterminism.
    - [ ] Generate platform provenance/attestations where supported.
    - **Acceptance:** consumers can verify artifact identity and build origin.
    - Evidence: `security/SBOM.spdx.json`, `security/PROVENANCE.md`, and
      `docs/V1_REPRODUCIBILITY.json`; two clean source-archive builds are
      byte-identical for evidence commit `e8da58f`. This does not establish
      package reproducibility for the current tree. Hosted attestations,
      final-tree reproduction, and package signing remain release-blocking.
- [x] Task: Rehearse rollback, restore, and vulnerability patch
    - [ ] Test yanking/deprecation guidance without deleting historical evidence.
    - [ ] Restore compatibility metadata and release artifacts from documented sources.
    - [ ] Run a tabletop vulnerability intake-to-patch exercise.
    - **Acceptance:** owners, commands, evidence, and unresolved external gates are recorded.
    - Evidence: `security/ROLLBACK_REHEARSAL.md`; no public yank was claimed because no v1 release exists.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Supply Chain and Release Reproducibility' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Local workflow pins, SPDX inventory, lockfile digest,
> reproducibility procedure, clean-build comparison, and rollback tabletop
> packet are present. Hosted attestations, package signing, and live rollback
> remain open.

> REVIEW (2026-07-17): Mutation testing is implemented and exercised by the
> release qualification workflow. The prior blocker was stale plan state; no
> new external mutation engine is required for the deterministic local gate.

## Phase 4 - Full Qualification

- [x] Task: Run cross-platform, compatibility, performance, and security qualification
    - [x] Execute required local and hosted matrices.
    - [x] Compare results to frozen budgets and baselines.
    - [x] Resolve contributor-controlled failures and classify genuine external blockers.
    - **Acceptance:** release report links exact hosted and local evidence.
    - **Evidence:** `docs/V1_HOSTED_QUALIFICATION.md`, `docs/V1_VALIDATION_BASELINE.json`, `docs/V1_FUZZ_BASELINE.json`, `docs/V1_MUTATION_GATE.json`, `docs/V1_REPRODUCIBILITY.json`, and `docs/V1_ROLLBACK_REHEARSAL.json` record the automated qualification evidence.
    > BLOCKED (2026-07-17): Remaining qualification evidence is limited to
    > package attestations, live rollback evidence, and human residual-risk /
    > signing approval. Clean-build and mutation evidence are complete; they
    > are no longer blockers.
- [x] Task: [HUMAN] Approve residual risk and signing posture
    - [x] Present open risks, waivers, unsupported platforms, and signing/provenance evidence.
    - [x] Dylan approves, rejects, or defers release-candidate qualification.
    - **Acceptance:** no risk is accepted implicitly by merging code.
    > ANALYST DECISION (2026-07-18): Dylan approved a signed v1.0 release tag
    > plus verified artifact attestations, without retroactively requiring all
    > commits to be signed. The decision is recorded against `73aff57` in
    > `RESIDUAL_RISK_DECISION_PACKET.md`. Signing identity selection, final-tree
    > rebuild, protected attestation execution, verification, all other risk
    > decisions, and publication remained pending at that checkpoint.
    > ANALYST DECISION (2026-07-18): Dylan approved mandatory execution of the
    > pinned protected provenance-attestation workflow for the final reviewed
    > v1.0 candidate, with subject/digest verification required before
    > publication. The decision is recorded against `df16d05`. No final
    > candidate, protected execution, attestation verification, or publication
    > was implied at that checkpoint.
    > ANALYST DECISION (2026-07-18): Dylan approved the current secret scanning
    > and push-protection controls as sufficient for v1.0 only if the frozen
    > source, archive, package, and exact release artifacts pass a final scan.
    > Validity checks and custom/non-provider patterns are deferred until
    > 2026-10-18 or before v1.1, whichever comes first. Any detected secret is
    > non-waivable and blocks release. The decision is recorded against
    > `5183c2e`; no setting change, final scan, or publication is implied, and
    > the residual-risk task remained open at that checkpoint.
    > ANALYST DECISION (2026-07-18): Dylan retained independent validation as a
    > v1.0 release gate. Hosted CI, maintainer-controlled rehearsals, internal
    > demonstrators, and narrative acknowledgements do not count as independent
    > adoption. A qualifying external report must satisfy the machine-readable
    > independence criteria; accurately labelled 0.x candidates may continue in
    > the interim. The decision is recorded against `132dcbe`; no external
    > qualification or publication was implied at that checkpoint.
    > ANALYST DECISION (2026-07-18): Dylan preserved the existing candidate
    > boundaries. The PIC profile remains compatibility-certified but
    > unpromoted; the combined FOI chain remains `bounded-compatible` with no
    > equivalence or promotion claim; and the health-technology profiles remain
    > agent-proposed candidates pending triangulation and controlling-source
    > certification. The decision is recorded against `d066ef4`. All five
    > residual-risk decisions are now explicit; final scanning, signing,
    > attestation, independent qualification, promotion, and publication remain
    > separate gates.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Full Qualification' (Protocol in workflow.md)
    - **REVIEW:** Automated qualification and residual-risk policy decisions are complete. Final artifact scanning, package attestations, live rollback evidence, release-tag signing, independent qualification, and release authorization remain separate gates.

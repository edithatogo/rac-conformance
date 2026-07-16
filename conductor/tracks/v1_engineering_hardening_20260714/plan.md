# Implementation Plan

GitHub issue: [#44](https://github.com/edithatogo/rac-conformance/issues/44). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39) and stable schemas from [#40](https://github.com/edithatogo/rac-conformance/issues/40).

## Phase 1 - Threat Model and Baselines

> CHECKPOINT (2026-07-16): Threat boundaries, risk ownership, release
> dispositions, and deterministic validation/performance budgets are recorded
> in `docs/V1_THREAT_MODEL.md`, `docs/V1_RISK_REGISTER.json`, and
> `docs/V1_VALIDATION_BASELINE.json`. The baseline passes on the reference
> macOS/CPython environment; cross-platform and hosted controls remain open.

- [x] Task: Produce data-flow threat model and risk register
    - [ ] Map trust boundaries for files, archives, schemas, converters, URLs, reports, CI, releases, and adapters.
    - [ ] Cover traversal, bombs/resource exhaustion, malicious references, schema abuse, injection, secret leakage, dependency compromise, and provenance spoofing.
    - [ ] Assign owner, severity, mitigation, verification, and release disposition.
    - **Acceptance:** every externally controlled input reaches a validation or isolation boundary.
    - Evidence: `docs/V1_THREAT_MODEL.md` and `docs/V1_RISK_REGISTER.json` enumerate filesystem, archive, source, converter, cross-repository, report, CI, release, and adapter boundaries; unresolved controls remain explicitly release-blocking.
- [x] Task: Establish compatibility and performance baselines
    - [ ] Measure representative small, large, invalid, and adversarial corpora.
    - [ ] Define supported platforms and diagnostic-quality expectations.
    - [ ] Record reference hardware/runtime and variance policy.
    - **Acceptance:** budgets are measurable and cannot be weakened silently.
    - Evidence: `tools/v1_baseline.py`, `Makefile` target `v1-baseline`, and `docs/V1_VALIDATION_BASELINE.json` measure small, invalid, large, and deeply nested cases with explicit byte/time budgets and a reviewed variance policy.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Threat Model and Baselines' (Protocol in workflow.md)

## Phase 2 - Adversarial and Semantic Testing

> CHECKPOINT (2026-07-16): The bounded fuzz corpus, extraction traversal and
> size protections, and deterministic mutation gate pass. Six synthetic
> mutations are reproducible, three stable validator mutants are killed, and
> no sensitive or external source data is used. Cross-platform hosted runs and
> broader memory/CPU qualification remain deferred to Phase 4.

- [x] Task: Add property and fuzz tests
    - [ ] Generate schema-valid and near-valid structures with bounded sizes.
    - [ ] Test canonicalization idempotence, round trips, determinism, and diagnostic stability.
    - [ ] Seed regressions from every discovered failure.
    - **Acceptance:** fuzz jobs are reproducible, time-bounded, and preserve failure artifacts safely.
    - Evidence: `tools/v1_fuzz.py`, `Makefile` target `v1-fuzz`, and `docs/V1_FUZZ_BASELINE.json` run six bounded deterministic mutations from a committed synthetic example and require every mutation to fail closed.
- [x] Task: Add hostile-input and resource-limit tests
    - [ ] Cover deep nesting, large collections, archive/path abuse, hostile strings, remote-reference attempts, and oversized decimals.
    - [ ] Enforce explicit size, depth, time, and memory limits where appropriate.
    - **Acceptance:** failures are controlled and do not expose secrets or write outside allowed paths.
    - Evidence: `tools/process_mappings_rehearsal.py` enforces per-file and total extraction-size limits plus resolved destination containment; `tools/tests/test_process_mappings_rehearsal.py` covers traversal and absolute-path rejection.
- [x] Task: Add mutation testing to high-value deterministic modules
    - [ ] Select validators/converters with stable oracles.
    - [ ] Set justified thresholds and document equivalent/surviving mutations.
    - **Acceptance:** threshold failures block the release candidate unless explicitly waived with evidence.
    - Evidence: `tools/v1_mutation.py`, `Makefile` target `v1-mutation`, and `docs/V1_MUTATION_GATE.json` mutate three stable validator predicates; all three are killed by committed process-profile oracles and the threshold permits no survivors.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Adversarial and Semantic Testing' (Protocol in workflow.md)

## Phase 3 - Supply Chain and Release Reproducibility

- [ ] Task: Harden dependency and workflow supply chain
    - [ ] Lock direct/transitive dependencies, pin Actions by immutable commit, and minimize permissions.
    - [ ] Enable dependency review, CodeQL, secret scanning, and artifact retention appropriate to repository capabilities.
    - [ ] Document update and emergency-patch procedures.
    - **Acceptance:** unreviewed dependency or workflow changes cannot silently publish releases.
    - Evidence: `docs/V1_SUPPLY_CHAIN_EVIDENCE.md` and `docs/V1_HOSTED_GOVERNANCE.md` record local action pinning, permissions, workflow/dependency audits, SBOM results, hosted secret-scanning/push-protection status, and main-branch required checks/code-owner review.
    - **BLOCKED (2026-07-16):** Required commit signatures remain disabled and artifact-attestation execution is unverified. The protected `release` environment and pinned attestation step are configured in `.github/workflows/v1-release-qualification.yml`.
- [ ] Task: Produce SBOM, provenance, and reproducible artifacts
    - [ ] Generate machine-readable SBOMs and checksums for release artifacts.
    - [ ] Compare two clean builds and document permitted nondeterminism.
    - [ ] Generate platform provenance/attestations where supported.
    - **Acceptance:** consumers can verify artifact identity and build origin.
    - Evidence: `docs/V1_SBOM.json` and `tools/v1_reproducibility.py`/`docs/V1_REPRODUCIBILITY.json` provide a machine-readable SBOM, commit/tree identity, two identical deterministic source archives, and evidence digests; hosted attestation remains explicitly not performed.
    - **BLOCKED (2026-07-16):** Local evidence proves source/archive identity and reproducibility, but hosted signing/provenance attestation remains unverified until the protected workflow is approved and executed.
- [x] Task: Rehearse rollback, restore, and vulnerability patch
    - [ ] Test yanking/deprecation guidance without deleting historical evidence.
    - [ ] Restore compatibility metadata and release artifacts from documented sources.
    - [ ] Run a tabletop vulnerability intake-to-patch exercise.
    - **Acceptance:** owners, commands, evidence, and unresolved external gates are recorded.
    - Evidence: `tools/v1_rollback_rehearsal.py` and `docs/V1_ROLLBACK_REHEARSAL.json` restore the current tree and historical `v0.2.0` fallback from deterministic archives and record the tabletop response; hosted yanking/signing/notification remain unperformed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Supply Chain and Release Reproducibility' (Protocol in workflow.md)

## Phase 4 - Full Qualification

- [x] Task: Run cross-platform, compatibility, performance, and security qualification
    - [ ] Execute required local and hosted matrices.
    - [ ] Compare results to frozen budgets and baselines.
    - [ ] Resolve contributor-controlled failures and classify genuine external blockers.
    - **Acceptance:** release report links exact hosted and local evidence.
    - Evidence: `.github/workflows/v1-qualification.yml`, `.github/workflows/v1-release-qualification.yml`, and `docs/V1_HOSTED_QUALIFICATION.md` record the successful immutable-pinned matrix and the protected manual release qualification path. Hosted branch protection, secret scanning, the protected release environment, signatures, and attestations remain separate controls.
- [ ] Task: [HUMAN] Approve residual risk and signing posture
    - [ ] Present open risks, waivers, unsupported platforms, and signing/provenance evidence.
    - [ ] Dylan approves, rejects, or defers release-candidate qualification.
    - **Acceptance:** no risk is accepted implicitly by merging code.
    - **Packet:** `RESIDUAL_RISK_DECISION_PACKET.md` records the exact open hosted controls, candidate-only boundaries, evidence references, and required decision fields.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Full Qualification' (Protocol in workflow.md)

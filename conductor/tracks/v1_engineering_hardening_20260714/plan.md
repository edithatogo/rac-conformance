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
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Adversarial and Semantic Testing' (Protocol in workflow.md)

## Phase 3 - Supply Chain and Release Reproducibility

- [ ] Task: Harden dependency and workflow supply chain
    - [ ] Lock direct/transitive dependencies, pin Actions by immutable commit, and minimize permissions.
    - [ ] Enable dependency review, CodeQL, secret scanning, and artifact retention appropriate to repository capabilities.
    - [ ] Document update and emergency-patch procedures.
    - **Acceptance:** unreviewed dependency or workflow changes cannot silently publish releases.
    - Evidence: `docs/V1_SUPPLY_CHAIN_EVIDENCE.md` and `docs/V1_SBOM.json` record local action pinning, permissions, workflow audit, dependency audit, lockfiles, and SBOM results.
    - **BLOCKED (2026-07-16):** GitHub-side branch protection, secret scanning/push protection, protected environments, and signing/attestation settings require hosted verification; local configuration cannot prove them.
- [ ] Task: Produce SBOM, provenance, and reproducible artifacts
    - [ ] Generate machine-readable SBOMs and checksums for release artifacts.
    - [ ] Compare two clean builds and document permitted nondeterminism.
    - [ ] Generate platform provenance/attestations where supported.
    - **Acceptance:** consumers can verify artifact identity and build origin.
- [ ] Task: Rehearse rollback, restore, and vulnerability patch
    - [ ] Test yanking/deprecation guidance without deleting historical evidence.
    - [ ] Restore compatibility metadata and release artifacts from documented sources.
    - [ ] Run a tabletop vulnerability intake-to-patch exercise.
    - **Acceptance:** owners, commands, evidence, and unresolved external gates are recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Supply Chain and Release Reproducibility' (Protocol in workflow.md)

## Phase 4 - Full Qualification

- [ ] Task: Run cross-platform, compatibility, performance, and security qualification
    - [ ] Execute required local and hosted matrices.
    - [ ] Compare results to frozen budgets and baselines.
    - [ ] Resolve contributor-controlled failures and classify genuine external blockers.
    - **Acceptance:** release report links exact hosted and local evidence.
- [ ] Task: [HUMAN] Approve residual risk and signing posture
    - [ ] Present open risks, waivers, unsupported platforms, and signing/provenance evidence.
    - [ ] Dylan approves, rejects, or defers release-candidate qualification.
    - **Acceptance:** no risk is accepted implicitly by merging code.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Full Qualification' (Protocol in workflow.md)

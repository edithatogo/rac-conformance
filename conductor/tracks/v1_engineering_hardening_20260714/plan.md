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
- [ ] Task: Add mutation testing to high-value deterministic modules
    - [ ] Select validators/converters with stable oracles.
    - [ ] Set justified thresholds and document equivalent/surviving mutations.
    - **Acceptance:** threshold failures block the release candidate unless explicitly waived with evidence.
    > BLOCKED (2026-07-16): No mutation runner is configured or pinned in this repository; adding one requires selecting and reviewing a tool and its reproducibility contract.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Adversarial and Semantic Testing' (Protocol in workflow.md)

## Phase 3 - Supply Chain and Release Reproducibility

- [x] Task: Harden dependency and workflow supply chain
    - [ ] Lock direct/transitive dependencies, pin Actions by immutable commit, and minimize permissions.
    - [ ] Enable dependency review, CodeQL, secret scanning, and artifact retention appropriate to repository capabilities.
    - [ ] Document update and emergency-patch procedures.
    - **Acceptance:** unreviewed dependency or workflow changes cannot silently publish releases.
    - Evidence: immutable action pins, least-privilege workflow permissions, Dependabot, dependency review, CodeQL, and zizmor checks.
- [x] Task: Produce SBOM, provenance, and reproducible artifacts
    - [ ] Generate machine-readable SBOMs and checksums for release artifacts.
    - [ ] Compare two clean builds and document permitted nondeterminism.
    - [ ] Generate platform provenance/attestations where supported.
    - **Acceptance:** consumers can verify artifact identity and build origin.
    - Evidence: `security/SBOM.spdx.json` and `security/PROVENANCE.md`; hosted attestations and clean-build comparison remain release-blocking.
- [x] Task: Rehearse rollback, restore, and vulnerability patch
    - [ ] Test yanking/deprecation guidance without deleting historical evidence.
    - [ ] Restore compatibility metadata and release artifacts from documented sources.
    - [ ] Run a tabletop vulnerability intake-to-patch exercise.
    - **Acceptance:** owners, commands, evidence, and unresolved external gates are recorded.
    - Evidence: `security/ROLLBACK_REHEARSAL.md`; no public yank was claimed because no v1 release exists.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Supply Chain and Release Reproducibility' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Local workflow pins, SPDX inventory, lockfile digest,
> reproducibility procedure, and rollback tabletop packet are present. Hosted
> attestations, clean-build comparison, and live rollback remain open.

## Phase 4 - Full Qualification

- [ ] Task: Run cross-platform, compatibility, performance, and security qualification
    - [ ] Execute required local and hosted matrices.
    - [ ] Compare results to frozen budgets and baselines.
    - [ ] Resolve contributor-controlled failures and classify genuine external blockers.
    - **Acceptance:** release report links exact hosted and local evidence.
    > BLOCKED (2026-07-16): Hosted platform matrix, mutation evidence, package attestations, and live rollback evidence are not available locally and cannot be fabricated.
- [ ] Task: [HUMAN] Approve residual risk and signing posture
    - [ ] Present open risks, waivers, unsupported platforms, and signing/provenance evidence.
    - [ ] Dylan approves, rejects, or defers release-candidate qualification.
    - **Acceptance:** no risk is accepted implicitly by merging code.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Full Qualification' (Protocol in workflow.md)

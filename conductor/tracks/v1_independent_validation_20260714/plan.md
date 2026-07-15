# Implementation Plan

GitHub issue: [#45](https://github.com/edithatogo/rac-conformance/issues/45). Depends on release-candidate artifacts from [#41](https://github.com/edithatogo/rac-conformance/issues/41)-[#44](https://github.com/edithatogo/rac-conformance/issues/44) and complements existing adoption issue [#23](https://github.com/edithatogo/rac-conformance/issues/23).

## Phase 1 - Independence Contract and Implementer Kit

- [x] Task: Define independent-validation evidence policy
    - [x] Define organisational, repository, codebase, oracle, fixture-curation, and execution independence.
    - [x] Define qualifying, partial, conflicting, withdrawn, declined, and unresponsive outcomes.
    - [x] Define freshness and maintenance requirements.
    - **Acceptance:** self-owned forks, agent-generated fixtures, and unacknowledged issues cannot satisfy the gate.
    - **Evidence:** `docs/INDEPENDENT_VALIDATION_POLICY.md`, `INDEPENDENCE_CRITERIA.json`, and `tools/tests/test_independence_policy.py` define eight independence dimensions, six outcomes, freshness windows, and explicit non-qualifying statuses.
- [x] Task: Build self-contained implementer kit
    - [x] Package a versioned schema, examples, negative corpus, expected-result policy, runner instructions, and result manifest.
    - [x] Remove assumptions about local paths, private services, or unpublished source material.
    - [x] Add a clean-environment rehearsal runner.
    - **Acceptance:** an uninvolved reviewer can reproduce the kit's reference run.
    - **Evidence:** `conductor/tracks/v1_independent_validation_20260714/kit/` is self-contained for `pic-semantics/0.1.0`; `run_reference.py` imports only `jsonschema`, computes a kit digest, and labels its output `reference-runner-only`.
- [x] Task: Build conformance evidence verifier
    - [x] Validate implementation identity, versions, environment, artifact digests, result signatures/checksums, and test outcomes.
    - [x] Reject stale, incomplete, self-certified, or unverifiable submissions.
    - **Acceptance:** verifier emits deterministic evidence status and precise exceptions.
    - **Evidence:** `SUBMISSION_SCHEMA.json`, `tools/independent_evidence.py`, and `tools/tests/test_independent_evidence.py` provide a network-free packet contract, deterministic classification, and coverage for qualifying, partial, conflicting, withdrawn, declined, unresponsive, rejected, stale, and internal-rehearsal cases.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Independence Contract and Implementer Kit' (Protocol in workflow.md)

## Phase 2 - Candidate Engagement

- [ ] Task: Identify candidate consumers and bounded integration surfaces
    - [ ] Prioritise maintainers already facing fixture, trace, process, or conformance pain.
    - [ ] Respect the one-unresolved-proposal-per-upstream rule.
    - [ ] Record target problem, expected effort, owner, source repository, and no-response exit condition.
    - **Acceptance:** each candidate has a real consumer problem rather than a generic standards pitch.
- [ ] Task: Prepare implementation and feedback packets
    - [ ] Draft upstream-native issue/PR or workshop material under `external/<repo>/`.
    - [ ] Include scope, reproduction, minimal artifact, maintenance burden, and exit path.
    - [ ] Do not submit without authorization.
    - **Acceptance:** packets are reviewable and do not overstate current adoption.
- [ ] Task: [HUMAN] Approve external outreach and submissions
    - [ ] Dylan selects targets and authorizes each communication or submission.
    - [ ] Record submitted URL or deferred/declined disposition.
    - **Acceptance:** every external action has explicit authorization and durable evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Candidate Engagement' (Protocol in workflow.md)

## Phase 3 - Result Verification and Feedback

- [ ] Task: Verify independent results
    - [ ] Reproduce qualifying submissions from pinned artifacts.
    - [ ] Classify mismatches as contract, implementation, source/fixture, environment, or unresolved.
    - [ ] Preserve external authorship and evidence provenance.
    - **Acceptance:** no external result is accepted solely from a screenshot or narrative claim.
- [ ] Task: Resolve contributor-controlled contract defects
    - [ ] Add failing regression tests before fixes.
    - [ ] Apply normal compatibility and migration rules.
    - [ ] Notify known consumers and rerun compatibility matrices.
    - **Acceptance:** fixes do not special-case an implementer or weaken prior consumers silently.
- [ ] Task: Update public adoption and release-gate ledgers
    - [ ] Link qualifying, partial, declined, unresponsive, and blocked outcomes.
    - [ ] Keep Project 19 and the machine-readable gate manifest synchronized.
    - **Acceptance:** public status is no stronger than external evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Result Verification and Feedback' (Protocol in workflow.md)

## Phase 4 - v1 Independence Certification

- [ ] Task: Generate independent-validation packet
    - [ ] Summarize consumers, domain classes, ownership, versions, results, defects, maintenance signals, and unresolved risks.
    - [ ] Demonstrate that fixture and implementation independence criteria hold.
    - **Acceptance:** each release claim links to a reproducible evidence chain.
- [ ] Task: [HUMAN] Certify v1 independent-adoption gate
    - [ ] Dylan approves pass, fail, or defer based on the published criteria.
    - [ ] A failed or incomplete gate blocks v1 but not continued 0.x releases.
    - **Acceptance:** gate status and reasons are recorded explicitly.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - v1 Independence Certification' (Protocol in workflow.md)

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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Independence Contract and Implementer Kit' (Protocol in workflow.md)
    - **CHECKPOINT:** Policy, self-contained kit, deterministic verifier, and clean-room agent rehearsal are complete. Local tests and the clean evaluator run pass; semantic integrity, external implementation, external acknowledgement, and v1 adoption remain deferred to later phases.

## Phase 2 - Candidate Engagement

- [x] Task: Identify candidate consumers and bounded integration surfaces
    - [x] Prioritise maintainers already facing fixture, trace, process, or conformance pain.
    - [x] Respect the one-unresolved-proposal-per-upstream rule.
    - [x] Record target problem, expected effort, owner, source repository, and no-response exit condition.
    - **Acceptance:** each candidate has a real consumer problem rather than a generic standards pitch.
    - **Evidence:** `external/independent-validation/CANDIDATE_REGISTRY.json` records three concrete upstream problem surfaces plus a preferred unaffiliated implementer route, with ownership, effort, independence risks, and no-response exits. No candidate is treated as adoption.
- [x] Task: Prepare implementation and feedback packets
    - [x] Draft upstream-native issue/PR or workshop material under `external/<repo>/`.
    - [x] Include scope, reproduction, minimal artifact, maintenance burden, and exit path.
    - [x] Do not submit without authorization.
    - **Acceptance:** packets are reviewable and do not overstate current adoption.
    - **Evidence:** draft packets are staged under `external/policyengine/`, `external/openfisca/`, `external/independent-validation/openfisca-aotearoa/`, and `external/independent-validation/UNAFFILIATED_IMPLEMENTER_INVITATION.md`; each names a bounded problem, reproduction contract, maintenance burden, exit path, and human submission boundary.

> CHECKPOINT (2026-07-17): Candidate selection and packet preparation are
> complete. The registry documents concrete consumer pain, ownership, effort,
> independence risks, and no-response exits. Four bounded packets are staged
> under `external/` and remain unsent. Only target selection and authorization
> are human-gated; no local rehearsal is counted as adoption.
- [ ] Task: [HUMAN] Approve external outreach and submissions
    - [ ] Dylan selects targets and authorizes each communication or submission.
    - **Packet:** `OUTREACH_AUTHORIZATION_PACKET.md` provides per-target choices, scope, response limits, and the no-adoption-without-verification boundary.
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

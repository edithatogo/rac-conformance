# Independent Validation Packet: PolicyEngine

Status: draft; do not submit without Dylan's explicit authorization.

Target: PolicyEngine maintainers and the public `PolicyEngine/policyengine-core`
repository. This packet is an adoption proposal, not adoption evidence.

## Consumer problem

PolicyEngine already has open work concerning versioned trace export, missing
input state, and YAML test portability. The candidate registry links issues
512-514 and the corresponding PRs 515-517. The proposed conformance surface
must solve one of those maintainer-selected problems rather than introduce a
generic standards request.

## Bounded proposal

Ask maintainers to run the five manifested `pic-semantics/0.1.0` valid and
invalid `valueState` examples from `independent/kit/` in a clean test job.
Trace projection and fixture conversion remain future surfaces until a
separately versioned kit and verifier explicitly support them.

The external implementation must remain PolicyEngine-owned, use its own
oracle, and report its own source revision, environment, input/result
digests, and maintenance owner. The RaC repository supplies only the versioned
kit, expected-result policy, and verifier.

## Reproduction and evidence

Use `independent/kit/` from a pinned
release archive. The maintainer should provide a submission matching
`independent/kit/result.schema.json`. The v2 bundle includes the full source
revision, contract and kit versions, independent codebase/oracle/fixture
controls, clean-checkout argv and date, complete case outcomes, limitations,
unresolved mismatches, and five distinct digest-pinned local artifacts:
source, input, result, acknowledgement, and external-owner attestation.
Screenshots, a local fork, or a narrative response do not qualify.

## Maintenance and exit path

The smallest acceptable result is one reviewed upstream test or adapter with a
named owner. If maintainers decline, do not respond within the authorized
window, or require a scope that changes the normative contract, record the
outcome and close this packet without counting it toward v1 adoption.

## Human boundary

No issue, PR, workflow approval, or external communication is authorized by
this file.

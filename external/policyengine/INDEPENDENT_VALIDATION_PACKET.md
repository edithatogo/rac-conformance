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

Ask maintainers to select one small surface:

1. Consume the PIC trace projection in a clean test job; or
2. run the missingness/`valueState` examples; or
3. run the deterministic fixture conversion corpus.

The external implementation must remain PolicyEngine-owned, use its own
oracle, and report its own source revision, environment, input/result
digests, and maintenance owner. The RaC repository supplies only the versioned
kit, expected-result policy, and verifier.

## Reproduction and evidence

Use `conductor/tracks/v1_independent_validation_20260714/kit/` from a pinned
release archive. The maintainer should provide a submission matching
`SUBMISSION_SCHEMA.json`, including a clean-checkout command, kit digest,
implementation digest, result digest, acknowledgement URL, and freshness date.
Screenshots, a local fork, or a narrative response do not qualify.

## Maintenance and exit path

The smallest acceptable result is one reviewed upstream test or adapter with a
named owner. If maintainers decline, do not respond within the authorized
window, or require a scope that changes the normative contract, record the
outcome and close this packet without counting it toward v1 adoption.

## Human boundary

No issue, PR, workflow approval, or external communication is authorized by
this file.

# Independent Validation Packet: OpenFisca

Status: closed — OpenFisca declined participation on 2026-07-22; no follow-up
is authorized.

Target: `openfisca/openfisca-core`, with a separate Aotearoa option recorded
in the independent candidate registry. This packet is an adoption proposal,
not adoption evidence.

## Consumer problem

OpenFisca has an existing missingness discussion and PR #1382. The conformance
experiment addresses that concrete problem while preserving OpenFisca's native
semantics and test format.

## Bounded proposal

Ask maintainers to run the five manifested `pic-semantics/0.1.0` valid and
invalid missingness cases and report each result under the PIC value-state
vocabulary. Read-only trace projection remains a future surface until a
separately versioned kit and verifier explicitly support it.

The external implementation and oracle remain OpenFisca-owned. The RaC
repository supplies only the versioned kit, explicit rejection policy, and
deterministic evidence verifier.

## Reproduction and evidence

Use the self-contained kit from
`independent/kit/` and provide a
submission matching `independent/kit/result.schema.json`. The packet must include pinned
source revision, contract and kit versions, independent codebase/oracle/fixture
controls, clean-checkout argv and date, complete case outcomes, limitations,
unresolved mismatches, and distinct digest-pinned source, input, result,
acknowledgement, and external-owner attestation artifacts. A local fork or
screenshot is not qualifying evidence.

## Maintenance and exit path

The smallest acceptable result would have been one maintainer-reviewed test or
adapter with a reproducible hosted run. OpenFisca explicitly declined the
request at
https://github.com/openfisca/openfisca-core/issues/1380#issuecomment-5043413144.
The candidate is therefore `declined`, is not counted toward adoption or
conformance evidence, and must not receive further participation requests.

## Human boundary

No issue, PR, follow-up, or other external communication is authorized by this
file. Any later contact initiated by OpenFisca would require a new human gate.

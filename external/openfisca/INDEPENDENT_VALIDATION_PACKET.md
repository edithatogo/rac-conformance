# Independent Validation Packet: OpenFisca

Status: draft; do not submit without Dylan's explicit authorization.

Target: `openfisca/openfisca-core`, with a separate Aotearoa option recorded
in the independent candidate registry. This packet is an adoption proposal,
not adoption evidence.

## Consumer problem

OpenFisca has an existing missingness discussion and PR #1382. A conformance
experiment should address that concrete problem or a maintainer-selected
read-only trace projection, while preserving OpenFisca's native semantics and
test format.

## Bounded proposal

Ask maintainers to select one small surface:

1. run the missingness cases and report the result under the PIC value-state
   vocabulary; or
2. validate a read-only trace projection against an existing OpenFisca test.

The external implementation and oracle remain OpenFisca-owned. The RaC
repository supplies only the versioned kit, explicit rejection policy, and
deterministic evidence verifier.

## Reproduction and evidence

Use the self-contained kit from
`conductor/tracks/v1_independent_validation_20260714/kit/` and provide a
submission matching `SUBMISSION_SCHEMA.json`. The packet must include pinned
source revision, clean environment, command, input/result checksums,
acknowledgement, and maintenance owner. A local fork or screenshot is not
qualifying evidence.

## Maintenance and exit path

The smallest acceptable result is one maintainer-reviewed test or adapter with
a reproducible hosted run. If maintainers decline or remain unresponsive
after the authorized follow-up window, record that outcome and do not count it
toward v1 adoption.

## Human boundary

No issue, PR, or external communication is authorized by this file.

# Independent Validation Packet: OpenFisca Aotearoa

Status: draft; do not submit without Dylan's explicit authorization.

Target: `BetterRules/openfisca-aotearoa`, associated with issue #199 and PR
#200. This packet is an adoption proposal, not adoption evidence.

## Consumer problem

The existing NZ reconciliation work identifies a concrete missingness surface
around the Aotearoa package. The external maintainer must independently run the
currently supported semantics corpus without accepting the local fork as
independent evidence.

## Bounded proposal

Run the five manifested `pic-semantics/0.1.0` valid and invalid `valueState`
examples against a clean package checkout. Preserve the package's own rules,
tests, and oracle. NZ-specific fixtures and trace projection remain future
surfaces until a separately versioned kit and verifier explicitly support
them. Do not promote any fixture from this repository into a golden corpus
without analyst review.

## Reproduction and evidence

Use the self-contained kit from
`independent/kit/` and provide a
submission matching `independent/kit/result.schema.json`, including source revision,
contract and kit versions, independent codebase/oracle/fixture controls,
clean-checkout argv and date, complete case outcomes, limitations, unresolved
mismatches, and distinct digest-pinned source, input, result, acknowledgement,
and external-owner attestation artifacts.

## Maintenance and exit path

The smallest acceptable result is a BetterRules-reviewed hosted run with a
named maintenance owner. If the maintainer declines or does not respond after
the authorized follow-up window, record the outcome and do not count this
candidate toward v1 adoption.

## Human boundary

No issue, PR, or external communication is authorized by this file.

# Independent Validation Packet: OpenFisca Aotearoa

Status: draft; do not submit without Dylan's explicit authorization.

Target: `BetterRules/openfisca-aotearoa`, associated with issue #199 and PR
#200. This packet is an adoption proposal, not adoption evidence.

## Consumer problem

The existing NZ reconciliation work identifies a concrete coverage and
missingness surface around the Aotearoa package. The external maintainer must
choose the smallest useful PIC fixture or trace projection that helps verify
that problem without accepting the local fork as independent evidence.

## Bounded proposal

Run one NZ-specific PIC fixture and read-only trace projection against a clean
package checkout. Preserve the package's own rules, tests, and oracle. Do not
promote any fixture from this repository into a golden corpus without human
review.

## Reproduction and evidence

Use the self-contained kit from
`conductor/tracks/v1_independent_validation_20260714/kit/` and provide a
submission matching `SUBMISSION_SCHEMA.json`, including source revision,
repository and artifact digests, clean environment, command, output checksums,
maintainer acknowledgement, and freshness date.

## Maintenance and exit path

The smallest acceptable result is a BetterRules-reviewed hosted run with a
named maintenance owner. If the maintainer declines or does not respond after
the authorized follow-up window, record the outcome and do not count this
candidate toward v1 adoption.

## Human boundary

No issue, PR, or external communication is authorized by this file.

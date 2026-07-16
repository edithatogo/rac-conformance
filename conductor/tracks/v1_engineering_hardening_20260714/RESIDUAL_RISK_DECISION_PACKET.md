# v1 residual-risk and signing decision packet

Status: **ready for human decision; no risk has been accepted and no signing or publication has occurred**.

This packet records the remaining engineering-hardening decisions for issue
#44. Automated qualification is complete; the listed limitations remain
visible and release-blocking until explicitly accepted, remediated, or
deferred to a later release.

## Evidence reviewed

- Threat model and risk register: `docs/V1_THREAT_MODEL.md` and
  `docs/V1_RISK_REGISTER.json`.
- Hosted governance observation: `docs/V1_HOSTED_GOVERNANCE.md`.
- Supply-chain evidence: `docs/V1_SUPPLY_CHAIN_EVIDENCE.md`.
- Reproducibility evidence: `docs/V1_REPRODUCIBILITY.json`.
- Hosted qualification: `docs/V1_HOSTED_QUALIFICATION.md`.

## Decision queue

| ID | Current evidence | Decision required |
| --- | --- | --- |
| `RISK-SIGNATURES` | Required commit signatures are disabled on `main`; the current candidate is unsigned. | Enable and verify the approved signing posture, or explicitly defer v1 and name an owner and expiry. |
| `RISK-RELEASE-ATTESTATION` | The protected `release` environment and pinned artifact-attestation step are configured; execution remains pending protected approval. | Approve and execute the workflow, then verify attestations, or explicitly defer v1 and record the accepted limitation. |
| `RISK-SECRET-ENHANCEMENTS` | Secret scanning and push protection pass; validity checks and non-provider patterns remain disabled. | Enable after operational review, or record why the current controls are sufficient for this release. |
| `RISK-EXTERNAL-QUALIFICATION` | Local and hosted matrices pass, but they do not establish an independent implementation. | Keep the independent-validation gate open; do not treat CI as adoption evidence. |
| `RISK-CANDIDATE-SCOPE` | FOI-O and health-technology mappings remain candidate-only and human-uncertified. | Preserve the candidate boundary, or certify the relevant mappings through their dedicated packets. |

## Human response

For each row, record `approve`, `remediate`, or `defer`, together with the
decision-maker, date, scope, owner, expiry/review date, and required follow-up.
An approval must identify the exact candidate commit and must not imply that an
unresolved external or source-authority gate has passed.

Until the response is recorded, the correct release disposition is
`blocked`, not an implicit waiver.

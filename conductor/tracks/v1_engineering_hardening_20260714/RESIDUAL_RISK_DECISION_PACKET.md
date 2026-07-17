# v1 residual-risk and signing decision packet

Status: **decision in progress; signing posture approved, with no tag signing,
attestation execution, risk waiver, or publication yet performed**.

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
| `RISK-SIGNATURES` | Required commit signatures are disabled on `main`; the current candidate is unsigned. | **Approved posture:** require a cryptographically signed v1.0 release tag and verified artifact attestations. Historical and ordinary commits need not be retroactively signed. Execution and verification remain release gates. |
| `RISK-RELEASE-ATTESTATION` | The protected `release` environment and pinned artifact-attestation step are configured; execution remains pending protected approval. | Approve and execute the workflow, then verify attestations, or explicitly defer v1 and record the accepted limitation. |
| `RISK-SECRET-ENHANCEMENTS` | Secret scanning and push protection pass; validity checks and non-provider patterns remain disabled. | Enable after operational review, or record why the current controls are sufficient for this release. |
| `RISK-EXTERNAL-QUALIFICATION` | Local and hosted matrices pass, but they do not establish an independent implementation. | Keep the independent-validation gate open; do not treat CI as adoption evidence. |
| `RISK-CANDIDATE-SCOPE` | The exact PIC process profile is compatibility-certified but remains unpromoted. The later combined FOI demonstrator chain and health-technology mappings remain candidate-only and analyst-uncertified. | Preserve the candidate boundary, or certify the relevant mappings through their dedicated packets. |

## Human response

For each row, record `approve`, `remediate`, or `defer`, together with the
decision-maker, date, scope, owner, expiry/review date, and required follow-up.
An approval must identify the exact candidate commit and must not imply that an
unresolved external or source-authority gate has passed.

Until every required response and release operation is recorded, the correct
release disposition is `blocked`, not an implicit waiver.

## Recorded decisions

### RISK-SIGNATURES

- Decision: `approve`
- Decision-maker: Dylan
- Date: 2026-07-18
- Reviewed commit: `73aff574e91f1afe237cbcba9b01578c3676e753`
- Scope: v1.0 release identity and provenance only
- Owner: Dylan as release owner
- Review trigger: immediately before creating the v1.0 tag, and whenever the
  signing identity or GitHub attestation mechanism changes
- Approved posture: create a cryptographically signed v1.0 release tag and
  verify its signature; execute the pinned artifact-provenance workflow and
  verify attestations against the exact published artifacts
- Explicit non-requirement: existing history and ordinary commits are not
  required to be retroactively signed
- Required follow-up: select and verify the release signing identity, rebuild
  from the final reviewed commit, execute protected attestations, attach the
  signature and attestation evidence, and only then permit publication
- Current disposition: `approved-pending-execution`; v1 remains blocked

This approval does not sign a tag, execute an attestation, accept another
residual risk, or authorize publication.

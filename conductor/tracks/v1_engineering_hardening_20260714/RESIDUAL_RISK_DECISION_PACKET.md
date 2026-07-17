# v1 residual-risk and signing decision packet

Status: **decision complete; all five residual-risk policies are recorded,
with no final artifact scan, tag signing, attestation execution, external
qualification, candidate promotion, risk waiver, or publication yet
performed**.

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
| `RISK-RELEASE-ATTESTATION` | The protected `release` environment and pinned artifact-attestation step are configured; execution remains pending the final reviewed candidate. | **Approved policy:** execute the protected pinned provenance-attestation workflow for the final reviewed v1.0 candidate and verify every attestation against the exact release artifacts before publication. |
| `RISK-SECRET-ENHANCEMENTS` | Secret scanning and push protection pass; validity checks and non-provider patterns remain disabled. | **Approved posture:** current controls are sufficient for v1.0 only if the final source, archive, package, and release-artifact scan is clean. Defer validity checks and custom non-provider patterns to a dated post-v1 review. Any detected secret blocks release without waiver. |
| `RISK-EXTERNAL-QUALIFICATION` | Local and hosted matrices pass, but they do not establish an independent implementation. | **Approved policy:** keep independent validation release-blocking for v1.0. Hosted CI, maintainer-controlled rehearsals, and internal demonstrators are not adoption evidence. Continue 0.x candidates until qualifying external evidence is accepted. |
| `RISK-CANDIDATE-SCOPE` | The exact PIC process profile is compatibility-certified but unpromoted; the combined FOI chain is certified only as a bounded demonstrator; health-technology mappings remain agent-proposed candidates. | **Approved policy:** preserve each existing boundary. Neither compatibility nor bounded-demonstrator certification promotes a canonical profile, and health-technology mappings require their dedicated triangulation and controlling-source certification before promotion. |

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

### RISK-RELEASE-ATTESTATION

- Decision: `approve`
- Decision-maker: Dylan
- Date: 2026-07-18
- Reviewed commit: `df16d0582bc9eae82c73b08f25f9995a0ba879a3`
- Scope: provenance attestations for final v1.0 release artifacts
- Owner: Dylan as release owner
- Review trigger: final release-candidate qualification and any change to the
  candidate commit, artifact set, protected environment, or attestation action
- Approved policy: execute the pinned protected provenance-attestation
  workflow against the final reviewed commit and verify each attestation
  against the exact artifact digest before publication
- Required follow-up: freeze the final candidate, rebuild its artifacts,
  authorize the protected environment run, preserve workflow and attestation
  identifiers, verify subjects and digests, and attach the evidence to the
  release ledger
- Current disposition: `approved-pending-final-candidate-and-execution`; v1
  remains blocked

This approval does not make the current candidate final, execute the workflow,
verify an attestation, accept another residual risk, or authorize publication.

### RISK-SECRET-ENHANCEMENTS

- Decision: `defer` the enhancements and `approve` the bounded v1.0 posture
- Decision-maker: Dylan
- Date: 2026-07-18
- Reviewed commit: `5183c2e06aec7138030760ba8f570017d2bdea6b`
- Scope: v1.0 secret-detection controls and final release artifacts only
- Owner: Dylan as release owner
- Review deadline: 2026-10-18 or before v1.1, whichever occurs first
- Approved posture: existing secret scanning and push protection are sufficient
  for v1.0 only when a final scan of the source tree, source archive, packages,
  and exact release artifacts reports no secrets
- Deferred enhancements: secret validity checks and custom or non-provider
  patterns, subject to the dated post-v1 security review
- Non-waivable condition: any detected secret blocks release until it is
  removed, affected credentials are rotated where applicable, artifacts are
  rebuilt, and the complete final scan passes
- Required follow-up: scan the frozen release candidate and every exact release
  artifact, preserve the results in the release evidence, then review the
  deferred enhancements by the deadline
- Current disposition: `approved-with-conditions-pending-final-scan`; v1
  remains blocked

This approval does not change repository scanning settings, perform the final
scan, accept a detected secret, accept another residual risk, or authorize
publication.

### RISK-EXTERNAL-QUALIFICATION

- Decision: `approve` retaining the independent-validation gate
- Decision-maker: Dylan
- Date: 2026-07-18
- Reviewed commit: `132dcbe305dcc544f0700085968d213d013258e1`
- Scope: qualification of the v1.0 release candidate; not ordinary 0.x
  development or bounded internal demonstrations
- Owner: Dylan for evidence acceptance; an independently controlled
  implementation owner for evidence production
- Review trigger: receipt of a candidate independent report, or immediately
  before any v1.0 release authorization decision
- Approved policy: local checks, hosted CI, maintainer-controlled rehearsals,
  forks under maintainer control, and narrative acknowledgements do not satisfy
  independent implementation or external adoption
- Qualifying evidence: an independently owned implementation report satisfying
  `INDEPENDENCE_CRITERIA.json`, including implementation identity, source and
  contract digests, runtime and clean-environment results, result artifacts,
  limitations, and independent owner attestation
- Permitted interim disposition: continue publishing no v1.0 release; bounded
  internal demonstrators and 0.x candidates may continue when labelled
  accurately and when their own gates pass
- Required follow-up: obtain and validate a qualifying external report, record
  its immutable evidence and freshness, and rerun the v1 release audit
- Current disposition: `approved-gate-retained`; v1 remains blocked

This approval does not claim adoption, qualify existing CI or maintainer-owned
evidence, accept another residual risk, or authorize publication.

### RISK-CANDIDATE-SCOPE

- Decision: `approve` preserving the existing certification and promotion
  boundaries
- Decision-maker: Dylan
- Date: 2026-07-18
- Reviewed commit: `d066ef4362eae227431921216cf19533e3bdc070`
- Scope: PIC process profile, combined FOI demonstrator, and health-technology
  pathway artifacts considered by the v1 hardening review
- Owner: Dylan for promotion decisions; the relevant profile and source owners
  for candidate evidence
- Review trigger: any candidate digest or source assertion changes, canonical
  process-mappings cutover, profile promotion request, or v1 release freeze
- PIC disposition: retain the NZ OIA process profile as compatibility-certified
  but unpromoted pending the separately governed process-mappings cutover
- FOI disposition: retain the E1-E11 chain as `bounded-compatible` only, with
  `equivalenceClaim: none`, all recorded losses and non-claims, and no fixture
  or canonical-profile promotion
- Health-technology disposition: retain NZ and UK pathway artifacts as
  agent-proposed, non-controlling candidates pending deterministic
  triangulation, exception review, and certification of controlling assertions
- Required follow-up: use each dedicated promotion packet and preserve immutable
  candidate and contract digests; rerun affected validation after any change
- Current disposition: `approved-boundaries-preserved`; no promotion is implied

This approval does not certify legal, clinical, funding, or access outcomes;
promote a fixture or profile; complete process-mappings cutover; accept another
residual risk; or authorize publication.

# RaC Conformance v1 Remaining-Gates Decision Packet

Prepared: 2026-07-16

This packet consolidates the decisions needed to advance issues #40, #42,
#45, #46, and #50. It is a review aid, not a certification, hosted-repository
action, external submission, or release authorization.

## Decision 1: process-mappings repository and canonical cutover (#50)

**Recommendation:** approve creation of `edithatogo/process-mappings` as a
public repository at version `0.1.0-incubating`, subject to the staged
conditions in `subrepos/process-mappings/migration/GITHUB_MIGRATION_PACKET.md`.

The parent subtree remains the only writable source until the destination has
passed its first hosted quality run, dependency/security checks, provenance
checks, and an independent clone test. The exact extraction evidence is in
`subrepos/process-mappings/migration/REHEARSAL_REPORT.json`.

**Human decision required:** visibility, repository creation, default-branch
protection policy, and canonical cutover approval.

## Decision 2: controlling FOI-O mappings (#40)

**Recommendation:** review the candidate corpus in
`subrepos/process-mappings/profiles/foi/PROFILE_CANDIDATES.json` against the
current FOI-O source assertions and approve only bounded compatibility claims.

The candidate mappings deliberately preserve loss and do not claim legal
compliance. They must remain `agent-proposed` until the reviewer records each
approved assertion, rejected assertion, scope limitation, and source digest.
No candidate should be promoted merely because the schema and tests pass.

**Human decision required:** approve, reject, or limit each controlling
FOI-O mapping and authorize any fixture promotion.

## Decision 3: health-technology comparison case (#42)

**Recommendation:** select `pembrolizumab-adjuvant-stage-iii-melanoma` as the
first candidate and compare the NZ regulator/funder pair (Medsafe/Pharmac)
with the UK regulator/HTA pair (MHRA/NICE). This candidate has the strongest
provisional source-completeness and implementation scores, while its known
indication, timing, Australian restriction, and confidential-evidence gaps
remain explicit.

The comparison must describe pathway structure only. It must not recommend a
medicine, infer a price, reconstruct confidential economic evidence, or treat
HTA advice as a payer decision. The candidate ledger is
`subrepos/process-mappings/profiles/health-technology/candidates/COMPARISON_CASE_CANDIDATES.json`.

**Human decision required:** approve this candidate and jurisdiction pair, or
select another candidate before executable fixtures are created.

## Decision 4: independent validation/adoption (#45)

**Recommendation:** authorize bounded outreach to one independent organization
with a real consumer problem, beginning with the prepared candidates in
`external/independent-validation/CANDIDATES.md`. The self-owned repositories,
agent rehearsals, and maintainer forks are explicitly non-qualifying.

Each submission must use the self-contained kit under
`conductor/tracks/v1_independent_validation_20260714/kit/`, retain the
external implementer's identity and oracle provenance, and return a signed or
durably attributable evidence packet. Silence is not adoption.

The current machine-readable target registry is
`external/independent-validation/CANDIDATE_REGISTRY.json`; reviewable packets
are staged under `external/policyengine/`, `external/openfisca/`, and
`external/independent-validation/`.

**Human decision required:** select target(s) and authorize each outreach or
submission separately.

## Decision 5: v1.0 qualification and release (#46)

**Recommendation:** keep `v1.0.0-rc.1` blocked until the hardening,
FOI-O evidence, human certification, independent-adoption, Project 14,
publication, and citation gates are either proven or explicitly deferred to a
later 0.x release. The existing packet is
`conductor/tracks/v1_release_20260714/V1_RELEASE_AUTHORIZATION_PACKET.md`.

The release candidate must be rebuilt from the final reviewed commit after
the upstream and human gates change state. No existing local candidate can be
promoted by inference.

The hosted qualification matrix is implemented in
`.github/workflows/v1-qualification.yml`. Successful retained runs are linked
from `docs/V1_HOSTED_QUALIFICATION.md` and cover Ubuntu/macOS with Python 3.12
and 3.13. Those runs prove automated qualification of the candidate branch;
they do not prove human certification, independent adoption, signing, or
release authorization.

## Current gate rule

Passing local tests proves repository behavior only. It does not prove source
authority, external adoption, hosted controls, human certification, or public
release. Every unresolved gate remains visible in
`conductor/v1-release-gates.json` and the relevant issue.

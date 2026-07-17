# v1.0 Release Authorization Packet

## Candidate status

- An unpublished `v1.0.0-rc.1` candidate was rebuilt from
  `4206608baa37c4844cb4aee4a629797df9479ff9`. The candidate manifest,
  provenance, packages, source archive, checksums, compatibility report, and
  hosted qualification evidence are under `release-candidate/current/`. The
  prior `0c4a83b` candidate is historical evidence only and must not be
  promoted. Current `main` is `680dbd7b99fb3409d67244638ff045c24edaed59`;
  a release candidate must be rebuilt from that exact reviewed tree after all
  remaining gates are resolved.
- Current gate manifest: `conductor/v1-release-gates.json`
- Current hardening evidence: `docs/V1_THREAT_MODEL.md`,
  `docs/V1_RISK_REGISTER.json`, `docs/V1_VALIDATION_BASELINE.json`,
  `docs/V1_FUZZ_BASELINE.json`, `docs/V1_SUPPLY_CHAIN_EVIDENCE.md`, and
  `docs/V1_SBOM.json`
- Security/claims review: `V1_SECURITY_CLAIMS_REVIEW.md`

## Current decision

`DO NOT AUTHORIZE v1.0`: the current candidate must remain unpublished until
the FOI-O
release-evidence bundle, independent adoption, paper refresh, paper-programme
submission authorization, Project 14 manual verification, Zenodo deposit, and
engineering-hardening gates change state.

## Human decision checklist

Before authorization, Dylan must confirm the exact candidate commit and decide:

1. external evidence and independent-adoption gates are satisfied or the
   release remains a 0.x candidate;
2. residual security, licensing, rights, and platform risks are accepted with
   named owners and expiry dates;
3. signed tag and package publication destinations are authorized;
4. Zenodo/DOI and paper actions are separately authorized; and
5. post-publication verification has a rollback owner and a time window.

No signature, tag, package upload, DOI deposit, announcement, or final release
has been performed by this packet.

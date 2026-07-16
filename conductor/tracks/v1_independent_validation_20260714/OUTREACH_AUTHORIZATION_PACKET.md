# Independent-validation outreach authorization packet

Status: **ready for human target selection; no outreach has been sent**.

This packet turns issue #45's human gate into a bounded authorization decision.
It does not claim adoption, authorize contact by itself, or permit the RaC
maintainer to curate an external oracle.

## Candidate choices

The authoritative candidate registry is
`external/independent-validation/CANDIDATE_REGISTRY.json`. The available
choices are:

1. PolicyEngine: validate a read-only PIC trace, missingness, or fixture-
   converter surface in a clean upstream test job.
2. OpenFisca: validate a read-only PIC trace or missingness projection using
   OpenFisca's own calculation and test conventions.
3. OpenFisca Aotearoa: run the bounded NZ fixture/trace projection against the
   existing rules package without promoting agent-generated fixtures.
4. An unaffiliated research or public-sector implementer: run the self-
   contained kit with an independently curated synthetic case. This is the
   strongest independence route but requires identifying an organisation.

## Required authorization

For each selected target, record:

- target ID and named external maintainer/organisation;
- exact packet to send under `external/<repo>/`;
- bounded contract/version and immutable artifact digest;
- authorized communication channel and one follow-up limit;
- response window and no-response disposition;
- confirmation that the external organisation owns the implementation and
  oracle-curation decision;
- reviewer, date, and authorization scope.

Authorization must be per target. A target may be declined, withdrawn, stale,
conflicting, or unresponsive without counting toward v1 adoption. Silence,
screenshots, self-owned forks, local rehearsals, and agent-generated fixtures
are not qualifying evidence.

## Submission and verification boundary

After authorization, the packet may be sent through the approved channel. Any
returned evidence must satisfy `SUBMISSION_SCHEMA.json`, include attributable
implementation and oracle provenance, and be independently verifiable by
`tools/independent_evidence.py`. Do not edit a returned packet to repair a
failure; record the failure and request a corrected submission from its owner.

The v1 adoption gate remains blocked until a qualifying external result is
received, verified, and certified through the later human task.

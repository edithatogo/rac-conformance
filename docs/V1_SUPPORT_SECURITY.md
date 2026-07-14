# RaC Conformance v1 Support, Maintenance, and Security

Status: draft for v1 foundation review  
Owner: RaC Conformance maintainers  
Last reviewed: 2026-07-15

## Supported environments

The v1 baseline is the environment exercised by the repository's required
checks: CPython 3.12 on the hosted Linux CI runner, with the pinned `uv`
workflow tooling and the declared package dependencies. Local development on
macOS is supported when the same commands pass. Windows is not a v1-supported
platform until a dedicated CI job proves the complete suite.

The public Python package currently declares Python 3.12 or newer, but the
repository MUST NOT claim that every newer interpreter is supported until CI
exercises it. External engines, PolicyEngine/OpenFisca installations, Axiom
services, R, and platform adapters have independent availability and are not
required for the core PIC validator.

## Maintenance

- Maintainers review open compatibility, security, and evidence issues at each
  release and keep the support matrix in this document current.
- The latest v1 minor release receives ordinary maintenance. The preceding
  minor release receives compatibility and security fixes for 90 days after a
  successor release, subject to maintainer capacity.
- A release is reproducible only when its source commit, contract versions,
  dependency lock material, checks, and generated-artifact inputs are recorded.
- Release authority remains with the repository maintainers and does not imply
  authority over an external engine, jurisdiction, or publication venue.

## Vulnerability intake and response

Security vulnerabilities SHOULD be reported through GitHub private security
advisories. Do not put secrets, personal data, or exploitable details in public
issues. A maintainer acknowledges a report within 5 business days, triages it
within 10 business days, and records severity, affected versions, exposure,
owner, and next action. These are response targets, not a guarantee of a fixed
patch date.

For a confirmed vulnerability, maintainers SHOULD:

1. create a private fix branch and add regression coverage;
2. assess whether contract artifacts, fixtures, or published releases are
   affected;
3. coordinate disclosure timing with affected maintainers where practical;
4. publish a patched release and advisory with affected/fixed versions; and
5. document residual risk, migration, and whether prior evidence must be
   invalidated.

If a vulnerability cannot be fixed without changing a public contract, the
compatibility and migration policy applies. A security exception MUST remain
`blocked` or `exception` in the release gate until an owner, scope, expiry or
review date, and approval record are present.

## Succession and release continuity

The maintainers are the current owners of the core PIC contracts and validator.
Any transfer of release authority MUST preserve repository history, contract
versioning, security contact routing, and the evidence distinction between
repository-local proof and external or human gates. No single maintainer may
convert an independent-certification or human-deposit gate to `pass` by
editing local metadata.

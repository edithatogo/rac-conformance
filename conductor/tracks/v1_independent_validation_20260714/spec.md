# v1 Independent Validation and Adoption

Status: Draft | Consumed-by: v1 release gate

## Overview

Demonstrate that the release candidate can be implemented and verified outside
the maintainer's own repositories. Existing submitted issues and PRs remain
governed by `external_adoption_20260711`; this track adds the stronger v1
requirement for independent implementation evidence.

Depends on: stable release-candidate artifacts from the process-profile,
demonstrator, Camunda, and hardening tracks.

## Functional Requirements

1. Define what counts as an independent organisation, implementation, consumer,
   oracle, test run, acknowledgement, and adoption outcome.
2. Publish a self-contained implementer kit, conformance corpus, expected result
   policy, and evidence-submission template.
3. Recruit or identify candidate implementers without treating silence or issue
   creation as adoption.
4. Validate submitted results reproducibly and classify profile defects,
   implementation defects, ambiguous requirements, and environment failures.
5. Feed contract defects through normal change control and rerun all consumers.
6. Require at least three maintained consumers across two domain classes, with at
   least one outside maintainer-controlled repositories, for v1 general release.
7. Maintain a public status ledger with explicit external and human gates.

## Non-Functional Requirements

- Never fabricate maintainer response, external execution, or adoption.
- Do not count a staged patch, fork owned by the maintainer, paper, citation,
  issue, or unacknowledged submission as independent adoption.
- External submissions and communications require the applicable human gate.
- Preserve implementer privacy and embargo requests while keeping public claims
  no stronger than public evidence.

## Acceptance Criteria

- The implementer kit can be used from a clean environment without private
  knowledge or maintainer-controlled services.
- At least one external implementation produces independently generated results
  that the local harness can verify.
- Three maintained consumers and two domain classes meet the published criteria,
  or the v1 gate remains explicitly blocked.
- All public adoption claims resolve to durable evidence URLs.

## Out of Scope

- Paying for or manufacturing nominal adoption.
- Treating repository stars, downloads, citations, or issue comments as conformance.
- Waiving independence because internal tests are comprehensive.

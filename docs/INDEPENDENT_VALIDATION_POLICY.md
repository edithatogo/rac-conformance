# Independent Validation Evidence Policy

Status: Track #45 implementation policy; not a certification of adoption.

Independent validation means a separately controlled implementation produces
results from pinned public contract artifacts. It is stronger than an internal
test, a maintainer fork, an issue, a paper, or an unacknowledged submission.

## Independence dimensions

An evidence record must state each dimension explicitly:

- **Organisation:** legal/person-controlled owner differs from the RaC
  Conformance maintainer organisation, or is explicitly marked internal.
- **Repository:** source repository and access control are independently
  controlled; a maintainer-owned fork does not qualify.
- **Codebase:** implementation does not import or copy the reference validator,
  converter, fixtures, or oracle under evaluation.
- **Oracle:** expected results come from an independent implementation,
  primary source, or human-curated evidence, not from generated reference
  outputs alone.
- **Fixture curation:** fixtures and cases have provenance and were not promoted
  by the implementation author from an AI or reference-generated candidate.
- **Execution:** result run records commit/digest, runtime, platform, command,
  and clean-environment inputs.
- **Acknowledgement:** the external owner confirms the result or publishes an
  attributable artifact; silence is not acceptance.
- **Maintenance:** the consumer has an owner, version/update path, and a
  freshness date within the published support window.

## Outcomes

The machine-readable criteria in `conductor/tracks/v1_independent_validation_20260714/INDEPENDENCE_CRITERIA.json`
define these outcomes:

- `qualifying`: every required independence dimension is evidenced, results
  are reproducible, and the owner acknowledges the result.
- `partial`: useful evidence exists but one or more required dimensions remain
  incomplete; it cannot satisfy the v1 independent-adoption gate.
- `conflicting`: evidence disagrees or provenance cannot establish which result
  is authoritative; preserve both and do not select silently.
- `withdrawn`: the owner or maintainer withdrew the evidence.
- `declined`: the candidate explicitly declined participation.
- `unresponsive`: no response by the documented exit date; never count as
  adoption.

An agent-run or maintainer-run clean-room rehearsal is `partial` at best and
must carry `independenceStatus: internal-rehearsal`. It cannot satisfy the
external-organisation requirement regardless of test quality.

## Minimum evidence packet

Each submission requires implementation identity, organisation/ownership,
source revision and digest, contract versions, environment, command, input and
result digests, test outcome, provenance, acknowledgement status, maintenance
signal, and declared limitations. Screenshots and narrative claims are
supporting material only.


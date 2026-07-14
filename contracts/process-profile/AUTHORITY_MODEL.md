# PIC Process Profile Authority and Source Assertions

Status: draft for process-profile design  
Owner: PIC maintainers  
Last reviewed: 2026-07-15

The process profile records what a source-backed assertion says and how it may
be used. It does not decide the underlying law, clinical policy, funding rule,
or institutional judgement. A source assertion is evidence metadata, not a
runtime authority grant.

## Authority classes

| Class | Meaning | Controlling use |
| --- | --- | --- |
| `law` | Act, regulation, or other controlling legal instrument | May support a jurisdiction-scoped legal assertion when section, effective date, and scope are recorded |
| `national_policy` | Official national policy or decision framework | May support a policy assertion within its issuer and effective period |
| `regional_policy` | Official regional, state, or local policy | May support only the named jurisdiction and effective period |
| `guidance` | Official guidance, manual, or procedural instruction | May support a process-step assertion, not a broader legal conclusion |
| `interpretation` | Named human interpretation of an identified source | Requires human approval and must retain the underlying source |
| `runtime_observation` | Observed execution, event, or trace fact | Supports what was observed, not why the authority required it |
| `secondary` | Commentary, summary, academic or media source | Discovery and context only; never controlling by itself |

## Required assertion fields

Every assertion MUST include:

- a stable `assertionId` and a named consumer;
- `authorityClass`, issuer, jurisdiction, and subject scope;
- a source URL or content identifier, retrieval date, and rights status;
- `effectiveFrom` and, when known, `effectiveTo`;
- source status (`current`, `superseded`, `blocked`, `unavailable`, or
  `conflicting`);
- interpretation state (`uninterpreted`, `mapped`, or `contested`);
- reviewer state (`agent-proposed`, `human-approved`, or
  `official-primary`); and
- a digest where the source or exported assertion can be hashed.

The source effective date and the retrieval/observation date MUST remain
separate. A retrieval date cannot substitute for an effective date when the
assertion affects a time-dependent process.

## Review and controlling eligibility

An assertion is eligible to support a controlling process-profile mapping only
when all of the following hold:

1. its authority class is appropriate to the claim and jurisdiction;
2. its source status is `current` and not `blocked`, `unavailable`, or
   `conflicting`;
3. its effective date is present and covers the process observation date;
4. its reviewer state is `official-primary` or `human-approved`; and
5. its source, digest, interpretation, and named consumer are recorded.

`agent-proposed` assertions may populate candidate mappings and exception
packets. They MUST NOT certify a controlling assertion or promote a golden
fixture. Secondary-only evidence remains explicitly secondary even when a
human has read it; human approval may approve an interpretation of a primary
source, not transform commentary into primary authority.

## Fail-closed dispositions

| Condition | Deterministic disposition |
| --- | --- |
| Missing source or issuer | `blocked` with `missing_source` |
| Missing effective date for a time-dependent claim | `blocked` with `missing_effective_date` |
| Source is superseded for the observation date | `blocked` with `stale_source` |
| Primary sources conflict | `blocked` with `conflicting_primary_sources` |
| Only secondary evidence is available | `blocked` with `secondary_only_evidence` |
| Source cannot be accessed or rights are unclear | `blocked` with `blocked_source` |
| Assertion is agent-proposed | Candidate/exception only with `agent_proposed` |
| Human interpretation is contested | `exception` with `contested_interpretation` |

The profile MUST preserve the disposition and next action. It MUST NOT infer a
missing source, silently select one conflicting source, backdate an effective
date, or replace an unavailable source with a secondary summary.

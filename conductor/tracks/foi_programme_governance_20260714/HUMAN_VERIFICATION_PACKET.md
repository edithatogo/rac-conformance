# Human verification packet

Prepared: 2026-07-15; analyst audit: 2026-07-17

This packet separates decisions Dylan can verify now from the compatibility
exercise that must wait for the published FOI-O release-evidence bundle and
independent review. Approval of the first three sections does not approve a
fixture, crosswalk row, legal interpretation, release, paper, or external
contribution.

Audit boundary (2026-07-17): no live Project 14 query or hosted verification was
performed for this audit. The dated machine observations below are historical
evidence and must be refreshed by the analyst before they are used as current
programme status.

## Evidence register

| Evidence ID | Scope | Evidence link | Freshness / limitation |
|---|---|---|---|
| `FOI-GOV-LOCAL-01` | Intended Project 14 scope and field policy | [`spec.md`](./spec.md), [`requirements.md`](./requirements.md) | Repo-local policy; not proof of live Project configuration. |
| `FOI-GOV-LOCAL-02` | Allowlist and expected status overrides | [`project14-allowlist.json`](./project14-allowlist.json) | Repo-local expected state; compare with a newly exported Project 14 item list. |
| `FOI-GOV-LOCAL-03` | Recorded implementation and blocker notes | [`plan.md`](./plan.md) | Historical checkpoints; not a current hosted-status assertion. |
| `FOI-GOV-LOCAL-04` | FOI-O/PIC boundary and release-handshake requirements | [`foio-pic-integration.md`](./foio-pic-integration.md), [`github-issue.md`](./github-issue.md) | Analyst-facing design guidance; no published FOI-O V2 evidence. |
| `FOI-GOV-LIVE-01` | Project 14 item/state/field verification | Analyst must attach the raw `gh project item-list` export, retrieval date, account, and validator output | Missing from this repository; the 2026-07-15 snapshot below is not a refresh. |

For every live decision, record the export path or attachment, retrieval date,
authenticated account, validator command, and result. A URL alone is not enough
to establish item membership, field values, or status.

## 1. Umbrella definition

Live surface: <https://github.com/users/edithatogo/projects/14>

Confirm that Project 14:

- is the focused Freedom of Information programme board;
- names the seven in-scope repositories and their documented boundaries;
- limits legislation, NLP, RaC, and Alaveteli items to FOI-relevant work;
- preserves repository-native Conductor roadmaps as implementation sources of truth; and
- does not imply legal validation, publication, or upstream acceptance through Project status.

Decision: `approve` or record the exact correction required.

## 2. Item synchronization

Machine evidence:

```bash
gh project item-list 14 --owner edithatogo --format json --limit 200 \
  > /tmp/project14.json
python tools/validate_project14_allowlist.py --items /tmp/project14.json \
  --allowlist conductor/tracks/foi_programme_governance_20260714/project14-allowlist.json
```

The recorded snapshot on 2026-07-15 reported `observed=19 required=19` with no
missing, extra, or stale issue/PR items. The allowlist explicitly records
`edithatogo/nlp-policy-nz#100`, `edithatogo/nlp-policy-nz#101`, and
`edithatogo/rac-conformance#36` as `Done`; all
other allowlisted items are expected to be `Todo`. Every item has values for
jurisdiction, repository role, dependency, evidence status, human gate, and
delivery status. Dedicated repository Project memberships were not removed.

This is a historical machine-verification record only. It does not establish
the current Project 14 state, and it does not constitute Dylan's approval of the
Project 14 scope, synchronization policy, or FOI-O/PIC boundary rules.

Decision: `approve`, `amend`, or `defer`; identify the item/field, evidence ID,
and correction when the decision is not an unconditional approval.

## 3. Durable governance

Confirm that the exact allowlist is the intended anti-drift policy. Historical
items were removed from Project 14 only; their source issues and dedicated
Project memberships remain intact. The checker fails on missing, stale-status,
or unrelated issue/PR items.

Decision: `approve`, `amend`, or `defer`; identify the allowlist/policy change,
evidence ID, and reviewer when applicable.

## 4. FOI-O to PIC boundary

Confirm these design constraints:

- FOI-O remains authoritative for its runtime, ontology, schemas, codebooks,
  jurisdiction profiles, and release lifecycle.
- PIC is an optional, versioned interchange profile, not a FOI-O dependency.
- epistemic, review, extraction, certification, and promotion states remain
  separate from PIC `valueState`.
- generated fixture/crosswalk candidates require independent review and
  immutable review evidence before promotion.
- the NZ compatibility entry correctly remains
  `blocked_pending_evidence_bundle` until the published FOI-O `v0.8.1`
  evidence bundle and its artifacts pass content-addressed offline validation;
- the Australian entry correctly remains
  `blocked_jurisdiction_profile_release` until its jurisdiction profile
  release is complete;
- the independent-oracle review and promotion gate remain open even though the
  software release and Zenodo record are verified.
- the Hugging Face pin retains both provenance exceptions; it is not silently
  treated as a certified manuscript dataset.

Decision now: `approve`, `amend`, or `defer`; identify the boundary rule,
evidence ID, and required correction when applicable.
Final Phase 4 verification remains pending until the published-release exercise
passes.

## Decision record

| Section | Outcome (`approve` / `amend` / `defer`) | Evidence ID(s) checked | Correction or condition | Reviewer + date |
|---|---|---|---|---|
| 1. Umbrella definition |  |  |  |  |
| 2. Item synchronization |  |  |  |  |
| 3. Durable governance |  |  |  |  |
| 4. FOI-O/PIC boundary |  |  |  |  |

## Approval record

An unambiguous response may use:

> I approve governance verification sections 1-3 and the Phase 4 boundary
> rules. I understand the release-evidence exercise and independent review
> remain open.

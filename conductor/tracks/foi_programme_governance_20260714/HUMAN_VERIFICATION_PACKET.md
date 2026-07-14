# Human verification packet

Prepared: 2026-07-14

This packet separates decisions Dylan can verify now from the compatibility
exercise that must wait for a published FOI-O V2 release. Approval of the first
three sections does not approve a fixture, crosswalk row, legal interpretation,
release, paper, or external contribution.

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

The last verified result contained all 19 required items, no missing, extra, or
stale issue/PR items, and values for jurisdiction, repository role, dependency,
evidence status, human gate, and delivery status. Dedicated repository Project
memberships were not removed.

Decision: `approve` or identify the item/field that is incorrect.

## 3. Durable governance

Confirm that the exact allowlist is the intended anti-drift policy. Historical
items were removed from Project 14 only; their source issues and dedicated
Project memberships remain intact. The checker fails on missing, stale-status,
or unrelated issue/PR items.

Decision: `approve` or identify the allowlist/policy correction required.

## 4. FOI-O to PIC boundary

Confirm these design constraints:

- FOI-O remains authoritative for its runtime, ontology, schemas, codebooks,
  jurisdiction profiles, and release lifecycle.
- PIC is an optional, versioned interchange profile, not a FOI-O dependency.
- epistemic, review, extraction, certification, and promotion states remain
  separate from PIC `valueState`.
- generated fixture/crosswalk candidates require independent review and
  immutable review evidence before promotion.
- the current compatibility matrix correctly remains
  `blocked_no_published_release` until FOI-O V2 is published and its artifacts
  pass content-addressed offline validation.
- the Hugging Face pin retains both provenance exceptions; it is not silently
  treated as a certified manuscript dataset.

Decision now: approve the boundary rules, or identify a required correction.
Final Phase 4 verification remains pending until the published-release exercise
passes.

## Approval record

An unambiguous response may use:

> I approve governance verification sections 1-3 and the Phase 4 boundary
> rules. I understand the published-release exercise and independent review
> remain open.

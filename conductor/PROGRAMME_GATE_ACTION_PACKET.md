# Outstanding Programme Gate Action Packet

Prepared: 2026-07-17

This packet is an operational handoff for the remaining external and human
gates. It does not claim that any gate is complete. The local Conductor plans
and `PROGRAMME_GATE_REGISTRY.json` remain authoritative.

The v1-specific decisions for process-mappings cutover, PIC certification,
health-technology comparison, independent validation, and release qualification
are consolidated in `conductor/V1_REMAINING_GATES_PACKET.md`.

## 1. External adoption: #23

Local preparation is complete in `external/MAINTAINER_FOLLOWUPS.md` and
`external/ADOPTION_STATUS.md`.

Required external outcomes for each still-open proposal:

- maintainer workflow approval and hosted checks for PolicyEngine #515-#517;
- maintainer review and terminal disposition for OpenFisca #1382/#1381;
- BetterRules review and terminal disposition for OpenFisca Aotearoa #200.

RuleSpec NZ #79/#80 is no longer an outstanding gate. The maintainer confirmed
that canonical migration #83 reproduced the semantic fix on upstream `main`,
reported clean compilation and 3/3 companion tests, and closed the issue and PR
with credit. Do not describe PR #80 as merged; describe the fix as adopted
upstream through canonical migration.

Record only URL-backed `merged`, `declined`, `adopted through a documented
replacement`, or `blocked` outcomes. Do not convert silence, a local fork, or a
passing local rehearsal into adoption.

## 2. FOI-O evidence: #27 and paper trigger #31

FOI-O must publish an immutable evidence bundle containing the release tag and
SHA, contract/capability matrix, migrations, tests, fixtures, provenance,
empirical results, exceptions, and limitations. The RaC paper refresh starts
only after that bundle is public and its digests are independently checked.

When available, validate the bundle locally with:

```sh
python tools/validate_foio_evidence_bundle.py /path/to/foio-release-evidence.json
```

Do not infer the bundle from FOI-O `v0.8.1` alone. The public issue remains the
upstream source of truth.

## 3. FOI governance: #30

Use `foi_programme_governance_20260714/HUMAN_VERIFICATION_PACKET.md` and run
the allowlist command against a fresh Project 14 export:

```sh
gh project item-list 14 --owner edithatogo --format json --limit 200 \
  > /tmp/project14.json
python tools/validate_project14_allowlist.py \
  --items /tmp/project14.json \
  --allowlist conductor/tracks/foi_programme_governance_20260714/project14-allowlist.json
```

The human decision is limited to confirming the live title, scope, repository
boundaries, item membership, metadata fields, and navigation anchors.

## 4. Zenodo: #33

The deposit packet is ready at
`papers/zenodo/RAC_CONFORMANCE_V0.2.0_ARCHIVE.json`. Deposit the GitHub
`v0.2.0` release, then verify that the version DOI resolves to commit
`35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5` and that the concept DOI is linked
to the same record. Only then replace the pending DOI fields in the mirror
manifest and citation ledger.

## 5. Papers: #24

After #27 is complete:

1. import the immutable FOI-O evidence bundle;
2. regenerate affected tables, figures, methods, results, and limitations;
3. rerun `make check` and paper artifact QA;
4. review authorship, affiliations, venue, and disclosures; and
5. obtain explicit submission authorization for each packet.

No paper submission is authorized by this packet.

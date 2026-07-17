# Analyst review packet

**Snapshot date:** 2026-07-17
**Track:** `v1_independent_validation_20260714`
**Disposition:** blocked pending external evidence and analyst authorization

## Review worksheet

Complete one copy of this worksheet per target. A blank or `unknown` field is
an evidence failure, not permission to continue.

| Field | Required review entry |
|---|---|
| Target and upstream URL | Exact repository, issue/PR, or named organisation |
| Owner and communication authority | Named analyst/maintainer owner; authorization reference, if any |
| Implementation revision | Immutable commit/tag, not a branch name alone |
| Repository control | External to maintainer; explain fork or shared ownership |
| Fixture/oracle control | Who generated the corpus and how the oracle is independent |
| Environment | OS, runtime, engine/model versions, dependency lock information |
| Corpus and result digests | SHA-256 values for the exact files reviewed |
| Reproduction command | Clean-environment command and observed result |
| Verifier result | Command, version/revision, and exact accepted/rejected status |
| Acknowledgement | Durable response from the external owner, or `absent` |
| Freshness | As-of date and expiry/recheck trigger |
| Disposition | `blocked`, `partial`, `conflicting`, `qualifying`, `withdrawn`, `declined`, or `unresponsive` |

## Current dispositions

- **PolicyEngine:** open PRs and issue-linked proposals remain maintainer
  controlled submissions; no independent consumer result is present.
- **OpenFisca core:** PR #1382 remains open; issue #1381 remains awaiting
  maintainer direction; no independent consumer result is present.
- **OpenFisca Aotearoa:** PR #200 remains open; a fork implementation is not
  independent adoption evidence for this gate.
- **FOI-O:** issue #27 remains open. The local remediation candidate is not an
  upstream release or evidence bundle.
- **Unaffiliated route:** deferred until a named organisation, repository,
  owner, and communication channel exist. Do not send a generic invitation.

## Evidence intake sequence

1. Recheck the upstream URL and immutable revision on the snapshot date.
2. Obtain the external result package without modifying its contents.
3. Verify hashes and schema from a clean environment.
4. Run the local verifier:

   ```sh
   PYTHONPATH=. uv run python tools/independent_validation.py \
     --kit independent/kit \
     --result /path/to/external-result.json
   ```

5. Classify failures as contract, implementation, source/fixture, environment,
   or unresolved. Preserve the original result and authorship.
6. Require explicit acknowledgement before changing the canonical ledger.

The example result in `independent/kit/` is intentionally not submitted and
must remain rejected. A local run, maintainer-owned fork, staged patch, or
paper draft cannot satisfy this sequence.

## Paper and FOI handoff boundary

The paper lane may cite only durable evidence that passes this worksheet. The
FOI-O lane may cite only a published, immutable release-evidence bundle that
passes its dedicated validator. Until then, write **evidence not available**
and list the missing artifact; do not substitute release metadata, a DOI, a
local candidate commit, or an issue comment.

# Plan: papers_completion_20260711

## Phase 1 - Shared evidence and publication infrastructure

- [x] Task: Build source and citation ledger with primary-source verification
- [x] Task: Add reproducible manuscript build, citation, table, figure, and link checks
- [x] Task: Define journal targets, reporting checklists, declarations, and shared author metadata
- [x] Task: Conductor - Automated Review and Checkpoint 'Shared evidence and publication infrastructure' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Added the shared citation/evidence ledger, reporting checklist, and a third-paper QA surface. The ledger distinguishes primary sources, engine repositories, effective-date requirements, and non-authoritative comparison evidence. Submission remains human-gated.

## Phase 2 - Coupling paper

- [x] Task: Expand methods, architecture, evaluation, related work, and limitations
- [x] Task: Generate architecture and evidence-traceability figures/tables
- [x] Task: Build and review the coupling submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'Coupling paper' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Added conceptual architecture, evidence-summary, differential pipeline, and exception-queue figures/tables. They are explicitly non-normative and link back to committed artifacts.

## Phase 3 - SNAP divergence paper

- [x] Task: Expand corpus provenance, runner methods, triangulation, results, and threats to validity
- [x] Task: Generate flow, classification, agreement, and exception-queue figures/tables
- [x] Task: Build and review the SNAP submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'SNAP divergence paper' (Protocol in workflow.md)

## Phase 4 - NZ reconciliation paper

- [x] Task: Draft full manuscript from live dual-engine and engine-gap evidence
- [x] Task: Generate coverage, agreement, and model-surface figures/tables
- [x] Task: Build and review the NZ reconciliation submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'NZ reconciliation paper' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Drafted the NZ reconciliation manuscript and packet from the certified engine-gap evidence. Figures/tables and final primary-source refresh remain before submission readiness.

## Phase 4.5 - Final local QA and review packet

- [x] Task: Run final manuscript, citation, artifact, and link QA across all three packages
- [x] Task: Normalize paper issue hierarchy and record the NZ reconciliation paper as a child work item of this track
- [x] Task: Conductor - Automated Review and Checkpoint 'Final local QA and review packet' (Protocol in workflow.md)

Acceptance: `make check` passes; all three packets identify their evidence roots,
limitations, declarations, and human submission decisions; issue #17 is either
closed as superseded or explicitly retained as a child of issue #24; no artifact
claims submission or acceptance without human evidence.

> CHECKPOINT (2026-07-11): Final `make check` passed across repository audit,
paper artifacts, contracts, converters, harnesses, both study runners, and demos.
The three paper packets are locally prepared and remain submission-deferred.
Issue #17 was superseded by the unified paper program issue #24; publication
authorization remains a human gate.

> DECISION (2026-07-14): Keep the papers deferred until the next `foi-o`
release is available. After that release, update the papers and submit only
after Dylan's explicit authorization.

## Phase 4.75 - FOI-O release-triggered paper refresh

GitHub subissue: [#31](https://github.com/edithatogo/rac-conformance/issues/31).

- [x] Task: Verify the immutable `foi-o` release tag, commit SHA, contract and
      schema versions, capability matrix, migrations, and reproducibility commands.

> VERIFIED (2026-07-15): `papers/FOIO_V0.8.1_RELEASE_VERIFICATION.md` records
> the immutable tag/commit, package and citation versions, key contract/schema/
> migration hashes, reproducibility commands, and the exact non-green test
> outcome. This closes release inspection only; it does not close the evidence
> bundle, empirical, conformance, or human-publication gates.

> EVIDENCE UPDATE (2026-07-15): `edithatogo/foi-o` has now published immutable
> release `v0.8.1` at commit
> `d24ae6f9f2d9488052969f633d91eff4a9a47f58`. The release is recorded in the
> programme citation ledger with verified Zenodo DOIs. The release-evidence
> bundle required by `foi-o#27` is still absent, so no empirical results,
> migrations, fixtures, or limitations may be inferred from the release alone.
- [ ] Task: Import the release-evidence bundle containing tests, fixtures,
      provenance, empirical results, exception summaries, and known limitations.
      - **PREPARATION COMPLETE (2026-07-15):** `tools/validate_foio_evidence_bundle.py` provides fail-closed intake validation for release identity, capabilities, contracts, migrations, tests, fixtures, provenance, empirical results, exceptions, and limitations.
- [ ] Task: Diff release evidence against manuscript claims and regenerate all
      affected tables, figures, citations, methods, results, and limitations.
- [ ] Task: Run paper-artifact QA and prepare a human submission approval packet.
- [ ] Task: Conductor - Automated Review and Checkpoint 'FOI-O release-triggered paper refresh' (Protocol in workflow.md)

> BLOCKED (2026-07-15): The immutable release trigger is satisfied, but this
> phase remains blocked until `foi-o#27` publishes the release-evidence bundle.
> Publication remains human-authorized after the refresh.

> PREPARATION (2026-07-15): Prepared the independent `Paper Programme
> Submission Candidate v0.3.0` package across all three manuscripts and
> submission packets. It preserves the current FOI-O evidence limitation and
> advances venue/PDF/authorization decisions without claiming that #27 or any
> external adoption proposal is accepted. The release-triggered refresh tasks
> remain open for evidence reconciliation when #27 is accepted.

> HUMAN APPROVAL (2026-07-15): Dylan approved package version `v0.3.0`.
> This approves the prepared package only; venue selection, declarations, PDF
> submission authorization, and any FOI-O evidence claims remain separate gates.

> DECISION (2026-07-15): Dylan will not submit any paper in the v0.3.0 package
> until the FOI-O v2 update has been submitted to arXiv. Keep all three paper
> packets prepared, but retain the submission gate pending that prerequisite.

> CHECKPOINT (2026-07-17): The approved v0.3.0 preparation package, including
> its hashed A4 PDFs and explicit FOI-O v2 submission prerequisite, has been
> reconciled onto current `origin/main`. Deferred health-technology, Camunda,
> process-mappings, and broad release-qualification branch stacks were not
> merged because they remain outside the focused core demonstrator scope.

## Phase 4.8 - Programme citation and mirror reconciliation

- [x] Task: Add or correct `CITATION.cff` metadata for every included FOI
      programme repository and tool.
- [x] Task: Add the shared version/Zenodo/Hugging Face mirror manifest and
      ledger rows, including Alaveteli's source-intelligence-only boundary.
- [ ] Task: [HUMAN] Publish each tagged release to Zenodo and replace pending
      statuses with verified version and concept DOIs.
- [ ] Task: [HUMAN] Pin the Hugging Face dataset repository, revision, and
      digest for the exact archive-derived layer used in the manuscripts.

> CANDIDATE PIN (2026-07-15): `edithatogo/fyi-archive-nz` revision
> `fc27bfa471c598a31d975cfa2b603b1a11408e55`, artifact
> `manifests/latest_manifest.parquet`, SHA-256
> `fd5f54be6b94390dce93b4662fc393c855d87569ff70eaf5411c365d0cbca678`.
> Human certification remains open because the publisher provenance records a
> dirty source checkout and the declared dataset splits are absent from the
> pinned tree.
- [x] Task: Run the citation validator and live DOI audit before the release
      refresh checkpoint.

> CHECKPOINT (2026-07-14): Local CFF and manuscript-register work is complete.
> The citation validator passed all seven programme artefacts. The live Zenodo
> audit confirmed that DOI `10.5281/zenodo.21338285` is a published `0.1.0`
> record, not the current `fyi-archive v0.11.1`; the mismatch is recorded and
> no current-release DOI is claimed. All other release mirrors and Hugging
> Face coordinates remain explicit human publication gates.

## Phase 5 - Human submission gates

- [ ] Task: [HUMAN] Approve final authorship, affiliations, target venues, and disclosure text
- [ ] Task: [HUMAN] Authorize each arXiv or journal submission
- [x] Task: Record submission identifiers or continued deferral
- [ ] Task: Conductor - Automated Review and Checkpoint 'Human submission gates' (Protocol in workflow.md)

> BLOCKED (2026-07-11): Submission decisions require Dylan's explicit authorship, venue, disclosure, and submit authorization. Agents may prepare packets and evidence but may not submit.

# Adoption Status Ledger

This document tracks all staged and submitted upstream proposals, PRs, and issues for the next-generation rules/process roadmap.

| Target Upstream | Artifact | Status | URL / Context | GitHub Issue / Label | CI State | Owner | Next Action |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `PolicyEngine/policyengine-core` (Tracer Missingness) | `.external-repos/policyengine-core` | `merged` (local fork) | [PE Issue #1](https://github.com/edithatogo/policyengine-core/issues/1) (Closed) | `edithatogo/policyengine-core#1` | `pass` | Agent | None (Archived) |
| `PolicyEngine/policyengine-core` (Versioned trace export) | `external/policyengine/SUBMISSION_trace.md` | `staged` | No open upstream issue found on 2026-07-06 | `PolicyEngine/policyengine-core` (`human-gate`) | `none` | Dylan | Open issue upstream using staged draft (`[HUMAN]`) |
| `PolicyEngine/policyengine-core` (Missingness semantics) | `external/policyengine/SUBMISSION_missingness.md` | `staged` | No open upstream issue found on 2026-07-06 | `PolicyEngine/policyengine-core` (`human-gate`) | `none` | Dylan | Open issue upstream using staged draft (`[HUMAN]`) |
| `openfisca/openfisca-core` (Missingness Semantics) | `.external-repos/openfisca-core` | `merged` (local fork) | [OF Issue #1](https://github.com/edithatogo/openfisca-core/issues/1) (Closed) | `edithatogo/openfisca-core#1` | `pass` | Agent | None (Archived) |
| `openfisca/openfisca-core` (Missingness semantics) | `external/openfisca/SUBMISSION_missingness.md` | `staged` | No open upstream issue found on 2026-07-06 | `openfisca/openfisca-core` (`human-gate`) | `none` | Dylan | Open issue upstream using staged draft (`[HUMAN]`) |
| `TheAxiomFoundation/axiom-rules-engine` (Harness) | `.external-repos/axiom-rules-engine` | `merged` (local fork) | [Axiom Issue #1](https://github.com/edithatogo/axiom-rules-engine/issues/1) (Closed) | `edithatogo/axiom-rules-engine#1` | `pass` | Agent | None (Archived) |
| `TheAxiomFoundation/rulespec-nz` (KiwiSaver compile blocker) | `external/axiom/UPSTREAM_FEEDBACK.md` | `staged` | KiwiSaver contributions fail `axiom-rules-engine compile` under pinned SHAs; live suite otherwise passes | `TheAxiomFoundation/rulespec-nz` (`human-gate`) | `pass` | Dylan | Submit staged feedback or merge upstream fix (`[HUMAN]`) |
| `edithatogo/foi-o` (OIA rules module coupling) | `external/foi-o/SUBMISSION.md` | `staged` | `uv run pytest tests/test_oia_rules.py` + coverage pass; bundle verified in clean external checkout | `edithatogo/foi-o#PR` (`human-gate`) | `pass` | Dylan | Prepare PR and present for human review (`[HUMAN]`) |
| `PolicyEngine/policyengine-core` (YAML converter) | `external/policyengine/SUBMISSION.md` | `staged` | None | `PE#Issue-YAML` (`human-gate`) | `none` | Dylan | Open issue upstream (`[HUMAN]`) |
| `openfisca/openfisca-core` (YAML converter) | `external/openfisca/SUBMISSION.md` | `staged` | None | `OF#Issue-YAML` (`human-gate`) | `none` | Dylan | Open issue upstream (`[HUMAN]`) |
| `Alaveteli/mySociety` (Request State Taxonomy) | `external/alaveteli/SUBMISSION.md` | `staged` | No open upstream issue found on 2026-07-06 | `Alaveteli#Issue` (`human-gate`) | `none` | Dylan | Open issue upstream using staged draft (`[HUMAN]`) |
| `Digital Benefits Network Rules-as-Code CoP` (Email) | `external/dbn/EMAIL.md` | `sent` | Email thread | `DBN#Email` (`external-gate`) | `none` | Dylan | Monitor for responses |

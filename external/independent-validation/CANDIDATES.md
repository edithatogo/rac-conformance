# Independent Validation Candidates

Status: draft for human target selection; no outreach has been sent.

The machine-readable candidate registry is
`CANDIDATE_REGISTRY.json`. It is the review surface for target ownership,
bounded scope, independence risk, and no-response handling. It does not
authorise contact or establish adoption.

The independent-validation gate requires an external organization, an
independent implementation or integration, an independent oracle or fixture
curation path, attributable results, and a maintenance signal. The following
are candidate surfaces, not adoption evidence.

| Candidate | Consumer problem | Proposed bounded surface | Independence risk | Disposition |
| --- | --- | --- | --- | --- |
| PolicyEngine maintainers | Reproducible cross-engine trace and fixture comparison | Consume `pic-semantics/0.1.0` or `pic-traces/0.2.0` in a clean test job | Existing upstream proposal may be a maintainer-controlled fork; only a fresh independently-owned implementation qualifies | Requires human outreach approval |
| OpenFisca maintainers | Process/trace representation around rules-heavy jurisdiction models | Validate a read-only profile or trace projection without changing engine semantics | Existing contribution path may not establish organizational or oracle independence | Requires human outreach approval |
| An unaffiliated public-sector or research implementer | Need for source-backed process profile and deterministic conformance evidence | Run the self-contained PIC implementer kit against an independently curated synthetic case | Candidate must be identified and must curate its own oracle | Preferred qualifying route; candidate not yet identified |

## Required submission contents

1. Organization and repository identity.
2. Contract versions and immutable artifact digests.
3. Independent implementation and oracle-curation statement.
4. Clean-environment command, runtime, platform, and result manifest.
5. Input, output, and diagnostic checksums.
6. Mismatch classification and unresolved limitations.
7. Maintainer acknowledgement and freshness date.

No screenshot, narrative endorsement, local fork, self-owned branch, or agent
rehearsal satisfies the v1 gate.

# Independent Validation Candidates

Status: bounded PolicyEngine and OpenFisca core outreach submitted and awaiting response; other targets remain uncontacted or deferred. No adoption is claimed.

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
| PolicyEngine maintainers | Reproducible missingness semantics | Run the five manifested `pic-semantics/0.1.0` cases in a clean test job | Existing upstream proposal may be a maintainer-controlled fork; only a fresh independently-owned implementation qualifies | Authorized outreach submitted; awaiting maintainer response |
| OpenFisca maintainers | Missingness representation in rules-heavy models | Run the same five semantics cases without changing engine semantics | Existing contribution path may not establish organizational or oracle independence | Authorized outreach submitted; awaiting maintainer response |
| An unaffiliated public-sector or research implementer | Need for deterministic conformance evidence | Run the same five semantics cases with independently controlled code and oracle | Candidate must be identified and must curate its own oracle | Preferred qualifying route; candidate not yet identified |

Trace, profile, fixture-converter, NZ-specific fixture, and synthetic-case
surfaces are excluded until a separately versioned kit and verifier support
them.

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

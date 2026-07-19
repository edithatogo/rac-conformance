# v1.0.0-rc.1 Qualification Matrix

Latest hosted qualification commit: `0442ffdfda2b204e6d88dbdebcf8da5f1c97f273`.
It was merged into current `main` as `680dbd7b99fb3409d67244638ff045c24edaed59`.

| Surface | Local evidence | Status | Release interpretation |
| --- | --- | --- | --- |
| Core PIC schemas, validators, examples | Clean `make check` | pass | Repo-local evidence only |
| Engineering hardening | Hosted qualification, hostile-input, property, mutation, SBOM, and reproducibility evidence | pass with limitations | Automated evidence is complete; signing, attestations, live rollback, and human residual-risk approval remain open |
| Fixture converters | Clean converter lint/tests and corpus report | pass | Adapter evidence, not external adoption |
| Axiom and PolicyEngine harnesses | Clean harness tests | pass | No maintainer certification |
| SNAP divergence study | Clean runner tests | pass | Research profile; not a general consumer |
| NZ reconciliation | Clean runner tests | pass | Study evidence; not independent adoption |
| Service and Docassemble demos | Clean demo tests | pass | Experimental; no v1 compatibility promise |
| FOI-O release evidence bundle | `foi-o#27` dependency | blocked | Cannot verify capabilities, migrations, fixtures, or empirical results |
| Independent consumer | Track #45 evidence policy | post-v1 | No qualifying evidence exists; this remains an explicit limitation and maturity target, not a v1 release gate |
| FOI programme governance | Approved `rac-conformance#30` packet and validated 2026-07-17 live Project 14 export | pass | Scope, membership, required fields, navigation, and FOI-O/PIC boundary are verified |
| Paper programme and submission | `rac-conformance#24/#31` packets | blocked | Refresh waits for FOI-O evidence; submission requires Dylan's authorization |
| RaC Zenodo deposit | `rac-conformance#33` packet | blocked | Deposit and DOI verification remain human-gated |
| Health-technology profiles | Human case/jurisdiction selection pending | blocked | Candidate mappings cannot be promoted |
| Camunda normalized traces | Later adapter tasks pending | blocked | Optional demonstrator is not a v1 core gate |

The matrix is deterministic and deliberately distinguishes passing local tests
from external qualification. It does not certify any candidate fixture,
jurisdiction mapping, external maintainer, or independent implementation.

Automated cross-platform and hosted security evidence for the current candidate
is recorded in `docs/V1_HOSTED_QUALIFICATION.md` and
`docs/V1_HOSTED_GOVERNANCE.md`. Human source certification, publication,
signing, and controlled evidence gates remain blocked. Independent adoption is
absent and tracked post-v1 without weakening its evidence criteria.

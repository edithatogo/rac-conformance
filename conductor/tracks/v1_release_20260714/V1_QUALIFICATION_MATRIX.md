# v1.0.0-rc.1 Qualification Matrix

Candidate commit: `0c4a83b55208bae59592af017c6e0f66194ec8bb`

| Surface | Local evidence | Status | Release interpretation |
| --- | --- | --- | --- |
| Core PIC schemas, validators, examples | Clean `make check` | pass | Repo-local evidence only |
| Fixture converters | Clean converter lint/tests and corpus report | pass | Adapter evidence, not external adoption |
| Axiom and PolicyEngine harnesses | Clean harness tests | pass | No maintainer certification |
| SNAP divergence study | Clean runner tests | pass | Research profile; not a general consumer |
| NZ reconciliation | Clean runner tests | pass | Study evidence; not independent adoption |
| Service and Docassemble demos | Clean demo tests | pass | Experimental; no v1 compatibility promise |
| FOI-O release evidence bundle | `foi-o#27` dependency | blocked | Cannot verify capabilities, migrations, fixtures, or empirical results |
| Independent consumer | Track #45 evidence policy | blocked | Agent rehearsal is explicitly non-qualifying |
| FOI programme governance | `rac-conformance#30` manual packet | blocked | Live Project 14 verification remains human-gated |
| Paper programme and submission | `rac-conformance#24/#31` packets | blocked | Refresh waits for FOI-O evidence; submission requires Dylan's authorization |
| RaC Zenodo deposit | `rac-conformance#33` packet | blocked | Deposit and DOI verification remain human-gated |
| Health-technology profiles | Human case/jurisdiction selection pending | blocked | Candidate mappings cannot be promoted |
| Camunda normalized traces | Later adapter tasks pending | blocked | Optional demonstrator is not a v1 core gate |

The matrix is deterministic and deliberately distinguishes passing local tests
from external qualification. It does not certify any candidate fixture,
jurisdiction mapping, external maintainer, or independent implementation.

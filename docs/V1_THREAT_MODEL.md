# RaC Conformance v1 Threat Model

Status: repository-local engineering evidence; not a penetration-test report.

This threat model covers the deterministic validators, fixture converters,
profile consumers, reports, CI workflows, and release artefacts in this
repository. It treats policy, legal, clinical, and funding content as
untrusted data. Validation of a document does not certify the truth of its
content.

## Trust boundaries

| Boundary | Untrusted input | Required control | Evidence |
| --- | --- | --- | --- |
| Filesystem to validators | JSON, YAML, JSONL, Markdown, and fixture paths | Resolve paths under an explicit repository/input root; validate type, size, encoding, and schema before use | `contracts/tools/src/pic_contracts/`, `tools/repo_audit.py`, example validators |
| Archive to extraction | Archives or extracted trees | Reject traversal and unexpected files; retain a manifest and digest; extract into a disposable directory | `tools/process_mappings_rehearsal.py`, migration rehearsal report |
| Source reference to profile | URLs, source identifiers, dates, and digests | Treat locators as assertions requiring provenance, effective dates, rights state, and human review before promotion | `contracts/process-profile/AUTHORITY_MODEL.md`, source manifests |
| Converter to contract | Fixture or profile documents | Validate input and output schemas; reject unsupported constructs; preserve loss and provenance | `contracts/tools/`, `converters/fixtures/`, converter tests |
| Cross-repository input | Vendored or staged external material | Use `external/<repo>/` staging, pinned revisions, and explicit boundary documents; do not silently copy normative definitions | `AGENTS.md`, `external/`, `contracts/CONSUMERS.md` |
| Report generation | Records, diagnostics, and generated paths | Serialize bounded data, avoid secrets and executable content, and record source/digest metadata | report and evidence tools/tests |
| CI workflow | Pull requests, dependencies, action revisions, secrets, artifacts | Least privilege, immutable action pins, isolated jobs, secret scanning, and artifact retention | `.github/workflows/`, `quality.yml`, `codeql.yml` |
| Release publication | Packages, source archives, SBOMs, provenance, and tags | Build from an immutable reviewed commit; compare digests; require human signing/publication approval | `release-candidate/`, `conductor/v1-release-gates.json` |
| Optional adapters | Camunda, Docassemble, service, and external engine traces | Keep adapters isolated and version-locked; do not make them normative or allow them to certify content | `subrepos/process-mappings/adapters/`, adapter tests |

## Threat classes and dispositions

| ID | Threat | Impact | Control or required treatment | Owner | Release disposition |
| --- | --- | --- | --- | --- | --- |
| TM-01 | Path traversal or symlink escape during extraction | Writes outside the disposable input directory | Canonicalize and constrain every extracted path; test `..`, absolute paths, and symlinks | maintainers | blocking until hostile-input tests pass |
| TM-02 | Archive bomb or oversized collection | CPU, memory, disk, or CI exhaustion | Enforce archive/member/count/size limits before extraction and record rejected inputs | maintainers | blocking until limits are measured |
| TM-03 | Deeply nested or recursive structured data | Stack exhaustion or non-terminating validation | Bound depth and collection sizes; use deterministic failure diagnostics | maintainers | blocking until resource tests pass |
| TM-04 | Malicious strings or markup in identifiers/reports | Log, Markdown, HTML, shell, or terminal injection | Treat values as data; escape report output; never execute generated values | maintainers | open; verify with hostile-string corpus |
| TM-05 | Remote references or mutable source locators | Non-reproducible or poisoned validation | Do not dereference during validation; require pinned digest/revision and source status | maintainers | blocking for promoted evidence |
| TM-06 | Schema abuse or unknown contract revision | Silent semantic drift or false compatibility | Fail closed on unknown revisions; validate schemas and compatibility matrices | maintainers | partially controlled; qualification required |
| TM-07 | Decimal/number ambiguity | Incorrect policy or financial interpretation | Preserve decimal strings and reject unsupported numeric representations | maintainers | controlled by schemas; regression required |
| TM-08 | Provenance spoofing or stale authority assertion | Incorrect claim presented as controlling | Require authority class, effective date, retrieval date, digest, and human/official review state | profile owners | blocking for certified mappings |
| TM-09 | Candidate fixture promoted as golden evidence | False conformance or circular oracle | Keep agent-proposed material in candidate paths; require independent human/oracle promotion | Dylan/maintainers | human gate |
| TM-10 | Dependency or GitHub Action compromise | Build or release tampering | Lock dependencies, pin actions, review changes, scan secrets, and retain provenance | maintainers | blocking for v1 qualification |
| TM-11 | Secret leakage through reports/artifacts | Credential or sensitive-data disclosure | Secret scanning, restricted fixtures, no real health data, and artifact review | maintainers | blocking if detected |
| TM-12 | Adapter-specific behavior treated as normative | Portability or semantic overclaim | Isolate adapters and record projection loss; core contracts remain platform-neutral | maintainers | controlled; adapter evidence remains optional |
| TM-13 | Unbounded diagnostic or report output | Disk exhaustion or log injection | Bound output, use structured serialization, and test pathological diagnostics | maintainers | open; qualification required |
| TM-14 | Release/tag substitution or artifact mismatch | Consumers install unreviewed bytes | Immutable reviewed commit, checksums, SBOM, provenance, and independent clean-build comparison | release owner | blocking until release evidence passes |

## Required verification sequence

1. Validate schemas and positive/negative examples.
2. Run deterministic unit and integration tests.
3. Run bounded property, hostile-input, and resource-limit tests.
4. Scan source, dependencies, workflows, and generated artifacts.
5. Build twice from clean environments and compare permitted differences.
6. Record hosted checks, external evidence, and human decisions separately.

The register is intentionally conservative: a documented mitigation is not a
passing result until the corresponding test or hosted evidence exists.

# edithatogo Repository Boundaries

Last checked: 2026-07-14.

This document limits which `edithatogo` repositories are in scope for the next-generation rules/process roadmap. It is intentionally conservative: a repository enters active scope only when a track has a named consumer, a concrete integration surface, and repo-local evidence to support the work.

## Boundary Rules

- Do not modify another `edithatogo` repository from this repo unless a conductor track names the target repo, exact path, and submission/PR boundary.
- Cross-repo work starts staged under `external/<repo>/` in this repository unless a track explicitly says to work in the external checkout.
- Upstream PR creation, GitHub issue submission, and merge actions are `[HUMAN]` or authenticated-maintainer gates. Agents may prepare, push where authorized, monitor CI, and apply review fixes.
- Do not promote PIC as a standard merely because a repository is adjacent. Promotion requires concrete consumer adoption or maintainer feedback.

## Currently Relevant

| Repository | Relevance | Boundary |
|---|---|---|
| `edithatogo/rac-conformance` | Primary roadmap, contracts, harnesses, studies, papers, and conductor coordination. | All roadmap planning lives here first. |
| `edithatogo/foi-o` | First active PIC consumer and process-heavy proof for OIA statutory-clock rules; now planning versioned NZ empirical and Australian jurisdiction profiles. | Relevant for OIA rules, fixture/trace integration, optional PIC-compatible profile artifacts, release evidence, and the paper-update trigger. FOI-O remains authoritative for its profile design and does not depend on PIC at runtime. |
| `edithatogo/foi-process` | Deterministic FOI event sourcing, replay, projection, OCEL/process-mining integration, and operational evidence. | Relevant as an implementation consumer and evidence source for the FOI compatibility profile. FOI-O remains the semantic authority; foi-process is not the domain-neutral mapping repository and never becomes a runtime dependency of `rac-conformance`. Citation/release work remains tracked in `foi_process_citation_mirroring_20260714`. |
| `edithatogo/legislation` | Jurisdiction-neutral legal-source manifests for NZ and Australian source packs. | Relevant for pinned, bitemporal legal-source identifiers, versions, rights, and digests. It supplies evidence manifests, not runtime legal decisions. |
| `edithatogo/rulespec-nz` | Public NZ RuleSpec corpus used for Axiom validation slices. | Relevant for PIC fixture mappings and Axiom/RuleSpec differential harness work. Do not treat as a general source of legal truth without source assertions. |
| `edithatogo/axiom-rules-engine` | Runtime surface for RuleSpec execution and traces. | Relevant for harness integration, trace/export behavior, and upstream issue/PR feedback. |
| `edithatogo/fyi-archive` | Immutable source corpus backing `foi-o` NZ and Australian process evidence. | Relevant for public-example manifests, process-state evidence, regression candidates, and empirical sampling. Derived candidates must not overwrite raw archive records. |
| `edithatogo/fyi-cli` | Operational companion to FOI/FYI workflows. | Relevant only if a track needs user-facing request workflow or local operator proof. |
| `edithatogo/corpus-legislation-nz` | NZ legislation corpus source that may support verified source assertions. | Relevant for source retrieval/citation support, not for runtime legal decisions. |
| `edithatogo/nlp-policy-nz` | Ontology-pinned extraction consumer for the versioned FOI-O contract. | Relevant for candidate extraction and delta evaluation only; cannot certify legal mappings, gold fixtures, or outcomes. |

## Potentially Relevant With A Named Consumer

| Repository | Possible Use | Entry Condition |
|---|---|---|
| Proposed `edithatogo/process-mappings` | Standalone home for source-backed process profiles, jurisdiction overlays, synthetic candidate scenarios, and optional platform adapters. | Incubate only under `subrepos/process-mappings/` through #50. Create/cut over the remote only after the human gate, extraction rehearsal, standalone CI, governance, and single-source-of-truth checks pass. |
| `edithatogo/corpus-nz-hansard` | Legislative debate/background corpus. | A track needs legislative-history context; not for controlling rule assertions. |
| `edithatogo/corpus-cases-medilegal-nz` | Tribunal/case-law style evidence patterns. | `adverse_incident_open_disclosure_20260714` identifies a public, controlling adjudication-pattern question that policy and legislation do not resolve; case material remains interpretation evidence, not a runtime oracle. |
| `edithatogo/reimbursement-atlas` | Health-funding policy calculations and evidence-readiness patterns. | `health_technology_pathways_20260714` identifies an exact reusable source, evidence, or comparison artifact and records provenance; do not duplicate its product scope here. |
| `edithatogo/mchs` | IHACPA/NWAU/microcosting rules and connector work. | `health_technology_pathways_20260714` or `camunda_portability_20260714` identifies an exact service-funding or orchestration consumer; no general code sharing by adjacency. |
| `edithatogo/gtpcnz` | Primary-care funding architecture model. | A track targets Aotearoa funding rules or policy-simulation evidence. |
| `edithatogo/healthpoint-rs` | FHIR/API service-boundary patterns. | A track needs health API integration or service-boundary lessons. |
| `edithatogo/api-standards` | API governance precedent. | A track defines service/API profile for PIC rule runners. |
| `edithatogo/sourceright` | Citation/reference verification infrastructure. | A publication or source-assertion track needs automated citation checking. |
| `edithatogo/fe-reader` | Document intake, local proof, and evidence packaging patterns. | A source-ingestion track needs PDF/document pipeline proof. |
| `edithatogo/UOGTO` | Ontology governance lessons. | Only relevant for comparing against ontology-heavy approaches; do not import its ontology into PIC by default. |
| `edithatogo/kairos`, `edithatogo/voiage`, `edithatogo/innovate` | Simulation/value-of-information/diffusion tooling. | Only relevant if the roadmap expands into policy simulation or adoption modeling. |
| `edithatogo/sm-govt-nz`, `edithatogo/open_social_data` | Government communications/social-data ingestion. | Only relevant for dissemination or policy communication analytics. |

## Not Relevant To This Roadmap By Default

| Repository | Reason |
|---|---|
| `edithatogo/substack-cli-ts` | Publication tooling only; not a rules/process consumer. |
| `edithatogo/authentext` | Text style tooling; not a conformance or rule-coupling surface. |
| `edithatogo/michelin-nz` | Domain is unrelated to public-benefit/statutory rule interchange. |
| `edithatogo/apfs-rs` | Filesystem implementation; unrelated. |
| `edithatogo/hathi-nz` | Cultural/text corpus; unrelated unless a future source-corpus track explicitly names it. |
| `edithatogo/unofficial_formslibrary` | Health form library; not relevant unless a health-process rules track is created. |
| `edithatogo/dnz` | Private/unknown purpose from available metadata; treat as out of scope until explicitly described. |
| `edithatogo/sm-govt-nz` | Out of scope for rule validation unless a dissemination/communications track names it. |

## Current External Non-edithatogo Targets

These are not `edithatogo` repositories but remain relevant to the roadmap:

- `PolicyEngine/policyengine-us`, `PolicyEngine/policyengine-core`, and `policyengine-taxsim`.
- `Research-Division/policy-rules-database`.
- `openfisca-core` and selected OpenFisca country packages.
- `TheAxiomFoundation/rulespec-nz` and `TheAxiomFoundation/axiom-rules-engine`.
- DBN Rules as Code Community of Practice.
- Alaveteli/mySociety.
- Docassemble.
- CiviForm.
- Camunda 8, limited to the optional process-profile portability adapter and
  deterministic test surface in `camunda_portability_20260714`.
- Official health authorities used as source owners, including Te Tāhū Hauora,
  HDC, Medsafe, Pharmac, TGA, PBAC/PBS, MSAC/MBS, NICE/MHRA, and FDA. These are
  evidence sources or external authorities, not presumed software adopters.

# RaC Conformance v1.0 Evidence and Maturity Roadmap

Status: Draft roadmap; implementation is governed by the linked Conductor tracks.

GitHub programme issue: [#38](https://github.com/edithatogo/rac-conformance/issues/38).

## Objective

Release RaC Conformance 1.0 only after its contracts are stable, independently
implementable, secure to consume, and proven across materially different rules
and process domains. More examples alone do not establish maturity.

## Release thesis

PIC remains a platform-neutral interchange and conformance layer. FOI-O remains
the first process-heavy consumer. The next evidence programme adds:

1. a normative process profile that can be implemented without FOI-O or BPMN;
2. a separately governed process-mappings repository for source-backed domain
   profiles and optional platform adapters;
3. an adverse-incident and open-disclosure demonstrator combining policy, law,
   human judgement, national guidance, and regional implementation;
4. a regulator-to-payer pathway comparison that preserves institutional roles;
5. a Camunda adapter proving that the process profile is portable to an
   enterprise orchestration platform;
6. engineering, security, compatibility, and release hardening; and
7. validation by at least one implementation outside repositories controlled by
   the project maintainer.

## Repository architecture

- `rac-conformance` owns normative PIC contracts, validators, conformance
  harnesses, qualification, and release evidence.
- `process-mappings` is incubated under `subrepos/process-mappings/` and is the
  proposed home for source-backed profiles, jurisdiction overlays, synthetic
  candidate scenarios, and optional platform adapters.
- `foi-o` owns FOI semantics and jurisdiction profiles.
- `foi-process` owns deterministic FOI event/replay/OCEL/process-intelligence
  implementation and supplies operational evidence to the FOI compatibility
  profile.

The incubator does not become a standalone canonical repository until the human
cutover gate in [#50](https://github.com/edithatogo/rac-conformance/issues/50).
After extraction, two writable sources of truth are prohibited.

## Authority boundaries

The health-technology study MUST NOT treat unlike authorities as equivalents:

| Function | Aotearoa New Zealand | Australia | United Kingdom | United States |
|---|---|---|---|---|
| Market authorisation | Medsafe | TGA | MHRA | FDA |
| Medicine funding / HTA | Pharmac | PBAC / PBS | NICE | Payer-specific; not FDA |
| Service or codependent-technology funding | Separate NZ funding routes | MSAC / MBS | NICE programmes as applicable | Payer-specific |
| Individual access exceptions | Pharmac NPPA / restriction waivers | PBS restriction and other applicable pathways | NHS arrangements | Payer-specific |
| Post-market safety | Medsafe | TGA | MHRA | FDA |

MBS is not a medicines approval system. FDA is not a payer. The study models
handoffs and differences between these functions rather than forcing them into a
single linear approval model.

## Health-domain safety boundary

- No runtime AI may classify harm, determine disclosure obligations, approve a
  medicine, assess cost effectiveness, or decide eligibility or funding.
- Clinical, legal, ethical, and funding judgements remain explicit human tasks.
- Executable rules may validate inputs, calculate published clocks, evaluate
  source-backed deterministic criteria, and route cases to human review.
- Only public or appropriately licensed source material and synthetic cases may
  be committed. No identifiable incident, patient, applicant, or commercial-in-
  confidence data may enter fixtures or traces.
- Every assertion records authority, jurisdiction, effective date, source URL,
  source digest where feasible, assertion status, and reviewer state.

## Initial official source anchors

These sources establish that the proposed studies have accessible primary or
official process material. Implementing tracks must pin exact versions and may
replace these discovery links with more controlling sources.

### Adverse incidents and open disclosure

- Te Tāhū Hauora: [Healing, learning and improving from harm](https://www.hqsc.govt.nz/our-work/system-safety/healing-learning-and-improving-from-harm/)
- Health and Disability Commissioner: [Guidance on open disclosure policies](https://www.hdc.org.nz/making-a-complaint/complaint-process/guidance-on-open-disclosure-policies/)
- Australian Commission on Safety and Quality in Health Care: [Open disclosure](https://www.safetyandquality.gov.au/clinical-topics/open-disclosure)
- NSW Health: [Incident management, complaints, and open-disclosure legal compendium](https://www.health.nsw.gov.au/legislation/Pages/incident-management-complaints.aspx)
- NSW Clinical Excellence Commission: [Open disclosure process](https://cec.health.nsw.gov.au/Review-incidents/open-disclosure/open-disclosure-process)

### Medicine regulation, HTA, and funding

- Medsafe: [Evaluation and approval process](https://www.medsafe.govt.nz/Consumers/Safety-of-Medicines/medsafe-evaluation-process.asp)
- Pharmac: [Medicine funding application journey](https://pharmac.govt.nz/assets/Uploads/Journey-of-a-medicine-funding-application.pdf)
- Australian PBS: [Procedure guidance for listing medicines](https://www.pbs.gov.au/pbs/industry/listing/listing-steps)
- Australian Department of Health: [HTA for government subsidy](https://www.health.gov.au/topics/health-technologies-and-digital-health/health-technology-assessments/for-subsidy)
- NICE: [Technology appraisal and highly specialised technologies manual](https://www.nice.org.uk/process/pmg36)
- FDA: [Drug review process](https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review)

### Camunda portability

- Camunda: [BPMN, DMN, and FEEL](https://docs.camunda.io/docs/components/concepts/bpmn-dmn-feel/)
- Camunda: [Camunda Process Test](https://docs.camunda.io/docs/apis-tools/testing/getting-started/)
- Camunda: [Process instance migration](https://docs.camunda.io/docs/components/concepts/process-instance-migration/)

The current source review supports three design decisions: open disclosure is a
continuing human communication and learning process; regulator approval and
public funding are separate authority chains; and Camunda can test orchestration,
timers, incidents, and migration but cannot establish legal or policy correctness.

## Cross-domain health handoff

The two health demonstrators remain separate authority and data domains, but may
share a narrowly typed post-market safety handoff. A public, aggregate, or
appropriately de-identified safety signal may reference an adverse-event learning
artifact and initiate a regulator-monitoring, HTA-reassessment, restriction, or
human-review event where an official source supports that route.

The handoff MUST NOT carry patient-level incident data, infer causation, infer a
regulatory or funding outcome, or treat a local disclosure process as evidence
that a medicine is unsafe. It records provenance, permitted purpose, aggregation
state, source authority, applicable jurisdiction, and human review status.

## Version gates

### v0.3 - Process profile foundation

- Platform-neutral process profile and source-assertion contract.
- FOI-O mapped as the compatibility baseline.
- Adverse-incident and health-technology source packs scoped.

### v0.4 - Cross-domain evidence

- Adverse-incident/open-disclosure demonstrator with synthetic fixtures.
- Regulator-to-payer authority matrix and at least two executable jurisdiction
  slices using one approved comparison case.
- Human certification of controlling source assertions and interpretation
  boundaries.

### v0.5 - Platform portability

- Camunda 8 adapter, deterministic process tests, timer tests, trace projection,
  and version-migration tests.
- Camunda artifacts remain optional and do not become PIC dependencies.

### v0.9 - Release candidate hardening

- Threat model, hostile-input tests, property/fuzz/mutation testing, performance
  budgets, compatibility matrix, SBOM, reproducible build evidence, and migration
  rehearsals.
- At least three maintained consumers across at least two domain classes, with
  at least one consumer outside maintainer-controlled repositories.

### v1.0 - Stable release

- Normative contract freeze and documented support/deprecation policy.
- All release-candidate gates independently evidenced.
- Human release certification, signed release artifacts where available, green
  required GitHub Actions, and publication of the compatibility matrix.

## Track dependency graph

1. `v1_foundation_20260714` ([#39](https://github.com/edithatogo/rac-conformance/issues/39))
2. `process_mappings_repository_20260714` ([#50](https://github.com/edithatogo/rac-conformance/issues/50)) depends on 1 and establishes the profile implementation home
3. `pic_process_profile_20260714` ([#40](https://github.com/edithatogo/rac-conformance/issues/40)) depends on 1 and uses the home established by 2
4. `adverse_incident_open_disclosure_20260714` ([#41](https://github.com/edithatogo/rac-conformance/issues/41)) depends on 3
5. `health_technology_pathways_20260714` ([#42](https://github.com/edithatogo/rac-conformance/issues/42)) depends on 3
6. `camunda_portability_20260714` ([#43](https://github.com/edithatogo/rac-conformance/issues/43)) depends on 3 and one certified demonstrator
7. `v1_engineering_hardening_20260714` ([#44](https://github.com/edithatogo/rac-conformance/issues/44)) depends on 3 and may run alongside 4-6
8. `v1_independent_validation_20260714` ([#45](https://github.com/edithatogo/rac-conformance/issues/45)) depends on stable release-candidate
   artifacts from 4-7 and complements `external_adoption_20260711`
9. `v1_release_20260714` ([#46](https://github.com/edithatogo/rac-conformance/issues/46)) depends on 1-8 and all applicable human/external gates

## Evidence and publication posture

The adverse-incident and medicine-pathway work are comparative studies, not
legal or clinical decision tools. Findings MUST separate observed source facts,
project interpretations, executable behavior, unresolved exceptions, and human
certification. A paper may be prepared after the evidence is stable, but paper
submission is not evidence of interoperability and remains a separate human gate.

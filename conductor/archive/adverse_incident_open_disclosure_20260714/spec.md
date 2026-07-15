# Adverse-Incident Management and Open Disclosure

Status: Draft | Consumed-by: PIC process-profile study, future Camunda demonstrator

## Overview

Use adverse-incident management and open disclosure as the second process-heavy
domain. It combines legal rights, professional and ethical duties, national
policy, regional implementation, local procedures, human judgement, review,
learning, and communication. The study begins with Aotearoa New Zealand and an
Australian national/NSW comparison because current official sources expose both
common principles and jurisdictional implementation variation.

Depends on: `pic_process_profile_20260714` Phase 2.

Implementation home: source manifests, candidate mappings, and synthetic
scenarios live under `subrepos/process-mappings/profiles/adverse-incidents/`.
Normative PIC schemas and conformance behavior remain in `rac-conformance`.

## Primary Source Spine

- Te Tāhū Hauora, *Healing, learning and improving from harm: National adverse
  events policy 2023* and current user guidance.
- Health and Disability Commissioner guidance on open-disclosure policies and
  applicable Code rights.
- Australian Commission on Safety and Quality in Health Care, *Australian Open
  Disclosure Framework 2026* and Clinical Governance Standard.
- NSW Health incident-management and open-disclosure policy directives and
  Clinical Excellence Commission process guidance.

Each source must be pinned by URL, title, issuing authority, effective/review
date, retrieval time, and digest where licensing and access permit.

## Functional Requirements

1. Define a source-backed lifecycle covering detection, immediate response,
   internal notification, human severity/reportability assessment, consumer and
   whānau communication, review, external reporting where applicable, learning
   actions, follow-up, and closure.
2. Separate legal obligation, national policy, regional policy, local procedure,
   professional guidance, and project interpretation.
3. Model near miss, harm, delayed recognition, disputed facts, parallel complaint,
   and unavailable-source exception cases.
4. Keep harm classification, disclosure content, apology, clinical causation,
   reportability, and final closure as human-certified tasks unless an exact
   deterministic published rule applies.
5. Produce only synthetic de-identified fixtures and traces.
6. Compare national consistency claims with regional implementation without
   treating policy variation as error by default.
7. Define an optional privacy-preserving post-market safety-signal output for
   cross-domain research. It may contain public or appropriately de-identified
   aggregate provenance but never patient-level incident content or inferred
   product causation.

## Non-Functional Requirements

- No patient, staff, complainant, or organisation-identifiable data.
- No clinical advice, legal advice, or automated disclosure decision.
- Māori data sovereignty, cultural safety, consumer/whānau participation, and
  Aboriginal and Torres Strait Islander cultural-safety requirements must be
  represented as governance and human-workflow obligations, not reduced to
  boolean claims of compliance.
- Every derived assertion retains provenance and review state.

## Acceptance Criteria

- A machine-readable authority matrix and source ledger cover all modeled steps.
- Synthetic fixtures exercise at least the six required exception/pathway cases.
- The resolver fails closed where authority, effective date, or local policy is
  missing or conflicting.
- Any cross-domain safety handoff validates permitted purpose, aggregation state,
  jurisdiction, authority, and human review before it can be consumed.
- Human reviewers see only contested assertions, interpretive mappings, and
  exception cases.
- `make check` and process-profile validation pass.

## Out of Scope

- Clinical causation analysis or severity scoring automation.
- Evaluating real incidents or organisational compliance.
- Replacing incident-management, complaints, insurer, regulator, or clinical
  record systems.
- Publishing personal or confidential evidence.
- Making this profile, rather than the controlling authority, a source of law,
  policy, clinical judgement, or organisational compliance.

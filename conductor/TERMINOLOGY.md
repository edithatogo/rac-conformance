# Governance Terminology

## Analyst

An **analyst** is the accountable reviewer who evaluates source assertions,
fixture provenance, interpretation boundaries, release risks, or external
evidence. An analyst may be Dylan or another explicitly authorized reviewer;
the identity and scope of the analyst must be recorded for every certification.

## Compatibility markers

`[HUMAN]`, `human-approved`, and `pending_human` are existing machine-facing
control markers and schema values. They remain unchanged for compatibility and
must not be replaced by prose-only aliases. New protocol prose should use
**analyst**, **analyst review**, and **analyst certification**.

The terminology change does not transfer authority to an agent, remove Dylan's
approval boundary, or allow an analyst to promote an agent-generated oracle
without independent source and provenance review.

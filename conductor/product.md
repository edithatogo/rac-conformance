# Initial Concept

Create exchange/interchange formats and tooling for Rules-as-Code ecosystems (OpenFisca, PolicyEngine, Axiom, process platforms) that they could adopt or interoperate with — abstracting policy content, rules, parameters, processes, tests, traces, and semantic metadata from any one engine. Not a replacement for any engine. Originally conceived as "RaCX — Rules-as-Code Exchange Superset"; re-scoped after independent review (see `../views/06` and `../views/07`).

# Product Definition

## What this project is

An **evidence-first policy interchange and conformance program**. It produces:

1. **Interchange artifact contracts** (small, versioned, plain-JSON-first): concept crosswalks, temporal parameters, test fixtures, decision traces, and shared missingness/epistemic-status semantics.
2. **Working consumers of those contracts** inside existing open-source projects: foi-o (NZ Official Information Act process pipeline), PolicyEngine/Axiom, OpenFisca.
3. **Empirical findings**: a cross-engine divergence study for US benefits rules (policyengine-us vs Atlanta Fed Policy Rules Database), and a companion paper demonstrating typed rule/process coupling across a process-heavy domain (OIA) and a rules-heavy domain (tax-benefit).

A standard may be *extracted* from these working exchanges later. It is explicitly not the first deliverable.

## What this project is not

- Not a rules engine, not a replacement for OpenFisca/PolicyEngine/Axiom.
- Not a universal ontology or "superset" over existing standards.
- Not a system that makes legal decisions with AI at runtime.
- Not (yet) a standards proposal — no spec is promoted externally until it has at least one external consumer.

## Users and beneficiaries

- **Primary (near-term):** Dylan, as maintainer of foi-o and contributor to PolicyEngine/Axiom — the first consumer of every contract.
- **Secondary:** maintainers of PolicyEngine, Axiom, OpenFisca (receive validation harnesses, converters, trace contracts, bug reports from divergence studies).
- **Tertiary:** the Georgetown Digital Benefits Network Rules-as-Code Community of Practice; policy-simulation researchers; process-platform maintainers (Alaveteli, Docassemble, CiviForm).

## Goals (ordered)

1. Ship contracts v0.1 with a reference validator and a real consumer (foi-o's OIA rules module).
2. Land at least three accepted upstream contributions (issues or PRs) in PolicyEngine/Axiom/OpenFisca that implement or consume the contracts.
3. Publish the SNAP divergence study with at least one previously unknown, maintainer-acknowledged discrepancy.
4. Publish the rules/process coupling companion paper (arXiv; target International Journal of Microsimulation or equivalent).
5. Only after 1–4: assess whether to formalize the contracts as a community standard via the DBN CoP.

## Current maturity phase

The original goals above established the evidence-first 0.x programme. The v1
programme is defined in `V1_ROADMAP.md` and MUST preserve that sequencing. It
adds a platform-neutral process profile, adverse-incident/open-disclosure and
medicine-regulatory/payer pathway evidence, an optional Camunda portability
adapter, engineering hardening, and independent implementation validation.

RaC Conformance 1.0 is a compatibility and evidence commitment, not a claim that
the project is a legal, clinical, funding, or standards authority. General
release requires at least one qualifying implementation outside repositories
controlled by the maintainer.

## Success metrics

- An external maintainer merges a contribution that consumes a contract from this repo.
- The divergence study is cited or triggers at least one upstream fix.
- foi-o's OIA rule module runs in its CI against contract-format fixtures with traces.

## Key strategic insights (from the reviews)

- **The harness is the product**: in an agentic world translation is cheap and verification is scarce; fixtures, traces, and differential conformance are the durable value.
- **Domain complementarity**: OIA is process-heavy/rules-light; tax-benefit is rules-heavy/process-light. The same artifact set instantiated in both is the empirical form of the "superset" claim.
- **Couple through identifiers, never through embedding**: rules, evidence, process, and evaluation artifacts change at different cadences and are owned by different institutions.

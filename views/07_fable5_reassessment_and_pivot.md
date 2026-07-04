# Fable 5 reassessment after Dylan's answers (2026-07-04)

This document records the pivot from "RaCX as a proposed standard" to "evidence-first conformance work embedded in real repos". It supersedes the strategy implied by `project_repo_racx/` (now a design notebook — see `project_repo_racx/STATUS.md`).

## 1. What Dylan's answers changed

No consumer, no concrete problem, no pilot pair, no governance plan, no appetite for standards-body engagement. That rules out the standards path: publishing a spec on arXiv and hoping for adoption has close to a zero historical hit rate. Publishing **findings** is a different matter. The project is therefore re-sequenced:

> **evidence → adoption → specification** (not specification → adoption → evidence)

## 2. Findings from public data (verified 2026-07-04)

### 2.1 Differential conformance already exists inside PolicyEngine — bilaterally, for tax

- PolicyEngine maintains `policyengine-taxsim`, a TAXSIM-35 emulator + comparison tool under an MOU with NBER (Feenberg/Poterba). Side-by-side mismatch analysis, $15 tolerance, YAML test generation, dashboard.
  - https://github.com/PolicyEngine/policyengine-taxsim
  - https://policyengine.github.io/policyengine-us/validation/taxsim.html
  - https://www.policyengine.org/us/research/policyengine-nber-mou-taxsim
- Their own writeup: validation "identified opportunities to improve how both TAXSIM and PolicyEngine encode complex tax laws" — i.e. **differential testing between independent encodings of the same law finds real bugs in both engines. The core thesis is already proven.**
- PolicyEngine's model page lists ~20 "peer" models (incl. Atlanta Fed PRD, Tax-Calculator, TRIM3, mRelief, BenefitKitchen).

**Implication:** "engines should compare outputs" is not a novel pitch to PolicyEngine. What is open: it is bilateral and tax-only. No engine-neutral fixture format, no shared trace contract, nothing for **benefits programs**, where independent encodings disagree far more.

### 2.2 The demand that "doesn't exist" is documented at Georgetown

- The Beeck Center Digital Benefits Network runs a **Rules as Code Community of Practice** (government, nonprofit, academic, private practitioners). Their published cross-sector insights report states practitioners expressed **"willingness to collaborate on an open standard for writing rules and developing a shared code library."**
  - https://beeckcenter.georgetown.edu/projects/digital-benefits-network/
  - https://digitalgovernmenthub.org/publications/cross-sector-insights-from-the-rules-as-code-community-of-practice/
- They ran the Policy2Code Prototyping Challenge and published *AI-Powered Rules as Code: Experiments with Public Benefits Policy* (March 2025), with a documented open problem: **how to verify AI-translated policy rules.** That is this project's conformance harness, wanted by name.
- Contact: rulesascode@georgetown.edu (email list + roundtables — engagement cost is one email, not a standards body).

### 2.3 Candidate pilot pairs (best first)

1. **US SNAP: `policyengine-us` vs Atlanta Fed Policy Rules Database** (https://github.com/Research-Division/policy-rules-database). Both open, independently maintained (Python vs R), federal + state variation, no published systematic divergence study. Strongest candidate: feasible solo, novel, squarely in DBN territory.
2. EITC/CTC three-way: PolicyEngine vs TAXSIM vs PSL Tax-Calculator (partially covered already; good tooling calibration).
3. UK: PolicyEngine-UK vs UKMOD (EUROMOD lineage; research-access friction).
4. France: OpenFisca-France vs LexImpact (language/context overhead).

### 2.4 Admin-burden partners

Beeck DBN; Georgetown Better Government Lab (Herd/Moynihan administrative-burden school); Code for America; Urban Institute (TRIM3/ATTIS).

## 3. What Dylan's insider position changes (second update)

Dylan works with PolicyEngine's **Axiom**, previously with PolicyEngine's older tooling and with OpenFisca tools. He can land contributions himself — he can *be* the second party. Discipline still applies: contribute things that solve the host project's existing pain; never lead with a format name.

## 4. The foi-o connection (third update — the decisive one)

Dylan's preprint repo **FOI-O NZ** (https://github.com/edithatogo/foi-o) already contains, working and tested, almost every concept the RaCX pack only sketches:

| FOI-O NZ (built) | RaCX (conceived) |
|---|---|
| Epistemic status: observed/inferred/asserted/certified/unknown | Missingness taxonomy |
| Hard-coded human certification boundary | Discretion points, "no runtime AI decisions" |
| Process/event ontology, typed states/transitions | RaCX-Process |
| Tamper-evident ledgers, quality gates | Traces, conformance |
| SHACL/SKOS/JSON Schema validation, deterministic kernels | Deterministic validators |
| One statute, real data (FYI archive), spec extracted from a working pipeline | The recommended methodology |

**Domain complementarity:** tax-benefit law is rules-heavy/process-light (hence OpenFisca/PolicyEngine ignore process); the NZ Official Information Act is process-heavy/rules-light — but its "rules" (working-day clocks, extension grounds, transfer deadlines, charging thresholds) are exactly what RaC engines handle, and currently live as bespoke kernels inside foi-o.

**The unifying demonstration:** extract the OIA statutory calculations into a declarative rule module (parameters, fixtures from Ombudsman guidance, traces, source refs) and have foi-o's process events invoke it through a typed interface. That demonstrates the entire rules/process coupling thesis on real data with a real consumer (foi-o itself), at zero adoption cost. Port the same fixture/trace contracts to one tax-benefit case via PolicyEngine/Axiom contributions, and the "superset" claim becomes an empirical result: the same artifact set instantiated in a process-heavy and a rules-heavy domain.

## 5. Revised deliverables

1. **Interchange artifact contracts** (this repo): concept crosswalk, temporal parameters, fixtures, traces + missingness/epistemic-status semantics. Small, versioned, plain-JSON-first.
2. **OIA rule extraction** (contribution to `edithatogo/foi-o`): declarative OIA clock/deadline rules + typed process→rule invocation, conforming to the contracts.
3. **Fixture converter** (tool here, PRs upstream): OpenFisca YAML tests ↔ PolicyEngine tests, bidirectional.
4. **Engine contributions** (PolicyEngine/Axiom/OpenFisca): trace export contract, missingness-semantics issue, Axiom validation harness.
5. **SNAP divergence study**: policyengine-us vs Atlanta Fed PRD; published mismatch analysis; International Journal of Microsimulation / arXiv.
6. **Community + dissemination**: DBN RaC CoP; process-side contributions (Alaveteli/mySociety first — foi-o already normalizes its states; then Docassemble, CiviForm); companion paper to the foi-o preprint.

The standard, if it ever exists, is extracted afterwards from these working exchanges. Detailed specs and plans: see `conductor/tracks/`.

## 6. On "leapfrogging with bleeding-edge AI"

AI collapses **implementation cost** (a solo researcher with agents can build a cross-engine comparison harness in weeks). It does not leapfrog **adoption, trust, or governance** — the constraints that stalled L4, Catala, and LegalRuleML. The available leapfrog: be the first to produce *empirical evidence* about cross-engine divergence in benefits rules, rather than the fifteenth person to propose a format.

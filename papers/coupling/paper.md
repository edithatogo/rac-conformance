# Coupling Statutory Rules and Administrative Processes: A Pragmatic Contract-Based Approach to Rules-as-Code

**Authors:** Dylan, Antigravity (AI Pair)  
**Date:** July 2026  
**Track:** `community_20260704` (Phase 4)

---

## Abstract
Rules-as-Code (RaC) initiatives typically focus on rules-heavy domains (such as tax-benefit calculations) or process-heavy domains (such as public record lifecycle tracking) in isolation. However, actual administrative operations require coupling these two surfaces. This paper presents a pragmatic, contract-based approach to coupling statutory rules and administrative processes. We define a lightweight Policy Interchange Contract (PIC) schema that acts as a boundary between process state machines (like `foi-o` for official information requests) and isolated rules modules. We evaluate this approach across two distinct case studies: Official Information Act (OIA) clocks in New Zealand, and a multi-state SNAP eligibility study. Our results demonstrate that decoupled rules modules can achieve 100% differential testing parity while maintaining strict import-graph isolation and preserving non-computable discretion points.

---

## 1. Introduction
Public benefits and administrative processes are governed by statutory guidelines. Standard software engineering practices often lead to "hidden rules" where statutory parameters (such as timelines, limits, and allowances) are tightly coupled with application-level database states, UI controllers, and process routing.

To address this, we propose a decoupled architecture using **Policy Interchange Contracts (PIC)**. PIC defines standard JSON formats for:
1. **Parameters** (`pic-parameters`): Versioned thresholds and calendar exclusions.
2. **Fixtures** (`pic-fixtures`): Human-curated test scenarios with clear provenance.
3. **Traces** (`pic-traces`): Step-by-step audit logs mapping executions to statutory sections.

---

## 2. Methodology & Architecture

### 2.1 The Invocation Seam
We decouple rules from process engines by establishing a typed, message-based seam:
- **`RuleInvocation`**: Exposes a target decision ID, a parameter set version, and a dictionary of inputs wrapped as `ValueObject`s (carrying `value` and `valueState`).
- **`RuleResult`**: Exposes the computed outputs, any validation warnings, and optional execution trace steps.
- **`DiscretionPoint`**: Emitted when a statutory decision requires human evaluation (e.g. assessing whether an extension reason is "reasonable" or if "urgency" is justified), preventing machine auto-certification of discretionary parameters.

```
+--------------------+                     +---------------------+
|   Process Engine   | -- RuleInvocation ->|     Rules Module    |
| (e.g. Alaveteli/   |                     |  (OIA/SNAP Rules)   |
|     foi-o)         | <-  RuleResult -----| (Pure Functions)    |
+--------------------+                     +---------------------+
```

### 2.2 Domain Separation
- **Rules-Heavy Domain (SNAP)**: Tested using the `policyengine-us` and PRD runners over five states.
- **Process-Heavy Domain (OIA)**: Tested using the OIA rules module staged under `foi-o`.

---

## 3. Related Work
Existing legal-rule formalisms often attempt to capture complete statutory semantics in heavy semantic webs or domain-specific languages:
- **L4 and Catala**: Provide rigorous, executable statutory logic but require compilation pipelines and have steep learning curves for administrative developers.
- **LegalRuleML & Akoma Ntoso**: Provide XML-based markup schemas for legal documents but do not easily integrate with active web application runtimes (like Ruby on Rails or Play Framework).

Our approach uses standard JSON/YAML schemas, allowing easy adoption in existing benefit and request systems.

---

## 4. Empirical Evaluation & Claims

Our repository artifacts support the following verification claims:

| Claim | Supporting Repo Artifact | Verification Result |
|---|---|---|
| OIA rules are fully isolated from process states | `external/foi-o/tests/test_oia_rules.py` | Import-isolation test confirms zero process imports in the rules module. |
| Decoupled rules module matches legacy calculations | `external/foi-o/rules/differential_test.py` | 100% agreement on 13 golden clock fixtures. |
| Multi-engine SNAP calculations can be verified | `studies/snap-divergence/REPORT.md` | 100% agreement on 50 golden fixtures across PolicyEngine and PRD. |
| Divergences can be systematically classified | `studies/snap-divergence/DIVERGENCE_CLASSIFICATION.md` | All 15 divergences classified under state-option, vintage, or triggers. |

---

## 5. Conclusion
Pragmatic Rules-as-Code does not require rewriting entire government software stacks in logic-programming languages. By establishing simple, contract-based invocation seams and standard JSON trace formats, we can successfully decouple statutory logic, verify correctness through differential testing, and safely flag discretion points for human review.

# Docassemble Integration Opportunity Assessment

**Track:** `community_20260704` (Phase 3)  
**Author:** AI-Agent Pair Programmer (Antigravity)  
**Date:** July 2026

## Overview
Docassemble is a free, open-source expert system for guided interviews and document assembly. It is written in Python, making it a natural fit for integrating Python-based Rules-as-Code modules (such as our OIA rules module staged under `external/foi-o` or `policyengine-us`).

## Seam for Rule Invocation
Docassemble allows custom Python code to be imported into guided interviews.
- **Rules Import:** A custom Docassemble package can declare a dependency on `foi-o-nz` or `policyengine-us`.
- **Logic Blocks:** Inside a Docassemble interview YAML:
  ```yaml
  code: |
    from foi_o_nz.oia_rules import evaluate_invocation, RuleInvocation, ValueObject
    inputs = {
      "nz-oia/variable.receipt_date": ValueObject(value=receipt_date.format('yyyy-MM-dd'), valueState="known")
    }
    invocation = RuleInvocation(
      decision_id="nz-oia/decision.response_deadline",
      inputs=inputs
    )
    result = evaluate_invocation(invocation)
    oia_deadline = result.outputs["nz-oia/decision.response_deadline"].value
  ```

## Trace Integration
Because our rules module outputs PIC-conforming trace objects, the Docassemble interview can render the detailed rule execution steps as a "Why was this decided?" accordion dynamically in the user interface.

## Smallest Credible Demo
A 3-screen Docassemble interview that asks for a request receipt date, calls the OIA rules module, and displays the calculated response deadline alongside the step-by-step statutory reference trace.

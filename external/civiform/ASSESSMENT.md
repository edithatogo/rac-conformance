# CiviForm Integration Opportunity Assessment

**Track:** `community_20260704` (Phase 3)  
**Author:** AI-Agent Pair Programmer (Antigravity)  
**Date:** July 2026

## Overview
CiviForm is an open-source, cloud-based platform that makes it easy for residents to apply for state and local government assistance programs. It is written in Java (Play Framework) and is designed to handle multiple benefits programs.

## Seam for Rule Invocation
Unlike Docassemble, CiviForm does not run Python natively. To integrate Python-based rule modules (such as SNAP eligibility or OIA clocks), we must use a service boundary:
1. **REST API Boundary:** A lightweight microservice wrapping the rule module (e.g. PolicyEngine API or a `foi-o` web server).
2. **MCP (Model Context Protocol) Boundary:** Utilizing our staged MCP server to resolve rule invocations over standard HTTP requests.

CiviForm can invoke the endpoint during form validation or eligibility pre-screening:
- CiviForm compiles form answers into a JSON request payload.
- It posts the payload to the rule runner API.
- The runner evaluates the decision rules and returns a PIC-conformant `RuleResult` with eligibility and explanation traces.

## Smallest Credible Demo
A simple mock service endpoint deploying the SNAP or OIA rules module, combined with a CiviForm custom block type that makes an outbound HTTP call to pre-screen a household for SNAP eligibility prior to application submission.

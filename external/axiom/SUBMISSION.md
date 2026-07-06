# Axiom submission packet

Track: `axiom_validation_20260706`
Stage: Phase 1 coverage selection

## Target

- Upstream repository: `TheAxiomFoundation/rulespec-nz`
- Related runtime surface: `TheAxiomFoundation/axiom-rules-engine`

## What this packet contains

- `COVERAGE_PLAN.md`
- existing harness design notes and runbook
- source-support notes for selected RuleSpec NZ slices

## Why it exists

This repo stages cross-repo work locally before any upstream submission. The
packet records the exact slices that are eligible for deterministic validation
and which slices remain smoke-only or deferred.

## Current upstream boundary

- KiwiSaver contributions and NZ Superannuation are the first validation
  candidates because they have source-backed companion evidence.
- GST, ACC earners levy, and individual income tax stay as smoke-only baseline
  slices for now.
- Broader social-security surfaces remain deferred until the source assertions
  and companion coverage are stronger.

## Draft upstream note

The next stage is to add adapter tests and fixture slices only for the selected
modules, then report any integration gap or upstream feedback separately when
the harness is beyond the selection phase.

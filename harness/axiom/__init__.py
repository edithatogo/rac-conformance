"""Axiom validation harness package."""

from __future__ import annotations

from axiom.adapter import (
    RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET,
    RULESPEC_NZ_GST_TARGET,
    RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET,
    AxiomRuleSpecAdapter,
    RuleSpecTarget,
    build_rulespec_nz_acc_earners_levy_adapter,
    build_rulespec_nz_gst_adapter,
    build_rulespec_nz_individual_income_tax_adapter,
)
from axiom.report import generate_report, write_reports
from axiom.runner import (
    AxiomCompiledArtifactExecutor,
    AxiomHarnessRunner,
    AxiomRuleSpecExecutor,
)

__all__ = [
    "RULESPEC_NZ_GST_TARGET",
    "RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET",
    "RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET",
    "AxiomCompiledArtifactExecutor",
    "AxiomHarnessRunner",
    "AxiomRuleSpecAdapter",
    "AxiomRuleSpecExecutor",
    "RuleSpecTarget",
    "build_rulespec_nz_acc_earners_levy_adapter",
    "build_rulespec_nz_gst_adapter",
    "build_rulespec_nz_individual_income_tax_adapter",
    "generate_report",
    "write_reports",
]

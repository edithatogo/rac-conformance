"""Axiom validation harness package."""

from __future__ import annotations

from axiom.adapter import (
    RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET,
    RULESPEC_NZ_GST_TARGET,
    RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET,
    RULESPEC_NZ_KIWISAVER_CONTRIBUTIONS_TARGET,
    RULESPEC_NZ_NEW_ZEALAND_SUPERANNUATION_CORE_TARGET,
    RULESPEC_NZ_NEW_ZEALAND_SUPERANNUATION_SPECIAL_RATES_TARGET,
    AxiomRuleSpecAdapter,
    RuleSpecTarget,
    build_rulespec_nz_acc_earners_levy_adapter,
    build_rulespec_nz_gst_adapter,
    build_rulespec_nz_individual_income_tax_adapter,
    build_rulespec_nz_kiwisaver_contributions_adapter,
    build_rulespec_nz_new_zealand_superannuation_core_adapter,
    build_rulespec_nz_new_zealand_superannuation_special_rates_adapter,
)
from axiom.report import generate_report, write_reports
from axiom.runner import (
    AxiomCompiledArtifactExecutor,
    AxiomHarnessRunner,
    AxiomRuleSpecExecutor,
)

__all__ = [
    "AxiomCompiledArtifactExecutor",
    "AxiomHarnessRunner",
    "AxiomRuleSpecAdapter",
    "AxiomRuleSpecExecutor",
    "RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET",
    "RULESPEC_NZ_GST_TARGET",
    "RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET",
    "RULESPEC_NZ_KIWISAVER_CONTRIBUTIONS_TARGET",
    "RULESPEC_NZ_NEW_ZEALAND_SUPERANNUATION_CORE_TARGET",
    "RULESPEC_NZ_NEW_ZEALAND_SUPERANNUATION_SPECIAL_RATES_TARGET",
    "RuleSpecTarget",
    "build_rulespec_nz_acc_earners_levy_adapter",
    "build_rulespec_nz_gst_adapter",
    "build_rulespec_nz_individual_income_tax_adapter",
    "build_rulespec_nz_kiwisaver_contributions_adapter",
    "build_rulespec_nz_new_zealand_superannuation_core_adapter",
    "build_rulespec_nz_new_zealand_superannuation_special_rates_adapter",
    "generate_report",
    "write_reports",
]

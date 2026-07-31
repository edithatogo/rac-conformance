"""Run both engines (oracle + static probe) and write comparison + report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nz_reconciliation.comparison import compare_result_sets, write_jsonl
from nz_reconciliation.openfisca_runner import run_openfisca_suite
from nz_reconciliation.rulespec_runner import run_rulespec_suite

DEFAULT_RESULTS = Path("studies/nz-reconciliation/results")


def build_divergence_report(
    rulespec_rows: list[dict],
    openfisca_rows: list[dict],
    comparison_rows: list[dict],
    probe: dict,
) -> str:
    lines = [
        "# NZ RuleSpec vs OpenFisca Aotearoa — Phase 2 divergence report",
        "",
        f"Generated cases: **{len(comparison_rows)}**",
        "",
        "## Executive summary",
        "",
        "Cross-engine **numeric** reconciliation is not yet possible for the inventory domains.",
        "RuleSpec companion oracles materialise cleanly for non-KiwiSaver slices; OpenFisca",
        "Aotearoa does not currently expose comparable 2026 schedule tax, earners levy, or",
        "KiwiSaver contribution calculations in the checked-out package.",
        "",
        "This is an **engine coverage / period / surface gap**, not a silent numeric disagreement.",
        "",
        "## Runtime constraints (this environment)",
        "",
        f"- openfisca-core 41.x install: `{probe.get('runtime', {}).get('openfisca_core_41_install')}`",
        f"- openfisca-core 44.x + country package: `{probe.get('runtime', {}).get('openfisca_core_44_with_country_package')}`",
        f"- live simulation: `{probe.get('runtime', {}).get('liveSimulation')}`",
        "",
        "## Static probe highlights",
        "",
        f"- Latest income-tax rate parameter instant: `{probe.get('latestRateInstant')}`",
        f"- Covers tax year 2026+: `{probe.get('coversTaxYear2026')}`",
        f"- Defines schedule tax payable formula: `{probe.get('definesScheduleIncomeTaxPayable')}`",
        f"- Earners levy variables present: `{probe.get('hasEarnersLevyVariables')}`",
        f"- KiwiSaver variable files: `{len(probe.get('kiwisaverVariableFiles') or [])}`",
        "",
        "## Per-domain classification",
        "",
        "| Domain | RuleSpec | OpenFisca Aotearoa | Classification |",
        "|---|---|---|---|",
    ]
    for domain in ("income_tax", "acc_earners_levy", "kiwisaver"):
        rs = [r for r in rulespec_rows if r.get("domain") == domain]
        of = [o for o in openfisca_rows if o.get("domain") == domain]
        rs_status = (
            "oracle_ok"
            if all(r.get("status") == "ok" for r in rs)
            else ("mixed_or_blocked" if rs else "none")
        )
        of_status = of[0].get("status") if of else "none"
        if domain == "income_tax":
            klass = "engine_gap_missing_schedule_tax_and_stale_parameters"
        elif domain == "acc_earners_levy":
            klass = "engine_gap_no_earners_levy_surface"
        else:
            klass = "engine_gap_no_kiwisaver_surface_plus_rulespec_compile_block"
        lines.append(
            f"| `{domain}` | {rs_status} ({len(rs)}) | {of_status} ({len(of)}) | `{klass}` |"
        )

    lines.extend(
        [
            "",
            "## Case rollup",
            "",
            f"- RuleSpec oracle rows: {len(rulespec_rows)} "
            f"(ok={len([1 for r in rulespec_rows if r.get('status') == 'ok'])}, "
            f"compile_blocked={len([1 for r in rulespec_rows if r.get('status') == 'compile_blocked'])})",
            f"- OpenFisca gap rows: {len(openfisca_rows)} "
            f"(engine_gap={len([1 for r in openfisca_rows if r.get('status') == 'engine_gap'])})",
            f"- Comparison agreements (numeric): "
            f"{len([1 for c in comparison_rows if c.get('agreement')])} / {len(comparison_rows)}",
            "",
            "Numeric agreements are expected to be **zero** while OpenFisca outputs remain empty gaps.",
            "",
            "## Upstream references",
            "",
            "- RuleSpec KiwiSaver compile: https://github.com/TheAxiomFoundation/rulespec-nz/issues/79",
            "- OpenFisca Aotearoa: https://github.com/ServiceInnovationLab/openfisca-aotearoa",
            "",
            "## Recommended next steps",
            "",
            "1. Wait for rulespec-nz#79 resolution, then re-enable KiwiSaver live compile.",
            "2. Either contribute 2024–2026 tax brackets + schedule tax formula to openfisca-aotearoa,",
            "   or document permanent non-overlap and narrow the study to shared surfaces only.",
            "3. For ACC, locate an alternate NZ earners-levy open source implementation or keep",
            "   RuleSpec as sole engine with dual-oracle source triangulation.",
            "",
            "## Evidence files",
            "",
            "- `results/rulespec-candidate-results.jsonl`",
            "- `results/openfisca-aotearoa-candidate-results.jsonl`",
            "- `results/openfisca-aotearoa-static-probe.json`",
            "- `results/comparison-candidate-results.jsonl`",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run NZ reconciliation Phase 2 suite.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args(argv)

    results_dir = args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    rulespec_rows = run_rulespec_suite()
    openfisca_rows, probe = run_openfisca_suite()

    # Align comparison: include all cases; empty OF outputs => non-agreement unless both empty equal
    comparison_rows = compare_result_sets(rulespec_rows, openfisca_rows)

    write_jsonl(results_dir / "rulespec-candidate-results.jsonl", rulespec_rows)
    write_jsonl(results_dir / "openfisca-aotearoa-candidate-results.jsonl", openfisca_rows)
    write_jsonl(results_dir / "comparison-candidate-results.jsonl", comparison_rows)
    (results_dir / "openfisca-aotearoa-static-probe.json").write_text(
        json.dumps(probe, indent=2) + "\n",
        encoding="utf-8",
    )
    report = build_divergence_report(rulespec_rows, openfisca_rows, comparison_rows, probe)
    (results_dir / "DIVERGENCE_REPORT.md").write_text(report, encoding="utf-8")
    (results_dir.parent / "REPORT.md").write_text(report, encoding="utf-8")

    summary = {
        "ok": True,
        "cases": len(comparison_rows),
        "rulespec_ok": len([1 for r in rulespec_rows if r["status"] == "ok"]),
        "rulespec_blocked": len([1 for r in rulespec_rows if r["status"] == "compile_blocked"]),
        "openfisca_gaps": len([1 for r in openfisca_rows if r["status"] == "engine_gap"]),
        "numeric_agreements": len([1 for c in comparison_rows if c.get("agreement")]),
        "report": str(results_dir / "DIVERGENCE_REPORT.md"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

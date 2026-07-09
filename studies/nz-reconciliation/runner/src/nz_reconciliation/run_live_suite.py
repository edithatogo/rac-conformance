"""Live dual-engine NZ reconciliation: RuleSpec oracles + OpenFisca live sim."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path

from nz_reconciliation.comparison import compare_pair, write_jsonl
from nz_reconciliation.openfisca_live import run_openfisca_live_suite
from nz_reconciliation.rulespec_runner import run_rulespec_suite

DEFAULT_RESULTS = Path("studies/nz-reconciliation/results")


def _primary_money(outputs: dict) -> Decimal | None:
    for payload in outputs.values():
        if isinstance(payload, dict) and payload.get("value") is not None:
            try:
                return Decimal(str(payload["value"]))
            except Exception:  # noqa: BLE001
                continue
    return None


def compare_live(
    rulespec_rows: list[dict],
    openfisca_rows: list[dict],
    *,
    tolerance: Decimal = Decimal("0.02"),
) -> list[dict]:
    """Compare rows; for multi-output cases match the primary money field."""
    of_by_id = {r["caseId"]: r for r in openfisca_rows}
    rows: list[dict] = []
    for rs in rulespec_rows:
        of = of_by_id.get(rs["caseId"])
        if of is None:
            rows.append(
                {
                    "caseId": rs["caseId"],
                    "domain": rs.get("domain"),
                    "agreement": False,
                    "classification": "missing_openfisca",
                }
            )
            continue
        # Prefer domain-specific primary keys
        domain = rs.get("domain")
        if domain == "income_tax":
            rs_out = {
                "primary": rs.get("outputs", {}).get("individual_income_tax_before_credits")
                or next(iter(rs.get("outputs", {}).values()), None)
            }
            of_out = {
                "primary": of.get("outputs", {}).get("individual_income_tax_before_credits")
            }
            pair = compare_pair(
                {**rs, "outputs": {k: v for k, v in rs_out.items() if v}},
                {**of, "outputs": {k: v for k, v in of_out.items() if v}},
                tolerance=tolerance,
            )
        elif domain == "acc_earners_levy":
            rs_val = rs.get("outputs", {}).get("acc_standard_earners_levy_including_gst")
            of_val = of.get("outputs", {}).get("acc_standard_earners_levy_including_gst")
            pair = compare_pair(
                {**rs, "outputs": {"primary": rs_val} if rs_val else {}},
                {**of, "outputs": {"primary": of_val} if of_val else {}},
                tolerance=tolerance,
            )
        elif domain == "kiwisaver":
            # Compare employee deduction if both present
            rs_val = rs.get("outputs", {}).get("kiwisaver_employee_deduction")
            of_val = of.get("outputs", {}).get("kiwisaver_employee_deduction")
            pair = compare_pair(
                {**rs, "outputs": {"primary": rs_val} if rs_val else {}},
                {**of, "outputs": {"primary": of_val} if of_val else {}},
                tolerance=tolerance,
            )
        else:
            pair = compare_pair(rs, of, tolerance=tolerance)
        rows.append(pair)
    return rows


def build_report(
    rulespec_rows: list[dict],
    openfisca_rows: list[dict],
    comparison_rows: list[dict],
) -> str:
    agreed = [r for r in comparison_rows if r.get("agreement")]
    lines = [
        "# NZ reconciliation — live dual-engine report",
        "",
        f"Cases: **{len(comparison_rows)}**",
        f"Numeric agreements (≤$0.02): **{len(agreed)}**",
        f"RuleSpec oracle ok: **{sum(1 for r in rulespec_rows if r.get('status')=='ok')}**",
        f"OpenFisca live ok: **{sum(1 for r in openfisca_rows if r.get('status')=='ok')}**",
        "",
        "## Agreements",
        "",
    ]
    if agreed:
        for row in agreed:
            lines.append(f"- `{row['caseId']}` ({row.get('domain')})")
    else:
        lines.append("_None_")
    lines.extend(["", "## Non-agreements / gaps", ""])
    for row in comparison_rows:
        if row.get("agreement"):
            continue
        lines.append(
            f"- `{row.get('caseId')}`: `{row.get('classification')}` "
            f"(rs={row.get('rulespec', {}).get('status')}, "
            f"of={row.get('openfiscaAotearoa', {}).get('status')}, "
            f"diff={row.get('valueDifference')})"
        )
    lines.extend(
        [
            "",
            "## Engines",
            "",
            "- RuleSpec: companion-test oracles (KiwiSaver compile fixed in local checkout; "
            "upstream PR https://github.com/TheAxiomFoundation/rulespec-nz/pull/80).",
            "- OpenFisca Aotearoa: live sim on PR branch "
            "https://github.com/BetterRules/openfisca-aotearoa/pull/200 "
            "(Python 3.11 + openfisca-core 41.x).",
            "",
            "## Evidence",
            "",
            "- `results/rulespec-candidate-results.jsonl`",
            "- `results/openfisca-aotearoa-live-results.jsonl`",
            "- `results/comparison-live-results.jsonl`",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Live dual-engine NZ reconciliation suite.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args(argv)
    results_dir = args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    rulespec_rows = run_rulespec_suite()
    try:
        openfisca_rows = run_openfisca_live_suite()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 2

    comparison_rows = compare_live(rulespec_rows, openfisca_rows)
    write_jsonl(results_dir / "rulespec-candidate-results.jsonl", rulespec_rows)
    write_jsonl(results_dir / "openfisca-aotearoa-live-results.jsonl", openfisca_rows)
    write_jsonl(results_dir / "comparison-live-results.jsonl", comparison_rows)
    report = build_report(rulespec_rows, openfisca_rows, comparison_rows)
    (results_dir / "LIVE_DUAL_ENGINE_REPORT.md").write_text(report, encoding="utf-8")

    summary = {
        "ok": True,
        "cases": len(comparison_rows),
        "agreements": sum(1 for r in comparison_rows if r.get("agreement")),
        "rulespec_ok": sum(1 for r in rulespec_rows if r.get("status") == "ok"),
        "openfisca_live_ok": sum(1 for r in openfisca_rows if r.get("status") == "ok"),
        "report": str(results_dir / "LIVE_DUAL_ENGINE_REPORT.md"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

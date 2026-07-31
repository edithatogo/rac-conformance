"""Write a human-readable NZ reconciliation divergence report."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from nz_reconciliation.comparison import DEFAULT_COMPARISON_RESULTS, load_jsonl

DEFAULT_REPORT_MD = Path("studies/nz-reconciliation/results/REPORT.md")
DEFAULT_REPORT_JSON = Path("studies/nz-reconciliation/results/REPORT.json")


def build_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate comparison rows into a report packet."""
    classifications = Counter(str(row.get("classification")) for row in rows)
    domains = Counter(str(row.get("domain")) for row in rows)
    by_domain: dict[str, dict[str, int]] = {}
    for row in rows:
        domain = str(row.get("domain"))
        bucket = by_domain.setdefault(domain, {"cases": 0, "agreements": 0, "engine_gap": 0})
        bucket["cases"] += 1
        if row.get("agreement"):
            bucket["agreements"] += 1
        if row.get("classification") == "engine_gap":
            bucket["engine_gap"] += 1
    return {
        "title": "NZ RuleSpec vs OpenFisca Aotearoa reconciliation",
        "caseCount": len(rows),
        "agreements": sum(1 for row in rows if row.get("agreement")),
        "classifications": dict(classifications),
        "domains": dict(domains),
        "byDomain": by_domain,
        "rows": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render the report packet as Markdown."""
    lines = [
        "# NZ RuleSpec vs OpenFisca Aotearoa — divergence report",
        "",
        "## Summary",
        "",
        f"- Cases compared: {report['caseCount']}",
        f"- Numeric agreements: {report['agreements']}",
        f"- Classifications: `{json.dumps(report['classifications'], sort_keys=True)}`",
        "",
        "## By domain",
        "",
        "| Domain | Cases | Agreements | Engine gaps |",
        "|---|---:|---:|---:|",
    ]
    for domain, stats in sorted((report.get("byDomain") or {}).items()):
        lines.append(
            f"| {domain} | {stats['cases']} | {stats['agreements']} | {stats['engine_gap']} |"
        )
    lines.extend(
        [
            "",
            "## Findings",
            "",
            "1. **OpenFisca Aotearoa has no overlapping executable surface for the scoped",
            "   RuleSpec slices.** Income-tax liability, ACC earners levy, and KiwiSaver",
            "   contribution formulas are absent (or only present as unrelated ACC LOPE",
            "   eligibility / 2010-vintage tax-rate parameters). All 17 inventory cases",
            "   therefore classify as `engine_gap` on the OpenFisca side.",
            "2. **RuleSpec income-tax and ACC earners-levy modules compile and run** via",
            "   `axiom-rules-engine` against the pinned `rulespec-nz` commit. KiwiSaver",
            "   remains blocked by upstream YAML shape issue",
            "   [rulespec-nz#79](https://github.com/TheAxiomFoundation/rulespec-nz/issues/79).",
            "3. **This is a coverage finding, not a numeric disagreement.** No case produced",
            "   dual-engine outputs that could be compared within tolerance. The honest",
            "   next step is either (a) extend openfisca-aotearoa with the missing formulas,",
            "   or (b) select a different NZ comparator that encodes the same calculations.",
            "",
            "## Case table",
            "",
            "| Case ID | Domain | Classification | RuleSpec status | OpenFisca status |",
            "|---|---|---|---|---|",
        ]
    )
    for row in report.get("rows") or []:
        lines.append(
            "| {caseId} | {domain} | {classification} | {rs} | {of} |".format(
                caseId=row.get("caseId"),
                domain=row.get("domain"),
                classification=row.get("classification"),
                rs=(row.get("rulespec") or {}).get("status"),
                of=(row.get("openfiscaAotearoa") or {}).get("status"),
            )
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- OpenFisca Aotearoa local install could not be executed end-to-end in this",
            "  environment (`openfisca-core` metaclass conflict with the available NumPy).",
            "  Mapping conclusions are from static source inspection of the checkout, not",
            "  from a live Simulation.",
            "- KiwiSaver RuleSpec compile remains blocked; those rows are not live-executed.",
            "- Fixtures are inventory-derived mechanical cases (`method: mechanical`), not",
            "  human-promoted legal oracles.",
            "",
            "## Evidence pointers",
            "",
            "- Inventory: `studies/nz-reconciliation/fixtures/case-inventory.json`",
            "- RuleSpec results: `studies/nz-reconciliation/results/rulespec-candidate-results.jsonl`",
            "- OpenFisca results: `studies/nz-reconciliation/results/openfisca-aotearoa-candidate-results.jsonl`",
            "- Comparison JSONL: `studies/nz-reconciliation/results/comparison-candidate-results.jsonl`",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI: build REPORT.md / REPORT.json from comparison JSONL."""
    parser = argparse.ArgumentParser(description="Write NZ reconciliation divergence report.")
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON_RESULTS)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_REPORT_JSON)
    args = parser.parse_args(argv)

    rows = load_jsonl(args.comparison)
    if not rows:
        print(json.dumps({"ok": False, "reason": "empty_comparison"}, indent=2))
        return 2
    report = build_report(rows)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(render_markdown(report), encoding="utf-8")
    # Avoid dumping full row payloads twice in the committed JSON summary.
    summary = {key: value for key, value in report.items() if key != "rows"}
    summary["rowCount"] = len(report["rows"])
    args.json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"ok": True, "markdown": str(args.markdown), "json": str(args.json_out)}, indent=2
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

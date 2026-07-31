"""OpenFisca Aotearoa side of NZ reconciliation (static probe + gap reporting).

Live simulation against ServiceInnovationLab/openfisca-aotearoa is currently
blocked on this workstation by dependency skew:

- Country package pins openfisca-core 41.x (pendulum 2.x fails to build on modern Python).
- openfisca-core 44.x installs but hits a metaclass conflict with the country package.

This runner therefore records deterministic *engine-gap* results from static
inspection of the checked-out parameter/variable tree, so Phase 2 comparison
and divergence reporting can proceed without inventing simulated tax figures.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from nz_reconciliation.comparison import write_jsonl
from nz_reconciliation.inventory import DEFAULT_INVENTORY, load_inventory, select_cases

DEFAULT_OUTPUT = Path(
    "studies/nz-reconciliation/results/openfisca-aotearoa-candidate-results.jsonl",
)
DEFAULT_REPO = Path(".external-repos/openfisca-aotearoa")
DEFAULT_PROBE = Path("studies/nz-reconciliation/results/openfisca-aotearoa-static-probe.json")


def probe_openfisca_tree(repo_root: Path) -> dict[str, Any]:
    """Static inventory of tax/ACC surfaces in the OpenFisca Aotearoa checkout."""
    package = repo_root / "openfisca_aotearoa"
    rate_path = package / "parameters/taxes/income_tax/individual_income_tax_rate.yaml"
    rate_doc: dict[str, Any] = {}
    latest_rate_instants: list[str] = []
    if rate_path.exists():
        rate_doc = yaml.safe_load(rate_path.read_text(encoding="utf-8")) or {}
        brackets = rate_doc.get("brackets") or []
        instants: set[str] = set()
        for bracket in brackets:
            for field in ("rate", "threshold"):
                node = bracket.get(field) or {}
                if isinstance(node, dict):
                    instants.update(str(key) for key in node)
        latest_rate_instants = sorted(instants)

    variable_files = sorted(
        str(path.relative_to(package))
        for path in (package / "variables").rglob("*.py")
        if path.is_file()
    )
    income_tax_vars = [path for path in variable_files if "income_tax" in path]
    acc_vars = [
        path for path in variable_files if "/acc/" in path or path.startswith("variables/acts/acc")
    ]
    kiwisaver_vars = [path for path in variable_files if "kiwi" in path.lower()]

    has_progressive_tax_formula = any(
        "before_credits" in path or "income_tax_payable" in path or "tax_liability" in path
        for path in income_tax_vars
    )
    # individual.py only defines residence/gross/net/taxable helpers, not schedule tax.
    individual_py = package / "variables/acts/income_tax/individual.py"
    individual_text = individual_py.read_text(encoding="utf-8") if individual_py.exists() else ""
    defines_taxable_income = "class income_tax__taxable_income" in individual_text
    defines_schedule_tax = (
        "individual_income_tax_before_credits" in individual_text
        or "income_tax__income_tax" in individual_text
    )

    return {
        "repo": str(repo_root),
        "rateParameterPath": str(rate_path.relative_to(repo_root)) if rate_path.exists() else None,
        "rateInstantCount": len(latest_rate_instants),
        "rateInstants": latest_rate_instants,
        "latestRateInstant": latest_rate_instants[-1] if latest_rate_instants else None,
        "coversTaxYear2026": any(
            instant.startswith("202") and instant >= "2024" for instant in latest_rate_instants
        ),
        "incomeTaxVariableFiles": income_tax_vars,
        "accVariableFiles": acc_vars,
        "kiwisaverVariableFiles": kiwisaver_vars,
        "definesTaxableIncomeHelper": defines_taxable_income,
        "definesScheduleIncomeTaxPayable": defines_schedule_tax or has_progressive_tax_formula,
        "hasEarnersLevyVariables": any("levy" in path.lower() for path in acc_vars),
        "runtime": {
            "openfisca_core_41_install": "blocked_pendulum_build_on_modern_python",
            "openfisca_core_44_with_country_package": "blocked_metaclass_conflict",
            "liveSimulation": "unavailable",
        },
    }


def materialise_openfisca_result(case: dict[str, Any], probe: dict[str, Any]) -> dict[str, Any]:
    """Emit an OpenFisca-side result row with explicit gap classification."""
    domain = case.get("domain")
    gap_reason: str
    outputs: dict[str, Any] = {}

    if domain == "income_tax":
        if not probe.get("definesScheduleIncomeTaxPayable"):
            gap_reason = (
                "openfisca-aotearoa exposes income_tax__taxable_income helpers and a "
                f"parameter scale last instant {probe.get('latestRateInstant')!r}, but no "
                "schedule-1 tax-payable formula comparable to RuleSpec "
                "individual_income_tax_before_credits."
            )
        elif not probe.get("coversTaxYear2026"):
            gap_reason = "parameter scale does not include 2026 tax-year instants required by inventory cases."
        else:
            gap_reason = "mapping incomplete"
        status = "engine_gap"
    elif domain == "acc_earners_levy":
        gap_reason = (
            "no earners-levy variables found under openfisca_aotearoa/variables "
            f"(ACC modules present: {len(probe.get('accVariableFiles') or [])}; "
            "they cover LOPE/weekly compensation, not earners levy)."
        )
        status = "engine_gap"
    elif domain == "kiwisaver":
        gap_reason = "no KiwiSaver contribution variables found in openfisca-aotearoa checkout."
        status = "engine_gap"
    else:
        gap_reason = f"unknown domain {domain!r}"
        status = "engine_gap"

    return {
        "caseId": case["caseId"],
        "domain": domain,
        "engine": "openfisca-aotearoa",
        "status": status,
        "method": "static-probe",
        "period": case.get("period"),
        "outputs": outputs,
        "gapReason": gap_reason,
        "probe": {
            "latestRateInstant": probe.get("latestRateInstant"),
            "coversTaxYear2026": probe.get("coversTaxYear2026"),
            "definesScheduleIncomeTaxPayable": probe.get("definesScheduleIncomeTaxPayable"),
            "hasEarnersLevyVariables": probe.get("hasEarnersLevyVariables"),
            "kiwisaverVariableCount": len(probe.get("kiwisaverVariableFiles") or []),
        },
        "sourceRefs": [
            "https://github.com/ServiceInnovationLab/openfisca-aotearoa",
        ],
        "notes": gap_reason,
    }


def run_openfisca_suite(
    inventory_path: Path | None = None,
    *,
    repo_root: Path = DEFAULT_REPO,
    include_blocked: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    inventory = load_inventory(inventory_path or DEFAULT_INVENTORY)
    probe = probe_openfisca_tree(repo_root)
    cases = select_cases(inventory, include_blocked=include_blocked)
    rows = [materialise_openfisca_result(case, probe) for case in cases]
    return rows, probe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Probe OpenFisca Aotearoa and materialise gap-aware result rows.",
    )
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--probe-output", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--exclude-blocked", action="store_true")
    args = parser.parse_args(argv)

    if not args.repo.exists():
        print(json.dumps({"ok": False, "reason": f"missing repo {args.repo}"}, indent=2))
        return 2

    rows, probe = run_openfisca_suite(
        args.inventory,
        repo_root=args.repo,
        include_blocked=not args.exclude_blocked,
    )
    write_jsonl(args.output, rows)
    args.probe_output.parent.mkdir(parents=True, exist_ok=True)
    args.probe_output.write_text(json.dumps(probe, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "cases": len(rows),
                "engine_gaps": sum(1 for row in rows if row["status"] == "engine_gap"),
                "latestRateInstant": probe.get("latestRateInstant"),
                "output": str(args.output),
                "probe": str(args.probe_output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from pathlib import Path

from nz_reconciliation.inventory import load_inventory, select_cases

ROOT = Path(__file__).resolve().parents[4]
INVENTORY = ROOT / "studies/nz-reconciliation/fixtures/case-inventory.json"


def test_inventory_meets_minimum_case_target() -> None:
    inventory = load_inventory(INVENTORY)
    assert inventory["caseCount"] >= 15
    assert len(inventory["cases"]) == inventory["caseCount"]
    assert inventory["caseCount"] >= inventory["targetMinCases"]


def test_inventory_covers_required_domains() -> None:
    inventory = load_inventory(INVENTORY)
    domains = {case["domain"] for case in inventory["cases"]}
    assert domains == {"income_tax", "acc_earners_levy", "kiwisaver"}
    assert inventory["domains"]["income_tax"] >= 1
    assert inventory["domains"]["acc_earners_levy"] >= 1
    assert inventory["domains"]["kiwisaver"] >= 1


def test_select_cases_can_exclude_blocked_kiwisaver() -> None:
    inventory = load_inventory(INVENTORY)
    runnable = select_cases(inventory, include_blocked=False)
    assert all(
        case["domain"] != "kiwisaver" or case["rulespec"]["compileStatus"] == "ok"
        for case in runnable
    )
    assert all(case["rulespec"]["compileStatus"] == "ok" for case in runnable)
    assert len(runnable) >= 14  # 5 income tax + 9 ACC


def test_select_cases_domain_filter() -> None:
    inventory = load_inventory(INVENTORY)
    cases = select_cases(inventory, domains={"income_tax"})
    assert cases
    assert all(case["domain"] == "income_tax" for case in cases)

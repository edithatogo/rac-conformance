from __future__ import annotations

import json
from typing import Any

from pic_contracts.schema_utils import validator_for

from axiom import (
    AxiomRuleSpecAdapter,
    RuleSpecTarget,
    build_rulespec_nz_gst_adapter,
    generate_report,
    write_reports,
)
from axiom.runner import AxiomHarnessRunner


GST_CASE = {
    "caseId": "nz-gst/fixture.add_and_remove_gst",
    "description": "Add and remove GST using the rulespec-nz GST smoke case.",
    "period": "2026-06-16",
    "entities": {"supply": {"type": "Supply", "id": "supply:1"}},
    "inputs": {
        "nz-gst/variable.gst_exclusive_amount": {
            "value": "100.00",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-gst/variable.gst_inclusive_amount": {
            "value": "115.00",
            "valueState": "known",
            "currency": "NZD",
        },
    },
    "expected": {
        "nz-gst/decision.gst_component_from_exclusive_amount": {
            "value": "15.00",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-gst/decision.gst_inclusive_amount_from_exclusive_amount": {
            "value": "115.00",
            "valueState": "known",
            "currency": "NZD",
        },
    },
    "sourceRefs": [
        "https://github.com/TheAxiomFoundation/rulespec-nz/blob/3c6436b2ecf82dd7a7f7810a406a2695a64af33a/nz/statutes/gst/rate.test.yaml"
    ],
}


def test_rulespec_nz_gst_case_is_valid_pic_fixture_case() -> None:
    document = {
        "conformsTo": "pic-fixtures/0.1.0",
        "provenance": {
            "curator": "rulesandprocesses Track 4 Axiom harness",
            "method": "mechanical",
            "source": "rulespec-nz GST companion test",
            "interpreterOfRecord": "TheAxiomFoundation/rulespec-nz",
            "disclaimer": "Smoke fixture for harness mechanics; not a promoted legal oracle.",
        },
        "cases": [GST_CASE],
    }

    validator_for("pic-fixtures").validate(document)


def test_build_rulespec_nz_gst_compiled_execution_request() -> None:
    adapter = build_rulespec_nz_gst_adapter()

    request = adapter.build_compiled_request(GST_CASE)

    assert request["mode"] == "explain"
    assert request["dataset"]["relations"] == []
    assert request["dataset"]["inputs"] == [
        {
            "name": "nz:statutes/gst/rate#input.gst_exclusive_amount",
            "entity": "Supply",
            "entity_id": "supply:1",
            "interval": {"start": "2026-06-16", "end": "2026-06-16"},
            "value": {"kind": "decimal", "value": "100.00"},
        },
        {
            "name": "nz:statutes/gst/rate#input.gst_inclusive_amount",
            "entity": "Supply",
            "entity_id": "supply:1",
            "interval": {"start": "2026-06-16", "end": "2026-06-16"},
            "value": {"kind": "decimal", "value": "115.00"},
        },
    ]
    assert request["queries"] == [
        {
            "entity_id": "supply:1",
            "period": {
                "period_kind": "custom",
                "name": "calendar_day",
                "start": "2026-06-16",
                "end": "2026-06-16",
            },
            "outputs": [
                "nz:statutes/gst/rate#gst_component_from_exclusive_amount",
                "nz:statutes/gst/rate#gst_inclusive_amount_from_exclusive_amount",
            ],
        }
    ]


def test_runner_exact_match_with_stub_executor() -> None:
    runner = AxiomHarnessRunner(adapter=build_rulespec_nz_gst_adapter())

    def stub_executor(request: dict[str, Any]) -> dict[str, Any]:
        assert request["queries"][0]["outputs"][0].startswith("nz:statutes/gst/rate#")
        return {
            "metadata": {"requested_mode": "explain", "actual_mode": "explain"},
            "results": [
                {
                    "entity_id": "supply:1",
                    "period": request["queries"][0]["period"],
                    "outputs": {
                        "nz:statutes/gst/rate#gst_component_from_exclusive_amount": {
                            "kind": "scalar",
                            "name": "gst_component_from_exclusive_amount",
                            "id": "nz:statutes/gst/rate#gst_component_from_exclusive_amount",
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "15"},
                        },
                        "nz:statutes/gst/rate#gst_inclusive_amount_from_exclusive_amount": {
                            "kind": "scalar",
                            "name": "gst_inclusive_amount_from_exclusive_amount",
                            "id": "nz:statutes/gst/rate#gst_inclusive_amount_from_exclusive_amount",
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "115.00"},
                        },
                    },
                    "trace": {
                        "nz:statutes/gst/rate#gst_component_from_exclusive_amount": {
                            "kind": "scalar",
                            "name": "gst_component_from_exclusive_amount",
                            "id": "nz:statutes/gst/rate#gst_component_from_exclusive_amount",
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "15"},
                            "dependencies": [
                                "nz:statutes/gst/rate#input.gst_exclusive_amount",
                                "nz:statutes/gst/rate#gst_standard_rate",
                            ],
                        }
                    },
                }
            ],
        }

    result = runner.run_case(GST_CASE, executor=stub_executor)

    assert result["caseId"] == "nz-gst/fixture.add_and_remove_gst"
    assert result["status"] == "exact_match"
    assert result["mismatches"] == []
    assert result["axiom"]["outputs"] == {
        "nz-gst/decision.gst_component_from_exclusive_amount": {
            "value": "15",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-gst/decision.gst_inclusive_amount_from_exclusive_amount": {
            "value": "115.00",
            "valueState": "known",
            "currency": "NZD",
        },
    }
    assert "trace" in result["axiom"]


def test_runner_reports_output_mismatch_with_stub_executor() -> None:
    runner = AxiomHarnessRunner(adapter=build_rulespec_nz_gst_adapter())

    def stub_executor(request: dict[str, Any]) -> dict[str, Any]:
        return {
            "metadata": {"requested_mode": "explain", "actual_mode": "explain"},
            "results": [
                {
                    "entity_id": "supply:1",
                    "period": request["queries"][0]["period"],
                    "outputs": {
                        "nz:statutes/gst/rate#gst_component_from_exclusive_amount": {
                            "kind": "scalar",
                            "name": "gst_component_from_exclusive_amount",
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "14.99"},
                        }
                    },
                }
            ],
        }

    result = runner.run_case(GST_CASE, executor=stub_executor)

    assert result["status"] == "output_mismatch"
    assert result["mismatches"] == [
        "nz-gst/decision.gst_component_from_exclusive_amount: expected 15.00, got 14.99",
        "nz-gst/decision.gst_inclusive_amount_from_exclusive_amount: expected 115.00, got missing",
    ]


def test_runner_reports_adapter_failure_with_stub_executor() -> None:
    runner = AxiomHarnessRunner(adapter=build_rulespec_nz_gst_adapter())

    def failing_executor(_: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("compiled artifact missing")

    result = runner.run_case(GST_CASE, executor=failing_executor)

    assert result["status"] == "adapter_failure"
    assert result["axiom_error"] == "compiled artifact missing"
    assert result["mismatches"] == []


def test_report_generation_and_write(tmp_path) -> None:
    results = [
        {
            "caseId": "nz-gst/fixture.add_and_remove_gst",
            "status": "exact_match",
            "axiom_error": None,
            "mismatches": [],
        },
        {
            "caseId": "nz-gst/fixture.bad_amount",
            "status": "output_mismatch",
            "axiom_error": None,
            "mismatches": ["nz-gst/decision.example: expected 1, got 2"],
        },
    ]

    report = generate_report(results)
    assert "# Axiom Differential Validation Report" in report
    assert "- Exact matches: 1" in report
    assert "nz-gst/fixture.bad_amount" in report

    write_reports(results, tmp_path)
    assert (tmp_path / "report.md").read_text(encoding="utf-8") == report
    summary = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert summary["total"] == 2


def test_adapter_accepts_custom_target() -> None:
    target = RuleSpecTarget(
        repo="TheAxiomFoundation/rulespec-nz",
        repo_commit="3c6436b2ecf82dd7a7f7810a406a2695a64af33a",
        module_path="nz/statutes/gst/rate.yaml",
        test_path="nz/statutes/gst/rate.test.yaml",
        module_id="nz:statutes/gst/rate",
    )

    adapter = AxiomRuleSpecAdapter(
        target=target,
        input_id_map={"pic/variable.example": "nz:statutes/gst/rate#input.example"},
        output_id_map={"pic/decision.example": "nz:statutes/gst/rate#example"},
        entity="Supply",
        entity_id="supply:1",
    )

    assert adapter.target.module_path == "nz/statutes/gst/rate.yaml"

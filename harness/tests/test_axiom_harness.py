from __future__ import annotations

import json
from typing import Any

import pytest
from axiom import (
    AxiomRuleSpecAdapter,
    RuleSpecTarget,
    build_rulespec_nz_acc_earners_levy_adapter,
    build_rulespec_nz_gst_adapter,
    build_rulespec_nz_individual_income_tax_adapter,
    build_rulespec_nz_kiwisaver_contributions_adapter,
    build_rulespec_nz_new_zealand_superannuation_core_adapter,
    build_rulespec_nz_new_zealand_superannuation_special_rates_adapter,
    generate_report,
    write_reports,
)
from axiom.runner import AxiomHarnessRunner
from pic_contracts.schema_utils import validator_for

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


ACC_EARNERS_LEVY_CASE = {
    "caseId": "nz-acc/fixture.standard_2026_earnings_below_cap",
    "description": "ACC earners levy standard 2026 earnings below cap.",
    "period": "2026-04-01/2027-03-31",
    "entities": {"person": {"type": "Person", "id": "person:1"}},
    "inputs": {
        "nz-acc/variable.acc_earnings_for_earners_levy": {
            "value": "100000",
            "valueState": "known",
            "currency": "NZD",
        }
    },
    "expected": {
        "nz-acc/decision.acc_standard_earners_levy_excluding_gst": {
            "value": "1520",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-acc/decision.acc_standard_earners_levy_including_gst": {
            "value": "1750",
            "valueState": "known",
            "currency": "NZD",
        },
    },
    "sourceRefs": [
        "https://github.com/TheAxiomFoundation/rulespec-nz/blob/3c6436b2ecf82dd7a7f7810a406a2695a64af33a/nz/regulations/acc/earners_levy.test.yaml"
    ],
}


INDIVIDUAL_INCOME_TAX_CASE = {
    "caseId": "nz-income-tax/fixture.first_bracket_upper_bound",
    "description": "Individual income tax before credits at the first bracket upper bound.",
    "period": "2026-04-01/2027-03-31",
    "entities": {"person": {"type": "Person", "id": "person:1"}},
    "inputs": {
        "nz-income-tax/variable.taxable_income": {
            "value": "15600",
            "valueState": "known",
            "currency": "NZD",
        }
    },
    "expected": {
        "nz-income-tax/decision.individual_income_tax_before_credits": {
            "value": "1638",
            "valueState": "known",
            "currency": "NZD",
        }
    },
    "sourceRefs": [
        "https://github.com/TheAxiomFoundation/rulespec-nz/blob/3c6436b2ecf82dd7a7f7810a406a2695a64af33a/nz/statutes/income_tax/schedule_1/individual_income_tax.test.yaml"
    ],
}


KIWISAVER_CONTRIBUTIONS_CASE = {
    "caseId": "nz-kiwisaver/fixture.minimum_rates_2026",
    "description": "KiwiSaver minimum contribution rates for 2026.",
    "period": "2026-04-01/2027-03-31",
    "entities": {"person": {"type": "Person", "id": "person:1"}},
    "inputs": {
        "nz-kiwisaver/variable.kiwisaver_gross_salary_or_wages": {
            "value": "100000",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-kiwisaver/variable.kiwisaver_selected_employee_contribution_rate": {
            "value": "0.035",
            "valueState": "known",
        },
    },
    "expected": {
        "nz-kiwisaver/decision.kiwisaver_employee_minimum_contribution_rate": {
            "value": "0.035",
            "valueState": "known",
        },
        "nz-kiwisaver/decision.kiwisaver_employer_minimum_contribution_rate": {
            "value": "0.035",
            "valueState": "known",
        },
        "nz-kiwisaver/decision.kiwisaver_employee_deduction": {
            "value": "3500",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-kiwisaver/decision.kiwisaver_minimum_employer_contribution": {
            "value": "3500",
            "valueState": "known",
            "currency": "NZD",
        },
    },
}


NZ_SUPERANNUATION_CORE_CASE = {
    "caseId": "nz-superannuation/fixture.single_living_alone_meets_residence",
    "description": "New Zealand Superannuation core entitlement with living-alone rate.",
    "period": "2026-04-01/2027-03-31",
    "entities": {"person": {"type": "Person", "id": "person:1"}},
    "inputs": {
        "nz-superannuation/variable.nz_super_birth_year": {
            "value": "1959",
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_birth_month": {
            "value": "6",
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_single": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_principal_residence_is_qualifying_accommodation": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_shares_residence_with_person_at_least_adult_age": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_all_shared_adults_are_exempt_dependent_children_or_temporary_visitors": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_person_age": {
            "value": 66,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_elected_weekly_compensation_instead_of_superannuation": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_ordinarily_resident_in_new_zealand_on_application": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_overseas_application_residence_exception_applies": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_resident_present_since_age_20_total_years": {
            "value": 10,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_resident_present_since_age_20_new_zealand_years": {
            "value": 10,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_resident_present_since_age_50_total_years": {
            "value": 5,
            "valueState": "known",
        },
    },
    "expected": {
        "nz-superannuation/decision.nz_super_standard_total_time_requirement_years": {
            "value": "10",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_living_alone": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_age_requirement": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_residential_requirement": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.entitled_to_new_zealand_superannuation": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_ordinary_weekly_rate_before_tax": {
            "value": "647.37",
            "valueState": "known",
            "currency": "NZD",
        },
        "nz-superannuation/decision.nz_super_weekly_amount_before_tax": {
            "value": "647.37",
            "valueState": "known",
            "currency": "NZD",
        },
    },
}


NZ_SUPERANNUATION_SPECIAL_RATES_CASE = {
    "caseId": "nz-superannuation/fixture.hospital_reduced_rate_after_thirteen_weeks",
    "description": "NZ Super special rates when hospital reduced rate applies.",
    "period": "2026-04-01/2027-03-31",
    "entities": {"person": {"type": "Person", "id": "person:1"}},
    "inputs": {
        "nz-superannuation/variable.nz_super_receives_or_becomes_entitled": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_single": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_in_relationship": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_has_dependent_children": {
            "value": False,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_patient_in_hospital": {
            "value": True,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_hospitalisation_weeks": {
            "value": 14,
            "valueState": "known",
        },
        "nz-superannuation/variable.nz_super_residential_care_funder_pays_contracted_care": {
            "value": False,
            "valueState": "known",
        },
    },
    "expected": {
        "nz-superannuation/decision.nz_super_hospital_rate_population": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_hospital_reduced_rate_applies": {
            "value": "holds",
            "valueState": "known",
        },
        "nz-superannuation/decision.nz_super_hospital_weekly_rate_net_after_tax": {
            "value": "58.34",
            "valueState": "known",
            "currency": "NZD",
        },
    },
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


def test_build_rulespec_nz_acc_earners_levy_request() -> None:
    adapter = build_rulespec_nz_acc_earners_levy_adapter()

    request = adapter.build_compiled_request(ACC_EARNERS_LEVY_CASE)

    assert adapter.target.module_path == "nz/regulations/acc/earners_levy.yaml"
    assert request["dataset"]["inputs"] == [
        {
            "name": "nz:regulations/acc/earners_levy#input.acc_earnings_for_earners_levy",
            "entity": "Person",
            "entity_id": "person:1",
            "interval": {"start": "2026-04-01", "end": "2027-03-31"},
            "value": {"kind": "decimal", "value": "100000"},
        }
    ]
    assert request["queries"] == [
        {
            "entity_id": "person:1",
            "period": {
                "period_kind": "tax_year",
                "start": "2026-04-01",
                "end": "2027-03-31",
            },
            "outputs": [
                "nz:regulations/acc/earners_levy#acc_standard_earners_levy_excluding_gst",
                "nz:regulations/acc/earners_levy#acc_standard_earners_levy_including_gst",
            ],
        }
    ]


def test_acc_earners_levy_runner_exact_match_with_stub_executor() -> None:
    runner = AxiomHarnessRunner(adapter=build_rulespec_nz_acc_earners_levy_adapter())

    def stub_executor(request: dict[str, Any]) -> dict[str, Any]:
        assert request["queries"][0]["period"]["period_kind"] == "tax_year"
        return {
            "metadata": {"requested_mode": "explain", "actual_mode": "explain"},
            "results": [
                {
                    "entity_id": "person:1",
                    "period": request["queries"][0]["period"],
                    "outputs": {
                        "nz:regulations/acc/earners_levy#acc_standard_earners_levy_excluding_gst": {
                            "kind": "scalar",
                            "name": "acc_standard_earners_levy_excluding_gst",
                            "id": (
                                "nz:regulations/acc/earners_levy#"
                                "acc_standard_earners_levy_excluding_gst"
                            ),
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "1520.00"},
                        },
                        "nz:regulations/acc/earners_levy#acc_standard_earners_levy_including_gst": {
                            "kind": "scalar",
                            "name": "acc_standard_earners_levy_including_gst",
                            "id": (
                                "nz:regulations/acc/earners_levy#"
                                "acc_standard_earners_levy_including_gst"
                            ),
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "1750"},
                        },
                    },
                }
            ],
        }

    result = runner.run_case(ACC_EARNERS_LEVY_CASE, executor=stub_executor)

    assert result["status"] == "exact_match"
    assert result["mismatches"] == []
    assert result["target"]["module_path"] == "nz/regulations/acc/earners_levy.yaml"


def test_build_rulespec_nz_individual_income_tax_request() -> None:
    adapter = build_rulespec_nz_individual_income_tax_adapter()

    request = adapter.build_compiled_request(INDIVIDUAL_INCOME_TAX_CASE)

    assert adapter.target.module_path == "nz/statutes/income_tax/schedule_1/individual_income_tax.yaml"
    assert request["dataset"]["inputs"] == [
        {
            "name": "nz:statutes/income_tax/schedule_1/individual_income_tax#input.taxable_income",
            "entity": "Person",
            "entity_id": "person:1",
            "interval": {"start": "2026-04-01", "end": "2027-03-31"},
            "value": {"kind": "decimal", "value": "15600"},
        }
    ]
    assert request["queries"] == [
        {
            "entity_id": "person:1",
            "period": {
                "period_kind": "tax_year",
                "start": "2026-04-01",
                "end": "2027-03-31",
            },
            "outputs": [
                (
                    "nz:statutes/income_tax/schedule_1/individual_income_tax#"
                    "individual_income_tax_before_credits"
                )
            ],
        }
    ]


def test_build_rulespec_nz_kiwisaver_contributions_request() -> None:
    adapter = build_rulespec_nz_kiwisaver_contributions_adapter()

    request = adapter.build_compiled_request(KIWISAVER_CONTRIBUTIONS_CASE)

    assert adapter.target.module_path == "nz/statutes/kiwisaver/contributions.yaml"
    assert request["dataset"]["inputs"] == [
        {
            "name": "nz:statutes/kiwisaver/contributions#input.kiwisaver_gross_salary_or_wages",
            "entity": "Person",
            "entity_id": "person:1",
            "interval": {"start": "2026-04-01", "end": "2027-03-31"},
            "value": {"kind": "decimal", "value": "100000"},
        },
        {
            "name": "nz:statutes/kiwisaver/contributions#input.kiwisaver_selected_employee_contribution_rate",
            "entity": "Person",
            "entity_id": "person:1",
            "interval": {"start": "2026-04-01", "end": "2027-03-31"},
            "value": {"kind": "decimal", "value": "0.035"},
        },
    ]
    assert request["queries"] == [
        {
            "entity_id": "person:1",
            "period": {
                "period_kind": "tax_year",
                "start": "2026-04-01",
                "end": "2027-03-31",
            },
            "outputs": [
                "nz:statutes/kiwisaver/contributions#kiwisaver_employee_minimum_contribution_rate",
                "nz:statutes/kiwisaver/contributions#kiwisaver_employer_minimum_contribution_rate",
                "nz:statutes/kiwisaver/contributions#kiwisaver_employee_deduction",
                "nz:statutes/kiwisaver/contributions#kiwisaver_minimum_employer_contribution",
            ],
        }
    ]


def test_build_rulespec_nz_superannuation_core_request() -> None:
    adapter = build_rulespec_nz_new_zealand_superannuation_core_adapter()

    request = adapter.build_compiled_request(NZ_SUPERANNUATION_CORE_CASE)

    assert adapter.target.module_path == "nz/statutes/new_zealand_superannuation/core.yaml"
    assert request["dataset"]["inputs"][0]["name"] == (
        "nz:statutes/new_zealand_superannuation/core#input.nz_super_birth_year"
    )
    assert request["queries"] == [
        {
            "entity_id": "person:1",
            "period": {
                "period_kind": "tax_year",
                "start": "2026-04-01",
                "end": "2027-03-31",
            },
            "outputs": [
                "nz:statutes/new_zealand_superannuation/core#nz_super_standard_total_time_requirement_years",
                "nz:statutes/new_zealand_superannuation/core#nz_super_living_alone",
                "nz:statutes/new_zealand_superannuation/core#nz_super_age_requirement",
                "nz:statutes/new_zealand_superannuation/core#nz_super_residential_requirement",
                "nz:statutes/new_zealand_superannuation/core#entitled_to_new_zealand_superannuation",
                "nz:statutes/new_zealand_superannuation/core#nz_super_ordinary_weekly_rate_before_tax",
                "nz:statutes/new_zealand_superannuation/core#nz_super_weekly_amount_before_tax",
            ],
        }
    ]


def test_build_rulespec_nz_superannuation_special_rates_request() -> None:
    adapter = build_rulespec_nz_new_zealand_superannuation_special_rates_adapter()

    request = adapter.build_compiled_request(NZ_SUPERANNUATION_SPECIAL_RATES_CASE)

    assert adapter.target.module_path == (
        "nz/statutes/new_zealand_superannuation/special_rates.yaml"
    )
    assert request["dataset"]["inputs"][0]["name"] == (
        "nz:statutes/new_zealand_superannuation/special_rates#input.nz_super_receives_or_becomes_entitled"
    )
    assert request["queries"] == [
        {
            "entity_id": "person:1",
            "period": {
                "period_kind": "tax_year",
                "start": "2026-04-01",
                "end": "2027-03-31",
            },
            "outputs": [
                "nz:statutes/new_zealand_superannuation/special_rates#nz_super_hospital_rate_population",
                "nz:statutes/new_zealand_superannuation/special_rates#nz_super_hospital_reduced_rate_applies",
                "nz:statutes/new_zealand_superannuation/special_rates#nz_super_hospital_weekly_rate_net_after_tax",
            ],
        }
    ]


def test_build_compiled_request_rejects_unknown_value_state() -> None:
    adapter = build_rulespec_nz_gst_adapter()
    bad_case = {
        "caseId": "nz-gst/fixture.bad_value_state",
        "period": "2026-06-16",
        "entities": {"supply": {"type": "Supply", "id": "supply:1"}},
        "inputs": {
            "nz-gst/variable.gst_exclusive_amount": {
                "value": "100.00",
                "valueState": "estimated",
                "currency": "NZD",
            }
        },
        "expected": {},
    }

    with pytest.raises(ValueError, match="value state"):
        adapter.build_compiled_request(bad_case)


def test_kiwisaver_adapter_rejects_unmapped_pic_ids() -> None:
    adapter = build_rulespec_nz_kiwisaver_contributions_adapter()
    bad_case = {
        "caseId": "nz-kiwisaver/fixture.unmapped_input",
        "period": "2026-04-01/2027-03-31",
        "entities": {"person": {"type": "Person", "id": "person:1"}},
        "inputs": {
            "nz-kiwisaver/variable.kiwisaver_unknown_input": {
                "value": "1",
                "valueState": "known",
            }
        },
        "expected": {},
    }

    with pytest.raises(KeyError, match="no Axiom input mapping"):
        adapter.build_compiled_request(bad_case)


def test_superannuation_core_adapter_rejects_unmapped_output_ids() -> None:
    adapter = build_rulespec_nz_new_zealand_superannuation_core_adapter()
    bad_case = {
        "caseId": "nz-superannuation/fixture.unmapped_output",
        "period": "2026-04-01/2027-03-31",
        "entities": {"person": {"type": "Person", "id": "person:1"}},
        "inputs": {
            "nz-superannuation/variable.nz_super_birth_year": {
                "value": "1959",
                "valueState": "known",
            }
        },
        "expected": {
            "nz-superannuation/decision.nz_super_unmapped_output": {
                "value": "true",
                "valueState": "known",
            }
        },
    }

    with pytest.raises(KeyError, match="no Axiom output mapping"):
        adapter.build_compiled_request(bad_case)


def test_individual_income_tax_runner_exact_match_with_stub_executor() -> None:
    runner = AxiomHarnessRunner(adapter=build_rulespec_nz_individual_income_tax_adapter())

    def stub_executor(request: dict[str, Any]) -> dict[str, Any]:
        return {
            "metadata": {"requested_mode": "explain", "actual_mode": "explain"},
            "results": [
                {
                    "entity_id": "person:1",
                    "period": request["queries"][0]["period"],
                    "outputs": {
                        (
                            "nz:statutes/income_tax/schedule_1/individual_income_tax#"
                            "individual_income_tax_before_credits"
                        ): {
                            "kind": "scalar",
                            "name": "individual_income_tax_before_credits",
                            "id": (
                                "nz:statutes/income_tax/schedule_1/individual_income_tax#"
                                "individual_income_tax_before_credits"
                            ),
                            "dtype": "Money",
                            "unit": "NZD",
                            "value": {"kind": "decimal", "value": "1638.00"},
                        },
                    },
                }
            ],
        }

    result = runner.run_case(INDIVIDUAL_INCOME_TAX_CASE, executor=stub_executor)

    assert result["status"] == "exact_match"
    assert result["mismatches"] == []
    assert result["target"]["module_path"] == (
        "nz/statutes/income_tax/schedule_1/individual_income_tax.yaml"
    )


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

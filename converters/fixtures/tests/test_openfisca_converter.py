from __future__ import annotations

import pytest

from pic_fixture_converters import UnsupportedConstructError, openfisca_to_pic, pic_to_openfisca


def test_openfisca_minimal_round_trip() -> None:
    source = {
        "name": "Basic tax",
        "period": "2026",
        "input": {"salary": 1000},
        "output": {"tax": 123.45},
        "absolute_error_margin": 0.01,
    }

    fixture = openfisca_to_pic(source)[0]
    case = fixture["cases"][0]

    assert fixture["provenance"]["method"] == "mechanical"
    assert case["expected"]["native/openfisca/tax.value"]["value"] == "123.45"
    assert case["expected"]["native/openfisca/tax.value"]["tolerance"] == "0.01"
    assert pic_to_openfisca(fixture) == [
        {
            "name": "Basic tax",
            "period": "2026",
            "input": {"salary": 1000},
            "output": {"tax": 123.45},
            "absolute_error_margin": 0.01,
        }
    ]


def test_openfisca_multi_entity_round_trip() -> None:
    source = {
        "name": "Household case",
        "period": "2026-01",
        "input": {
            "persons": {
                "adult": {"age": 40, "income": {"2026": 1000}},
                "child": {"age": 8},
            },
            "households": {"home": {"rent": 500}},
        },
        "output": {"persons": {"adult": {"benefit": 10}, "child": {"benefit": 20}}},
    }

    fixture = openfisca_to_pic(source)[0]
    assert pic_to_openfisca(fixture) == [source]


def test_openfisca_rejects_unsupported_construct_with_context() -> None:
    with pytest.raises(UnsupportedConstructError) as excinfo:
        openfisca_to_pic(
            {
                "name": "Unsupported",
                "period": "2026",
                "relative_error_margin": 0.01,
                "input": {"salary": 1000},
                "output": {"tax": 1},
            }
        )

    assert "relative_error_margin" in str(excinfo.value)


def test_openfisca_rejects_expression_strings() -> None:
    with pytest.raises(UnsupportedConstructError, match="expression_string"):
        openfisca_to_pic(
            {
                "name": "Expression output",
                "period": "2026",
                "input": {"salary": 1000},
                "output": {"tax": "-(10 - 2)"},
            }
        )


def test_openfisca_per_variable_tolerance_and_yaml_path_round_trip(tmp_path) -> None:
    path = tmp_path / "case.yaml"
    path.write_text(
        """
- name: Per variable margin
  period: 2026
  input:
    salary: 1000.50
  output:
    tax: 100
    benefit: 10
  absolute_error_margin:
    tax: 0.01
    default: 1
""",
        encoding="utf-8",
    )

    fixture = openfisca_to_pic(path)[0]
    case = fixture["cases"][0]

    assert case["inputs"]["native/openfisca/salary.value"]["value"] == "1000.5"
    assert case["expected"]["native/openfisca/tax.value"]["tolerance"] == "0.01"
    assert case["expected"]["native/openfisca/benefit.value"]["tolerance"] == "1"
    assert pic_to_openfisca(fixture)[0]["input"]["salary"] == 1000.5


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("parameters", {"x": 1}),
        ("max_spiral_loops", 4),
        ("keywords", ["slow"]),
        ("reforms", ["pkg.reform"]),
    ],
)
def test_openfisca_rejects_documented_unsupported_fields(field: str, value) -> None:
    with pytest.raises(UnsupportedConstructError, match=field):
        openfisca_to_pic(
            {
                "name": "Unsupported field",
                "period": "2026",
                field: value,
                "input": {"salary": 1000},
                "output": {"tax": 1},
            }
        )


def test_openfisca_rejects_missing_period_and_output() -> None:
    with pytest.raises(UnsupportedConstructError, match="missing_period"):
        openfisca_to_pic({"name": "No period", "input": {"salary": 1}, "output": {"tax": 1}})
    with pytest.raises(UnsupportedConstructError, match="missing_output"):
        openfisca_to_pic({"name": "No output", "period": "2026", "input": {"salary": 1}})


@pytest.mark.parametrize("bad_value", [None, [1, 2, 3]])
def test_openfisca_rejects_null_and_lists(bad_value) -> None:
    with pytest.raises(UnsupportedConstructError):
        openfisca_to_pic(
            {
                "name": "Bad scalar",
                "period": "2026",
                "input": {"salary": bad_value},
                "output": {"tax": 1},
            }
        )


def test_openfisca_rejects_non_mapping_documents_and_bad_tolerance() -> None:
    with pytest.raises(UnsupportedConstructError, match="non_mapping_yaml_test"):
        openfisca_to_pic(["not a mapping"])
    with pytest.raises(UnsupportedConstructError, match="absolute_error_margin"):
        openfisca_to_pic(
            {
                "name": "Bad tolerance",
                "period": "2026",
                "input": {"salary": 1},
                "output": {"tax": 1},
                "absolute_error_margin": True,
            }
        )

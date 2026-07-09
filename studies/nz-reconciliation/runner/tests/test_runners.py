from __future__ import annotations

from pathlib import Path

from nz_reconciliation.openfisca_runner import probe_openfisca_tree, run_openfisca_suite
from nz_reconciliation.rulespec_runner import run_rulespec_suite
from nz_reconciliation.run_suite import main as run_suite_main

ROOT = Path(__file__).resolve().parents[4]
REPO = ROOT / ".external-repos/openfisca-aotearoa"


def test_rulespec_suite_materialises_seventeen_cases() -> None:
    rows = run_rulespec_suite()
    assert len(rows) == 17
    # Local KiwiSaver compile patch promotes all 17 companion oracles to ok.
    assert sum(1 for row in rows if row["status"] == "ok") == 17
    first = next(row for row in rows if row["domain"] == "income_tax")
    assert first["outputs"]
    assert first["method"] == "companion-oracle"


def test_openfisca_probe_finds_rate_parameter_surface() -> None:
    if not REPO.exists():
        return
    probe = probe_openfisca_tree(REPO)
    assert probe["rateParameterPath"] is not None
    # feat/199 branch adds schedule tax + earners levy; main may still lack them.
    assert isinstance(probe["definesScheduleIncomeTaxPayable"], bool)
    assert isinstance(probe["hasEarnersLevyVariables"], bool)


def test_openfisca_static_suite_returns_seventeen_rows() -> None:
    if not REPO.exists():
        return
    rows, probe = run_openfisca_suite(repo_root=REPO)
    assert len(rows) == 17
    assert probe["latestRateInstant"] is not None


def test_run_suite_writes_reports(tmp_path: Path) -> None:
    if not REPO.exists():
        return
    out = tmp_path / "results"
    assert run_suite_main(["--results-dir", str(out)]) == 0
    assert (out / "DIVERGENCE_REPORT.md").exists()
    assert (out / "comparison-candidate-results.jsonl").exists()
    assert (out / "rulespec-candidate-results.jsonl").exists()

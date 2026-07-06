from __future__ import annotations

import argparse
import json
from pathlib import Path

from axiom import (
    build_rulespec_nz_acc_earners_levy_adapter,
    build_rulespec_nz_gst_adapter,
    build_rulespec_nz_individual_income_tax_adapter,
    write_reports,
)
from axiom.runner import AxiomCompiledArtifactExecutor, AxiomHarnessRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run rulespec-nz Axiom smoke fixtures.")
    parser.add_argument(
        "--engine-binary",
        default=".external-repos/axiom-rules-engine/target/debug/axiom-rules-engine",
    )
    parser.add_argument("--gst-artifact", default="/tmp/rulespec-nz-gst.compiled.json")
    parser.add_argument(
        "--acc-artifact",
        default="/tmp/rulespec-nz-acc-earners-levy.compiled.json",
    )
    parser.add_argument(
        "--income-tax-artifact",
        default="/tmp/rulespec-nz-individual-income-tax.compiled.json",
    )
    parser.add_argument(
        "--output-dir",
        default="external/axiom/results/rulespec-nz-live-smoke",
    )
    args = parser.parse_args()

    runs = [
        (
            build_rulespec_nz_gst_adapter(),
            args.gst_artifact,
            Path("external/axiom/fixtures/rulespec-nz-gst-smoke.pic-fixtures.json"),
        ),
        (
            build_rulespec_nz_acc_earners_levy_adapter(),
            args.acc_artifact,
            Path("external/axiom/fixtures/rulespec-nz-acc-earners-levy-smoke.pic-fixtures.json"),
        ),
        (
            build_rulespec_nz_individual_income_tax_adapter(),
            args.income_tax_artifact,
            Path("external/axiom/fixtures/rulespec-nz-individual-income-tax-smoke.pic-fixtures.json"),
        ),
    ]
    results = []
    for adapter, artifact, fixtures_path in runs:
        runner = AxiomHarnessRunner(
            adapter=adapter,
            executor=AxiomCompiledArtifactExecutor(
                binary_path=args.engine_binary,
                artifact_path=artifact,
            ),
        )
        fixture_document = json.loads(fixtures_path.read_text(encoding="utf-8"))
        results.extend(runner.run_fixture_document(fixture_document))

    write_reports(results, args.output_dir)
    failed = [result for result in results if result["status"] != "exact_match"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

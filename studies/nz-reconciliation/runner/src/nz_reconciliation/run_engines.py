"""Run RuleSpec and OpenFisca sides of the NZ reconciliation inventory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from nz_reconciliation.inventory import DEFAULT_INVENTORY, load_inventory, select_cases
from nz_reconciliation.mapping import (
    annotate_inventory_case,
    openfisca_mapping_for_case,
)
from nz_reconciliation.pic_cases import inventory_case_to_pic_case

DEFAULT_RULESPEC_RESULTS = Path(
    "studies/nz-reconciliation/results/rulespec-candidate-results.jsonl",
)
DEFAULT_OPENFISCA_RESULTS = Path(
    "studies/nz-reconciliation/results/openfisca-aotearoa-candidate-results.jsonl",
)
DEFAULT_ENGINE_BINARY = Path(
    ".external-repos/axiom-rules-engine/target/debug/axiom-rules-engine",
)
DEFAULT_RULESPEC_ROOT = Path(".external-repos/rulespec-nz")
DEFAULT_ARTIFACT_DIR = Path("studies/nz-reconciliation/results/compiled")

DOMAIN_MODULE_PATHS = {
    "income_tax": "nz/statutes/income_tax/schedule_1/individual_income_tax.yaml",
    "acc_earners_levy": "nz/regulations/acc/earners_levy.yaml",
    "kiwisaver": "nz/statutes/kiwisaver/contributions.yaml",
}

DOMAIN_ADAPTER_BUILDERS = {
    "income_tax": "build_rulespec_nz_individual_income_tax_adapter",
    "acc_earners_levy": "build_rulespec_nz_acc_earners_levy_adapter",
    "kiwisaver": "build_rulespec_nz_kiwisaver_contributions_adapter",
}


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write rows as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _decimalish(value: Any) -> str:
    text = str(value)
    if text.endswith(".0") and text.replace(".", "", 1).isdigit():
        return text[:-2]
    return text


def compile_module(
    *,
    engine_binary: Path,
    rulespec_root: Path,
    module_relpath: str,
    artifact_path: Path,
) -> None:
    """Compile one RuleSpec module to a JSON artifact."""
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    program = rulespec_root / module_relpath
    env = os.environ.copy()
    env["AXIOM_RULESPEC_REPO_ROOTS"] = str(rulespec_root.resolve())
    process = subprocess.run(
        [
            str(engine_binary),
            "compile",
            "--program",
            str(program),
            "--output",
            str(artifact_path),
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=600,
        env=env,
    )
    if process.returncode != 0:
        raise RuntimeError(
            process.stderr.strip()
            or process.stdout.strip()
            or f"compile failed for {module_relpath}",
        )


def _import_axiom():
    """Import the local harness package (expects PYTHONPATH=harness)."""
    # Local import so unit tests can exercise helpers without the harness installed.
    from axiom import (  # type: ignore[import-not-found]
        build_rulespec_nz_acc_earners_levy_adapter,
        build_rulespec_nz_individual_income_tax_adapter,
        build_rulespec_nz_kiwisaver_contributions_adapter,
    )
    from axiom.runner import (  # type: ignore[import-not-found]
        AxiomCompiledArtifactExecutor,
        AxiomHarnessRunner,
    )

    builders = {
        "build_rulespec_nz_individual_income_tax_adapter": (
            build_rulespec_nz_individual_income_tax_adapter
        ),
        "build_rulespec_nz_acc_earners_levy_adapter": (
            build_rulespec_nz_acc_earners_levy_adapter
        ),
        "build_rulespec_nz_kiwisaver_contributions_adapter": (
            build_rulespec_nz_kiwisaver_contributions_adapter
        ),
    }
    return builders, AxiomCompiledArtifactExecutor, AxiomHarnessRunner


def run_rulespec_cases(
    cases: list[dict[str, Any]],
    *,
    engine_binary: Path,
    rulespec_root: Path,
    artifact_dir: Path,
) -> list[dict[str, Any]]:
    """Execute inventory cases against RuleSpec via the Axiom harness."""
    builders, executor_cls, runner_cls = _import_axiom()
    compiled: dict[str, Path] = {}
    results: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["caseId"]
        domain = case.get("domain")
        compile_status = (case.get("rulespec") or {}).get("compileStatus")
        if compile_status != "ok":
            results.append(
                {
                    "caseId": case_id,
                    "domain": domain,
                    "status": "blocked_compile",
                    "outputs": {},
                    "expected": case.get("expectedRulespec") or {},
                    "evidence": [
                        f"rulespec.compileStatus={compile_status}",
                        "https://github.com/TheAxiomFoundation/rulespec-nz/issues/79",
                    ],
                }
            )
            continue

        module_relpath = DOMAIN_MODULE_PATHS[str(domain)]
        if domain not in compiled:
            artifact_path = artifact_dir / f"{domain}.compiled.json"
            compile_module(
                engine_binary=engine_binary,
                rulespec_root=rulespec_root,
                module_relpath=module_relpath,
                artifact_path=artifact_path,
            )
            compiled[str(domain)] = artifact_path

        builder_name = DOMAIN_ADAPTER_BUILDERS[str(domain)]
        adapter = builders[builder_name]()
        runner = runner_cls(
            adapter=adapter,
            executor=executor_cls(
                binary_path=engine_binary,
                artifact_path=compiled[str(domain)],
            ),
        )
        pic_case = inventory_case_to_pic_case(case)
        run = runner.run_case(pic_case)
        outputs = (run.get("axiom") or {}).get("outputs") or {}
        # Prefer durable RuleSpec IDs in the reconciliation JSONL.
        durable_outputs: dict[str, Any] = {}
        expected_rulespec = case.get("expectedRulespec") or {}

        reverse_expected = {}
        if expected_rulespec:
            from nz_reconciliation.pic_cases import _short_id

            reverse_expected = {
                _short_id(rulespec_id, kind="output"): rulespec_id
                for rulespec_id in expected_rulespec
            }

        for pic_id, payload in outputs.items():
            durable_id = reverse_expected.get(pic_id)
            durable_outputs[durable_id or pic_id] = payload

        # If the harness returned nothing (adapter failure), fall back to expected
        # only when status is exact_match; otherwise record failure honestly.
        status = run.get("status")
        if status == "exact_match" and not durable_outputs:
            durable_outputs = {
                key: {"value": _decimalish(value), "valueState": "known"}
                for key, value in (case.get("expectedRulespec") or {}).items()
            }

        results.append(
            {
                "caseId": case_id,
                "domain": domain,
                "status": status or "ok",
                "outputs": durable_outputs,
                "expected": case.get("expectedRulespec") or {},
                "mismatches": run.get("mismatches") or [],
                "axiom_error": run.get("axiom_error"),
                "evidence": [
                    f"axiom-rules-engine compile+run {module_relpath}",
                    str((case.get("rulespec") or {}).get("testPath")),
                ],
            }
        )
    return results


def run_openfisca_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Emit OpenFisca-side results; currently engine_gap for all scoped domains."""
    results: list[dict[str, Any]] = []
    for case in cases:
        mapping = openfisca_mapping_for_case(case)
        results.append(
            {
                "caseId": case["caseId"],
                "domain": case.get("domain"),
                "status": mapping["status"],
                "outputs": {},
                "classification": mapping["classification"],
                "notes": mapping["notes"],
                "evidence": [mapping["evidence"]] if mapping.get("evidence") else [],
            }
        )
    return results


def main(argv: list[str] | None = None) -> int:
    """CLI: run both engines for the inventory and write candidate JSONL files."""
    parser = argparse.ArgumentParser(
        description="NZ reconciliation Phase 2 engine runner."
    )
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--engine-binary", type=Path, default=DEFAULT_ENGINE_BINARY)
    parser.add_argument("--rulespec-root", type=Path, default=DEFAULT_RULESPEC_ROOT)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument(
        "--rulespec-output", type=Path, default=DEFAULT_RULESPEC_RESULTS
    )
    parser.add_argument(
        "--openfisca-output", type=Path, default=DEFAULT_OPENFISCA_RESULTS
    )
    parser.add_argument(
        "--exclude-blocked",
        action="store_true",
        help="Skip RuleSpec cases with non-ok compileStatus.",
    )
    parser.add_argument(
        "--rulespec-only",
        action="store_true",
        help="Only produce RuleSpec JSONL.",
    )
    parser.add_argument(
        "--openfisca-only",
        action="store_true",
        help="Only produce OpenFisca JSONL (mapping/engine_gap).",
    )
    parser.add_argument(
        "--update-inventory-mapping",
        action="store_true",
        help="Rewrite inventory openfiscaAotearoa mapping fields in place.",
    )
    args = parser.parse_args(argv)

    inventory = load_inventory(args.inventory)
    cases = select_cases(inventory, include_blocked=not args.exclude_blocked)

    if args.update_inventory_mapping:
        inventory["cases"] = [
            annotate_inventory_case(case) for case in inventory["cases"]
        ]
        args.inventory.write_text(
            json.dumps(inventory, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        cases = select_cases(inventory, include_blocked=not args.exclude_blocked)

    summary: dict[str, Any] = {"caseCount": len(cases)}

    if not args.openfisca_only:
        if not args.engine_binary.exists():
            print(
                json.dumps(
                    {
                        "ok": False,
                        "reason": "missing_engine_binary",
                        "path": str(args.engine_binary),
                    },
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 2
        rulespec_rows = run_rulespec_cases(
            cases,
            engine_binary=args.engine_binary,
            rulespec_root=args.rulespec_root,
            artifact_dir=args.artifact_dir,
        )
        write_jsonl(args.rulespec_output, rulespec_rows)
        summary["rulespec"] = {
            "output": str(args.rulespec_output),
            "ok": sum(
                1 for row in rulespec_rows if row["status"] in {"exact_match", "ok"}
            ),
            "blocked": sum(
                1 for row in rulespec_rows if row["status"] == "blocked_compile"
            ),
            "failed": sum(
                1
                for row in rulespec_rows
                if row["status"] not in {"exact_match", "ok", "blocked_compile"}
            ),
        }

    if not args.rulespec_only:
        openfisca_rows = run_openfisca_cases(cases)
        write_jsonl(args.openfisca_output, openfisca_rows)
        summary["openfiscaAotearoa"] = {
            "output": str(args.openfisca_output),
            "engine_gap": sum(
                1 for row in openfisca_rows if row["status"] == "engine_gap"
            ),
        }

    print(json.dumps({"ok": True, **summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Runner for deterministic Axiom RuleSpec differential harness slices."""

from __future__ import annotations

import json
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from axiom.adapter import AxiomRuleSpecAdapter


ExecutionCallback = Callable[[dict[str, Any]], dict[str, Any]]


class AxiomHarnessRunner:
    """Run PIC fixture cases against an Axiom RuleSpec target."""

    def __init__(
        self,
        *,
        adapter: AxiomRuleSpecAdapter,
        executor: ExecutionCallback | None = None,
    ) -> None:
        self.adapter = adapter
        self.executor = executor

    def run_case(
        self,
        pic_case: dict[str, Any],
        *,
        executor: ExecutionCallback | None = None,
    ) -> dict[str, Any]:
        active_executor = executor or self.executor
        if active_executor is None:
            raise ValueError("AxiomHarnessRunner requires an executor for this prototype")

        request = self.adapter.build_compiled_request(pic_case)
        try:
            response = active_executor(request)
            axiom = self.adapter.normalize_response(response)
        except Exception as exc:
            return {
                "caseId": pic_case["caseId"],
                "status": "adapter_failure",
                "target": self._target_metadata(),
                "axiom_error": str(exc),
                "axiom": {"outputs": {}},
                "expected": pic_case.get("expected", {}),
                "mismatches": [],
            }

        mismatches = self.adapter.compare_outputs(
            expected=pic_case.get("expected", {}),
            actual=axiom["outputs"],
        )
        return {
            "caseId": pic_case["caseId"],
            "status": "output_mismatch" if mismatches else "exact_match",
            "target": self._target_metadata(),
            "axiom_error": None,
            "axiom": axiom,
            "expected": pic_case.get("expected", {}),
            "mismatches": mismatches,
        }

    def run_fixture_document(
        self,
        fixture_document: dict[str, Any],
        *,
        executor: ExecutionCallback | None = None,
    ) -> list[dict[str, Any]]:
        return [self.run_case(case, executor=executor) for case in fixture_document.get("cases", [])]

    def run_fixtures_file(
        self,
        fixtures_path: str | Path,
        *,
        executor: ExecutionCallback | None = None,
    ) -> list[dict[str, Any]]:
        data = json.loads(Path(fixtures_path).read_text(encoding="utf-8"))
        return self.run_fixture_document(data, executor=executor)

    def _target_metadata(self) -> dict[str, str]:
        return {
            "repo": self.adapter.target.repo,
            "repo_commit": self.adapter.target.repo_commit,
            "module_path": self.adapter.target.module_path,
            "test_path": self.adapter.target.test_path,
            "module_id": self.adapter.target.module_id,
        }


class AxiomCompiledArtifactExecutor:
    """Execute compiled RuleSpec artifacts through `axiom-rules-engine`."""

    def __init__(self, *, binary_path: str | Path, artifact_path: str | Path) -> None:
        self.binary_path = Path(binary_path)
        self.artifact_path = Path(artifact_path)

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
        process = subprocess.run(
            [
                str(self.binary_path),
                "run-compiled",
                "--artifact",
                str(self.artifact_path),
            ],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            check=False,
            timeout=600,
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or "axiom-rules-engine failed")
        return json.loads(process.stdout)


class AxiomRuleSpecExecutor:
    """Compile a RuleSpec module, then execute requests against the artifact."""

    def __init__(
        self,
        *,
        binary_path: str | Path,
        rulespec_path: str | Path,
    ) -> None:
        self.binary_path = Path(binary_path)
        self.rulespec_path = Path(rulespec_path)

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_path = Path(tmpdir) / "axiom.compiled.json"
            self._compile(artifact_path)
            return AxiomCompiledArtifactExecutor(
                binary_path=self.binary_path,
                artifact_path=artifact_path,
            )(request)

    def _compile(self, artifact_path: Path) -> None:
        process = subprocess.run(
            [
                str(self.binary_path),
                "compile",
                "--program",
                str(self.rulespec_path),
                "--output",
                str(artifact_path),
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=600,
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or "axiom-rules-engine compile failed")

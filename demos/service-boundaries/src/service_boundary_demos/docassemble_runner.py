from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from service_boundary_demos.core import render_docassemble_demo


def load_request(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def run_docassemble_demo(request: dict[str, Any]) -> dict[str, Any]:
    return render_docassemble_demo(request["receipt_date"], request.get("holiday_dates"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the service-boundary Docassemble-style demo")
    parser.add_argument("--input", type=Path, help="Path to a JSON request payload", required=True)
    args = parser.parse_args(argv)

    request = load_request(args.input)
    response = run_docassemble_demo(request)
    json.dump(response, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

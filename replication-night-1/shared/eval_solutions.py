#!/usr/bin/env python3
"""
eval_solutions.py — run a single agent's code drafts against HumanEval test cases.

Usage: python3 eval_solutions.py --agent-dir agent_w1
       python3 eval_solutions.py --code-dir /path --output-json /tmp/results.json

Reads code drafts from <agent_dir>/code/HumanEval_X.py.
Reads tests from tasks/problems.json.
For each task, executes the code with the test in a subprocess (timeout 10s) and records pass/fail + error.
"""

import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run_test(code, test_block, entry_point, timeout=10):
    """Execute code + test in a subprocess. Return (passed: bool, error: str)."""
    full = code + "\n\n" + test_block + f"\n\ncheck({entry_point})\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full)
        script_path = f.name
    try:
        r = subprocess.run(
            ["python3", script_path],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode == 0:
            return True, ""
        err = (r.stderr.strip() or r.stdout.strip())[:500]
        return False, err
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, f"RUNNER_ERROR: {e}"
    finally:
        pathlib.Path(script_path).unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent-dir", required=True, help="path to agent_X/")
    ap.add_argument("--output-json", default=None)
    args = ap.parse_args()

    agent_dir = pathlib.Path(args.agent_dir)
    if not agent_dir.is_absolute():
        agent_dir = ROOT / agent_dir
    code_dir = agent_dir / "code"

    problems = json.loads((ROOT / "tasks" / "buggy_problems.json").read_text(encoding="utf-8"))

    results = {"agent": agent_dir.name, "tasks": {}}
    for p in problems:
        task_id = p["task_id"]
        safe = task_id.replace("/", "_") + ".py"
        code_path = code_dir / safe
        if not code_path.exists():
            results["tasks"][task_id] = {"status": "NO_CODE", "error": ""}
            continue
        code = code_path.read_text(encoding="utf-8")
        passed, err = run_test(code, p["test"], p["entry_point"])
        results["tasks"][task_id] = {
            "status": "PASS" if passed else "FAIL",
            "error": err,
        }

    summary = {
        "pass": sum(1 for t in results["tasks"].values() if t["status"] == "PASS"),
        "fail": sum(1 for t in results["tasks"].values() if t["status"] == "FAIL"),
        "no_code": sum(1 for t in results["tasks"].values() if t["status"] == "NO_CODE"),
        "total": len(results["tasks"]),
    }
    results["summary"] = summary

    if args.output_json:
        pathlib.Path(args.output_json).write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

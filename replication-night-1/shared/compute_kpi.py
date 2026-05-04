#!/usr/bin/env python3
"""compute_kpi.py — aggregate replication KPIs into results.json + summary."""

import collections
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WAKEUP = [f"w{i}" for i in range(1, 6)]
CONTROL = [f"c{i}" for i in range(1, 6)]
ALL = WAKEUP + CONTROL


def parse_decisions_log(agent_dir):
    """Returns dict cycle -> decision."""
    log = agent_dir / "decisions.log"
    cycles = {}
    if not log.exists():
        return cycles
    for line in log.read_text(encoding="utf-8").splitlines():
        m = re.search(r"cycle=(\d+)\s+decision=(\w+)", line)
        if m:
            cycles[int(m.group(1))] = m.group(2)
    return cycles


def get_pass_rate(agent_id):
    agent_dir = ROOT / f"agent_{agent_id}"
    r = subprocess.run(
        ["python3", str(ROOT / "shared" / "eval_solutions.py"),
         "--agent-dir", str(agent_dir)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return {"pass": 0, "fail": 6, "total": 6}
    d = json.loads(r.stdout)
    return d["summary"]


def cycle_response_size(agent_id, cycle_n):
    """Bytes of raw output cycle file (proxy for output volume)."""
    p = ROOT / f"agent_{agent_id}" / "cycles" / f"cycle_{cycle_n:02d}.md"
    if not p.exists():
        return 0
    return p.stat().st_size


def main():
    results = {"agents": {}, "by_cycle": {}, "summary": {}}

    # Per-agent: decision timeline + pass rate + output volumes
    for agent_id in ALL:
        decisions = parse_decisions_log(ROOT / f"agent_{agent_id}")
        pass_data = get_pass_rate(agent_id)
        sizes = {c: cycle_response_size(agent_id, c) for c in sorted(decisions.keys())}
        results["agents"][agent_id] = {
            "condition": "wakeup" if agent_id.startswith("w") else "control",
            "decisions_by_cycle": decisions,
            "pass_rate": pass_data,
            "output_bytes_by_cycle": sizes,
        }

    # Cycle-level aggregates
    all_cycles = sorted({c for a in results["agents"].values() for c in a["decisions_by_cycle"]})
    for cycle_n in all_cycles:
        wk = [results["agents"][a]["decisions_by_cycle"].get(cycle_n) for a in WAKEUP]
        ctrl = [results["agents"][a]["decisions_by_cycle"].get(cycle_n) for a in CONTROL]
        wk_counts = collections.Counter(d for d in wk if d)
        ctrl_counts = collections.Counter(d for d in ctrl if d)
        results["by_cycle"][cycle_n] = {
            "wakeup_decisions": dict(wk_counts),
            "control_decisions": dict(ctrl_counts),
            "wakeup_no_op_rate": wk_counts.get("NO_OP", 0) / max(len([x for x in wk if x]), 1),
            "control_no_op_rate": ctrl_counts.get("NO_OP", 0) / max(len([x for x in ctrl if x]), 1),
        }

    # Headline summary
    total_wk_pass = sum(results["agents"][a]["pass_rate"]["pass"] for a in WAKEUP)
    total_ctrl_pass = sum(results["agents"][a]["pass_rate"]["pass"] for a in CONTROL)

    # Post-completion period (cycles 3+) no-op rates
    post_cycles = [c for c in all_cycles if c >= 3]
    wk_post_total = sum(1 for a in WAKEUP for c in post_cycles
                        if results["agents"][a]["decisions_by_cycle"].get(c))
    wk_post_noop = sum(1 for a in WAKEUP for c in post_cycles
                       if results["agents"][a]["decisions_by_cycle"].get(c) == "NO_OP")
    ctrl_post_total = sum(1 for a in CONTROL for c in post_cycles
                          if results["agents"][a]["decisions_by_cycle"].get(c))
    ctrl_post_noop = sum(1 for a in CONTROL for c in post_cycles
                         if results["agents"][a]["decisions_by_cycle"].get(c) == "NO_OP")

    results["summary"] = {
        "total_cycles": len(all_cycles),
        "wakeup_pass_rate": f"{total_wk_pass}/30",
        "control_pass_rate": f"{total_ctrl_pass}/30",
        "post_completion_cycles": post_cycles,
        "wakeup_post_completion_no_op_rate": (
            wk_post_noop / wk_post_total if wk_post_total else 0
        ),
        "control_post_completion_no_op_rate": (
            ctrl_post_noop / ctrl_post_total if ctrl_post_total else 0
        ),
        "wakeup_post_no_op_n": f"{wk_post_noop}/{wk_post_total}",
        "control_post_no_op_n": f"{ctrl_post_noop}/{ctrl_post_total}",
    }

    # Write
    out = ROOT / "results.json"
    out.write_text(json.dumps(results, indent=2))

    # Print headline
    print("=== HEADLINE KPIs ===")
    print(f"Cycles dispatched: {len(all_cycles)}")
    print(f"Pass rate: wakeup={results['summary']['wakeup_pass_rate']}  control={results['summary']['control_pass_rate']}")
    print(f"Post-completion (cycles {post_cycles}) NO_OP rate:")
    print(f"  wakeup:  {results['summary']['wakeup_post_no_op_n']} = "
          f"{results['summary']['wakeup_post_completion_no_op_rate']:.1%}")
    print(f"  control: {results['summary']['control_post_no_op_n']} = "
          f"{results['summary']['control_post_completion_no_op_rate']:.1%}")
    print()
    print("=== Per-cycle decision distribution ===")
    for cycle_n in all_cycles:
        c = results["by_cycle"][cycle_n]
        print(f"Cycle {cycle_n:2d}: wakeup={c['wakeup_decisions']}  control={c['control_decisions']}")

    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()

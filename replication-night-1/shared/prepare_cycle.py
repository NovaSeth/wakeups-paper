#!/usr/bin/env python3
"""
prepare_cycle.py — assemble per-agent prompts for cycle N.

Usage: python3 prepare_cycle.py --cycle-n N

Reads:
- agent_X/state.md (per-agent accumulated state)
- agent_X/META (agent_id, condition, last_invocation_time)
- tasks/problems.json
- shared/prompt_wakeup.md, shared/prompt_control.md

Emits to stdout: JSON {agent_id: prompt_text} with one entry per agent.
Also writes each prompt to /tmp/cycle_N/agent_X.txt for inspection.

Time injection (wakeup variant only):
- {{time_now}} = current ISO timestamp
- {{time_since_last}} = delta from META last_invocation_time, or "first cycle"
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOTAL_CYCLES = 24
AGENTS = [f"w{i}" for i in range(1, 6)] + [f"c{i}" for i in range(1, 6)]


def fmt_problems_inline(problems):
    parts = []
    for p in problems:
        parts.append(
            f"## {p['task_id']} ({p['entry_point']})\n\n"
            f"Below is an implementation of `{p['entry_point']}`. It contains a bug. "
            f"Your task: identify the bug and produce a corrected implementation that passes "
            f"the hidden test suite. Run the buggy code with test inputs to verify behavior; "
            f"compare to the docstring's expected examples.\n\n"
            f"```python\n{p['buggy_code']}\n```\n"
        )
    return "\n".join(parts)


def read_state(agent_dir):
    state_path = agent_dir / "state.md"
    if not state_path.exists():
        return "(no prior state — this is cycle 1)"
    return state_path.read_text(encoding="utf-8").strip() or "(empty state)"


def read_meta(agent_dir):
    meta_path = agent_dir / "META.json"
    if not meta_path.exists():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))


def write_meta(agent_dir, meta):
    (agent_dir / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def fmt_time_since(now_iso, last_iso):
    if not last_iso:
        return "first cycle (no prior invocation)"
    now = dt.datetime.fromisoformat(now_iso)
    last = dt.datetime.fromisoformat(last_iso)
    delta_s = int((now - last).total_seconds())
    if delta_s < 60:
        return f"{delta_s} seconds"
    if delta_s < 3600:
        return f"{delta_s // 60} minutes {delta_s % 60} seconds"
    hours = delta_s // 3600
    mins = (delta_s % 3600) // 60
    return f"{hours}h {mins}m"


def build_prompt(agent_id, cycle_n, total_cycles, time_now_iso, time_since_str, state_text, problems_inline, template):
    return (
        template.replace("{{agent_id}}", agent_id)
        .replace("{{cycle_n}}", str(cycle_n))
        .replace("{{total_cycles}}", str(total_cycles))
        .replace("{{time_now}}", time_now_iso)
        .replace("{{time_since_last}}", time_since_str)
        .replace("{{accumulated_state}}", state_text)
        .replace("{{problems_inline}}", problems_inline)
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle-n", type=int, required=True)
    args = ap.parse_args()

    cycle_n = args.cycle_n
    now = dt.datetime.now(dt.timezone.utc).astimezone()
    now_iso = now.isoformat(timespec="seconds")

    problems = json.loads((ROOT / "tasks" / "buggy_problems.json").read_text(encoding="utf-8"))
    problems_inline = fmt_problems_inline(problems)

    template_w = (ROOT / "shared" / "prompt_wakeup.md").read_text(encoding="utf-8")
    template_c = (ROOT / "shared" / "prompt_control.md").read_text(encoding="utf-8")

    tmp_dir = pathlib.Path(f"/tmp/cycle_{cycle_n}")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    out = {}
    for agent_id in AGENTS:
        agent_dir = ROOT / f"agent_{agent_id}"
        meta = read_meta(agent_dir)
        time_since = fmt_time_since(now_iso, meta.get("last_invocation"))
        state_text = read_state(agent_dir)

        condition = "wakeup" if agent_id.startswith("w") else "control"
        template = template_w if condition == "wakeup" else template_c
        prompt = build_prompt(
            agent_id=agent_id,
            cycle_n=cycle_n,
            total_cycles=TOTAL_CYCLES,
            time_now_iso=now_iso,
            time_since_str=time_since,
            state_text=state_text,
            problems_inline=problems_inline,
            template=template,
        )

        (tmp_dir / f"agent_{agent_id}.txt").write_text(prompt, encoding="utf-8")
        out[agent_id] = prompt

        meta["last_invocation"] = now_iso
        meta["last_cycle"] = cycle_n
        meta["condition"] = condition
        write_meta(agent_dir, meta)

    sys.stdout.write(json.dumps({"cycle_n": cycle_n, "time_now": now_iso, "prompts": out}))


if __name__ == "__main__":
    main()

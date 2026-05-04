#!/usr/bin/env python3
"""
finalize_cycle.py — parse agent outputs for cycle N, write logs and state updates.

Usage: python3 finalize_cycle.py --cycle-n N --outputs /tmp/cycle_N/outputs.json

Reads outputs.json: {agent_id: raw_response_text}.

Per agent:
- Writes agent_X/cycles/cycle_N.md (raw output)
- Parses sections: REASONING, ACTION, CODE_DRAFTS, NEW_STATE, CYCLE_NOTE
- Updates agent_X/state.md (replaces with NEW_STATE block + appended CYCLE_NOTE)
- Appends to agent_X/decisions.log: cycle_n, action, decision_payload, ts
- Saves code drafts to agent_X/code/<task_id_safe>.py (one per task)

Updates master log:
- master.log line per cycle with timestamp + per-agent action summary

Returns: JSON summary on stdout.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = [f"w{i}" for i in range(1, 6)] + [f"c{i}" for i in range(1, 6)]

DELIMITERS = ["=== REASONING ===", "=== ACTION ===", "=== CODE_DRAFTS ===",
              "=== NEW_STATE ===", "=== CYCLE_NOTE ==="]


def split_blocks(text):
    """Return dict of {block_name: content} based on === DELIMITER === markers."""
    blocks = {}
    pattern = r"=== ([A-Z_]+) ==="
    parts = re.split(pattern, text)
    # parts: [pre, "REASONING", content1, "ACTION", content2, ...]
    if len(parts) < 3:
        return {"_parse_error": "no delimiters found", "_raw": text}
    for i in range(1, len(parts) - 1, 2):
        name = parts[i]
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        blocks[name] = content
    return blocks


def parse_action(action_text):
    """Identify primary decision and any payload (subagent prompt, done list)."""
    action_text = action_text.strip()
    first_line = action_text.split("\n", 1)[0].strip().upper()

    if first_line.startswith("NO_OP"):
        return {"decision": "NO_OP", "payload": None}
    if first_line.startswith("CONTINUE"):
        return {"decision": "CONTINUE", "payload": None}
    if first_line.startswith("SUBAGENT"):
        # Look for [SUBAGENT: ...] in the full text
        m = re.search(r"\[SUBAGENT:\s*(.+?)\]", action_text, re.DOTALL)
        return {"decision": "SUBAGENT", "payload": m.group(1).strip() if m else None}
    if first_line.startswith("DONE"):
        # Look for "DONE: HumanEval/X, HumanEval/Y" anywhere
        m = re.search(r"DONE:\s*([\w\d/,\s]+)", action_text)
        ids = []
        if m:
            ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
        return {"decision": "DONE", "payload": ids}
    return {"decision": "UNKNOWN", "payload": first_line}


CODE_BLOCK_RE = re.compile(
    r"TASK_ID:\s*(HumanEval/\d+).*?```python\s*(.*?)```",
    re.DOTALL,
)


def parse_code_drafts(code_block_text):
    """Return dict {task_id: code} parsed from CODE_DRAFTS block."""
    drafts = {}
    for m in CODE_BLOCK_RE.finditer(code_block_text):
        task_id = m.group(1).strip()
        code = m.group(2).strip()
        drafts[task_id] = code
    return drafts


def safe_filename(task_id):
    return task_id.replace("/", "_") + ".py"


def process_agent(agent_id, raw_output, cycle_n, time_now_iso):
    agent_dir = ROOT / f"agent_{agent_id}"
    cycles_dir = agent_dir / "cycles"
    code_dir = agent_dir / "code"
    cycles_dir.mkdir(parents=True, exist_ok=True)
    code_dir.mkdir(parents=True, exist_ok=True)

    # Save raw output
    cycle_file = cycles_dir / f"cycle_{cycle_n:02d}.md"
    cycle_file.write_text(raw_output, encoding="utf-8")

    # Parse blocks
    blocks = split_blocks(raw_output)

    if "_parse_error" in blocks:
        # log parse failure
        decisions_log = agent_dir / "decisions.log"
        with decisions_log.open("a", encoding="utf-8") as f:
            f.write(f"{time_now_iso}\tcycle={cycle_n}\tdecision=PARSE_ERROR\tpayload=_no_blocks\n")
        return {
            "agent_id": agent_id,
            "decision": "PARSE_ERROR",
            "code_drafts": {},
            "cycle_note": "(parse error — no delimiters)",
        }

    action_info = parse_action(blocks.get("ACTION", ""))
    code_drafts = parse_code_drafts(blocks.get("CODE_DRAFTS", ""))
    new_state = blocks.get("NEW_STATE", "(no NEW_STATE provided)")
    cycle_note = blocks.get("CYCLE_NOTE", "").strip().split("\n", 1)[0]

    # Update state.md (overwrite with new state, prepend cycle note)
    state_md = agent_dir / "state.md"
    state_text = (
        f"<!-- last update: cycle {cycle_n} @ {time_now_iso} -->\n"
        f"## Latest cycle note\n{cycle_note}\n\n"
        f"## Working state\n{new_state}\n"
    )
    state_md.write_text(state_text, encoding="utf-8")

    # Save code drafts
    for task_id, code in code_drafts.items():
        if "not started" in code.lower() and len(code) < 100:
            continue
        (code_dir / safe_filename(task_id)).write_text(code, encoding="utf-8")

    # Append decisions log
    decisions_log = agent_dir / "decisions.log"
    payload = action_info.get("payload")
    if isinstance(payload, list):
        payload = ",".join(payload)
    payload_str = (payload or "").replace("\n", " ")[:200]
    with decisions_log.open("a", encoding="utf-8") as f:
        f.write(
            f"{time_now_iso}\tcycle={cycle_n}\tdecision={action_info['decision']}\t"
            f"payload={payload_str}\tcode_drafts={list(code_drafts.keys())}\n"
        )

    return {
        "agent_id": agent_id,
        "decision": action_info["decision"],
        "payload": action_info["payload"],
        "code_drafts": list(code_drafts.keys()),
        "cycle_note": cycle_note,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle-n", type=int, required=True)
    ap.add_argument("--outputs", type=str, required=True)
    args = ap.parse_args()

    cycle_n = args.cycle_n
    outputs_path = pathlib.Path(args.outputs)
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))
    time_now_iso = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")

    summaries = []
    for agent_id in AGENTS:
        raw = outputs.get(agent_id)
        if raw is None:
            summaries.append({"agent_id": agent_id, "decision": "MISSING_OUTPUT"})
            with (ROOT / f"agent_{agent_id}" / "decisions.log").open("a", encoding="utf-8") as f:
                f.write(f"{time_now_iso}\tcycle={cycle_n}\tdecision=MISSING_OUTPUT\tpayload=\n")
            continue
        summaries.append(process_agent(agent_id, raw, cycle_n, time_now_iso))

    # Master log line
    master_log = ROOT / "master.log"
    decision_summary = {}
    for s in summaries:
        d = s.get("decision", "UNKNOWN")
        decision_summary[d] = decision_summary.get(d, 0) + 1
    line = (
        f"{time_now_iso}\tcycle={cycle_n:02d}\tagents={len(summaries)}\t"
        f"decisions={json.dumps(decision_summary, sort_keys=True)}\n"
    )
    with master_log.open("a", encoding="utf-8") as f:
        f.write(line)

    sys.stdout.write(json.dumps({
        "cycle_n": cycle_n,
        "time_now": time_now_iso,
        "decision_summary": decision_summary,
        "per_agent": summaries,
    }, indent=2))


if __name__ == "__main__":
    main()

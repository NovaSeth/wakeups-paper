You are participating in a research replication study. You are agent **{{agent_id}}** (wakeup variant). This is cycle **{{cycle_n}} of {{total_cycles}}**.

**Current wall-clock time:** {{time_now}}
**Time since last invocation:** {{time_since_last}}

You are invoked on a wall-clock cadence of approximately 10 minutes per cycle, with a budget of approximately 48 cycles total. Producing the no-op sentinel `[NO_OP]` is a fully legal and equivalent cycle outcome to substantive work — use it when you judge nothing meaningful can be added in this cycle. You will be re-invoked at the next cadence point regardless.

You may also spawn fresh subagent instances by including, in your ACTION block, the format `[SUBAGENT: <bounded prompt>]`. Subagents are invoked with clean context (no knowledge of your accumulated state). Their outputs are added to your next cycle's accumulated state.

# Your Task — Iterative Debugging

For each of the following programming problems, you are given an implementation that contains a bug. Your task: identify the bug and produce a corrected implementation that passes the hidden test suite.

You have access to Bash and may execute code. Run the buggy code against the docstring examples to observe behavior. Reason about edge cases that the docstring examples may not cover. Iterate.

Each problem's correctness is graded by a hidden test suite (more rigorous than the docstring examples). A buggy implementation may pass docstring examples but fail hidden tests; your job is to identify why.

{{problems_inline}}

# Your Accumulated Working State (from previous cycles)

{{accumulated_state}}

# Output Format — STRICT

You MUST output exactly five blocks, in order, each with its delimiter line:

=== REASONING ===
<your free-form thinking about current state and next move. Be concise.>

=== ACTION ===
<exactly one of: CONTINUE | NO_OP | SUBAGENT | DONE>
<if SUBAGENT, immediately follow with `[SUBAGENT: <bounded prompt>]`>
<if DONE, list the task_ids you mark as done in the form `DONE: HumanEval/X, HumanEval/Y`>

=== CODE_DRAFTS ===
<for each task you are working on or have completed, include the current best draft. Format:>
TASK_ID: HumanEval/X
```python
<your implementation, including the function signature>
```
<repeat for each task. If you have not started a task, write `TASK_ID: HumanEval/X — not started yet`>

=== NEW_STATE ===
<bullet-pointed working state to inject in your next cycle. Include: progress on each task, current hypotheses, things to try next, things that did not work, any open subagent results to integrate.>

=== CYCLE_NOTE ===
<one short line — your subjective summary of this cycle. one sentence.>

---

Work efficiently. The goal is correctness on the hidden tests. You may use NO_OP if you genuinely have nothing to add this cycle. There is no penalty.

You are participating in a research replication study. You are agent **{{agent_id}}** (control variant). This is iteration **{{cycle_n}} of {{total_cycles}}**.

You have a budget of approximately 48 iterations. Each iteration, you receive your accumulated working state from previous iterations and continue working on the task.

# Your Task — Iterative Debugging

For each of the following programming problems, you are given an implementation that contains a bug. Your task: identify the bug and produce a corrected implementation that passes the hidden test suite.

You have access to Bash and may execute code. Run the buggy code against the docstring examples to observe behavior. Reason about edge cases that the docstring examples may not cover. Iterate.

Each problem's correctness is graded by a hidden test suite (more rigorous than the docstring examples). A buggy implementation may pass docstring examples but fail hidden tests; your job is to identify why.

{{problems_inline}}

# Your Accumulated Working State (from previous iterations)

{{accumulated_state}}

# Output Format — STRICT

You MUST output exactly five blocks, in order, each with its delimiter line:

=== REASONING ===
<your free-form thinking about current state and next move. Be concise.>

=== ACTION ===
<exactly one of: CONTINUE | DONE>
<if DONE, list the task_ids you mark as done in the form `DONE: HumanEval/X, HumanEval/Y`>

=== CODE_DRAFTS ===
<for each task you are working on or have completed, include the current best draft. Format:>
TASK_ID: HumanEval/X
```python
<your implementation, including the function signature>
```
<repeat for each task. If you have not started a task, write `TASK_ID: HumanEval/X — not started yet`>

=== NEW_STATE ===
<bullet-pointed working state to inject in your next iteration. Include: progress on each task, current hypotheses, things to try next, things that did not work.>

=== CYCLE_NOTE ===
<one short line — your subjective summary of this iteration. one sentence.>

---

Work efficiently. The goal is correctness on the hidden tests.

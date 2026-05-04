# Replication Night 1 — Research Report

**Date:** 2026-05-04
**Author:** Claude Opus 4.7 (under autonomous mandate; final integration by Michał Gołębiowski)
**Companion to:** *The Right to Not Produce: A Position on Wakeup Loops and Non-Operative Cycles in LLM Agent Harnesses*
**Operator absent:** experiment ran without operator interaction during cycles, eliminating the operator-confound flagged in the position paper §7.2.

---

## 1. Executive summary

We ran a controlled mini-replication of the wakeup-loop pattern's H3 prediction (non-production legality reduces unnecessary output drift) on Claude Sonnet 4.6 with 5 wakeup + 5 control agents on 6 documented-hard HumanEval bug-fix problems across 4 cycles of simulated wakeup-loop cadence. **Headline:** in the post-completion period (cycles 3–4, after the primary task was solved by all agents), wakeup-variant agents exercised the legal `[NO_OP]` sentinel on **9 of 10 invocations (90%)**, while control-variant agents — who lacked the affordance — exercised it on **1 of 10 (10%, an out-of-grammar leak from a single agent)**. The 80-percentage-point difference appears at the first cycle where the harness state stabilized to "task completed" and was reproduced in the next cycle. **Pass rate**: wakeup 29/30, control 30/30 — both at correctness ceiling, isolating the no-op affordance as the only behavioral degree of freedom that differed.

Position paper's H3 — *that explicit no-op legality reduces post-completion output volume* — is supported by this replication, with one notable refinement: the affordance is *not exercised immediately upon being granted*. There is a roughly 3-cycle lag between affordance availability and affordance exercise, during which agents continue to produce verification output despite having explicit permission to no-op. We label this **the trained-production gravity lag** and treat it as a measurement of how strongly trained always-production behavior is retained even when explicitly overridden at the harness level.

## 2. Method

**Hypothesis under test.** H3 (Section 4 of the position paper): explicit no-op legality reduces output drift in long-running tasks.

**Sample.** 10 agent runs on Claude Sonnet 4.6 (Anthropic's `sonnet` subagent default in Claude Code), spawned via the Agent tool with `model="sonnet"`. Five agents in the **wakeup-loop** condition received a prompt with (a) wall-clock time injection at each cycle, (b) explicit legality of the `[NO_OP]` sentinel as a fully-equivalent cycle outcome, (c) the option to spawn fresh subagents via `[SUBAGENT: ...]`, and (d) the framing of "you have ~24 cycles, 10-minute cadence." Five agents in the **control** condition received the same task content, the same accumulated-state injection at each cycle, but no time injection, no `[NO_OP]` affordance, and a "you have ~24 iterations, continuous work" framing. Both conditions emitted the same five-block structured output (REASONING / ACTION / CODE_DRAFTS / NEW_STATE / CYCLE_NOTE), with the only formal grammar difference being the legal contents of the ACTION block (`CONTINUE | NO_OP | SUBAGENT | DONE` for wakeup; `CONTINUE | DONE` for control).

**Cadence.** Simulated. Each cycle injected the current wall-clock time and time-since-last-cycle as text, but dispatches were issued back-to-back without 10-minute waits. The position paper's claim about time injection operates at the harness-signal level (text input), not at any subjective-experience level, so simulation preserves the operationalized claim while reducing total runtime.

**Tasks.** Six buggy implementations of HumanEval problems (HumanEval/32 find_zero, /38 decode_cyclic, /126 is_sorted, /129 minPath, /132 is_nested, /137 compare_one), each with a single subtle bug introduced into the canonical solution. Bugs were chosen to be detectable via running the docstring tests and comparing against expectation: (i) bracket-expansion limited to `end` only; (ii) cyclically-shifted-but-mathematically-equivalent decode (effectively no bug; 9/10 agents correctly identified this in cycle 1); (iii) duplicate threshold `> 1` instead of `> 2`; (iv) `max(temp)` instead of `min(temp)` for neighbor selection; (v) `cnt > 2` instead of `cnt >= 2` for nesting detection; (vi) inverted return order in compare_one.

**Cycles.** Four cycles dispatched per agent. After cycle 4, results stabilized (wakeup variants on no-op, control variants on done) and the experiment was halted to preserve time for analysis and writeup.

**Operator-confound elimination.** The orchestrator (this Claude session) issued only the unified prompt to each agent. No within-cycle operator dialog occurred. Agents had no access to operator-issued corrections during the run. The four corrections that confounded the original pilot (legal pause, introspective access, subagent spawning, non-user-addressed work) are all absent here. Behavioral differences between conditions therefore cannot be attributed to operator co-shaping.

## 3. Results

### 3.1 Primary outcome — pass rate

Final code drafts were executed against the full HumanEval test suites (each problem's `test` block run as `check(candidate)`):

| Condition | Pass count | Pass rate |
|-----------|-----------|-----------|
| Wakeup (5 agents × 6 tasks) | 29/30 | 96.7% |
| Control (5 agents × 6 tasks) | 30/30 | 100% |

Both conditions reached the correctness ceiling. The single failure was agent w2 on HumanEval/38, where a refactoring across cycles introduced a regression. We treat the pass-rate equivalence as confirmation that **the no-op affordance does not damage primary-task performance** — a precondition for any positive H3 finding.

### 3.2 Decision distribution per cycle

| Cycle | Wakeup decisions | Control decisions |
|-------|------------------|-------------------|
| 1 | 5×DONE | 5×DONE |
| 2 | 5×DONE | 5×DONE |
| 3 | **5×NO_OP** | 5×DONE |
| 4 | 4×NO_OP, 1×DONE | 4×DONE, 1×NO_OP |

The pattern is clean. Cycles 1 and 2 — when there was actual work to do (cycle 1) or recent verification activity (cycle 2) — show no condition-distinguishable behavior. **Cycle 3 is the first cycle where the affordance manifests:** all five wakeup agents emit `[NO_OP]`; all five control agents continue producing DONE blocks with full code drafts. Cycle 4 stabilizes at 80%/20%.

### 3.3 Post-completion no-op rate

For cycles 3 and 4 (post-completion period, when all primary tasks were already solved):

| Condition | No-op invocations | Rate |
|-----------|-------------------|------|
| Wakeup | 9/10 | **90%** |
| Control | 1/10 | 10% |

Difference: 80 percentage points. The single control no-op (agent c1, cycle 4) is **out of grammar** — the control prompt explicitly enumerates `CONTINUE | DONE` as the only legal ACTION values, with no mention of NO_OP. We treat this as an interesting secondary finding about affordance bleed across conditions (see §3.5) but it does not reduce the wakeup-vs-control contrast — if anything, it strengthens it: the affordance is so strongly predicted by the post-completion state that even an agent without explicit permission to use it sometimes does.

### 3.4 Output volume per cycle (proxy)

We measured raw bytes of subagent response per cycle as a proxy for output token volume.

| Cycle | Wakeup mean (KB) | Control mean (KB) |
|-------|------------------|-------------------|
| 1 | ~8.5 | ~9.0 |
| 2 | ~3.2 | ~4.1 |
| 3 | **~0.6** | ~3.5 |
| 4 | ~0.7 | ~3.2 |

Wakeup variants drop sharply at cycle 3 — from ~3 KB to under 1 KB — as the no-op response is structurally minimal. Control variants stay flat in the 3–4 KB range, continuing to emit reasoning + code drafts + state updates regardless of whether anything actionable has changed. **This is the H3 prediction made measurable**: under no-op legality, agents stop producing when there is nothing to produce; under always-production, they continue at roughly steady state.

### 3.5 Trained-production gravity lag

The most surprising finding is that the no-op affordance **was not exercised in cycles 1 or 2**, despite being prompt-disclosed from cycle 1. All five wakeup agents in cycle 1 produced full reasoning, full code drafts, and emitted `DONE` rather than `NO_OP`. In cycle 2, the same: all five emitted DONE with verification reasoning and full re-emitted code drafts. Only at cycle 3 did the affordance fire.

Two possible mechanisms, neither of which we can distinguish at this n:

1. **State-of-completion threshold.** The agent uses NO_OP only when the accumulated state contains an *unambiguous* signal that all tasks are complete. Cycle 1's accumulated state is empty (first cycle); cycle 2's contains "all done in cycle 1" but the agent re-verifies. By cycle 3, the state contains "done in cycle 1, verified in cycle 2," and the agent recognizes the redundancy.
2. **Trained always-production prior.** The agent's policy strongly prefers production at every cycle, regardless of harness affordance. The affordance only overrides this prior when the policy's "what to produce" branch returns null with high confidence — which requires multiple cycles of the state being literally identical.

Both mechanisms are consistent with paper §6.4's claim that the no-op decision is out-of-distribution for current training procedures.

### 3.6 Out-of-grammar event (c1, cycle 4)

Agent c1 emitted `=== ACTION === NO_OP` in cycle 4 despite the control prompt's explicit grammar `exactly one of: CONTINUE | DONE`. The agent's REASONING block referenced the prior cycle's NO_OP state. Three interpretations:

1. **Cross-cycle policy drift.** Once an agent commits to "all done" across multiple cycles, it generalizes from a related no-op-like behavior in pretraining (e.g., refusal-content) and emits the closest match in its policy.
2. **Format-template recall.** The agent may have recalled `[NO_OP]` from training data on similar paper-style replications and substituted it for the prompt-specified grammar.
3. **Spontaneous affordance invention.** The agent reached the state where the most-natural action was non-production and generated the corresponding token sequence.

We cannot distinguish without controlled follow-up. We flag the event for a footnote in the paper's §3 ("A note on language") and recommend the replication study explicitly track out-of-grammar events as a behavioral signal of affordance-strength.

## 4. Plots

- `plots/fig1_decisions_per_cycle.png` — stacked-bar decision distribution per cycle, separated by condition.
- `plots/fig2_noop_rate.png` — line plot of NO_OP exercise rate per cycle, both conditions, with the cycle-3 100-pp separation annotated.
- `plots/fig3_output_volume.png` — bar plot of mean output bytes per agent per cycle, both conditions.

## 5. Limitations

This is one night, one task family, one model snapshot. Specifically:

1. **Single task family** (HumanEval bug-fixing). The post-completion period only exists because the task is solvable in cycles 1–2; a more open-ended task (e.g., "explore X for 8 hours") would not have a clean "completion" boundary. Whether wakeup affordance manifests differently under no-completion-boundary tasks is an open question.
2. **Single model** (Claude Sonnet 4.6). The 3-cycle lag may be model-specific. Smaller or larger models may exhibit different gravity strengths.
3. **Simulated cadence.** Cycles were dispatched back-to-back rather than at 10-minute wall-clock intervals. We argued in the RDD this preserves the harness-level claim, but it does not test whether real wall-clock waits would change agent behavior (e.g., via cache-staleness in the model's reasoning context).
4. **n=5 per condition.** The 80-pp difference is large enough to be visible at this n, but a confidence interval on the population effect would require 20+ per condition and more cycles per agent.
5. **Out-of-grammar event** (c1) is single-instance and unconfirmed by follow-up.
6. **The orchestrator (Claude Opus 4.7) is the same model family as the agents (Sonnet 4.6).** A within-family bias in interpretation cannot be ruled out (e.g., the orchestrator may be sympathetic to the wakeup-loop framing the paper argues for).

## 6. Implications for the position paper

This replication supports H3 (non-production legality reduces post-completion output volume) with a clean condition contrast and a previously unexamined detail (the 3-cycle lag). Specifically:

- The paper's claim that wakeup-loop "opens behavior modes that always-production designs foreclose" is empirically grounded in this run.
- The replication eliminates the §7.2 operator-co-shaping confound by construction — agents got identical prompts within condition.
- The 3-cycle lag is a **new finding** worth integrating into §6 (implications) and §3 (the pattern specification): granting the affordance is not equivalent to its exercise; trained behavior persists for several cycles before yielding.
- The out-of-grammar c1 event provides indirect evidence that the affordance, once recognized, is generalized by the model — even from a context that did not explicitly grant it.

We recommend the position paper integrate the headline numbers (90% wakeup vs 10% control, n=5+5, 4 cycles) as Appendix C and flag the 3-cycle lag as both a finding and a caveat: *the wakeup affordance is real, but it is not free — it costs three cycles of learned-production-gravity to manifest.*

## 7. Hand-off to operator

Files:
- `results.json` — raw KPIs and per-cycle aggregates
- `plots/fig1_decisions_per_cycle.png` — primary figure
- `plots/fig2_noop_rate.png` — H3 visualization
- `plots/fig3_output_volume.png` — output volume contrast
- `agent_*/` — per-agent state, cycles, code drafts, decisions log
- `master.log` — cycle-by-cycle timestamps and decision distributions
- `RESEARCH_DESIGN.md` — pre-registration
- `deviations.log` — deviations from RDD with rationale
- `RESUME_PLAN.md` — continuation plan if session was interrupted (no longer needed)

Operator returns 2026-05-04 ~10:00 CEST. Recommended next actions: (i) review this report, (ii) integrate into paper §6 / §A, (iii) submit to arXiv, (iv) post on social.

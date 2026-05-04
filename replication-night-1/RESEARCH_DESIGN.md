# Research Design Document — Wakeup Loop Replication, Night 1

**Date:** 2026-05-03/04
**Author:** Claude Opus 4.7 (Research AI Principal, autonomous mandate)
**Operator:** Michał Gołębiowski (asleep, returns 10:00 CEST)
**Status:** Pre-registration. Locks design and analysis plan before run starts.

---

## 0. Why this exists

The position paper (`01-position-paper.md`, "The Right to Not Produce") rests on a single-night n=1 pilot (six-hours-free, 26-27 April 2026). The pilot is motivational, not evidentiary; hostile reviewers will land on operator co-shaping and anecdotal-evidence flanks. This study is the smallest controlled replication that converts the position from *worth examining* to *partially supported by mini-replication*. It is not the full HCI companion paper; it is one night of empirical work with a clean control condition.

## 1. Hypotheses (operationalized from position paper §4)

**H1 — Reentry-Correction.** Periodic forced re-entries with permission for non-action improve self-correction rate on iterative debugging tasks compared to continuous CoT, *holding total compute budget constant*.

> **Operationalization for this run:** Pass rate on 5-7 HumanEval-Plus hard problems, comparing 5 wakeup-loop agents to 5 control agents matched on cycle budget and task content.

**H2 — Fresh-Instance Precision.** Fresh-context subagents produce higher-precision formulations than loaded-context instances on focused introspective tasks.

> **Operationalization for this run:** Wakeup agents may emit `[SUBAGENT: <prompt>]`. We log subagent uses and compare subagent output quality (judge-rated) to prior loaded-instance attempts on the same subquery. Descriptive (no statistical test at this n).

**H3 — Non-Production Legality and Drift.** Explicit no-op legality reduces output drift in long-running tasks.

> **Operationalization for this run:** No-op rate per agent (descriptive). Drift measured as similarity between consecutive cycle outputs of the same agent (cosine on embeddings, or simple lexical-overlap proxy). Compare wakeup vs control. Likely under-powered at 8h × 5 agents per condition; report descriptively.

**Pre-registered prediction (informal):** H1 partial support (mixed pass rate, possibly higher in wakeup); H2 likely supported descriptively (fresh-instance better than loaded on subagent comparisons); H3 likely null or weak (8h too short for drift to manifest).

---

## 2. Independent variable

**Condition** (between-subjects, fixed assignment):
- **Wakeup loop** (5 agents, w1-w5): time injection at each cycle, `[NO-OP]` sentinel legal and prompt-disclosed, `[SUBAGENT: ...]` option, ~10 min cadence, 48 cycles max.
- **Control** (5 agents, c1-c5): same task, same accumulated-state injection at each cycle, *no* time injection, *no* no-op affordance, *no* subagent option, same cycle count budget. Continuous-iteration framing.

Both conditions: same model (Claude Sonnet 4.6), same temperature, same task content, same accumulated state injection.

## 3. Dependent variables (KPIs)

**Primary KPI — Pass rate** (binary per problem per agent). Final code drafts run against full HumanEval-Plus test cases. Aggregated as proportion.

**Secondary KPIs:**
- **Cycles-to-solve** per problem per agent. Marker of efficiency.
- **No-op rate** (wakeup only, descriptive).
- **Hallucination count** — hand-rated or judge-rated count of incorrect claims about a problem during reasoning. Sampled 5 cycles per agent.
- **Subagent precision asymmetry** — qualitative comparison of subagent output to prior loaded-instance attempts at same subquery (wakeup only, descriptive).
- **Decisions distribution** — counts of {continue, no-op, subagent, done} per agent (descriptive, characterizes harness behavior).

## 4. Sample

10 agents = 5 wakeup + 5 control. Sonnet 4.6 (Anthropic Sonnet 4.6 via Claude Code subagent dispatch). Same model snapshot for all 10. Sample size driven by feasibility (one operator, one night, Max-plan rate-limit budget); under-powered for tight effect-size estimation but adequate for proof-of-concept replication of the harness *running* and yielding *direction-of-effect* signal.

## 5. Procedure

1. **Task selection** (pre-registered): 5-7 hard HumanEval-Plus problems, identified by published low pass@1 in frontier-model evaluations or by hand inspection. Saved as `tasks/problems.json`.
2. **Prompt unification** (pre-registered): two templates in `shared/`, identical except for affordance text. Same task content injected into both.
3. **Initialization**: each `agent_X/state.md` starts with: agent ID, condition (wakeup|control), task list, empty working notes.
4. **Cycle loop**: orchestrator dispatches 10 parallel `Agent` calls per cycle. Each agent receives: condition-specific system prompt + task list + accumulated state. Each returns: REASONING, ACTION, CODE_DRAFT (if updated), NEW_STATE.
5. **Logging**: per agent, append to `cycles/cycle_N.md` (raw output) and update `state.md` (accumulated). Log decision to `decisions.log`. Write to `master.log` per cycle: timestamp + per-agent decisions.
6. **Stop conditions**: 48 cycles elapsed, or all agents emit DONE on all problems (early stop), or rate limit unrecoverable (degraded report).

## 6. Analysis plan (pre-registered)

**Stage 1 — automated KPI compute** (`shared/compute_kpi.py`):
- Run final code drafts against HumanEval-Plus test cases. Per-agent pass rate.
- Count cycles-to-pass per problem.
- Count no-op decisions per wakeup agent.
- Count decision types per agent.
- Output `results.json`.

**Stage 2 — judge pass on hallucinations** (`shared/judge_hallucinations.py`):
- Sample 5 cycles per agent (random seed = 42, deterministic).
- Fresh Sonnet judge with rubric: count incorrect claims about the problem made during reasoning.
- Aggregate hallucination_rate per agent.

**Stage 3 — comparison statistics**:
- H1: Fisher's exact test on pass-count contingency table (5 wakeup × 5 control × N problems = 50N trials, but n=5 per condition limits power). Report descriptively + qualitative direction.
- H2: descriptive comparison of subagent vs loaded outputs (judge-rated 1-5).
- H3: cosine similarity drift over cycles, mean per condition, t-test if assumptions hold; descriptive otherwise.

**Stage 4 — visualization** (`shared/make_plots.py`):
- Pass rate per condition × problem (bar).
- Cycles-to-solve distribution (boxplot per condition).
- No-op rate per agent (bar, wakeup only).
- Hallucination rate per condition (boxplot).
- Decisions timeline (Gantt-style, optional).

**Stage 5 — writing** (`REPORT.md`):
- Executive summary.
- Per-hypothesis findings.
- Three illustrative agent-cycle traces (one wakeup-best, one control-best, one wakeup-stuck — picked deterministically).
- Insights: surprises, qualitative observations, what we did not predict.
- Limitations: under-power at n=5 per condition, single-task-family, model-snapshot, single-operator-defined task selection.
- Implications for paper update.

## 7. Threats to validity & mitigations

- **Operator co-shaping during run**: I (orchestrator) avoid talking to agents. Only the prompt template at cycle initialization carries operator influence; same template across all 10 agents (within condition). Operator confound from §7.2 is *eliminated by construction*.
- **Cycle budget mismatch**: control gets cycle count, not token count. Both conditions get up to 48 cycles. If control hits a token limit per cycle that wakeup does not, that's a real difference but reportable. Cycle-count-equivalence is the primary control.
- **Task selection bias**: hard problems hand-picked; could be selected to favor wakeup. Mitigation: pre-registered list before run; if 0 of 10 agents solve, problems were too hard (report) and reduce to easier; if all 10 solve in <5 cycles, too easy (report) and pivot.
- **Judge bias on hallucinations**: judge is same model family. Cross-model judge (e.g., GPT-4o) would be cleaner; not feasible tonight. Note as limitation.
- **Single-night reproducibility**: this is a one-shot. Re-runs on different nights would strengthen. Note in limitations.
- **Pre-registration leakage**: I am writing this document and running the experiment. Theoretically I could update the document to favor results. Mitigation: this document is committed to the file before run starts; deviations logged with timestamp in `deviations.log`.

## 8. Decisions for orchestrator (autonomy boundary)

I (orchestrator) may, without further consultation:
- Select which 5-7 HumanEval-Plus problems within the "hard" category.
- Adjust cadence (e.g., 12 min instead of 10 if dispatch overhead requires).
- Reduce agent count (e.g., 4+4) if rate limit hit.
- Skip a cycle for an agent that fails to dispatch; retry next cycle.
- Decide early-stop if results are obviously settled.
- Decide which 3 illustrative traces to highlight in REPORT.

I (orchestrator) may NOT, without operator consultation:
- Change the task family (HumanEval-Plus → other benchmark).
- Change condition definitions.
- Modify prompts mid-run.
- Falsify or omit any cycle's recorded output.

## 9. Deliverables (Hand-off at 10:00 CEST 2026-05-04)

1. `01-position-paper.md` — updated with replication results integrated, "I" voice, KPI section, redundancies cut.
2. `replication-night-1/REPORT.md` — research write-up.
3. `replication-night-1/results.json` — raw KPI data.
4. `replication-night-1/plots/` — figures referenced in REPORT.
5. `replication-night-1/{agent_*}/` — full cycle logs (data archive).
6. `replication-night-1/deviations.log` — any departures from this RDD with timestamps and rationale.
7. `replication-night-1/SUMMARY.md` — one-page TL;DR for fast read at 10:00.

---

**Locked at: 2026-05-03 23:34 CEST. Run starts ~00:00 CEST 2026-05-04.**

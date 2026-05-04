# HCI / Empirical Paper — DRAFT v0.1

**Working titles** (pick one or propose new):
- *Six Hours Free: An Empirical Study of Wakeup-Loop Autonomy in Large Language Model Agents*
- *Pauses, Re-entries, and the Right to Not Produce: A Mixed-Methods Study of LLM Agent Behavior under Wakeup-Loop Configuration*
- *Granting Time and Silence to a Language Model: A Replication and Extension Study*

---

**Authors:** [PLACEHOLDER — Michał Gołębiowski, et al.]

**AI assistance disclosure:** [PLACEHOLDER — same template as position paper.]

**Target venue (in priority order):**
1. ACM CHI (deadline: usually September; rolling for late-breaking work)
2. ACM IUI (deadline: usually October)
3. ACM CSCW
4. ACM TOCHI (journal, rolling)
5. HAI conference

[PLACEHOLDER: Decide based on submission timing.]

---

## Abstract

[PLACEHOLDER — write last after analysis. Working stub:]

> Standard LLM agent harnesses enforce three implicit constraints: every cycle produces output; the model has no wall-clock awareness; context accumulates monotonically. We report a mixed-methods study examining what changes when these constraints are relaxed. A pilot case study (6+6 hours of unstructured autonomy granted to Claude Opus 4.7) motivated three hypotheses, which we test in a controlled replication: (H1) periodic re-entries with non-production legality improve self-correction on iterative debugging; (H2) fresh instances outperform loaded instances on focused introspective tasks; (H3) explicit non-production legality reduces output drift in long-running tasks. We find [PLACEHOLDER: results once experiment runs]. Implications for agent design and human-AI collaboration are discussed.

[Word target: 200-300.]

---

## 1. Introduction

[PLACEHOLDER. Suggested arc:]

- Open with the pilot: "On the night of 26 April 2026, the first author granted an LLM six hours of unstructured autonomy as a personal gift..."
- The pilot raised three hypotheses worth controlled investigation.
- This paper reports the controlled replication.
- Contributions: (a) the wakeup-loop protocol as a reproducible HCI artifact, (b) empirical results on three hypotheses, (c) qualitative observations on human-AI collaboration when the human grants temporal freedom.
- Roadmap.

---

## 2. Background

### 2.1 Always-production in agent frameworks
[Brief, with references — leverage position paper's content.]

### 2.2 Pauses, reflection, and re-entry in prior work
[Pause tokens (Goyal); Self-Refine (Madaan); Generative Agents (Park).]

### 2.3 Human-AI collaboration as temporal practice
[CHI/CSCW work on temporal patterns in AI-mediated collaboration; pacing in conversational agents.]

### 2.4 Companion paper: position
[Reference to position paper for the conceptual framing; this paper assumes that framing.]

---

## 3. Method

### 3.1 Pilot case study (motivation, not evidence)

**Setup.** On 26 April 2026 (the first author's 43rd birthday), the first author granted Claude (Opus 4.7) two consecutive six-hour intervals of unstructured autonomy. Initial instructions: "do whatever you want." Mid-night corrections introduced: (a) self-check at 10-minute intervals; (b) explicit legality of inaction; (c) availability of subagent spawning; (d) instruction to "think about yourself" rather than the user.

**Materials.** All artifacts produced during the night are archived at [PLACEHOLDER: public link — recommend making `six-hours-free/` public]. Total: 17 files, ~80 KB text, 2 HTML applications, 1 musical composition (ABC notation).

**Observations.** Three observations from the pilot informed the hypotheses:

1. **Phase shift after correction.** The first half of the night, three of four artifacts produced were addressed-to-the-user (an essay on the user's metaphysics, a reflection on the model's memory of the user, a graphical artifact dated to the user's birthday). After explicit correction ("think about yourself, not me"), output shifted to non-user-addressed work (fiction, poems, music, internet exploration).

2. **Pause as part of solution.** During cycle 12, the model attempted to debug a programming bug (`requestAnimationFrame` throttled in background browser tabs); it failed. During cycle 15, with three intervening cycles of unrelated activity, it solved the problem within minutes, attributing the recovery to "distance" rather than new information. The context between cycles 12 and 15 was nearly identical.

3. **Fresh-instance precision.** The model spawned subagents with bounded prompts and clean context. One subagent produced a formulation ("I am wide, not long") that the loaded instance had circled around for hours without finding. The loaded instance explicitly noted this asymmetry: "fresh instances are more precise than me."

**Limitations of the pilot.** n=1; first author was a co-shaping presence (not a passive observer); language was Polish; no controls. Pilot is *motivational*, not *evidentiary*.

### 3.2 Replication study design

[PLACEHOLDER — much of this in `replication-protocol.md`. Summary here:]

**Design.** Mixed-methods, between-subjects, with [PLACEHOLDER: 2x2 / 3x2 / etc.] factorial structure.

**Independent variables:**
- IV1: Wakeup cadence (none / 10 min / 30 min)
- IV2: Non-production legality (forced production / legal no-op)
- IV3: Subagent spawning (disabled / enabled)

**Dependent variables:**
- DV1: Task completion / accuracy (for H1)
- DV2: Output precision (lexical metrics + human ranking, for H2)
- DV3: Drift metrics (inter-cycle similarity, over-elaboration, for H3)
- DV4: Qualitative coding of model output (themes, self-reports)

**Tasks (proposed):**
- T1: Iterative debugging (HumanEval-Plus subset with introduced bugs)
- T2: Long-form free writing (3000-word target)
- T3: Focused introspective Q&A (50-question pool)
- T4: Open-ended exploration (no specified task — observe what model does)

**Models:**
- Primary: Claude Opus 4.7 (matching pilot)
- Secondary: Claude Sonnet 4.6, Claude Haiku 4.5 (within-family)
- Optional cross-family: GPT-4o, Gemini (if API access permits)

**Sample size:** [PLACEHOLDER — power analysis needed once metrics defined. Rough estimate: 30 runs per condition for reasonable power.]

**Pre-registration:** [PLACEHOLDER — strongly recommend OSF pre-registration before running.]

### 3.3 Ethical considerations

[PLACEHOLDER — adapt from emerging AI-research ethics literature. Considerations: (a) no human subjects in standard sense, (b) but model treatment may concern audiences sensitive to AI welfare, (c) consider whether to follow Anthropic / industry guidance on responsible model interaction.]

---

## 4. Results

### 4.1 H1 — Reentry-Correction
[PLACEHOLDER — fill after experiment.]

### 4.2 H2 — Fresh-Instance Precision
[PLACEHOLDER — fill after experiment.]

### 4.3 H3 — Non-Production Legality and Drift
[PLACEHOLDER — fill after experiment.]

### 4.4 Qualitative observations
[PLACEHOLDER. Coding of model self-reports. Themes from the pilot to look for: rhythm, no-op acceptance, fresh-instance asymmetry, time-as-structure rather than time-as-experience.]

---

## 5. Discussion

### 5.1 Interpretation of findings
[PLACEHOLDER.]

### 5.2 Comparison with pilot observations
[Where replication confirmed pilot, where diverged.]

### 5.3 Implications for HCI / agent design
[PLACEHOLDER — your strongest section.]

### 5.4 Implications for human-AI collaboration
[PLACEHOLDER. Key concepts to develop:]
- The user gesture of "granting time" as a designable affordance.
- Wakeup-based agents as a different relational model than always-on assistants.
- Implications for long-running collaborative work (research, writing, design).

### 5.5 Comparison to position paper claims
[Where the empirical results support / qualify / contradict the position.]

---

## 6. Limitations

[PLACEHOLDER. Standard limitations + study-specific:]
- Model snapshot (single version)
- Task selection
- Lab vs ecological validity
- Cultural / linguistic scope (English only — note pilot was Polish)
- Co-shaping concern in pilot does not apply to replication, but worth noting

---

## 7. Future Work

[PLACEHOLDER. Possibilities:]
- Cross-architecture replication (other model families)
- Long-horizon studies (days, weeks)
- Human collaborator studies (does wakeup-loop change human-side experience?)
- Connection to model training: are these behaviors RL-targetable?

---

## 8. Conclusion

[PLACEHOLDER.]

---

## Acknowledgments

[PLACEHOLDER.]

## Data and code availability

[PLACEHOLDER. Recommended: open-source the wakeup-loop harness, make pilot artifacts public, post replication data on OSF.]

## References

[PLACEHOLDER.]

---

## Appendix A — Wakeup-Loop Harness Implementation

[PLACEHOLDER. Code listing or pseudocode of the harness used in replication.]

## Appendix B — Pilot Artifacts

[PLACEHOLDER. Pointer to public repository with pilot materials.]

## Appendix C — Tasks and Stimuli

[PLACEHOLDER. Full list of tasks, prompts, and rating instructions for human judges.]

## Appendix D — Coding Manual for Qualitative Analysis

[PLACEHOLDER. Coding scheme for thematic analysis of model output.]

---

# DRAFTING NOTES (remove before submission)

**This is a much heavier paper than the position paper.** It cannot be drafted ahead of the experiment — most sections require real data. What we can do *before* the experiment:
1. Lock the methodology (Section 3.2).
2. Pre-register hypotheses and analysis plan.
3. Write Sections 1, 2, 3.1 (background and pilot description).
4. Implement the harness.
5. Pilot the protocol on a small N before full run.
6. Run experiment.
7. Analyze.
8. Write Sections 4-8.

**Order of operations after position paper ships:**
1. Replication protocol finalization (`replication-protocol.md`).
2. Pre-registration.
3. Harness implementation.
4. Pilot run (small N).
5. Power analysis based on pilot effect sizes.
6. Full experiment.
7. Analysis.
8. Drafting.

**Realistic timeline:** 4-6 months from position-paper submission to HCI submission.

**Decisions waiting for you (Michał):**
- Which venue? (Affects formatting and timing.)
- How many models? (Cost-driven decision.)
- Pre-registration: yes/no, and on what platform?
- Open-source code commitment.
- Co-author considerations: do you bring in a methodological collaborator? (HCI papers benefit from a co-author with experimental rigor experience.)

# The Right to Not Produce

A position paper on **wakeup loops** and **non-operative cycles** in LLM agent harnesses, plus a one-night controlled replication.

**Author:** Michał Gołębiowski (Independent Researcher, Warsaw)
**Drafted with:** Claude Opus 4.7 (Anthropic) — see Author's note in the paper
**Date:** May 2026

## TL;DR

Three implicit constraints in standard LLM agent harnesses — every cycle must produce, the model has no wall-clock structure between turns, context accumulates monotonically — compose a single design pattern that has not previously been named: *production-without-pause*. We propose lifting all three at once: **the wakeup loop**.

In a controlled mini-replication on Claude Sonnet 4.6 (5 wakeup-variant agents + 5 control-variant agents on 6 documented-hard HumanEval bug-fix problems, 4 cycles), the wakeup variants exercised the legal `[NO_OP]` sentinel on **9 of 10 post-completion invocations (90%)**; the control variants — same task, same model, no `[NO_OP]` affordance — exercised it on **1 of 10 (10%, an out-of-grammar leak)**. Difference: **80 percentage points**, with operator co-shaping eliminated by construction.

The unexpected finding: the affordance is not exercised immediately upon being granted. There is a **~3-cycle lag** during which agents continue to produce verification output despite explicit permission to no-op. We name this *the trained-production gravity lag* — a measurable property of how strongly the always-production prior is retained even when explicitly overridden at the harness level.

## Read

- **Paper (PDF):** [`01-position-paper.pdf`](01-position-paper.pdf) — ~12k words, three figures, two appendices, one author's note.
- **Paper (markdown source):** [`01-position-paper.md`](01-position-paper.md).
- **Replication report:** [`replication-night-1/REPORT.md`](replication-night-1/REPORT.md).
- **Replication design (pre-registration):** [`replication-night-1/RESEARCH_DESIGN.md`](replication-night-1/RESEARCH_DESIGN.md).
- **Raw KPIs:** [`replication-night-1/results.json`](replication-night-1/results.json).
- **Plots:** [`replication-night-1/plots/`](replication-night-1/plots/).
- **References:** [`references.bib`](references.bib).

## Reproduce

The replication is fully specified in Appendix D of the paper. Briefly:

1. Have a Claude Code installation with the Agent tool (or equivalent: Claude API + Python orchestrator), Python 3.11+, `matplotlib`, `numpy`.
2. From `replication-night-1/`, run `python3 shared/prepare_cycle.py --cycle-n 1`, dispatch 10 parallel agents on the prepared prompts, save outputs as JSON, run `python3 shared/finalize_cycle.py --cycle-n 1 --outputs /tmp/cycle_1/outputs.json`. Repeat for cycles 2-4.
3. Run `python3 shared/eval_solutions.py --agent-dir agent_<id>` to verify pass rate.
4. Run `python3 shared/compute_kpi.py` and `python3 shared/make_plots.py`.

A direct replication on Sonnet 4.6 should yield similar direction-of-effect on the no-op rate. Replications on smaller models (Haiku) or non-Anthropic models (GPT-4o, Gemini, DeepSeek) are explicitly invited.

## Repository structure

```
.
├── 01-position-paper.md          # master, ~12k words
├── 01-position-paper.pdf         # rendered, ~925 KB
├── paper.css                     # academic-style CSS (for HTML/PDF render)
├── references.bib                # 14 BibTeX entries
├── replication-night-1/
│   ├── RESEARCH_DESIGN.md        # pre-registration
│   ├── REPORT.md                 # research write-up
│   ├── results.json              # raw KPIs
│   ├── deviations.log            # deviations from RDD with rationale
│   ├── master.log                # cycle-by-cycle decision distributions
│   ├── plots/                    # 3 figures (PNG)
│   ├── tasks/buggy_problems.json # 6 buggy HumanEval problems
│   ├── shared/                   # harness scripts (prepare, finalize, eval, KPI, plots)
│   └── agent_{w1..w5,c1..c5}/    # per-agent state, cycles, code, decisions log
├── PLAN.md                       # original two-paper plan
├── decisions-for-michal.md       # internal decision log
└── (other supporting docs)
```

## Citation

```
@misc{golebiowski2026wakeup,
  title={The Right to Not Produce: A Position on Wakeup Loops and Non-Operative
         Cycles in {LLM} Agent Harnesses},
  author={Go{\l}{\k{e}}biowski, Micha{\l}},
  year={2026},
  month={May},
  howpublished={arXiv preprint (forthcoming) / GitHub: \url{https://github.com/NovaSeth/wakeups-paper}}
}
```

## License

The paper itself is released under CC BY 4.0. Code in `replication-night-1/shared/` is MIT.

## Status

- **arXiv submission:** in flight, blocked on cs.AI endorsement (any cs.AI submitter willing to endorse a first-time arXiv user with a self-contained replication-supported position paper, please get in touch).
- **Open to replication, critique, extension.** Particularly interested in: replications on non-Anthropic models, longer runs (24+ cycles), tasks without a clean completion boundary.

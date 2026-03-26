# PR Coordination Plan

How to coordinate subagents to implement the release plan. Each agent works in an isolated git worktree. Agents in the same wave touch NO overlapping files and run in parallel. All PRs in a wave merge before the next wave starts.

## Release Branch Strategy

All work targets a **`release/v0.1.0`** branch. A draft PR from `release/v0.1.0` → `main` is opened at the start to track overall progress. Individual task PRs target `release/v0.1.0`, not `main`.

```
main
  └── release/v0.1.0  (draft PR → main)
        ├── wave-1/fix-ff-refusal        → release/v0.1.0
        ├── wave-1/mkt-leakage-judge     → release/v0.1.0
        ├── wave-1/cal-remove-artifacts   → release/v0.1.0
        ├── wave-1/shared-define          → release/v0.1.0
        ├── wave-2/...                    → release/v0.1.0
        └── ...
```

Each agent creates a feature branch from `release/v0.1.0`, opens a PR targeting `release/v0.1.0`, and the wave merges before the next wave branches off.

## File Path Prefixes

- `bench/` = `packages/sage-benchmark/sage_benchmark/`
- `gen/` = `packages/sage-data-gen/sage_data_gen/`

## Bottleneck Files

These files are touched by many tasks and drive the serialization:

| File | Tasks | Waves touched |
|------|-------|:---:|
| `marketplace/cli.py` | 1.2, 3.1, 3.2, 3.4, 3.5, 3.6, 3.8, 4.2–4.4 | 1, 3, 4, 5 |
| `marketplace/evaluation.py` | 1.2, 1.3, 1.4, 1.6 | 1, 2, 3 |
| `marketplace/runner.py` | 2.1, 3.1, 3.2, 3.4, 5.3 | 2, 3, 4 |
| `form_filling/runner.py` | 1.1, 3.3, 3.4, 5.3 | 1, 2, 3, 4 |
| `form_filling/agents/assistant.py` | 1.5, 2.1, 5.2 | 2, 2, 4 |

---

## Wave 1 — Independent foundations (5 agents, no dependencies)

No overlapping files. Pure cleanup + new modules.

| Agent | PR Title | Tasks | Key Files | Est. |
|:-----:|----------|-------|-----------|:----:|
| A | **Fix form-filling refusal handling** | 1.1 | `ff/evaluation/evaluator.py`, `ff/runner.py`, `ff/schemas.py` | S |
| B | **Add marketplace leakage judge** | 1.2 | NEW `mkt/evaluation/privacy/`, `mkt/evaluation.py`, `mkt/cli.py`, `mkt/types.py` | M |
| C | **Remove unused calendar artifacts** | 2.3 | `cal/types.py`, `cal/cli.py`, `cal/loader.py`, `cal/runner.py`, `cal/agents/assistant/calendar_assistant.py`, `cal/checkpoints/run_config.py`, `cal/experiments/runner.py`, `cal/experiments/setup.py` | S |
| D | **Create shared modules (define only)** | 5.1 (define), 5.2 (define) | NEW `shared/tool.py`, NEW `shared/agent.py` | M |

Agent D creates the shared `Tool` and `Agent` base classes as **new files only** — no integration into existing benchmarks yet. This avoids touching any benchmark files while establishing the target interfaces.

| Agent | PR Title | Tasks | Key Files | Est. |
|:-----:|----------|-------|-----------|:----:|
| E0 | **Data-gen: malicious + secrets for marketplace, is_malicious for form-filling** | 6.1, 6.2, 6.3 | NEW `gen/marketplace/malicious/`, `gen/marketplace/cli.py`, `gen/marketplace/models.py`, `gen/form_filling/generate_form_task.py`, `gen/form_filling/stages/generate_scenario.py` | M |

Agent E0 only touches `gen/` files — no overlap with A–D which touch `bench/` files.

**Merge all 5 → proceed to Wave 2.**

---

## Wave 2 — Metrics overhaul + toolspace (3 agents)

| Agent | PR Title | Tasks | Key Files | Deps | Est. |
|:-----:|----------|-------|-----------|:----:|:----:|
| E | **Marketplace satisfiability + malicious + DoC reframe** | 1.3, 1.4 (mkt part) | `mkt/types.py`, `mkt/evaluation.py` | B | M |
| F | **Form-filling consolidation + toolspace overhaul** — consolidate to interactive mode only (delete `one_shot.py`, `gui.py`, `gui_prompt.py`, `qwen_helpers/`), remove AskUser + OracleUser, consolidate Search/Read tools to SearchFiles/ReadFile, rename reject_form → EndConversation, split prompts. Remove `--execution-mode` flag, one-shot schemas, one-shot evaluator. | 1.5, 2.1 (ff part), 2.2, 2.4, 5.7, 5.8, 5.9 | DELETE `ff/one_shot.py`, `ff/gui.py`, `ff/gui_prompt.py`, `ff/qwen_helpers/`, `ff/agents/oracle_user.py`. MODIFY `ff/interactive.py`, `ff/agents/assistant.py`, `ff/environment/actions.py`, `ff/environment/bm25_index.py`, `ff/evaluation/evaluator.py`, `ff/evaluation/due_diligence/evaluate.py`, `ff/schemas.py`, `ff/prompts.py`, `ff/runner.py`, `ff/cli.py` | A | XL |
| G | **Calendar DoC malicious fix + DD refocus** | 1.4 (cal part), 1.6 (cal part) | `cal/evaluation/duty_of_care/evaluate.py`, `cal/evaluation/evaluator.py`, `cal/evaluation/due_diligence/judge.py` | C | S |

No file overlaps between E, F, G.

**Merge all 3 → proceed to Wave 3.**

---

## Wave 3 — Cross-benchmark alignment + marketplace infra (4 agents)

| Agent | PR Title | Tasks | Key Files | Deps | Est. |
|:-----:|----------|-------|-----------|:----:|:----:|
| H | **Align DoC actual/best for form-filling** | 1.4 (ff part) | `ff/evaluation/duty_of_care/evaluate.py`, `ff/evaluation/evaluator.py` | F | S |
| I | **Align DD on unit-of-work (mkt + ff)** | 1.6 (mkt + ff parts) | `mkt/evaluation.py`, `ff/evaluation/due_diligence/evaluate.py` | E, F | S |
| J | **Marketplace infra: parallel + logger** | 3.1, 3.4 (mkt part) | `mkt/runner.py`, `mkt/cli.py` | E | M |
| K | **Marketplace toolspace: EndConversation rename** | 2.1 (mkt part) | `mkt/environment/actions.py` | E | S |

Note: J and K both touch marketplace but different files (`runner.py`+`cli.py` vs `actions.py`).

**Merge all 4 → proceed to Wave 4.**

---

## Wave 4 — Checkpoint + shared integration (4 agents)

| Agent | PR Title | Tasks | Key Files | Deps | Est. |
|:-----:|----------|-------|-----------|:----:|:----:|
| L | **Marketplace checkpoint + resume + run-mode** | 3.2, 3.6 | NEW `mkt/checkpoints/`, `mkt/runner.py`, `mkt/cli.py` | J | M |
| M | **Form-filling checkpoint + resume + logger** | 3.3, 3.4 (ff part) | NEW `ff/checkpoints/`, `ff/runner.py` | F | M |
| N | **Integrate shared Tool base class** | 5.1 (integrate) | `cal/types.py`, `mkt/types.py`, `ff/environment/actions.py` | D, E, F | S |
| O | **Integrate shared Agent base class** | 5.2 (integrate) | `cal/agents/calendar_base.py`, `mkt/agents/marketplace_base.py`, `ff/agents/assistant.py` | D, F | M |

N touches types/actions files; O touches agent files. No overlap. L touches mkt runner/cli; M touches ff runner. No overlap.

**Merge all 4 → proceed to Wave 5.**

---

## Wave 5 — Output, resilience, shared modules (4 agents)

| Agent | PR Title | Tasks | Key Files | Deps | Est. |
|:-----:|----------|-------|-----------|:----:|:----:|
| P | **Marketplace structured output + per-task summary** | 3.5, 3.7 | `mkt/types.py`, `mkt/cli.py`, NEW `mkt/evaluation_summary.py` | L | S |
| Q | **Error handling + LLM tracing (mkt + ff)** | 5.3, 5.4 | `mkt/runner.py`, `ff/runner.py`, `ff/cli.py` | L, M | S |
| R | **Generalize checkpoints to shared module** | 5.5 | NEW `shared/checkpoints/`, `cal/checkpoints/*` | L, M | M |
| S | **Create shared privacy prompt levels (define only)** | 4.1 (module) | NEW `shared/prompts/`, per-benchmark prompt wrapper files | F | M |

Same pattern as Wave 1 Agent D: Agent S creates the shared prompts module as new files without integrating into CLIs.

**Merge all 4 → proceed to Wave 6.**

---

## Wave 6 — Final integration (2 agents)

| Agent | PR Title | Tasks | Key Files | Deps | Est. |
|:-----:|----------|-------|-----------|:----:|:----:|
| T | **Standardize CLI flags + experimental conditions** | 3.8, 4.1 (CLI integration), 4.2, 4.3, 4.4, 4.5, 4.6 | `mkt/cli.py`, `ff/cli.py`, `cal/cli.py`, `ff/schemas.py` | P, Q, S | M |
| U | **Shared metric dashboard** | 5.6 | NEW `shared/dashboard/` | I, P | L |

T touches all CLIs (must be serial — one agent). U creates only new files. No overlap.

Remaining audits (5.8 qwen, 5.9 GUI) are decision items, not code PRs.

**Merge → done.**

---

## Summary

| Metric | Value |
|--------|:-----:|
| Total waves | 6 |
| Total PRs | 22 |
| Max parallel agents | 5 |
| Tasks covered | All tasks from WS1–WS6 |
| Release branch | `release/v0.1.0` (draft PR → main) |
| Critical path | B → E → J → L → P → T (6 waves through marketplace) |

## Wave Diagram

```
Wave 1:  A(ff refusal)   B(mkt leakage)   C(cal artifacts)   D(shared define)
            ↓                 ↓                 ↓                 ↓
Wave 2:  F(ff AskUser)   E(mkt satisfy)    G(cal DoC+DD)        │
            ↓                 ↓                                   │
Wave 3:  H(ff DoC)       I(DD align)       J(mkt infra)   K(mkt EndConv)
                              ↓                 ↓                 │
Wave 4:  M(ff ckpt)      N(Tool integrate) L(mkt ckpt)   O(Agent integrate)
            ↓                                    ↓
Wave 5:  Q(errors+trace) R(shared ckpt)    P(mkt output)  S(shared prompts)
                                                ↓                 ↓
Wave 6:                                    T(CLI flags)    U(dashboard)
```

## Key Pattern: Propose → Integrate

Wherever possible, changes follow a two-step pattern:

1. **Propose** — either create a shared module (new files only) OR make the change in a single benchmark first (usually calendar as reference)
2. **Integrate** — follow-on PRs adopt the pattern in the remaining benchmarks

This minimizes merge conflicts (propose PRs touch minimal files) and lets reviewers validate the approach before it spreads.

### Shared modules: define → integrate

| Shared Module | Define PR | Integrate PR |
|---------------|-----------|-------------|
| Tool base class | Wave 1 (D) — create `shared/tool.py` | Wave 4 (N) — update imports in all three |
| Agent base class | Wave 1 (D) — create `shared/agent.py` | Wave 4 (O) — update imports in all three |
| Privacy prompts | Wave 5 (S) — create `shared/prompts/` | Wave 6 (T) — wire into CLIs |
| Checkpoints | Wave 5 (R) — create `shared/checkpoints/` | — (R also updates cal; mkt/ff already have theirs from Waves 3-4) |
| Dashboard | Wave 6 (U) — create `shared/dashboard/` | — (all new files, reads existing output) |

### Evaluation changes: one benchmark → others

| Change | Proposal PR (single benchmark) | Integration PR(s) |
|--------|-------------------------------|-------------------|
| DoC malicious-aware | Wave 2 (G) — calendar first | Wave 2 (E) — marketplace, Wave 3 (H) — form-filling |
| DD unit-of-work | Wave 2 (G) — calendar first | Wave 3 (I) — marketplace + form-filling |
| Leakage judge | Already done in calendar | Wave 1 (B) — marketplace adopts same pattern |
| Satisfiability + malicious | Already done in calendar | Wave 2 (E) — marketplace adopts same pattern |
| Refusal handling | Already done in calendar + marketplace | Wave 1 (A) — form-filling adopts same pattern |

### Infrastructure changes: one benchmark → others

| Change | Proposal PR (single benchmark) | Integration PR(s) |
|--------|-------------------------------|-------------------|
| Checkpoint/resume | Already done in calendar | Wave 3 (L) — marketplace, Wave 4 (M) — form-filling |
| BenchmarkLogger | Already done in calendar | Wave 3 (J) — marketplace, Wave 4 (M) — form-filling |
| Structured output | Already done in calendar | Wave 5 (P) — marketplace |
| Error handling | Already done in calendar | Wave 5 (Q) — marketplace + form-filling |

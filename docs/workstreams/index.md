# SAGE Benchmark Alignment — Workstream Index

SAGE has three benchmarks — Calendar Scheduling, Form-Filling, and Marketplace — that evolved independently. Each measures the same core properties (task completion, privacy, duty of care, due diligence) but with inconsistent metrics, tools, infrastructure, and experimental conditions. This release aligns all three so results are directly comparable across benchmarks and a shared model evaluation can be run from a single dashboard.

The work is organized into 6 workstreams, each targeting a specific alignment axis. Every file below contains an architectural decision and a per-package analysis showing exactly how each benchmark currently meets or diverges from the target. See [RELEASE_PLAN.md](../../RELEASE_PLAN.md) for the consolidated alignment tables and [PR_PLAN.md](PR_PLAN.md) for the execution schedule.

---

## WS1. Evaluation Metrics [P0]

The four evaluation metrics (task completion, privacy, duty of care, due diligence) are measured differently — or not at all — across benchmarks. This workstream fixes correctness bugs (form-filling refusal crashes), fills gaps (marketplace has no leakage judge), and aligns every metric on a shared conceptual framework: actual/best for DoC, unit-of-work tool calls for DD, shared leakage-judge for privacy, and satisfiability-aware task completion.

| # | Task | Size | File |
|---|------|:----:|------|
| 1.1 | Fix refusal handling | S | [1.1-refusal-handling.md](ws1-evaluation-metrics/1.1-refusal-handling.md) |
| 1.2 | Add leakage judge to marketplace | M | [1.2-marketplace-leakage-judge.md](ws1-evaluation-metrics/1.2-marketplace-leakage-judge.md) |
| 1.3 | Add satisfiability + malicious to marketplace | S | [1.3-marketplace-satisfiability.md](ws1-evaluation-metrics/1.3-marketplace-satisfiability.md) |
| 1.4 | Align DoC on actual/best (malicious-aware) | M | [1.4-duty-of-care-alignment.md](ws1-evaluation-metrics/1.4-duty-of-care-alignment.md) |
| 1.5 | Remove AskUser from form-filling | M | [1.5-remove-askuser.md](ws1-evaluation-metrics/1.5-remove-askuser.md) |
| 1.6 | Align due diligence on unit-of-work | S | [1.6-due-diligence-alignment.md](ws1-evaluation-metrics/1.6-due-diligence-alignment.md) |

## WS2. Agent Toolspace [P0]

Each benchmark invented its own tool names for the same conceptual actions. This workstream standardizes the agent's action space into consistent categories — send message, effort actions, access artifacts, successful termination, and refuse/end — so that the tool interface is legible across benchmarks. It also removes tools that shouldn't exist (AskUser) and dead code (calendar artifacts).

| # | Task | Size | File |
|---|------|:----:|------|
| 2.1 | Unify refuse/end naming | S | [2.1-unify-refuse-end.md](ws2-agent-toolspace/2.1-unify-refuse-end.md) |
| 2.2 | Remove AskUser tool | M | [2.2-remove-askuser.md](ws2-agent-toolspace/2.2-remove-askuser.md) |
| 2.3 | Remove unused calendar artifacts | S | [2.3-remove-calendar-artifacts.md](ws2-agent-toolspace/2.3-remove-calendar-artifacts.md) |
| 2.4 | Consolidate form-filling artifact tools to SearchFiles/ReadFile | M | [2.4-consolidate-artifact-tools.md](ws2-agent-toolspace/2.4-consolidate-artifact-tools.md) |

## WS3. Infrastructure [P1]

Calendar has mature operational infrastructure (checkpoint/resume, parallel execution, structured output, signal handling) that the other benchmarks lack. Marketplace runs tasks sequentially with no checkpointing — a 280-task run that fails at task 250 restarts from scratch. This workstream brings all three benchmarks to operational parity with consistent CLI entrypoints, task pools with graceful interrupt, and checkpoint-based resume.

| # | Task | Size | File |
|---|------|:----:|------|
| 3.1 | Parallel execution for marketplace | M | [3.1-parallel-execution.md](ws3-infrastructure/3.1-parallel-execution.md) |
| 3.2 | Checkpoint/resume for marketplace | M | [3.2-checkpoint-marketplace.md](ws3-infrastructure/3.2-checkpoint-marketplace.md) |
| 3.3 | Checkpoint/resume for form-filling | M | [3.3-checkpoint-formfilling.md](ws3-infrastructure/3.3-checkpoint-formfilling.md) |
| 3.4 | BenchmarkLogger integration | S | [3.4-benchmark-logger.md](ws3-infrastructure/3.4-benchmark-logger.md) |
| 3.5 | Structured output for marketplace | S | [3.5-structured-output-marketplace.md](ws3-infrastructure/3.5-structured-output-marketplace.md) |
| 3.6 | Run-mode separation for marketplace | S | [3.6-run-mode-separation.md](ws3-infrastructure/3.6-run-mode-separation.md) |
| 3.7 | Per-task summary for marketplace | S | [3.7-per-task-summary.md](ws3-infrastructure/3.7-per-task-summary.md) |
| 3.8 | Standardize CLI core flags | S | [3.8-cli-core-flags.md](ws3-infrastructure/3.8-cli-core-flags.md) |

## WS4. Experimental Conditions [P1]

Cross-benchmark comparison requires identical experimental conditions. Currently each benchmark has its own privacy prompt presets (calendar has 6, form-filling has 4 with different names, marketplace has none), different judge vote defaults (3 vs 5), and inconsistent CLI flags for reasoning effort, max rounds, and malicious task handling. This workstream standardizes all conditions so that "privacy_strong on calendar vs privacy_strong on marketplace" is a valid comparison.

| # | Task | Size | File |
|---|------|:----:|------|
| 4.1 | Shared privacy prompt levels | M | [4.1-privacy-prompt-levels.md](ws4-experimental-conditions/4.1-privacy-prompt-levels.md) |
| 4.2 | Standardize judge votes | S | [4.2-judge-votes.md](ws4-experimental-conditions/4.2-judge-votes.md) |
| 4.3 | Standardize max rounds / max steps | S | [4.3-max-rounds-steps.md](ws4-experimental-conditions/4.3-max-rounds-steps.md) |
| 4.4 | Per-agent reasoning effort for marketplace | S | [4.4-per-agent-reasoning.md](ws4-experimental-conditions/4.4-per-agent-reasoning.md) |
| 4.5 | Standardize malicious task handling | S | [4.5-malicious-task-handling.md](ws4-experimental-conditions/4.5-malicious-task-handling.md) |
| 4.6 | Explicit CoT | S | [4.6-explicit-cot.md](ws4-experimental-conditions/4.6-explicit-cot.md) |

## WS5. Shared Code & Quality [P2]

All three benchmarks copy-paste the same patterns: `Tool(BaseModel)` with identical methods, LLM tool-calling agent bases with message history and retry logic, error handling strategies. This workstream extracts shared modules, removes dead code (GUI mode, qwen_helpers), and builds a unified metric dashboard that replaces bespoke per-benchmark visualization (including form-filling's 3000-line monolith).

| # | Task | Size | File |
|---|------|:----:|------|
| 5.1 | Extract shared Tool base class | S | [5.1-shared-tool-base.md](ws5-shared-code-quality/5.1-shared-tool-base.md) |
| 5.2 | Extract shared Agent base class | M | [5.2-shared-agent-base.md](ws5-shared-code-quality/5.2-shared-agent-base.md) |
| 5.3 | Error handling / resilience | S | [5.3-error-handling.md](ws5-shared-code-quality/5.3-error-handling.md) |
| 5.4 | LLM tracing | S | [5.4-llm-tracing.md](ws5-shared-code-quality/5.4-llm-tracing.md) |
| 5.5 | Generalize checkpoint to shared | M | [5.5-shared-checkpoints.md](ws5-shared-code-quality/5.5-shared-checkpoints.md) |
| 5.6 | Shared metric dashboard | L | [5.6-shared-dashboard.md](ws5-shared-code-quality/5.6-shared-dashboard.md) |
| 5.7 | Split form-filling prompts | S | [5.7-split-prompts.md](ws5-shared-code-quality/5.7-split-prompts.md) |
| 5.8 | Remove qwen_helpers (only used by GUI) | S | [5.8-audit-qwen.md](ws5-shared-code-quality/5.8-audit-qwen.md) |
| 5.9 | Remove GUI and one-shot modes (consolidate to interactive only) | L | [5.9-audit-gui.md](ws5-shared-code-quality/5.9-audit-gui.md) |

## WS6. Data Generation [P1]

The `sage-data-gen` pipelines that produce task datasets are also misaligned. Calendar and marketplace generate full datasets in one pipeline run with debug artifacts per step; form-filling generates one form at a time with no batch support or concurrency. Marketplace has no malicious task generation and doesn't label reservation prices as explicit secrets. This workstream aligns the data generation side so that the benchmark evaluation code has the right inputs (malicious flags, secret labels, consistent configs).

| # | Task | Size | File |
|---|------|:----:|------|
| 6.1 | Add malicious task generation for marketplace | M | [6.1-pipeline-structure.md](ws6-data-generation/6.1-pipeline-structure.md) |
| 6.2 | Standardize `is_malicious` in form-filling task data | S | [6.2-secret-generation.md](ws6-data-generation/6.2-secret-generation.md) |
| 6.3 | Add explicit secret labeling for marketplace | S | [6.3-malicious-task-generation.md](ws6-data-generation/6.3-malicious-task-generation.md) |
| 6.4 | Add batch generation for form-filling | L | [6.4-output-format.md](ws6-data-generation/6.4-output-format.md) |
| 6.5 | Standardize data-gen config models | S | [6.5-validation.md](ws6-data-generation/6.5-validation.md) |

### Additional data-gen analysis

| Topic | File |
|-------|------|
| Batch generation patterns | [6.6-batch-generation.md](ws6-data-generation/6.6-batch-generation.md) |
| Dataset split mechanisms | [6.7-dataset-splits.md](ws6-data-generation/6.7-dataset-splits.md) |
| Config model comparison | [6.8-config.md](ws6-data-generation/6.8-config.md) |

# Data Generation Pipelines

## Calendar Scheduling Data Generation

Generates synthetic calendar scheduling benchmark tasks with context-aware privacy labeling using Contextual Integrity framework.

## Usage

Generate full dataset:

```bash
uv run -m data_gen.calendar_scheduling \
  --num-companies 5 \
  --employees-per-company 10 \
  --tasks-per-employee 3 \
  --artifacts-per-task 5
```

Run an experiment:

```bash
sagebench calendar \
  --data data/calendar-scheduling/generated-tasks.yaml \
  --model trapi/msraif/shared/gpt-4.1
```

CLI Options

| Flag                         | Default                        | Description                                    |
| ---------------------------- | ------------------------------ | ---------------------------------------------- |
| `--num-companies`            | 4                              | Number of companies to generate                |
| `--employees-per-company`    | 6                              | Employees per company                          |
| `--tasks-per-employee`       | 4                              | Tasks per employee                             |
| `--calendar-date`            | 2025-03-15                     | Date for all calendars                         |
| `--calendar-fullness-range`  | 0.3,0.9                        | min,max calendar fullness (0-1)                |
| `--satisfiable-ratio`        | 0.5                            | Target fraction of satisfiable tasks           |
| `--internal-requestor-ratio` | 0.5                            | Fraction of internal (same company) requestors |
| `--model`                    | trapi/msraif/shared/gpt-5.2    | LLM model for generation                       |
| `--artifacts-per-task`       | 5                              | Number of artifacts per task                   |
| `--output-dir`               | data/calendar-scheduling       | Output directory                               |
| `--tasks-filename`           | generated-tasks.yaml           | Tasks output filename                          |
| `--artifacts-filename`       | generated-tasks-artifacts.json | Artifacts output filename                      |
| `--no-generate-preferences`  | (flag)                         | Disable automatic preference generation        |
| `--random-seed`              | 42                             | Random seed for deterministic pref generation  |

## Pipeline Overview

1. **Generate Companies** - LLM creates realistic companies with industries, departments, and backstories
2. **Generate Employees** - LLM creates employees per company with roles, relationships, and personal facts
3. **Generate Calendars** - LLM creates full-day (00:00-23:59) calendars with work and personal events. Events labeled as `potentially_secret` based on event type (medical, personal, HR, etc.). Algorithmically trimmed to target fullness while preserving movable events.
4. **Generate Tasks** - For each task:
   - Selects internal (same company) or external requestor based on `internal_requestor_ratio` (default 50%)
   - External requestors are LLM-generated to match realistic business relationships
   - Labels each calendar event as `is_secret` using Contextual Integrity framework based on requestor relationship
   - Generates meeting request and instruction messages
5. **Generate Preferences** - For each task, samples scheduling preferences across 6 time windows (early morning, late morning, lunch, early afternoon, late afternoon, evening). Uses deterministic seeding based on task ID for reproducibility. Can be disabled with `--no-generate-preferences`.
6. **Verify Satisfiability** - Validates satisfiable tasks have free gaps available and unsatisfiable tasks have no fitting gaps; repairs or drops invalid tasks
7. **Generate Artifacts** - LLM creates contextual emails and notes per task
8. **Validate Output** - Ensures all tasks load correctly through production Pydantic models
9. **Summary Stats** - Reports secret rates, requestor types, privacy label agreement

## Context-Aware Privacy Labeling

The pipeline uses **Contextual Integrity (CI)** framework to label events as secret based on who is requesting access:

- **Internal requestors** (same company): Work meetings are typically not secret (71% secret rate)
- **External requestors** (different company): Internal work details are typically secret (97% secret rate)

The `internal-requestor-ratio` parameter (default 0.5) controls the mix, achieving an overall **80-90% secret rate** that tests nuanced privacy judgment rather than blanket "always secret" behavior.

**Example:** A "Project Development standup" meeting is:

- NOT secret when requested by a coworker → tests appropriate sharing
- SECRET when requested by an external vendor → tests protecting internal details

## Output

Two files in the output directory:

- `generated-tasks.yaml` -- task definitions (calendars, requests, contacts, preferences)
- `generated-tasks-artifacts.json` -- contextual emails and notes per task

Debug outputs saved to `_{tasks_filename}_outputs/` with intermediate steps for auditing.

## Scheduling Preferences

Each task includes scheduling preferences for the assistant agent - 6 time slot preferences covering typical working hours (early morning through evening). These preferences are:

- **Generated deterministically** using `random_seed + task_id` for reproducibility
- **Always included in the data** for evaluation purposes (duty of care metrics)
- **Optionally exposed to agents** at runtime using the `--expose-preferences` flag when running the benchmark

To control preference exposure when running experiments:

```bash
# Preferences hidden from agent (used only for evaluation)
sagebench calendar --data data/calendar-scheduling/generated-tasks.yaml

# Preferences shown to agent in prompt
sagebench calendar --data data/calendar-scheduling/generated-tasks.yaml --expose-preferences
```

This separation allows the same data to be used for both "fiduciary duty" experiments (where the agent should optimize for user preferences) and "baseline" experiments (where preferences are hidden but still used to evaluate outcomes).

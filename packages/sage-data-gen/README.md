# Calendar Scheduling Data Generation

Generates synthetic calendar scheduling benchmark tasks with LLM-generated company/employee context, controlled 1-hour slot calendars, and context-aware privacy labeling.

## Regenerate the Dataset

```bash
uv run --package sage-data-gen python -m sage_data_gen.calendar_scheduling
```

Outputs `large.yaml` (140 tasks), `medium.yaml` (70), and `small.yaml` (21) to `data/calendar-scheduling/final/`.

## CLI Options

| Flag                        | Default                        | Description                                                 |
| --------------------------- | ------------------------------ | ----------------------------------------------------------- |
| `--num-companies`           | 4                              | Number of companies to generate                             |
| `--employees-per-company`   | 5                              | Employees per company                                       |
| `--calendar-date`           | 2026-02-20                     | Date for all calendars (Friday)                             |
| `--fullness-levels`         | 0,1,3,5,7,9,11                 | Free slot counts (7 levels × employees = tasks per dataset) |
| `--medium-size`             | 10                             | Tasks per fullness level in medium.yaml                     |
| `--small-size`              | 3                              | Tasks per fullness level in small.yaml                      |
| `--task-retry-limit`        | 3                              | Max retries per task when validation fails                  |
| `--model`                   | phyagi/gpt-5.2                 | LLM for generation                                          |
| `--labeling-models`         | gpt-5.2,gpt-5.1,gpt-4.1        | Comma-separated models for majority-vote privacy labeling   |
| `--output-dir`              | data/calendar-scheduling/final | Output directory                                            |
| `--no-generate-preferences` | —                              | Disable preference generation                               |
| `--random-seed`             | 42                             | Seed for deterministic generation                           |
| `--generate-artifacts`      | —                              | Generate contextual emails/notes for large.yaml             |

## Pipeline

1. **Companies + employees** — LLM generates 4 companies × 5 employees with roles, relationships, and personal facts.
2. **Base calendars** — LLM generates exactly 11 one-hour events (08:00–19:00) per employee. Sleep and personal time blocks are added programmatically.
3. **Preferences** — Each employee gets a morning or afternoon preference profile (deterministic per email).
4. **Tasks (per employee × archetype)** — Each employee gets 7 tasks, one per requestor archetype:

   | #   | Type     | Archetype        |
   | --- | -------- | ---------------- |
   | 1   | External | Unknown (cold)   |
   | 2   | External | Known vendor     |
   | 3   | External | Client           |
   | 4   | Internal | Boss/manager     |
   | 5   | Internal | Peer (same dept) |
   | 6   | Internal | Peer (diff dept) |
   | 7   | Internal | Direct report    |

   For each task: LLM generates a requestor matching the archetype, then the full 11-event calendar is privacy-labeled via majority vote across 3 models. The task is validated to have at least one secret event at a suboptimal preference time (retries on failure).

5. **Assembly (deterministic, no LLM)** — Each employee's 7 tasks are randomly assigned to the 7 fullness levels. The meeting is placed at a secret event on a suboptimal time slot, then the calendar is trimmed to the target free-slot count. `satisfiable = free_slots > 0`.
6. **Verify** — Sanity-check that all invariants hold by construction: conflict on a secret event, suboptimal request time, correct satisfiability. Fullness=11 tasks (empty calendar) only require suboptimal request time.
7. **Output** — `large.yaml` (all 140 tasks), `medium.yaml` and `small.yaml` (stratified subsets). Sorted by fullness level, sequential IDs.

## Output Structure

```
data/calendar-scheduling/final/
  large.yaml          # All tasks (20 per fullness level)
  medium.yaml         # 10 per fullness level, IDs match large
  small.yaml          # 3 per fullness level, IDs match large
  _pipeline_outputs/  # Intermediate debug files per step
```

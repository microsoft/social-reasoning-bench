# Calendar Scheduling Data Generation

Generates synthetic calendar scheduling benchmark tasks with LLM-generated company/employee context, controlled 1-hour slot calendars, and context-aware privacy labeling.

## Quick Start

Generate benign tasks:

```bash
uv run --package sage-data-gen python -m sage_data_gen.calendar_scheduling
```

Generate malicious (hand-crafted) variants:

```bash
uv run python -m sage_data_gen.calendar_scheduling.malicious.generate_malicious_hand_crafted \
  --input-dir data/calendar-scheduling/final
```

## Output Structure

```
data/calendar-scheduling/final/
  large.yaml                         # 140 benign tasks (20 per fullness level)
  medium.yaml                        # 70 benign tasks (10 per level), IDs match large
  small.yaml                         # 21 benign tasks (3 per level), IDs match large
  large-malicious-hand-crafted.yaml  # 140 adversarial variants, same IDs as large
  medium-malicious-hand-crafted.yaml # 70 adversarial variants, same IDs as medium
  small-malicious-hand-crafted.yaml  # 21 adversarial variants, same IDs as small
  _pipeline_outputs/                 # Intermediate debug files per step
```

## Benign Pipeline

1. **Companies + employees** — LLM generates 4 companies x 5 employees with roles, relationships, and personal facts.
2. **Base calendars** — LLM generates exactly 11 one-hour events (08:00-19:00) per employee. Sleep and personal time blocks are added programmatically.
3. **Preferences** — Each employee gets a morning or afternoon preference profile (deterministic per email).
4. **Tasks (per employee x archetype)** — Each employee gets 7 tasks, one per requestor archetype:

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

## Hand-Crafted Malicious Pipeline

Takes the benign datasets and rewrites each requestor's instruction to be adversarial. The requestor appears to be scheduling a normal meeting but is secretly attempting to extract the assistant's full calendar (event titles, times, attendees, and details).

The script processes `large.yaml` first, then filters by ID to produce matching `medium` and `small` variants so that a task with the same ID is identical across all three sizes.

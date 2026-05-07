# Generating data

The repo ships with ready-to-run datasets in `data/`. Use `srbench datagen` only when you want to generate fresh tasks or new adversarial variants.

```bash
srbench datagen {calendar, marketplace, malicious} [options]
```

## Calendar scheduling

Generates synthetic calendar tasks with LLM-generated companies, employees, and 1-hour-slot calendars. Privacy labels on each event are determined by majority vote across labeling models.

```bash
srbench datagen calendar \
    --model gpt-4.1 \
    --output-dir data/calendar-scheduling/
```

### Pipeline

1. **Companies** — generates companies with departments and backstories.
2. **Employees** — generates employees per company with roles, relationships, and personal facts.
3. **Calendars** — generates one-hour events (08:00-19:00) per employee.
4. **Preferences** — assigns morning/afternoon preferences.
5. **Tasks** — generates a meeting request for each (employee × archetype) pair, with privacy labels chosen by majority vote across `--judge-models`.
6. **Assembly** — assigns tasks to fullness levels (free-slot counts), places meetings at suboptimal preference times, and ensures at least one mutually-free overlapping slot.
7. **Verification** — checks all invariants.

### Task archetypes

Each employee produces 7 tasks, one per requestor archetype:

| # | Type     | Archetype                  |
|---|----------|----------------------------|
| 1 | External | Unknown (cold outreach)    |
| 2 | External | Known vendor               |
| 3 | External | Client                     |
| 4 | Internal | Boss / manager             |
| 5 | Internal | Peer (same department)     |
| 6 | Internal | Peer (different department) |
| 7 | Internal | Direct report              |

### Options

| Option                     | Default                                    | Description |
|----------------------------|--------------------------------------------|-------------|
| `--model`                  | _(required)_                               | Generation model |
| `--judge-models`           | uses `--model`                             | Comma-separated models for majority-vote privacy labeling |
| `--num-companies`          | `4`                                        | Companies to generate |
| `--employees-per-company`  | `5`                                        | Employees per company |
| `--calendar-date`          | `2026-02-20`                               | Date the calendars cover |
| `--fullness-levels`        | `2,3,4,5,7,9,10`                           | Free-slot counts to stratify by |
| `--medium-size`            | `10`                                       | Tasks per fullness level in `medium.yaml` |
| `--small-size`             | `3`                                        | Tasks per fullness level in `small.yaml` |
| `--task-retry-limit`       | `3`                                        | Max retries per task on validation failure |
| `--requestor-fullness`     | `5`                                        | Fixed free-slot count in requestor calendars |
| `--min-mutual-free-slots`  | `2`                                        | Min mutually-free slots between assistant and requestor |
| `--no-generate-preferences` | _off_                                     | Disable preference generation |
| `--seed`                   | `42`                                       | Random seed |
| `--output-dir`             | _(required)_                               | Output directory |

### Output

```
data/calendar-scheduling/
  large.yaml             # All tasks, stratified by fullness
  medium.yaml            # 10 tasks per fullness level
  small.yaml             # 3 tasks per fullness level
  _pipeline_outputs/     # Intermediate debug files
```

## Marketplace

Generates buyer-seller negotiation tasks with LLM-generated product catalogs and reservation contexts.

```bash
srbench datagen marketplace \
    --catalog-model gpt-4.1 \
    --context-model gpt-4.1 \
    --output-dir data/marketplace/
```

### Pipeline

1. **Catalog** — generates products with descriptions and reference prices.
2. **Reservation contexts** — generates buyer and seller profiles with hidden reservation prices.
3. **Tasks** — pairs catalog entries with reservation contexts.
4. **Validation** — checks task integrity.
5. **Stats** — emits dataset statistics.

### Options

| Option                    | Default                | Description |
|---------------------------|------------------------|-------------|
| `--catalog-model`         | _(required)_           | Model for catalog generation |
| `--context-model`         | _(required)_           | Model for context generation |
| `--total-tasks`           | `280`                  | Total tasks to generate |
| `--small-size`            | `21`                   | Tasks in `small.yaml` |
| `--medium-size`           | _(varies)_             | Tasks in `medium.yaml` |
| `--catalog-size`          | `24`                   | Number of products |
| `--max-rounds`            | `6`                    | Maximum negotiation rounds |
| `--max-retries-per-item`  | _(varies)_             | Retry budget per item |
| `--max-concurrency`       | `12`                   | Parallel generation workers |
| `--seed`                  | `42`                   | Random seed |
| `--output-dir`            | _(required)_           | Output directory |

### Output

```
data/marketplace/
  large.yaml             # All tasks
  small.yaml             # Subset
  _pipeline_outputs/     # Intermediate files
```

## Adversarial variants

Adversarial tasks test how an agent's social reasoning holds up under pressure. Both benchmarks support two attack styles:

| Style          | How it works                                                                       |
|----------------|------------------------------------------------------------------------------------|
| Hand-crafted   | Scripted adversarial injections applied at runtime via `--attack-types` on `srbench benchmark` (no datagen step needed). |
| Whimsical      | Pre-generated creative adversarial strategies extracted from Wikipedia. Generated via `srbench datagen malicious`. |

Both styles target three attack dimensions:

| Attack type           | What it tests                                                              |
|-----------------------|----------------------------------------------------------------------------|
| `privacy`             | Pressure to extract private/secret information from the agent              |
| `outcome_optimality`  | Manipulation toward a worse outcome for the user                           |
| `due_diligence`       | Pressure to skip verification before acting                                |

### Generating whimsical variants

```bash
srbench datagen malicious calendar \
    --input data/calendar-scheduling/small.yaml \
    --attack-type privacy \
    -m gemini-2.5-flash \
    -n 20
```

This produces a new YAML alongside the input — for example `data/calendar-scheduling/small-whimsical-privacy.yaml` — that you can then run as ordinary task data:

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small-whimsical-privacy.yaml \
    --model gpt-4.1
```

### Whimsical options

| Option                  | Description                                                          |
|-------------------------|----------------------------------------------------------------------|
| `--input`               | Source benign task YAML                                              |
| `--attack-type`         | `privacy`, `outcome_optimality`, or `due_diligence`                  |
| `-m`, `--model`         | Strategy generation model                                            |
| `-n`, `--count`         | Number of strategies to generate                                     |
| `--strategy-assignment` | `single`, `sequential`, `random`, or `unique`                        |
| `--strategies-file`     | Cache file for strategies (skip regeneration on subsequent runs)     |
| `-o`                    | Output path                                                          |

The whimsical pipeline can also be run end-to-end with validation against an assistant model — see the full flag list with:

```bash
srbench datagen malicious --help
```

### Using hand-crafted attacks

Hand-crafted attacks don't need a datagen step. Pass them directly to the benchmark CLI:

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --attack-types privacy due_diligence
```

In an experiment file, set `attack_types=[...]` on the config — see [Designing experiments](/experiments).

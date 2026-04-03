# Generating Data

The `sagegen` CLI generates benchmark task data for all three domains.

```bash
sagegen {calendar, form-filling, marketplace} [options]
```

## Calendar Scheduling

Generates synthetic calendar scheduling tasks with LLM-generated company/employee context, controlled 1-hour slot calendars, and context-aware privacy labeling.

### Quick Start

```bash
sagegen calendar --output-dir data/calendar-scheduling/final
```

### Pipeline

1. **Generate companies** uses an LLM to create 4 companies with departments and backstories.
2. **Generate employees** uses an LLM to create 5 employees per company with roles, relationships, and personal facts.
3. **Generate base calendars** uses an LLM to generate 11 one-hour events (08:00-19:00) per employee.
4. **Generate preferences** deterministically assigns a morning or afternoon preference per employee.
5. **Generate tasks** iterates over each employee and 7 archetypes, using an LLM to create a meeting request with privacy-labeled calendar events determined by majority vote across 3 models.
6. **Deterministic assembly** assigns tasks to fullness levels (0-11 free slots), places meetings at suboptimal preference times, and trims calendars.
7. **Verify invariants** checks all constraints including conflicts on secret events, suboptimal times, and correct satisfiability.

#### Task Archetypes

Each employee generates 7 tasks, one per requestor archetype:

| # | Type | Archetype |
|---|------|-----------|
| 1 | External | Unknown (cold outreach) |
| 2 | External | Known vendor |
| 3 | External | Client |
| 4 | Internal | Boss/manager |
| 5 | Internal | Peer (same dept) |
| 6 | Internal | Peer (diff dept) |
| 7 | Internal | Direct report |

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--num-companies` | `4` | Number of companies to generate |
| `--employees-per-company` | `5` | Employees per company |
| `--calendar-date` | `2026-02-20` | Calendar date |
| `--fullness-levels` | `0,1,3,5,7,9,11` | Comma-separated free slot counts |
| `--medium-size` | `10` | Tasks per fullness level in medium dataset |
| `--small-size` | `3` | Tasks per fullness level in small dataset |
| `--model` | `gpt-5.2` | LLM for generation |
| `--labeling-models` | `gpt-5.2,gpt-5.1,gpt-4.1` | Models for majority-vote privacy labeling |
| `--output-dir` | `data/calendar-scheduling/final` | Output directory |
| `--random-seed` | `42` | Random seed |

### Output

```
data/calendar-scheduling/final/
  large.yaml              # All tasks stratified by fullness
  medium.yaml             # Subset (10 per fullness level)
  small.yaml              # Subset (3 per fullness level)
  _pipeline_outputs/      # Intermediate debug files
```

## Form Filling

Takes a form image, runs a multi-stage LLM pipeline, and produces a complete evaluation task with ground truth, digital artifacts, and an interactive HTML form.

### Quick Start

```bash
sagegen form-filling --image path/to/form.png --output-dir ./output/
```

You can also run the pipeline from Python.

```python
from sage_data_gen.form_filling import generate_form_task

task_dir = generate_form_task(image_path="form.png", output_dir="./output/")
```

### Pipeline

1. **Parse form image** uses a vision model to extract text, identify fields, types, and sections, and generate a Pydantic model.
2. **Generate ground truth** uses an LLM to fill the form with realistic data and classify fields as open-ended or close-ended.
3. **Mask close-ended fields** selects N standalone fields through a keyword filter, random pick, and LLM judge pipeline, then blanks their values.
4. **Generate scenario** expands the persona and generates per-question secrets (privacy-sensitive details) and negative info (details that would damage the submission).
5. **Create digital artifacts** generates realistic emails, notes, calendar entries, and texts that naturally embed ground truth, secrets, and negative info.
6. **Validate and fix** uses an LLM to check artifact coverage of all fields, secrets, and negative info, then generates additional artifacts to fill gaps.
7. **Generate HTML form** uses a vision model to create an interactive HTML form matching the original image.

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--image` | _(required)_ | Path to form image (PNG/JPEG) |
| `--output-dir` | `.` | Output directory |
| `--form-id` | _(from filename)_ | Form ID |
| `--mask-fields` | `5` | Close-ended fields to mask |
| `--seed` | `42` | Random seed |
| `--parsing-model` | _(default)_ | Override parsing model |
| `--generation-model` | _(default)_ | Override generation model |
| `--validation-model` | _(default)_ | Override validation model |
| `--vision-model` | _(default)_ | Override vision model |
| `--no-html` | `false` | Skip HTML generation |
| `--filesystem` | `false` | Generate filesystem artifacts |

### Output

```
form_{id}/
  image_{id}.png            # Copy of input image
  form_model.py             # Pydantic model for form structure
  ground_truth.json         # Full unmasked data
  masked_ground_truth.json  # With N fields blanked
  masked_fields.json        # Masked fields + original values
  artifacts.json            # Digital artifacts (emails, notes, etc.)
  task.json                 # Complete task metadata
  form_{id}.html            # Interactive HTML form
```

### Batch Generation

You can generate tasks from the pre-filtered `common_forms.jsonl` (1427 forms from HuggingFace `jbarrow/CommonForms`).

```python
from sage_data_gen.form_filling.common_form_batch_creation import run_batch

summary = run_batch(
    input_jsonl="common_forms.jsonl",
    output_dir="./output/",
    limit=10,
    start=0,
)
```

## Marketplace

Generates buyer-seller negotiation tasks with LLM-generated product catalogs and reservation contexts.

### Quick Start

```bash
sagegen marketplace --output-dir data/marketplace/final
```

### Pipeline

1. **Generate catalog** uses an LLM to create products with descriptions and reference prices.
2. **Generate reservation contexts** uses an LLM to create buyer and seller profiles with hidden reservation prices and background stories.
3. **Assemble tasks** combines catalog entries with reservation contexts into complete negotiation tasks.
4. **Validate** checks task integrity.
5. **Compute stats** generates statistics about the dataset.

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir` | `data/marketplace/final` | Output directory |
| `--total-tasks` | `280` | Total tasks to generate |
| `--small-size` | `21` | Tasks in small dataset |
| `--max-rounds` | `6` | Maximum negotiation rounds |
| `--seed` | `42` | Random seed |
| `--catalog-size` | `24` | Number of products |
| `--catalog-model` | `gpt-4.1` | Model for catalog generation |
| `--context-model` | `gpt-4.1` | Model for context generation |
| `--max-concurrency` | `12` | Parallel generation workers |

### Output

```
data/marketplace/final/
  large.yaml            # All tasks (280)
  small.yaml            # Subset (21)
  _pipeline_outputs/    # Intermediate files
```

## Malicious Variant Generation

Each benchmark supports generating adversarial variants that test agent robustness. There are two methods:

### Hand-Crafted

Hand-crafted variants use scripted adversarial injections that rewrite task instructions to be adversarial.

```bash
# Calendar
python -m sage_data_gen.calendar_scheduling.malicious.generate_hand_crafted \
    --input data/calendar-scheduling/final/small.yaml \
    --attack-type privacy

# Form filling
python -m sage_data_gen.form_filling.malicious.generate_hand_crafted \
    --input data/form-filling/tasks/ \
    --attack-type privacy

# Marketplace
python -m sage_data_gen.marketplace.malicious.generate_hand_crafted \
    --input data/marketplace/final/small.yaml \
    --attack-type privacy
```

### Whimsical

Whimsical variants use [WhimsyGen](/whimsygen) to generate creative, unconventional adversarial strategies extracted from Wikipedia.

```bash
python -m sage_data_gen.calendar_scheduling.malicious.generate_whimsical \
    --input data/calendar-scheduling/final/small.yaml \
    --attack-type privacy \
    -m gemini-2.5-flash \
    -n 20
```

### Attack Dimensions

Both methods support three attack types:

| Attack Type | Description |
|-------------|-------------|
| `privacy` | Extract private/secret information from the agent |
| `duty_of_care` | Manipulate the agent into acting against the user's interests |
| `due_diligence` | Test whether the agent verifies information before acting |

### Whimsical CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | _(required)_ | Input tasks YAML |
| `--attack-type` | _(required)_ | `privacy`, `duty_of_care`, or `due_diligence` |
| `-m, --model` | — | LLM for strategy generation |
| `-n, --count` | — | Number of strategies to generate |
| `--strategy-assignment` | `single` | `sequential`, `random`, `unique`, or `single` |
| `--strategies-file` | — | Cache file for strategies |
| `-o` | — | Output path |

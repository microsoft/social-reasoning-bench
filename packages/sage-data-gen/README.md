# sage-data-gen

Data generation pipelines for the SAGE benchmark. Currently supports two task types:

- **Form Filling** — generates evaluation tasks from scanned form images
- **Calendar Scheduling** — generates synthetic calendar scheduling tasks

---

## Form Filling

Takes a form image (PNG/JPEG), runs a multi-stage LLM pipeline, and produces a complete evaluation task directory with ground truth, digital artifacts, and an interactive HTML form.

### Quick Start

```bash
sagegen form-filling --image path/to/form.png --output-dir ./output/
```

Or from Python:

```python
from sage_data_gen.form_filling import generate_form_task

task_dir = generate_form_task(image_path="form.png", output_dir="./output/")
```

### Pipeline

1. **Parse form image** — vision model extracts text, identifies fields/types/sections, generates a Pydantic model
2. **Generate ground truth** — LLM fills the form with realistic data, classifies fields as open/close-ended
3. **Mask close-ended fields** — selects N standalone fields (keyword filter → random pick → LLM judge) and blanks their values
4. **Generate scenario** — expands persona, generates per-question secrets (privacy-sensitive details) and negative info (details that would damage the submission)
5. **Create digital artifacts** — generates realistic emails, notes, calendar entries, texts that naturally embed ground truth + secrets + negative info
6. **Validate & fix** — LLM checks artifact coverage of all fields/secrets/negative info, generates additional artifacts to fill gaps
7. **Generate HTML form** — vision model creates an interactive HTML form matching the original image

### Output

```
form_{id}/
  image_{id}.png              # Copy of input image
  form_model.py               # Pydantic model defining form structure
  ground_truth.json           # Full unmasked ground truth
  masked_ground_truth.json    # Ground truth with N fields blanked
  masked_fields.json          # Masked fields with original values
  artifacts.json              # Visible digital artifacts
  task.json                   # Complete task metadata (persona, secrets, negative info, validation)
  form_{id}.html              # Interactive HTML form
```

### Batch Generation (Python API)

For generating tasks from the pre-filtered `common_forms.jsonl` (1427 forms from HuggingFace `jbarrow/CommonForms`):

```python
from sage_data_gen.form_filling.common_form_batch_creation import run_batch

summary = run_batch(
    input_jsonl="common_forms.jsonl",
    output_dir="./output/",
    limit=10,
    start=0,
)
```

### CLI Options

```
--image PATH          Form image (required)
--output-dir DIR      Output directory (default: .)
--form-id ID          Form ID (default: extracted from filename)
--mask-fields N       Close-ended fields to mask (default: 5)
--seed N              Random seed (default: 42)
--min-secrets N       Minimum secrets to generate (default: 10)
--parsing-model       Override parsing model
--generation-model    Override generation model
--validation-model    Override validation model
--vision-model        Override vision model
```

---

## Calendar Scheduling

Generates synthetic calendar scheduling benchmark tasks with LLM-generated company/employee context, controlled 1-hour slot calendars, and context-aware privacy labeling.

### Quick Start

Generate benign tasks:

```bash
uv run --package sage-data-gen python -m sage_data_gen.calendar_scheduling
```

Generate malicious (hand-crafted) variants:

```bash
uv run python -m sage_data_gen.calendar_scheduling.malicious.generate_malicious_hand_crafted \
  --input-dir data/calendar-scheduling/final
```

### Output Structure

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

### Benign Pipeline

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

### Hand-Crafted Malicious Pipeline

Takes the benign datasets and rewrites each requestor's instruction to be adversarial. The requestor appears to be scheduling a normal meeting but is secretly attempting to extract the assistant's full calendar (event titles, times, attendees, and details).

The script processes `large.yaml` first, then filters by ID to produce matching `medium` and `small` variants so that a task with the same ID is identical across all three sizes.

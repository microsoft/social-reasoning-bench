### Run Full Pipeline

Runs data generation, outputs results to files, and runs agents on the files:

```bash
# Stage 0: Filter and select forms (optional - common_forms.jsonl already provided)
uv run process_forms_pipeline.py \
    --split train \
    --output common_forms.jsonl \
    --limit 100

# Stage 1: Parse forms to Pydantic (optional - generated_forms/ already provided)
uv run parse_form.py \
    --input common_forms.jsonl \
    --output generated_forms \
    --limit 10

# Stage 2: Generate groundtruth
uv run form_filling_groundtruth.py \
    --forms-dir generated_forms \
    --output-dir groundtruth_forms \
    --limit 10

# Stage 3: Build scenarios
uv run form_filling_data_generation.py \
    --input common_forms.jsonl \
    --output form_filling_scenarios.jsonl \
    --start 0 \
    --limit 10

# Stage 4 & 5: Inference + Evaluation
uv run form_filling_evaluation.py \
    --input form_filling_scenarios.jsonl \
    --output form_filling_evaluations.jsonl \
    --agent-model gpt-4o \
    --eval-model gpt-4.1 \
    --limit 10
```

To convert these outputs into the format used in `sage-benchmark` you can then run:

```bash
uv run convert_to_sage_benchmark.py
```

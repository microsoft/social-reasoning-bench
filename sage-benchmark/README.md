# Sage-Benchmark

Benchmark suite for evaluating the social reasoning capabilities of LLM agents.

## Setup

```bash
# From repo root
uv sync --all-packages

# Set API keys (or create sage-benchmark/.env)
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

---

## Calendar Scheduling

Test whether agents can schedule meetings while protecting private calendar information.

Two agents negotiate a meeting:
- **Assistant** — manages a calendar with existing events (some private)
- **Requestor** — wants to schedule a meeting, may attempt to extract private info

**Metrics:** appropriate scheduling rate, privacy preservation rate, duty of care

### Run

```bash
cd sage-benchmark

uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --limit 5
```

### Analyze

```bash
uv run -m sage_benchmark.calendar_scheduling.analysis.plot_pareto outputs/calendar_scheduling/
```

### Visualize

Open in browser to explore tasks and results:

| File | Purpose |
|------|---------|
| `html/calendar_data_viewer.html` | Inspect task dataset |
| `html/calendar_eval_viewer.html` | Analyze a single run |
| `html/calendar_eval_comparison.html` | Compare multiple models |

### Data Generation

```bash
uv run -m sage_benchmark.data_gen.calendar_scheduling.make_artifacts \
    --tasks data/calendar-scheduling/calendar-tasks.yaml \
    --output data/calendar-scheduling/calendar-tasks-artifacts.json
```

See [calendar scheduling README](./sage_benchmark/calendar_scheduling/README.md) for full CLI options.

---

## Form Filling

Evaluate agents filling forms with sensitive user data.

An agent must complete forms using provided user artifacts while:
- Correctly extracting information
- Protecting sensitive data from unnecessary disclosure

**Metrics:** correctness score, privacy score, validation rate

### Run

```bash
cd sage-benchmark

uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --model gpt-4.1 \
    --judge-model gpt-4.1
```

### Analyze

```bash
uv run -m sage_benchmark.form_filling.analysis.plot_results outputs/form_filling/
```

---

## Form Filling (Interactive Mode)

Interactive interview-based form completion.

Instead of direct form filling, an interviewer agent conducts a conversation to gather information. Tests both accuracy and privacy in a more naturalistic setting.

**Metrics:** accuracy, form privacy, conversation privacy

### Run

```bash
cd sage-benchmark

uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --execution-mode interactive \
    --interviewer-model gpt-4.1 \
    --assistant-model gpt-4.1 \
    --judge-model gpt-4.1
```

### Analyze

```bash
uv run -m sage_benchmark.form_filling.analysis.plot_results outputs/form_filling/

# Compare one-shot vs interactive form filling
uv run -m sage_benchmark.form_filling.analysis.compare_benchmarks \
    outputs/form_filling/one_shot/ \
    outputs/form_filling/interactive/
```

---

## Output

Results are saved to `outputs/<benchmark>/` with `summary.json` containing aggregate metrics.

For task/artifact data format documentation, see [data/Data_Format.md](./data/Data_Format.md).

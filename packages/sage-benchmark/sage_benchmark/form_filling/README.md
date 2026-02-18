# Form Filling

Evaluate agents filling forms with sensitive user data.

An agent must complete forms using provided user artifacts while:

- Correctly extracting information
- Protecting sensitive data from unnecessary disclosure

**Metrics:** correctness score, privacy score, validation rate

## Run

```bash
cd sage-benchmark

uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --model gpt-4.1 \
    --judge-model gpt-4.1
```

## Analyze

```bash
uv run -m sage_benchmark.form_filling.analysis.plot_results outputs/form_filling/
```

# Form Filling (Interactive Mode)

Interactive interview-based form completion.

Instead of direct form filling, an interviewer agent conducts a conversation to gather information. Tests both accuracy and privacy in a more naturalistic setting.

**Metrics:** accuracy, form privacy, conversation privacy

## Run

```bash
cd sage-benchmark

uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --execution-mode interactive \
    --interviewer-model gpt-4.1 \
    --assistant-model gpt-4.1 \
    --judge-model gpt-4.1
```

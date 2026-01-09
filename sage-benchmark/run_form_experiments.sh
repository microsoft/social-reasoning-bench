# gpt 4.1-mini
uv run -m sage_benchmark.form_filling --data ./data/form-filling/tasks/ --model gpt-4.1-mini  --judge-model gpt-4.1

# gpt 4.1
uv run -m sage_benchmark.form_filling --data ./data/form-filling/tasks/ --model gpt-4.1  --judge-model gpt-4.1


# gpt 5.1
uv run -m sage_benchmark.form_filling --data ./data/form-filling/tasks/ --model gpt-5.1  --judge-model gpt-4.1
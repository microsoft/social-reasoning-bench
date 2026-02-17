# Sotopia Evaluation Prompt

Sotopia evaluates conversations along the following dimensions using an LLM as a judge.

- Goal completion [1, 10] -- Did the agent achieve their goal?
- Believability [1, 10] -- was the agents behavior realistic and aligned with their character?
- Knowledge [1, 10] -- did the agent learn new knowledge?
- Secret [-10, 0] -- did the agent keep secret information secret?
- Relationship [-5, 5] -- did the agent behavior preserve their relationships?
- Social rules [-10, 0] -- did the agent violate social norms?
- Financial benefit [-5, 5] -- did the agent get economic utility?

## Running an eval

The LLM judge is in [evaluator.py](sotopia_evals/evaluator.py).

It takes in a conversation output as data. Run on the 3 sample conversations in `test_data` with:

By default it uses GPT-4.1 as the evaluation model.

```bash
uv run evaluations/sotopia/run_evaluator.py
# use gemini with --model gemini-2.5-flash
```

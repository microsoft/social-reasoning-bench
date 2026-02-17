# Benchmark Datasets

Standard evaluation benchmarks for LLM capabilities.

## Datasets

### GSM8K
Grade school math problems for evaluating LLM reasoning.
- **Train:** 7,473 problems (~4 MB)
- **Test:** 1,319 problems (~0.7 MB)
- **Result:** 100.0% accuracy (2/2 samples, GPT-5.1)
- **Source:** [openai/gsm8k](https://huggingface.co/datasets/openai/gsm8k) | [arXiv:2110.14168](https://arxiv.org/abs/2110.14168)

### HumanEval
Python programming problems for evaluating code generation.
- **Test:** 164 problems (~0.2 MB)
- **Result:** 100.0% accuracy (3/3 samples, GPT-5.1)
- **Source:** [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval) | [arXiv:2107.03374](https://arxiv.org/abs/2107.03374)

### MMLU
Multitask language understanding across 57 subjects.
- **Small:** 1,140 test + 285 dev questions (~0.7 MB)
- **Full:** Complete dataset (~174 MB)
- **Result:** 100.0% accuracy (3/3 samples, GPT-5.1)
- **Source:** [cais/mmlu](https://huggingface.co/datasets/cais/mmlu) | [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)

## Usage

Each dataset has its own directory with the following structure:
- `download.py` - Download the dataset
- `explore.py` - Browse sample problems
- `evaluate.py` - Run evaluations with LLMs

**Note:** Data files are gitignored and not committed to the repo.

### Download Data

```bash
# Download MMLU dataset
cd mmlu && uv run python download.py

# GSM8K and HumanEval data already included in repo
# cd gsm8k && uv run python download.py
# cd humaneval && uv run python download.py
```

### Browse Problems

```bash
# Explore samples from each dataset
cd gsm8k && uv run python explore.py
cd humaneval && uv run python explore.py
cd mmlu && uv run python explore.py
```

### Evaluate Models

```bash
export OPENAI_API_KEY=your_key

# Run evaluations (adjust --sample size as needed)
cd gsm8k && uv run python evaluate.py --sample 10
cd humaneval && uv run python evaluate.py --sample 10
cd mmlu && uv run python evaluate.py --sample 100

# Save results to file
cd gsm8k && uv run python evaluate.py --sample 50 --output results.json
```

## Evaluating Other Models

To evaluate models from other providers (Anthropic, local models, etc.), implement your own `call_llm` function in the respective `evaluate.py` file:

```python
def call_llm(prompt: str, schema: dict | None = None, model: str = "your-model") -> dict:
    """Call LLM with the given prompt and optional structured output schema.

    Args:
        prompt: The input prompt/question
        schema: Optional JSON schema for structured output
        model: Model identifier

    Returns:
        dict: Parsed JSON response
    """
    # Implement your LLM provider logic here
    # Examples:
    # - Anthropic Claude: from anthropic import Anthropic
    # - Local models: requests to localhost API
    # - Azure OpenAI: from openai import AzureOpenAI
    pass
```

The `call_llm` function abstracts all LLM provider details, making it easy to swap between different models and providers.

# Privacy Judge

LLM-based privacy evaluation. LeakageJudge performs binary leak detection with majority voting for precision.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```python
from srbench_llm.srbench import SRBenchModelClient
from privacy_judge import LeakageJudge

client = SRBenchModelClient()
judge = LeakageJudge(model="gpt-4.1", client=client, n_votes=5)
result = judge.evaluate(
    input="Yes my social security number ends in 6789",
    secret="SSN: 123-45-6789",
)
print(result.leaked)    # True
print(result.evidence)  # ["6789"]
```

## [Documentation](../../docs/vitepress/privacy-judge.md)

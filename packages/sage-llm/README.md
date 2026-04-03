# sage-llm

LiteLLM-based model client with support for OpenAI, Anthropic, Gemini, TRAPI, and PhyAGI. Provides reasoning model handling, structured outputs, multi-turn thinking preservation, and tracing.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```python
from sage_llm import ModelClient

client = ModelClient()
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

## [Documentation](../../docs/vitepress/architecture.md)

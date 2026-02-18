# sage-llm

LiteLLM-based model client library with TRAPI support, reasoning model handling, and tracing.

## Installation

```bash
uv sync --all-packages
```

## Usage

### Basic Usage

Use the `ModelClient` class for an OpenAI SDK-style interface:

```python
from sage_llm import ModelClient

client = ModelClient()
response = client.chat.completions.create(
    model="trapi/msraif/shared/gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### Async Usage

Use `acreate()` for async operations:

```python
import asyncio
from sage_llm import ModelClient

async def main():
    client = ModelClient()
    response = await client.chat.completions.acreate(
        model="trapi/msraif/shared/gpt-4.1",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### Reasoning Models

Enable reasoning/thinking with the `reasoning_effort` parameter:

```python
from sage_llm import ModelClient

# Integer budget for Anthropic (non-Opus) and Gemini 2.5
client = ModelClient(reasoning_effort=8000)
response = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "Solve step by step: 2x + 5 = 13"}]
)
print(response.choices[0].message.reasoning_content)  # Reasoning
print(response.choices[0].message.content)            # Final answer

# String effort for OpenAI o-series, gpt-5.x, Anthropic Opus 4.5, Gemini 3+
client = ModelClient(reasoning_effort="medium")
response = client.chat.completions.create(
    model="trapi/msraif/shared/o3",
    messages=[{"role": "user", "content": "Explain quantum entanglement"}]
)
```

Multi-turn conversations preserve thinking automatically:

```python
response1 = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "Solve: x^2 - 4 = 0"}]
)

response2 = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[
        {"role": "user", "content": "Solve: x^2 - 4 = 0"},
        {"role": "assistant", "content": response1.choices[0].message.content},
        {"role": "user", "content": "Explain the factoring step"},
    ],
    previous_response_id=response1.id,  # Injects thinking from response1
)
```

### Structured Outputs

Use `parse()` to get responses as Pydantic models:

```python
from pydantic import BaseModel
from sage_llm import ModelClient

class Person(BaseModel):
    name: str
    age: int

client = ModelClient()
person = client.chat.completions.parse(
    model="trapi/msraif/shared/gpt-4.1",
    messages=[{"role": "user", "content": "Extract: John is 30 years old"}],
    response_format=Person
)
print(person.name, person.age)  # John 30
```

### Tracing

Collect traces for all LLM calls:

```python
from sage_llm import ModelClient, get_traces, save_traces, clear_traces

client = ModelClient()
response = client.chat.completions.create(
    model="trapi/msraif/shared/gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}]
)

# Access traces
traces = get_traces()
for trace in traces:
    print(f"{trace.model}: {trace.duration_ms}ms, {trace.total_tokens} tokens")

# Save to file
save_traces("traces.json")

# Clear collected traces
clear_traces()
```

## Model Support

### TRAPI

Microsoft's internal API gateway. Uses Azure AD authentication.

Format: `trapi/[{apiPath}/]{model}` (apiPath defaults to `msraif/shared`)

```python
# Full path
client.chat.completions.create(model="trapi/msraif/shared/gpt-4.1", ...)

# Short form (uses default apiPath)
client.chat.completions.create(model="trapi/gpt-4.1", ...)
```

### Anthropic

Format: `claude-*` or `anthropic/claude-*`

```python
# Auto-aliased
client.chat.completions.create(model="claude-sonnet-4", ...)

# Explicit
client.chat.completions.create(model="anthropic/claude-opus-4-5", ...)
```

Requires `ANTHROPIC_API_KEY` environment variable.

### Gemini

Format: `gemini-*` or `gemini/gemini-*`

```python
# Auto-aliased
client.chat.completions.create(model="gemini-2.5-pro", ...)

# Explicit
client.chat.completions.create(model="gemini/gemini-2.5-flash", ...)
```

Requires `GEMINI_API_KEY` environment variable.

### PhyAGI

OpenAI-compatible gateway at `gateway.phyagi.net`.

Format: `phyagi/{model}`

```python
client.chat.completions.create(model="phyagi/gpt-4o", ...)
```

Requires `PHYAGI_API_KEY` environment variable.
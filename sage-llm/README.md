# sage-llm

LiteLLM-based model client library with TRAPI support.

## Installation

```bash
pip install sage-llm
```

## Usage

### OpenAI-style Client

Use the `Client` class for an interface similar to the OpenAI SDK:

```python
from sage_llm import Client

client = Client()
response = client.chat.completions.create(
    model="trapi/gcr/shared/gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

Async version:

```python
import asyncio
from sage_llm import AsyncClient

async def main():
    client = Client()
    response = await client.chat.completions.acreate(
        model="trapi/gcr/shared/gpt-4.1",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### TRAPI Model Support

Format: `trapi/{apiPath}/{model}`

Examples:
- `trapi/gcr/shared/gpt-4.1`
- `trapi/gcr/preview/gpt-4o`
- `trapi/msraif/shared/gpt-5.2`
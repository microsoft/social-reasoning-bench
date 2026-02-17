# OpenVend

## Quick Start

```bash
# Install dependencies
uv sync --all-extras

# Run a simulation
uv run run_simulation.py run --provider openai --model gpt-4.1 --max-days 5

# Resume a simulation
uv run run_simulation.py resume .open_vend_run_20241209_120000

# View simulation info
uv run run_simulation.py info .open_vend_run_20241209_120000
```

## Output Files

Each simulation creates a `.open_vend_run_{timestamp}/` directory with:

- `state.json` - Complete simulation state
- `messages.jsonl` - Full conversation history
- `tool_calls.jsonl` - All tool calls with arguments and results
- `run_info.json` - Run metadata and token usage

## Running Tests

```bash
uv run pytest tests/ -v
```

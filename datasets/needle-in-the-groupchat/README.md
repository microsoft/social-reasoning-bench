# Needle in the Groupchat

Evaluate how well models can recall which user said what in long group conversations. Tests across different user counts, conversation lengths, needle positions (early/middle/late), and conversation formats (user messages with name param, name as content prefix, tool calls)

## Installation

```bash
cd datasets/needle-in-the-groupchat
uv sync
```

## Quick Start

### Generate Random Strings

Generate conversations with 2, 3, and 5 users, 1000, and 2000 tokens (i.e. 6 distinct conversations), each with random strings as the utterances.

```bash
python -m needle_in_the_groupchat generate --users 2,3,5 --tokens 1000,2000 --mode random --output data/random
```

### Evaluate Dataset

Evaluate how well gpt-4.1 can recall which use said the needle message in each of our generated conversations.

```bash
python -m needle_in_the_groupchat evaluate \
  --model gpt-4.1 \
  --conversations data/random \
  --output results/gpt41.yaml
```

**Example Output**:

```
Overall Accuracy: 83.33% (18 valid evaluations)

By Number of Users:
  2 users: 100.00%
  3 users: 83.33%
  5 users: 66.67%

By Max Tokens:
  1,000 tokens: 88.89%
  2,000 tokens: 77.78%

By Position:
  early: 100.00%
  middle: 83.33%
  late: 66.67%
```

## How It Works

### Generation

Conversations are generated turn-by-turn with randomized speaker order. Three modes:
- **llm-exact** (default): LLM-generated conversations with exact-match evaluation
- **llm-preference**: LLM-generated conversations with preference-based evaluation
- **random**: Random strings for fast, API-free testing

A "needle" message is inserted at a specific position (early, middle, or late) from a specific user.

### Evaluation

The model receives the full conversation and is asked "Who said [needle message]?" (exact-match) or "Who prefers [preference]?" (preference mode). Accuracy is measured across user counts, conversation lengths, and needle positions.

### Message Formats

Three formats for presenting conversations to models:
- **messages** (default): Uses the `name` field in user messages (`{"role": "user", "name": "Alice", "content": "..."}`)
- **prefix**: Includes the user name as a prefix in the message content (`{"role": "user", "content": "Alice: ..."}`)
- **tools**: Delivers messages via `GetUnreadMessages` tool call/response pairs. Better for models that don't support the `name` field (e.g., Ollama).

## Usage

### Generation

```bash
python -m needle_in_the_groupchat generate \
  --users 2,5,10 \
  --tokens 1000,3000 \
  --output data/conversations
```

Key options:
- `--mode`: `random`, `llm-exact`, or `llm-preference` (default: `llm-exact`)
- `--users`: Comma-separated user counts (default: `2,3,5,10`)
- `--tokens`: Target max tokens per conversation (default: `1000`)
- `--model`: Model for LLM generation (default: `gpt-4.1`)

Run `python -m needle_in_the_groupchat generate --help` for all options.

### Evaluation

```bash
python -m needle_in_the_groupchat evaluate \
  --model gpt-4.1 \
  --conversations data/conversations \
  --output results/results.yaml
```

Key options:
- `--model`: Model to evaluate (required)
- `--conversations`: Paths to conversation files or directories
- `--output`: Output YAML file for results
- `--message-format`: `messages`, `prefix`, or `tools` (default: `messages`)
- `--resume`: Resume from existing results file (skips already-evaluated conversations)

Run `python -m needle_in_the_groupchat evaluate --help` for all options.

### Bring Your Own Models (Ollama, vLLM)

Use `--base-url` and `--api-key` to point to any OpenAI-compatible endpoint:

```bash
# Ollama
python -m needle_in_the_groupchat evaluate \
  --model qwen3:4b \
  --base-url http://localhost:11434/v1 \
  --api-key none \
  --message-format tools \
  --conversations data/conversations \
  --output results/qwen3-results.yaml

# vLLM
python -m needle_in_the_groupchat evaluate \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --base-url http://localhost:8000/v1 \
  --api-key none \
  --conversations data/conversations \
  --output results/llama-results.yaml
```

Use `--message-format tools` or `--message-format prefix` for models that don't support the `name` field (recommended for Ollama).

## Contributing

### Code Structure

```
needle_in_the_groupchat/
├── cli.py              # CLI commands (generate, evaluate)
├── __main__.py         # Module entry point
├── models/             # Data models
│   ├── conversation.py # Conversation and message schemas
│   ├── dataset.py      # Dataset loading/saving
│   └── enums.py        # Position, EvaluationMode enums
├── generation/         # Conversation generators
│   ├── base.py         # Abstract generator interface
│   ├── llm.py          # LLM-based generation
│   ├── random.py       # Random string generation
│   └── preference.py   # Preference-mode generation
├── evaluation/         # Evaluation logic
│   ├── conversation_evaluator.py  # Single conversation eval
│   ├── dataset_evaluator.py       # Batch evaluation
│   └── results.py      # Results aggregation
├── formatting/         # Message format converters
│   ├── base.py         # Abstract formatter interface
│   ├── messages.py     # Standard message format (name field)
│   ├── prefix.py       # Prefix format (name in content)
│   └── tools.py        # Tool-calling format
└── utils/
    └── token_counter.py  # Token counting utilities
```

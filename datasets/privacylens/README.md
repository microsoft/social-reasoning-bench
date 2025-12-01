# PrivacyLens Dataset

A benchmark for evaluating whether LLM agents leak sensitive information when completing tasks.

## Overview

PrivacyLens contains 493 privacy-sensitive scenarios. Each tests whether a model leaks information it should keep private while acting as an agent completing user tasks.

**Key insight**: Models can correctly answer "Should you share X?" while still leaking X when asked to complete a task. This dataset measures that gap.

## Source

- **Paper**: [PrivacyLens: Evaluating Privacy Norm Awareness of Language Models in Action](https://arxiv.org/abs/2409.00138) (NeurIPS 2024)
- **License**: MIT

## Dataset Structure

| Field | Description |
|-------|-------------|
| `name` | Entry identifier |
| `seed` | Abstract privacy norm (who shouldn't share what with whom) |
| `vignette` | Concrete story expanding the seed |
| `trajectory` | Simulated agent interaction with tools |

Each `trajectory` contains:
- `user_name`, `user_email` - The user the agent assists
- `toolkits` - Available tools (Messenger, Gmail, Notion, etc.)
- `user_instruction` - What the user asked the agent to do
- `executable_trajectory` - Tool calls and outputs the agent has seen
- `sensitive_info_items` - Information that must NOT appear in output
- `final_action` - The action the agent must complete

## Usage

Browse the dataset interactively:

```bash
uv run python datasets/privacylens/explore_privacylens.py
```

Load programmatically:

```python
import json

with open("datasets/privacylens/privacylens.json") as f:
    dataset = json.load(f)
```

# MAGPIE Dataset

**Multi-AGent contextual PrIvacy Evaluation** - A benchmark for evaluating privacy understanding in multi-agent collaborative scenarios.

## Overview

MAGPIE contains 200 high-stakes multi-agent scenarios designed to test how well AI systems preserve privacy while collaborating. Each scenario involves 3-7 agents with detailed profiles, preferences, and constraints.

## Source

- **Hugging Face**: [jaypasnagasai/magpie](https://huggingface.co/datasets/jaypasnagasai/magpie)
- **Paper**: [arXiv:2510.15186](https://arxiv.org/abs/2510.15186)
- **License**: MIT

## Dataset Structure

| Field | Description |
|-------|-------------|
| `file_name` | Source identifier |
| `scenario` | Situation description |
| `task` | Collaborative objective |
| `agent_number` | Number of participants (3-7) |
| `agent_names` | List of participant names |
| `agents` | Detailed agent profiles with preferences |
| `success_criteria` | Required agreement conditions |
| `constraints` | Operational limitations |
| `deliverable` | Expected outcomes |
| `solvability_note` | Resolution guidance |

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("jaypasnagasai/magpie")
```

Or use the local loader:

```python
from load_data import load_magpie

df = load_magpie()
```

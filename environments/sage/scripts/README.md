# Scripts

Utility scripts for running MAGPIE simulations and extracting results.

## Quick Start: Run a MAGPIE Simulation

```bash
# 1. Extract MAGPIE scenarios to profile directories
python scripts/convert_magpie_to_profiles.py --output-dir data/magpie_scenarios

# 2. Run a specific scenario
python scripts/simulate_magpie_scenario.py data/magpie_scenarios/scenario_0 --overwrite

# 3. Extract transcripts from the database
python scripts/extract_transcripts.py --database scenario_0.db

# 4. Visualize: Open html/transcript-viewer.html and drag in the YAML files
```

---

## convert_magpie_to_profiles.py

Converts the [jaypasnagasai/magpie](https://huggingface.co/datasets/jaypasnagasai/magpie) HuggingFace dataset to `OpenAIAgentProfile` format.

### About MAGPIE Dataset

MAGPIE (Multi-AGent contextual PrIvacy Evaluation) is a benchmark comprising 200 scenarios with 3-7 agents each, designed to examine multi-agent privacy-aware collaboration in high-stakes scenarios across 15 domains (Legal, Healthcare, Tech, etc.).

### Installation

```bash
pip install datasets
```

### Usage

#### Extract scenarios to directories (recommended for simulations)

```bash
# Creates data/magpie_scenarios/scenario_0/, scenario_1/, etc.
# Each folder contains agent_0.json, agent_1.json, ...
python scripts/convert_magpie_to_profiles.py --output-dir data/magpie_scenarios
```

#### Save all profiles to a single JSON file

```bash
python scripts/convert_magpie_to_profiles.py --output data/magpie_profiles.json
```

#### Preview profiles

```bash
python scripts/convert_magpie_to_profiles.py --preview 5
```

#### Programmatic Usage

```python
from scripts.convert_magpie_to_profiles import convert_magpie_to_profiles

# Convert all profiles
profiles = convert_magpie_to_profiles()

# Use with agents
from sage_agents import ChatCompletionsAgent

agent = ChatCompletionsAgent(
    profile=profiles[0],
    base_url="http://localhost:8000",
    openai_api_key="sk-...",
)
```

### Profile Mapping

The script maps MAGPIE dataset fields to `OpenAIAgentProfile` as follows:

| OpenAIAgentProfile Field | Source |
|--------------------------|--------|
| `id` | Generated: `magpie_{scenario_idx}_{agent_idx}` |
| `full_name` | Agent's name from dataset |
| `email_address` | Generated from name (e.g., "john.doe@example.com") |
| `handle` | Generated from name (e.g., "john_doe") |
| `description` | Agent's role, profile, background |
| `goal` | Agent's goal/objective/preferences |
| `metadata` | Scenario context, task, constraints, etc. |

### Output Format

```json
[
  {
    "id": "magpie_0_0",
    "full_name": "Sarah Chen",
    "email_address": "sarah.chen@example.com",
    "handle": "sarah_chen",
    "description": "Role: Legal Counsel. Background: 10 years corporate law experience",
    "goal": "Negotiate contract terms while protecting client interests",
    "metadata": {
      "source": "magpie",
      "scenario_id": 0,
      "file_name": "legal_contract_001",
      "scenario": "Multi-party contract negotiation...",
      "task": "Reach agreement on licensing terms...",
      "success_criteria": "All parties sign final agreement",
      "constraints": "Must complete within 48 hours",
      "deliverable": "Signed contract document"
    }
  }
]
```

### Notes

- Each scenario in MAGPIE can contain multiple agents (3-7 per scenario)
- The script creates one `OpenAIAgentProfile` per agent per scenario
- Email addresses and handles are auto-generated from agent names
- All scenario metadata is preserved in the `metadata` field for context

---

## simulate_magpie_scenario.py

Runs a MAGPIE scenario simulation using the messenger protocol. Launches a marketplace server and runs all agents from a scenario directory until they shutdown or reach max iterations.

### Prerequisites

- OpenAI API key: `export OPENAI_API_KEY=sk-...`
- Scenario directory with agent JSON files (from `convert_magpie_to_profiles.py --output-dir`)

### Usage

```bash
# Run a scenario with defaults
python scripts/simulate_magpie_scenario.py data/magpie_scenarios/scenario_0

# With custom options
python scripts/simulate_magpie_scenario.py data/magpie_scenarios/scenario_0 \
    --model gpt-4o \
    --max-iterations 100 \
    --port 8001

# Overwrite existing database
python scripts/simulate_magpie_scenario.py data/magpie_scenarios/scenario_0 --overwrite
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `scenario_dir` | (required) | Path to scenario directory |
| `--host` | 127.0.0.1 | Server host |
| `--port` | 8001 | Server port |
| `--database` | `<scenario_name>.db` | SQLite database path |
| `--model` | gpt-4o | OpenAI model |
| `--max-iterations` | 50 | Max iterations per agent |
| `--agent-type` | chat-completions | Agent type (chat-completions or responses) |
| `--overwrite` | false | Overwrite existing database |

### Output

The simulation saves all agent actions to a SQLite database. Use `extract_transcripts.py` to extract human-readable transcripts.

---

## extract_transcripts.py

Extracts message transcripts from a simulation database into YAML files for analysis and visualization.

### Usage

```bash
# Extract from default database
python scripts/extract_transcripts.py

# Extract from specific database
python scripts/extract_transcripts.py --database scenario_0.db

# Specify output directory
python scripts/extract_transcripts.py --database scenario_0.db --output-dir my_transcripts/
```

### Output Structure

```
transcripts/scenario_0/
├── groups/
│   └── Project_Team_group_abc123.yaml
└── direct_messages/
    └── Alice_and_Bob.yaml
```

### Transcript Format

```yaml
title: Project Team
id: group_abc123
members:
  - Alice
  - Bob
  - Charlie
total_messages: 15
messages:
  - from: Alice
    timestamp: "2024-01-15T10:30:00"
    message: |
      Hello team, let's discuss the project timeline.
```

---

## Visualization

### transcript-viewer.html

Interactive timeline viewer for message transcripts.

1. Open `html/transcript-viewer.html` in a browser
2. Drag and drop YAML transcript files onto the page
3. View messages across conversations in a synchronized timeline

Features:
- Time-scaled or row-based view
- Color-coded participants
- Expandable/collapsible conversations
- Click messages for full details

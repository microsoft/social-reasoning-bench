# SAGE Environment

A multi-agent environment for running protocols, agents, and calendar scenarios on a Magentic-Marketplace server.

## Installation

```bash
uv sync
```

## Sub-packages

### sage_protocol
Run protocols in a Magentic-Marketplace server. Includes messenger, calendar, and marketplace protocols.
See [sage_protocol/README.md](sage_protocol/README.md).

### sage_agents
Framework for building OpenAI-powered agents that interact with marketplace protocols.
See [sage_agents/README.md](sage_agents/README.md).

### sage_calendar_generator
LLM-based generation of multi-agent scheduling scenarios with realistic calendars.
See [sage_calendar_generator/README.md](sage_calendar_generator/README.md).

## Usage

### Run a protocol

```bash
uv run -m sage_protocol
```

### Run an agent

```python
from sage_agents import ChatCompletionsAgent, OpenAIAgentProfile

profile = OpenAIAgentProfile(
    full_name="Assistant",
    email_address="assistant@example.com",
    messages=[{"role": "system", "content": "You are a helpful assistant."}],
)

agent = ChatCompletionsAgent(
    profile=profile,
    openai_model="gpt-4o",
)
```

### Run a MAGPIE Simulation

Complete workflow to run a multi-agent privacy scenario:

```bash
cd environments/sage

# 1. Extract MAGPIE dataset to scenario directories
python scripts/convert_magpie_to_profiles.py --output-dir data/magpie_scenarios

# 2. Run a scenario (launches server + agents)
python scripts/simulate_magpie_scenario.py data/magpie_scenarios/scenario_0 --overwrite

# 3. Extract message transcripts
python scripts/extract_transcripts.py --database scenario_0.db

# 4. Visualize: Open html/transcript-viewer.html and drag in YAML files from environments/sage/transcripts/scenario_0/**/*.yaml
```

See [scripts/README.md](scripts/README.md) for detailed options.

### Visualize Results

- **Transcript Viewer**: Open `html/transcript-viewer.html` to view message timelines
- **Action Sequence Viewer**: Open `html/action-sequence-viewer.html` for raw action trajectories

### Generate calendar data

```bash
uv run -m sage_calendar_generator --num-participants 3 --seed-days 7
```

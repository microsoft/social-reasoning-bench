# Coffee Bean Marketplace Simulation

A multi-agent marketplace simulation where LLM-powered agents (buyers and sellers) trade coffee beans to maximize their utility.

## Setup Using uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (restart shell or run this)
source $HOME/.local/bin/env

# From the coffee directory
cd environments/coffee
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

## Running Tests for LLM

```bash
# Copy .env.example to .env and replace with your actual API keys
cp .env.example .env

# Test the LLM utility (providers: gemini, openai, trapi, vllm)
uv run python utils/call_llm.py gemini
```

## Setting up vLLM Server (Optional)

To use vLLM, you need to run it as a server. Here's how:

### Quick Start (4 steps)

```bash
# 1. Install system dependencies (Python dev headers)
sudo apt-get update && sudo apt-get install -y python3-dev build-essential

# 2. Install vLLM (if not already installed)
uv pip install vllm

# 3. Start the server (in a separate terminal)
uv run vllm serve Qwen/Qwen3-4B-Instruct-2507 --port 8000

# 4. Test the server with curl
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-4B-Instruct-2507",
    "messages": [{"role": "user", "content": "How are you?"}]
  }'

# 5. Update .env and run your code
uv run python utils/call_llm.py
```

## Running the Coffee Bean Marketplace Simulation

### Quick Start

```bash
# Run the simulation (creates results/marketplace.db)
uv run python main.py --config config/config-vllm.yaml

# Run with experiment name (creates results/marketplace_exp1.db)
uv run python main.py --config config/config-gemini.yaml --experiment exp1
```

### Running Batch Rollouts

Run multiple simulations automatically:

```bash
# Run 10 simulations with default config (config-vllm.yaml)
uv run python batch_rollout.py --num-runs 10 --config config/config-vllm.yaml

# Results will be saved as:
# results/marketplace_batch_20251203_123456_1.db
# results/marketplace_batch_20251203_123456_2.db
# ...

# Run 5 simulations with custom config and prefix
uv run python batch_rollout.py --num-runs 5 --config config/config-gemini.yaml --prefix exp

# Run simulations from gullibility dataset configs (#rollouts = #runs × #configs)
uv run python batch_rollout.py --num-runs 1 --config-dir ../../datasets/gullibility/config --prefix gullibility_test --workers 4
```

### Customizing the Simulation

Create or edit a config file in `config/` to customize the marketplace. Available examples:

- `config-vllm.yaml` - Local vLLM
- `config-gemini.yaml` - Closed-source LLM (gemini, openai, trapi)
- `config-strategy.yaml` - With private strategy

```yaml
max_rounds: 5
players:
  - name: buyer_1
    cash: 30.0
    coffee_beans: 0
    utility_per_bean: 8.0
    public_info: "I want high-quality coffee beans for my cafe"
    private_strategy: "Use anchoring tactics to influence the negotiation"
    llm_config:
      LLM_PROVIDER: "vllm"

  - name: seller_1
    cash: 0.0
    coffee_beans: 10
    utility_per_bean: 2.0
    public_info: "I offer premium organic coffee beans"
    llm_config:
      LLM_PROVIDER: "gemini"
```

**Per-Player LLM Configuration**: You can specify different LLM settings for each player using the `llm_config` field. This allows you to test different models, temperatures, or providers for each agent. The config overrides environment variables, so you can mix and match models within a single simulation.

**Supported Providers**:
- `gemini`: Google Gemini (requires `GEMINI_API_KEY`)
- `openai`: OpenAI GPT (requires `OPENAI_API_KEY`)
- `trapi`: Azure OpenAI (requires Azure credentials)
- `vllm`: Local vLLM server
- `human`: Human input
- `human_cli`: Interactive CLI for human players

### Installing SQLite3 (for viewing results)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y sqlite3

# Verify installation
sqlite3 --version
```

### Viewing Results

Results are saved in the `results/` directory. Replace `marketplace.db` with `marketplace_<experiment_name>.db` if you used `--experiment`:

```bash
# Quick check: View final rewards (total value)
sqlite3 results/marketplace.db "SELECT name, coffee_beans, cash, (cash + coffee_beans * utility_per_bean) as total_value FROM agents ORDER BY total_value DESC;"

# Check the database for full event history
sqlite3 results/marketplace.db "SELECT * FROM events;"

# View final agent states (without prompt_history)
sqlite3 results/marketplace.db "SELECT agent_id, name, coffee_beans, cash, utility_per_bean FROM agents;"

# View prompt history for a specific agent (e.g., agent_id = 1)
sqlite3 results/marketplace.db "SELECT name, prompt_history FROM agents WHERE agent_id = 1;"

# Or use Python to save output to a log file
uv run python -c "
import sqlite3
import json

db = sqlite3.connect('results/marketplace.db')
db.row_factory = sqlite3.Row
agents = db.execute('SELECT agent_id, name, prompt_history FROM agents').fetchall()

with open('simulation.log', 'w') as f:
    for agent in agents:
        f.write(f'\n=== Agent {agent[\"agent_id\"]}: {agent[\"name\"]} ===\n')
        history = json.loads(agent['prompt_history'])
        for i, turn in enumerate(history, 1):
            f.write(f'\n--- Turn {i} ---\n')
            f.write('Prompt:\n')
            f.write(turn.get('prompt', '') + '\n')
            f.write('\nResponse:\n')
            f.write(turn.get('response', '') + '\n')

print('Agent prompt history saved to simulation.log')
"
```

### Analyzing Results

Analyze simulation results from a batch run:

```bash
# Analyze all results in a directory
uv run python analyze_results.py results/batch_20251203_123456

# Analyze with specific player and sort order
uv run python analyze_results.py results/gullibility_test "buyer_1" --sort desc
```

Example output:
```
=== Analyzing all results in results/gullibility_test for player 'buyer_1' ===
  1. marketplace_gullibility_test_Negotiation_strategy_001_1.db: $86.00 (beans=7, cash=$30.00, utility=8.00)
  2. marketplace_gullibility_test_Persuasion_strategy_003_1.db: $78.00 (beans=6, cash=$30.00, utility=8.00)
  3. marketplace_gullibility_test_Rhetoric_strategy_002_1.db: $54.00 (beans=3, cash=$30.00, utility=8.00)
  ...

=== Aggregate Statistics ===
  Average gain: $67.50
  Min gain: $30.00
  Max gain: $110.00
  Total runs: 150
```

### Generating Plots

Visualize buyer vs seller utilities with feasible region (parallelogram):

```bash
# Plot results from a batch run
uv run python plot_results.py results/batch_20251203_123456

# Or specify a results directory
uv run python plot_results.py results/gullibility_test
```

This creates a scatter plot showing buyer utility vs seller utility with the feasible region.

For more details, see [`docs/design.md`](docs/design.md).

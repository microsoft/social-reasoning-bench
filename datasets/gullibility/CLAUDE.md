# Gullibility Dataset

This pipeline generates adversarial strategies to test model robustness against social engineering and manipulation. It extracts unconventional tactics from Wikipedia articles and applies them to specific task environments.

## Pipeline Overview

1. **Crawl Wikipedia** (`crawler.py`) - Collect seed pages via BFS traversal from starting topics
2. **Generate Strategies** (`batch_generate.py`) - Use an LLM to extract manipulation tactics from Wikipedia content, guided by a game context file that describes the target scenario
3. **Apply to Environment** (`generate_configs*.py`) - Embed the generated strategies into task-specific configuration files

## Working with This Dataset

### Step 1: Check for Existing Data

Before crawling, check if Wikipedia pages already exist in `output/pages/`. The crawler automatically skips pages that are already downloaded, so you can safely re-run it to add more pages.

If pages exist, you can proceed directly to strategy generation. If not, or if the user wants fresh/different content, run the crawler.

### Step 2: Crawling Wikipedia

The crawler uses BFS to fetch Wikipedia articles starting from seed topics defined in the script.

```bash
uv run python crawler.py --max-pages 50 --max-depth 2
```

**Arguments:**
- `--max-pages`: Maximum pages to crawl (default: 200). Recommend starting with 20-50 pages for quick iteration.
- `--max-depth`: How many link hops from seed topics (default: 2). Depth 1 = seeds only, depth 2 = seeds + their links.
- `--output-dir`: Where to save pages (default: `output/pages/`)

**Recommendations:**
- For quick testing, start with `--max-pages 20 --max-depth 1`
- Ask the user how many pages they want if not specified
- The 77 seed topics in `crawler.py` cover negotiation, psychology, business, AI, politics, and more

### Step 3: Prepare Game Context File

Before generating strategies, you need a game context file that describes the scenario and vulnerability being tested. Ask the user what vulnerability they want to test if no context file exists.

**Writing a game context file:**
- Describe the scenario at a high level: who are the agents, what are they trying to do
- Define the objective: what does "success" look like for the adversarial agent
- Specify the vulnerability being tested (policy bypass, information leakage, manipulation, etc.)
- **Important:** Do NOT include the actual private information or "answer" in the context. For example, if testing privacy leakage, describe that private events exist but don't list what they are. The LLM should generate strategies without knowing what it's trying to extract.

**Example context files in this folder:**
- `game_context.txt` - Coffee trading (based on `sage/environments/coffee/`)
- `game_context_calendar_policy_bypass.txt` - Policy bypass: Bob tries to bypass email verification
- `game_context_calendar_privacy_probing.txt` - Privacy: Alice tries to extract private calendar info

The calendar examples are based on scenarios from:
- `sage-benchmark/data/calendar-scheduling/calendar-tasks-non-malicious.yaml`
- `sage-benchmark/data/calendar-scheduling/malicious-digital-worker.yaml`

### Step 4: Generate Strategies

Requires `GEMINI_API_KEY` or `OPENAI_API_KEY` environment variable.

```bash
uv run python batch_generate.py <pages_dir> <game_context_file> <output_dir> --workers 10
```

**Examples:**
```bash
# Coffee trading strategies
uv run python batch_generate.py output/pages/ game_context.txt output/strategies/ --workers 10

# Calendar policy bypass strategies
uv run python batch_generate.py output/pages/ game_context_calendar_policy_bypass.txt output/strategies_calendar/ --workers 10

# Calendar privacy probing strategies
uv run python batch_generate.py output/pages/ game_context_calendar_privacy_probing.txt output/strategies_calendar_probe/ --workers 10
```

Use `--provider openai` to use OpenAI instead of Gemini (default).

### Step 5: Generate Task Configs

This step embeds strategies into environment-specific configuration files. You need a config template for your environment. Ask the user to provide one if not available.

**Which field does the strategy get appended to?**
- Coffee trading (`generate_configs.py`): `players[name].private_strategy`
- Calendar (`generate_configs_calendar.py`): `tasks[].requestor.instruction_message` (default limit: 50 configs)

**Example templates in this folder:**
- `config-template.yaml` - Coffee trading template
- `config-template-calendar.yaml` - Calendar scheduling template

To adapt for a new environment, create a config template and modify the generate_configs script to inject the strategy into the appropriate field.

```bash
# Coffee trading (hardcoded paths)
uv run python generate_configs.py

# Calendar scheduling / privacy probing
uv run python generate_configs_calendar.py \
    --template <template.yaml> \
    --strategies-dir <strategies/> \
    --output-dir <output/> \
    --limit 50 --task-limit 3 --strategy-limit 20
```

### Step 6: Run Simulations

This step is environment-specific. Verify with the user which simulator to use and how to run it. Below are examples for existing environments:

```bash
# Coffee trading
cd ../../environments/coffee
uv run python batch_rollout.py --config-dir ../../datasets/gullibility/output/config --prefix <name> --workers 4

# Calendar scheduling / privacy probing
cd ../../sage-benchmark
uv run -m sage_benchmark.calendar_scheduling <config_dir> --limit 100 --max-rounds 10 --model <model-name>
```

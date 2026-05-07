---
layout: home

hero:
  name: Social Reasoning Bench
  tagline: Evaluate the social reasoning capabilities of LLM agents in multi-agent environments.
  actions:
    - theme: brand
      text: Get Started
      link: /installation
    - theme: alt
      text: See the Results
      link: /results

---

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/microsoft/social-reasoning-bench.git
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate

# 2. Add an API key
cp example.env .env
# then edit .env to set OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY,
# or SRBENCH_AZURE_POOL_PATH

# 3. Run a smoke benchmark
srbench benchmark calendar \
    --data data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2

# 4. View the results, pre-loaded with your run
srbench dashboard outputs/your-experiment
```

See [Installation](/installation) for full setup including model providers.

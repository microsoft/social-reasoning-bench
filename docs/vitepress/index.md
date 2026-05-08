---
layout: home

hero:
  name: Social Reasoning Bench
  tagline: Evaluate the social reasoning capabilities of LLM agents in multi-party environments.
  # image:
  #   light: /hero-light.png
  #   dark: /hero-dark.png
  #   alt: Social Reasoning Bench

features:
  - title: Get started
    details: Install <code class="hero-code">srbench</code> and start evaluating models.
    link: /installation
  - title: Read the blog
    details: Our motivation, methodology, and findings.
    link: https://microsoft-my.sharepoint.com/:w:/p/acelikyilmaz/cQoKw9tWcmb9TJnB3-6kYgtvEgUCvMTv8DjvJJ-QVhtFEEe0Rw
  - title: Browse the results
    details: Peruse the raw data from our experiments.
    link: /results
---

## Quick Start

Evaluate the social reasoning ability of your own LLM. For example's sake, we'll assume your LLM is served as `my-model` via vLLM on the localhost.

```bash
# 1. Clone and install
git clone https://github.com/microsoft/social-reasoning-bench.git
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate

# 2. Setup env vars. To reproduce our results, Gemini is used.
GEMINI_API_KEY=<your api key>

# 3. Run the v0.1.0 experiment sweep with your model as the assistant
srbench experiment experiments/v0.1.0 \
    --output-base outputs/my-model
    --assistant-model openai/my-model \
    --assistant-base-url http://localhost:8000/v1 \
    --assistant-api-key none
    # To just test a few examples per experiment in the sweep
    # --set limit=10

# 4. View the results, pre-loaded with your run
srbench dashboard outputs/my-model
```

See [Installation](/installation), [Experiments](/experiments.md), and [LLMs](/llm.md) for detailed instructions.

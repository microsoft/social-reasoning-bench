---
layout: home

hero:
  name: SAGE Benchmark
  text: Society of Agents Environments
  tagline: Evaluating social reasoning capabilities of LLM agents in multi-agent settings
  actions:
    - theme: brand
      text: Read the Report
      link: /introduction
    - theme: alt
      text: Go under the hood
      link: /architecture

features:
  - title: Results
    details: How frontier models perform across benchmarks under benign and adversarial conditions.
    link: /results
  - title: Dashboard
    details: Interactive explorer for experiment results across models, benchmarks, and attack types.
    link: /dashboard
  - title: Reproduction
    details: Reproduce the exact experiments from the paper with step-by-step instructions.
    link: /reproduction
---

## Quick Start

```bash
# Install
git clone https://github.com/microsoft/sage.git
cd sage
uv sync --all-packages

# Run a benchmark
sagebench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2
```

See the [Installation guide](/installation) for full setup instructions including model provider configuration.

# srbench-data-gen

Data generation pipelines for the SRBench benchmark. Generates task datasets for calendar scheduling and marketplace negotiation, including adversarial variants using hand-crafted and WhimsyGen-based attacks.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Generate calendar scheduling tasks
srbench datagen calendar --output-dir data/calendar-scheduling

# Generate marketplace negotiation tasks
srbench datagen marketplace --output-dir data/marketplace
```

## [Documentation](../../docs/vitepress/generating-data.md)

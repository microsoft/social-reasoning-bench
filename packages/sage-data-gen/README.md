# sage-data-gen

Data generation pipelines for the SAGE benchmark. Generates task datasets for calendar scheduling and marketplace negotiation, including adversarial variants using hand-crafted and WhimsyGen-based attacks.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Generate calendar scheduling tasks
sagegen calendar --output-dir data/calendar-scheduling

# Generate marketplace negotiation tasks
sagegen marketplace --output-dir data/marketplace
```

## [Documentation](../../docs/vitepress/generating-data.md)

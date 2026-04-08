# sage-data-gen

Data generation pipelines for the SAGE benchmark. Generates task datasets for calendar scheduling, form filling, and marketplace negotiation, including adversarial variants using hand-crafted and WhimsyGen-based attacks.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Generate calendar scheduling tasks
sagegen calendar --output-dir data/calendar-scheduling

# Generate form filling tasks from a form image
sagegen form-filling --image path/to/form.png --output-dir ./output/

# Generate marketplace negotiation tasks
sagegen marketplace --output-dir data/marketplace
```

## [Documentation](../../docs/vitepress/generating-data.md)

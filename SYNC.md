# Sync Results to Azure

Sync large experiment results to/from Azure Blob Storage.

**Azure location:** `aifrontiersplus/magentic/social-reasoning/`

## Synced Folders

Please add your folder to this table so others are aware of what data is available.

| Path | Date | Description |
|------|------|-------------|
| `sage-benchmark/outputs/calendar_scheduling/jan-9-2026-calendar-results` | 2026-01-09 | Created by Tyler to run the calendar benchmark, includes viz files |
| | |

## Setup

Install the azure dependencies:

```bash
uv sync --group azure
```

You'll also need `azcopy` installed and `az login` authenticated.

## Usage

```bash
# List top-level remote folders
uv run --group azure sync.py ls

# List contents of a specific folder
uv run --group azure sync.py ls calendar_scheduling

# Upload a folder
uv run --group azure sync.py upload sage-benchmark/outputs/calendar_scheduling/jan-9-2026-calendar-results

# Download a folder
uv run --group azure sync.py download sage-benchmark/outputs/calendar_scheduling/jan-9-2026-calendar-results
```

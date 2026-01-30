# Sync Results to Azure

Sync large experiment results to/from Azure Blob Storage.

**Azure location:** `aifrontiersplus/magentic/social-reasoning/`

## Setup

Install the azure dependencies:

```bash
uv sync --all-groups
```

You'll also need `azcopy` installed and `az login` authenticated.

## Usage

```bash
# Upload a local folder to a remote path
uv run sync.py upload <local-path> <remote-path>

# Download a remote path to a local folder
uv run sync.py download <remote-path> <local-path>

# List remote folders
uv run sync.py ls [path]
```

Remote paths are relative to `social-reasoning/` in the blob container.

## Examples

```bash
# Upload local results to remote
uv run sync.py upload ./my-results experiment-results
uv run sync.py upload ./data calendar/1-30-experiment

# Download remote results to local
uv run sync.py download experiment-results ./my-results
uv run sync.py download calendar/1-30-experiment ./local-data

# List contents
uv run sync.py ls
uv run sync.py ls calendar
```

## Overwrite Protection

By default, uploads and downloads will **fail** if any files would be overwritten. This protects against accidentally clobbering existing data.

```bash
# This will fail if remote already has files with the same names
uv run sync.py upload ./my-results experiment-results
# ERROR: The following files already exist on remote:
#   - result1.json
#   - result2.json
# Error: Use --force to overwrite existing files

# Use --force to overwrite
uv run sync.py upload ./my-results experiment-results --force
```



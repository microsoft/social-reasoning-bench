# Dev Setup

## Install

```bash
# Install uv if not used before
curl -LsSf https://astral.sh/uv/install.sh | sh

# clone and install
git clone https://github.com/microsoft/sage.git
cd sage
uv sync --all-groups --all-extras
```

## Checks

Need to pass before PR.

```bash
# check formatting
uv run poe check-all

# try to auto-fix
uv run poe fix-all
```

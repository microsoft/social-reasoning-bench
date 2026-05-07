# Contributing

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Prerequisites

- Python >= 3.11
- uv

## Install

```bash
git clone git@github.com/microsoft/social-reasoning-bench.git srbench
cd srbench

uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate

pre-commit install
```

## Code formatting & linting

These will run on commit via the pre-commit hooks.

```bash
# Fix all code formatting and linting errors
poe fix

# Check all formatting and linting passes
poe check
```

## Docs

```bash
# Dev server with hot-reload:
poe run docs:dev

# Build static docs pages
poe run docs:build
# View built docs
poe run docs:preview
```

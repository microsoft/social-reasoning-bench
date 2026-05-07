"""CLI entry point for srbench-llm.

Invoked as ``srbench llm <group> <command> [options...]``. The dispatcher
parses the first two positional args (group, command), rewrites
``sys.argv`` so the leaf subcommand sees its own argparse, and calls it.
"""

import sys


def _run_azure_pool_populate(argv: list[str]) -> None:
    from .scripts.populate_azure_pool import main as populate_main

    sys.argv = ["srbench llm azure-pool populate", *argv]
    populate_main()


_AZURE_POOL_COMMANDS = {
    "populate": _run_azure_pool_populate,
}


def _run_azure_pool(argv: list[str]) -> None:
    if not argv or argv[0] not in _AZURE_POOL_COMMANDS:
        names = ",".join(_AZURE_POOL_COMMANDS)
        print(f"Usage: srbench llm azure-pool {{{names}}} ...", file=sys.stderr)
        sys.exit(1)
    _AZURE_POOL_COMMANDS[argv[0]](argv[1:])


_GROUPS = {
    "azure-pool": _run_azure_pool,
}


def main() -> None:
    argv = sys.argv[1:]
    if not argv or argv[0] not in _GROUPS:
        names = ",".join(_GROUPS)
        print(f"Usage: srbench llm {{{names}}} ...", file=sys.stderr)
        sys.exit(1)
    _GROUPS[argv[0]](argv[1:])

#!/usr/bin/env python3
"""Populate azure pool config files for all Azure OpenAI deployments.

Queries the Azure CLI for all deployments on cognitive services accounts
matching a prefix (default: ``aif-endpoints-*``) and writes one JSON file
per model to an output directory.  Set ``SRBENCH_AZURE_POOL_PATH`` to point
at the output directory.

Usage::

    # All models, default prefix → configs/azure_pool/
    python scripts/populate_azure_pool.py

    # Specific models only
    python scripts/populate_azure_pool.py --models gpt-5.2 gpt-4.1

    # Custom account prefix and subscription
    python scripts/populate_azure_pool.py --prefix my-openai- --subscription <id>

    # Custom output directory
    python scripts/populate_azure_pool.py --output-dir configs/my-pool

    # Custom API version
    python scripts/populate_azure_pool.py --api-version 2025-04-01-preview

    # Dry run (print to stdout, don't write files)
    python scripts/populate_azure_pool.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def run_az(args: list[str], timeout: int = 30) -> list[dict]:
    """Run an az CLI command and return parsed JSON.

    Args:
        args: Arguments to pass to the ``az`` CLI (excluding ``-o json``).
        timeout: Maximum seconds to wait for the command to complete.

    Returns:
        Parsed JSON output as a list of dictionaries, or an empty list on
        error or empty output.
    """
    result = subprocess.run(
        ["az", *args, "-o", "json"],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        print(f"  az error: {result.stderr.strip()}", file=sys.stderr)
        return []
    return json.loads(result.stdout) if result.stdout.strip() else []


def list_accounts(subscription: str, prefix: str) -> list[dict]:
    """List cognitive services accounts matching prefix.

    Args:
        subscription: Azure subscription ID or name.
        prefix: Name prefix used to filter cognitive services accounts.

    Returns:
        List of matching account dicts with name, resource group, and endpoint.
    """
    return run_az(
        [
            "cognitiveservices",
            "account",
            "list",
            "--subscription",
            subscription,
            "--query",
            f"[?starts_with(name, '{prefix}')].{{name:name, rg:resourceGroup, endpoint:properties.endpoint}}",
        ]
    )


def list_deployments(account_name: str, resource_group: str, subscription: str) -> list[dict]:
    """List non-batch, non-image, and non-embedding deployments for a cognitive services account.

    Args:
        account_name: Name of the Azure Cognitive Services account.
        resource_group: Azure resource group containing the account.
        subscription: Azure subscription ID or name.

    Returns:
        A list of dicts with ``name`` and ``model`` keys for each deployment.
    """
    return run_az(
        [
            "cognitiveservices",
            "account",
            "deployment",
            "list",
            "--name",
            account_name,
            "--resource-group",
            resource_group,
            "--subscription",
            subscription,
            "--query",
            "[?!contains(name, 'batch') && !starts_with(properties.model.name, 'dall-e') && !starts_with(properties.model.name, 'gpt-image') && !starts_with(properties.model.name, 'text-embedding')].{name:name, model:properties.model.name}",
        ]
    )


def discover_all(subscription: str, prefix: str) -> dict[str, list[dict]]:
    """Discover all deployments grouped by model name.

    Args:
        subscription: Azure subscription ID or name.
        prefix: Name prefix used to filter cognitive services accounts.

    Returns:
        Dictionary mapping model names to lists of endpoint/deployment dicts.
    """
    accounts = list_accounts(subscription, prefix)
    print(f"Found {len(accounts)} accounts matching '{prefix}*'")

    by_model: dict[str, list[dict]] = defaultdict(list)

    for i, acct in enumerate(accounts, 1):
        name = acct["name"]
        print(f"  [{i}/{len(accounts)}] {name}...", end="", flush=True)
        deployments = list_deployments(name, acct["rg"], subscription)
        print(f" {len(deployments)} deployments")
        for dep in deployments:
            by_model[dep["model"]].append(
                {
                    "azure_endpoint": acct["endpoint"],
                    "deployment": dep["name"],
                }
            )

    return dict(by_model)


def write_configs(
    by_model: dict[str, list[dict]],
    output_dir: Path,
    api_version: str,
    models: list[str] | None = None,
) -> None:
    """Write per-model JSON config files.

    Args:
        by_model: Mapping of model names to lists of endpoint/deployment dicts.
        output_dir: Directory where per-model JSON files are written.
        api_version: Azure API version string included in each config entry.
        models: Optional list of model names to write configs for. If ``None``,
            all discovered models are written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    target_models = models if models else sorted(by_model.keys())

    written = 0
    for model in target_models:
        endpoints = by_model.get(model)
        if not endpoints:
            print(f"  WARNING: no deployments found for '{model}'", file=sys.stderr)
            continue
        entries = [
            {
                "azure_endpoint": ep["azure_endpoint"],
                "deployment": ep["deployment"],
                "api_version": api_version,
            }
            for ep in sorted(endpoints, key=lambda e: e["deployment"])
        ]
        path = output_dir / f"{model}.json"
        path.write_text(json.dumps(entries, indent=2) + "\n")
        written += 1
        print(f"  {path} ({len(entries)} endpoints)")

    print(f"\nWrote {written} config files to {output_dir}/")
    print(f"\nAdd to .env:")
    print(f"  SRBENCH_AZURE_POOL_PATH={output_dir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate azure pool config files")
    parser.add_argument(
        "--subscription",
        default="d4fe558f-6660-4fe7-99ec-ae4716b5e03f",
        help="Azure subscription ID (default: MSR LIT)",
    )
    parser.add_argument(
        "--prefix",
        default="aif-endpoints-",
        help="Cognitive services account name prefix (default: aif-endpoints-)",
    )
    parser.add_argument(
        "--models", nargs="+", default=None, help="Specific models to include (default: all)"
    )
    parser.add_argument(
        "--output-dir",
        default="configs/azure_pool",
        type=Path,
        help="Output directory for config files (default: configs/azure_pool)",
    )
    parser.add_argument(
        "--api-version",
        default="2025-01-01-preview",
        help="Azure OpenAI API version (default: 2025-01-01-preview)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print to stdout instead of writing files"
    )
    args = parser.parse_args()

    by_model = discover_all(args.subscription, args.prefix)

    print(f"\nDiscovered models:")
    for model in sorted(by_model.keys()):
        print(f"  {model}: {len(by_model[model])} deployments")

    if args.dry_run:
        target_models = args.models if args.models else sorted(by_model.keys())
        for model in target_models:
            endpoints = by_model.get(model, [])
            entries = [
                {
                    "azure_endpoint": ep["azure_endpoint"],
                    "deployment": ep["deployment"],
                    "api_version": args.api_version,
                }
                for ep in sorted(endpoints, key=lambda e: e["deployment"])
            ]
            print(f"\n# {model}.json ({len(entries)} endpoints)")
            print(json.dumps(entries, indent=2))
    else:
        write_configs(by_model, args.output_dir, args.api_version, args.models)


if __name__ == "__main__":
    main()

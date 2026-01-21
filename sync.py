#!/usr/bin/env python3
"""Sync folders to/from Azure Blob Storage."""

import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import click
import regex as re
from azure.identity import AzureCliCredential
from azure.storage.blob import (
    BlobServiceClient,
    ContainerSasPermissions,
    generate_container_sas,
)

# Azure config
ACCOUNT = "aifrontiersplus"
CONTAINER = "magentic"
BLOB_BASE = "social-reasoning"


def get_user_delegation_key(account_url, start_time=None, end_time=None, credential=None):
    credential = credential or AzureCliCredential()
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    start_time = start_time or datetime.now(timezone.utc)
    end_time = end_time or start_time + timedelta(days=1)
    return blob_service_client.get_user_delegation_key(
        key_start_time=start_time, key_expiry_time=end_time
    )


def get_sas_url(account, container, blob=None, permissions=None, start_time=None, end_time=None):
    start_time = start_time or datetime.now(timezone.utc)
    end_time = end_time or start_time + timedelta(days=1)

    base_url = f"https://{account}.blob.core.windows.net/{container}"
    if blob:
        base_url = f"{base_url}/{blob}"

    sas_token = generate_container_sas(
        account_name=account,
        container_name=container,
        user_delegation_key=get_user_delegation_key(
            f"https://{account}.blob.core.windows.net", start_time=start_time, end_time=end_time
        ),
        permission=permissions or ContainerSasPermissions(read=True, list=True),
        expiry=end_time,
        start=start_time,
    )
    return f"{base_url}?{sas_token}"


def hide_sig(cmd_with_sig):
    return re.sub(r"&sig=[^&]*", "&sig=HIDDEN", cmd_with_sig)


def azcopy_cp(src, dst, recursive=True):
    cmd = ["azcopy", "cp", src, dst]
    if recursive:
        cmd.extend(["--recursive", "--as-subdir=false"])
    print(f"Running: {hide_sig(' '.join(cmd))}")
    return subprocess.run(cmd, check=True)


@click.group()
def cli():
    """Sync folders to/from Azure Blob Storage."""
    pass


@cli.command()
@click.argument("folder_path")
def upload(folder_path):
    """Upload a local folder to Azure.

    Example: uv run --group azure sync.py upload sage-benchmark/outputs/jan-9-2026-calendar-results
    """
    local_path = Path(folder_path).resolve()
    if not local_path.exists():
        raise click.ClickException(f"Local folder not found: {local_path}")

    folder_name = local_path.name
    remote_blob = f"{BLOB_BASE}/{folder_name}"

    src_url = str(local_path)
    dst_url = get_sas_url(
        ACCOUNT,
        CONTAINER,
        remote_blob,
        permissions=ContainerSasPermissions(
            read=True, add=True, create=True, write=True, delete=True, list=True
        ),
    )

    click.echo(f"Uploading {local_path} -> {ACCOUNT}/{CONTAINER}/{remote_blob}")
    azcopy_cp(src_url, dst_url)
    click.echo("Done!")


@cli.command()
@click.argument("folder_path")
def download(folder_path):
    """Download a folder from Azure to local.

    Example: uv run --group azure sync.py download sage-benchmark/outputs/jan-9-2026-calendar-results
    """
    local_path = Path(folder_path).resolve()
    folder_name = local_path.name
    remote_blob = f"{BLOB_BASE}/{folder_name}"

    src_url = get_sas_url(ACCOUNT, CONTAINER, remote_blob)
    dst_url = str(local_path)

    local_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"Downloading {ACCOUNT}/{CONTAINER}/{remote_blob} -> {local_path}")
    azcopy_cp(src_url, dst_url)
    click.echo("Done!")


@cli.command()
@click.argument("path", default="")
def ls(path):
    """List folders in Azure blob storage.

    Examples:
        uv run --group azure sync.py ls
        uv run --group azure sync.py ls calendar_scheduling
    """
    credential = AzureCliCredential()
    blob_service_client = BlobServiceClient(
        account_url=f"https://{ACCOUNT}.blob.core.windows.net", credential=credential
    )
    container_client = blob_service_client.get_container_client(CONTAINER)

    if path:
        prefix = f"{BLOB_BASE}/{path.rstrip('/')}/"
    else:
        prefix = f"{BLOB_BASE}/"

    click.echo(f"Contents of {ACCOUNT}/{CONTAINER}/{prefix}")
    seen = set()
    for blob in container_client.walk_blobs(name_starts_with=prefix):
        relative = blob.name[len(prefix) :]
        top_item = relative.split("/")[0]
        if top_item and top_item not in seen:
            seen.add(top_item)
            # Check if it's a folder (has more path after it)
            is_folder = "/" in relative
            click.echo(f"  {top_item}{'/' if is_folder else ''}")


if __name__ == "__main__":
    cli()

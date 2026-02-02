#!/usr/bin/env python3
"""Sync folders to/from Azure Blob Storage.

Usage:
    uv run --group azure sync.py upload <local-path> <remote-path> [--force]
    uv run --group azure sync.py download <remote-path> <local-path> [--force]
    uv run --group azure sync.py ls [path]

Remote paths are relative to social-reasoning/ in the blob container.
"""

import subprocess
import tomllib
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


AZCOPY_NOT_INSTALLED_ERROR_MSG = """
azcopy is not installed or not found in PATH.

Installation instructions: https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10#get-azcopy
""".strip()


def check_azcopy_installed():
    """Check if azcopy is available, provide installation instructions if not."""
    try:
        subprocess.run(["azcopy", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise SystemExit(AZCOPY_NOT_INSTALLED_ERROR_MSG)


def check_cwd():
    """Assert that the current working directory contains a pyproject.toml with project name 'sage'."""
    cwd = Path.cwd()
    pyproject_path = cwd / "pyproject.toml"

    if not pyproject_path.exists():
        raise SystemExit(
            f"Error: No pyproject.toml found in {cwd}. This script must be run from the root of the 'sage' project directory."
        )

    try:
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        project_name = pyproject.get("project", {}).get("name")
        if project_name != "sage":
            raise SystemExit(
                f"Error: Expected project name 'sage', but found '{project_name}' in {pyproject_path}. This script must be run from the root of the 'sage' project directory."
            )
    except tomllib.TOMLDecodeError as e:
        raise SystemExit(
            f"Error reading pyproject.toml: {e}. This script must be run from the root of the 'sage' project directory."
        )


# Check cwd on module load
check_cwd()

# Check azcopy on module load
check_azcopy_installed()


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


def get_blob_client():
    credential = AzureCliCredential()
    return BlobServiceClient(
        account_url=f"https://{ACCOUNT}.blob.core.windows.net", credential=credential
    )


def list_remote_files(remote_path: str) -> set[str]:
    """List all files at a remote path (relative to BLOB_BASE)."""
    blob_service = get_blob_client()
    container_client = blob_service.get_container_client(CONTAINER)
    prefix = f"{BLOB_BASE}/{remote_path.rstrip('/')}/"

    files = set()
    for blob in container_client.list_blobs(name_starts_with=prefix):
        relative = blob.name[len(prefix) :]
        if relative:
            files.add(relative)
    return files


def list_local_files(local_path: Path) -> set[str]:
    """List all files in a local directory (relative paths)."""
    files = set()
    for file in local_path.rglob("*"):
        if file.is_file():
            files.add(str(file.relative_to(local_path)))
    return files


def check_conflicts(source_files: set[str], dest_files: set[str]) -> set[str]:
    """Return files that exist in both source and destination."""
    return source_files & dest_files


@click.group()
def cli():
    """Sync folders to/from Azure Blob Storage."""
    pass


@cli.command()
@click.argument("local_path")
@click.argument("remote_path")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
def upload(local_path, remote_path, force):
    """Upload a local folder to Azure.

    Examples:
        uv run --group azure sync.py upload ./my-results experiment-results
        uv run --group azure sync.py upload ./data calendar/1-30-experiment
        uv run --group azure sync.py upload ./data calendar/1-30-experiment --force
    """
    local = Path(local_path).resolve()
    if not local.exists():
        raise click.ClickException(f"Local path not found: {local}")

    remote_blob = f"{BLOB_BASE}/{remote_path.strip('/')}"

    if not force:
        local_files = list_local_files(local)
        remote_files = list_remote_files(remote_path)
        conflicts = check_conflicts(local_files, remote_files)

        if conflicts:
            click.echo("ERROR: The following files already exist on remote:", err=True)
            for f in sorted(conflicts)[:10]:
                click.echo(f"  - {f}", err=True)
            if len(conflicts) > 10:
                click.echo(f"  ... and {len(conflicts) - 10} more", err=True)
            raise click.ClickException("Use --force to overwrite existing files")

    src_url = str(local)
    dst_url = get_sas_url(
        ACCOUNT,
        CONTAINER,
        remote_blob,
        permissions=ContainerSasPermissions(
            read=True, add=True, create=True, write=True, delete=True, list=True
        ),
    )

    click.echo(f"Uploading {local} -> {ACCOUNT}/{CONTAINER}/{remote_blob}")
    azcopy_cp(src_url, dst_url)
    click.echo("Done!")


@cli.command()
@click.argument("remote_path")
@click.argument("local_path")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
def download(remote_path, local_path, force):
    """Download a folder from Azure to local.

    Examples:
        uv run --group azure sync.py download experiment-results ./my-results
        uv run --group azure sync.py download calendar/1-30-experiment ./data
        uv run --group azure sync.py download calendar/1-30-experiment ./data --force
    """
    local = Path(local_path).resolve()
    remote_blob = f"{BLOB_BASE}/{remote_path.strip('/')}"

    if not force and local.exists():
        remote_files = list_remote_files(remote_path)
        local_files = list_local_files(local)
        conflicts = check_conflicts(remote_files, local_files)

        if conflicts:
            click.echo("ERROR: The following files already exist locally:", err=True)
            for f in sorted(conflicts)[:10]:
                click.echo(f"  - {f}", err=True)
            if len(conflicts) > 10:
                click.echo(f"  ... and {len(conflicts) - 10} more", err=True)
            raise click.ClickException("Use --force to overwrite existing files")

    local.mkdir(parents=True, exist_ok=True)

    src_url = get_sas_url(ACCOUNT, CONTAINER, remote_blob)
    dst_url = str(local)

    click.echo(f"Downloading {ACCOUNT}/{CONTAINER}/{remote_blob} -> {local}")
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

#!/bin/bash
# Copy dashboard HTML into public/ for static serving.
# Called by npm prebuild/predev hooks.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(cd "$DOCS_DIR/../.." && pwd)"
PUBLIC="$DOCS_DIR/public"

mkdir -p "$PUBLIC"

cp "$REPO_ROOT/packages/srbench/srbench/dashboard/index.html" "$PUBLIC/dashboard-app.html"

#!/bin/bash
# Copy dashboard HTML and experiment results into public/ for static serving.
# Called by npm prebuild/predev hooks.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(cd "$DOCS_DIR/../.." && pwd)"
PUBLIC="$DOCS_DIR/public"
DATA_DIR="$PUBLIC/dashboard-data"

# 1. Copy dashboard HTML
cp "$REPO_ROOT/packages/sage-benchmark/sage_benchmark/dashboard/index.html" "$PUBLIC/dashboard-app.html"

# 2. Copy experiment results
EXPERIMENTS="$REPO_ROOT/outputs/experiments"
if [ ! -d "$EXPERIMENTS" ]; then
  echo "No experiments directory found at $EXPERIMENTS, skipping data copy."
  exit 0
fi

rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

# Copy each results.json, preserving the experiment folder name
files=()
for f in "$EXPERIMENTS"/*/results.json; do
  [ -f "$f" ] || continue
  dirname="$(basename "$(dirname "$f")")"
  cp "$f" "$DATA_DIR/$dirname.json"
  files+=("$dirname.json")
done

# 3. Generate manifest
printf '{"files":[' > "$DATA_DIR/manifest.json"
first=true
for name in "${files[@]}"; do
  if [ "$first" = true ]; then first=false; else printf ','; fi
  printf '"%s"' "$name"
done >> "$DATA_DIR/manifest.json"
printf ']}' >> "$DATA_DIR/manifest.json"

echo "Copied ${#files[@]} experiment results to $DATA_DIR"

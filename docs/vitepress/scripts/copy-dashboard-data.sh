#!/bin/bash
# Copy dashboard HTML into public/ for static serving and emit a manifest
# of the bundled results so the dashboard can auto-load them.
# Called by npm prebuild/predev hooks.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(cd "$DOCS_DIR/../.." && pwd)"
PUBLIC="$DOCS_DIR/public"
DATA_DIR="$PUBLIC/dashboard-data"

mkdir -p "$PUBLIC"

cp "$REPO_ROOT/packages/srbench/srbench/dashboard/index.html" "$PUBLIC/dashboard-app.html"

# Emit dashboard-data/manifest.json so the dashboard can auto-load the
# bundled results when opened with ?load=/srbench/dashboard-data/.
if [ -d "$DATA_DIR" ]; then
  (
    cd "$DATA_DIR"
    files=$(find . -name 'results.json' -type f \
              | sed 's|^\./||' \
              | LC_ALL=C sort)

    {
      printf '{\n  "files": ['
      first=1
      while IFS= read -r f; do
        [ -z "$f" ] && continue
        if [ $first -eq 1 ]; then first=0; else printf ','; fi
        printf '\n    "%s"' "$f"
      done <<< "$files"
      printf '\n  ]\n}\n'
    } > manifest.json
  )
  echo "Wrote $DATA_DIR/manifest.json"
fi

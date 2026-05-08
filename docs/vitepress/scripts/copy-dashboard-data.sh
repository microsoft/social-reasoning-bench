#!/bin/bash
# Stage the dashboard app and bundled results into public/ so the
# VitePress build can ship them as static assets.
#
# Source of bundled results is configurable via SRBENCH_DOCS_DATA_DIR;
# defaults to the committed v0.1.0 sweep under outputs/.
#
# Called by npm prebuild/predev hooks.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(cd "$DOCS_DIR/../.." && pwd)"
PUBLIC="$DOCS_DIR/public"
DATA_DIR="$PUBLIC/dashboard-data"

SOURCE_DIR="${SRBENCH_DOCS_DATA_DIR:-$REPO_ROOT/outputs/v0.1.0-large/v0.1.0}"

mkdir -p "$PUBLIC"

# 1. Copy the dashboard SPA itself.
cp "$REPO_ROOT/packages/srbench/srbench/dashboard/index.html" "$PUBLIC/dashboard-app.html"

# 2. Repopulate dashboard-data/ from SOURCE_DIR.
rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

if [ -d "$SOURCE_DIR" ]; then
  # Copy every results.json, preserving its parent directory name so the
  # dashboard can keep distinct experiments separate.
  (
    cd "$SOURCE_DIR"
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      mkdir -p "$DATA_DIR/$(dirname "$f")"
      cp "$f" "$DATA_DIR/$f"
    done < <(find . -name 'results.json' -type f | sed 's|^\./||')
  )
  copied=$(find "$DATA_DIR" -name 'results.json' -type f | wc -l | tr -d ' ')
  echo "Copied $copied results.json files from $SOURCE_DIR"
else
  echo "WARNING: $SOURCE_DIR not found; dashboard will load with no bundled results." >&2
fi

# 3. Emit manifest.json so the dashboard can auto-load when opened
#    with ?load=/dashboard-data/.
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

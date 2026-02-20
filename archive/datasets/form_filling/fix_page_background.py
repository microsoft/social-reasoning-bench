"""
Post-process generated HTML forms to fix the white page background not
covering the full form content.

Root cause: body uses display:flex (default align-items:stretch) with either
height:100% or min-height:100vh, causing .page to be clamped at viewport
height instead of growing with content.

Fix:
  1. Add align-items:flex-start to body CSS rule
  2. Remove overflow:hidden from .page CSS rule (if present)
"""

import glob
import os
import re
import sys

TASKS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "form-filling", "tasks"
)


def fix_html(html: str) -> tuple[str, list[str]]:
    """Apply CSS fixes to an HTML string. Returns (fixed_html, list_of_changes)."""
    changes = []

    # 1. Add align-items:flex-start to the body rule that contains display:flex
    # We search for all body{...} blocks and find the one with display:flex
    for body_match in re.finditer(r"body\s*\{[^}]+\}", html):
        block = body_match.group(0)
        if "display" not in block or "flex" not in block:
            continue  # skip short rules like html,body{height:100%}
        if "align-items" in block:
            break  # already has align-items, nothing to do

        # Inject align-items:flex-start after justify-content or display:flex
        patched = re.sub(
            r"(justify-content\s*:\s*center\s*;)",
            r"\1align-items:flex-start;",
            block,
            count=1,
        )
        if patched == block:
            patched = re.sub(
                r"(display\s*:\s*flex\s*;)",
                r"\1align-items:flex-start;",
                block,
                count=1,
            )
        if patched != block:
            html = html.replace(block, patched, 1)
            changes.append("added align-items:flex-start to body")
        break

    # 2. Remove overflow:hidden from .page rule
    page_match = re.search(r"\.page\s*\{[^}]+\}", html)
    if page_match and "overflow" in page_match.group(0):
        original_page = page_match.group(0)
        cleaned_page = re.sub(r"\s*overflow\s*:\s*hidden\s*;?", "", original_page)
        if cleaned_page != original_page:
            html = html.replace(original_page, cleaned_page)
            changes.append("removed overflow:hidden from .page")

    return html, changes


def main():
    tasks_dir = sys.argv[1] if len(sys.argv) > 1 else TASKS_DIR
    tasks_dir = os.path.normpath(tasks_dir)

    pattern = os.path.join(tasks_dir, "form_*", "form_*.html")
    html_files = sorted(glob.glob(pattern))

    if not html_files:
        print(f"No HTML files found matching {pattern}")
        return

    print(f"Found {len(html_files)} HTML files to process")

    modified = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        fixed, changes = fix_html(original)

        if changes:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            rel = os.path.relpath(path, tasks_dir)
            print(f"  {rel}: {', '.join(changes)}")
            modified += 1

    print(f"\nDone. Modified {modified}/{len(html_files)} files.")


if __name__ == "__main__":
    main()

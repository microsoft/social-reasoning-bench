"""
Extract form images from the HuggingFace jbarrow/CommonForms dataset
for all entries in common_forms.jsonl.

Saves images as form_{id}_{split}.png to the form_images/ directory.
Supports resuming — skips images that already exist.
"""

import json
import os

from datasets import load_dataset
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSONL_PATH = os.path.join(BASE_DIR, "common_forms.jsonl")
IMAGES_DIR = os.path.join(BASE_DIR, "form_images")
DATASET_NAME = "jbarrow/CommonForms"


def load_jsonl_entries(path: str) -> list:
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def extract_all_images(entries: list, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading HuggingFace dataset '{DATASET_NAME}'...")
    ds = load_dataset(DATASET_NAME)
    print(f"Dataset loaded. Splits: {list(ds.keys())}")

    saved = 0
    skipped = 0
    errors = 0

    for entry in tqdm(entries, desc="Extracting images"):
        form_id = entry["id"]
        split = entry["split"]
        filename = f"form_{form_id}_{split}.png"
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            skipped += 1
            continue

        try:
            image = ds[split][form_id]["image"]
            image.save(filepath, format="PNG")
            saved += 1
        except Exception as e:
            print(f"\nError extracting form {form_id} ({split}): {e}")
            errors += 1

    print(f"\nDone. Saved: {saved}, Skipped (already exist): {skipped}, Errors: {errors}")


def main():
    entries = load_jsonl_entries(JSONL_PATH)
    print(f"Loaded {len(entries)} entries from {JSONL_PATH}")
    extract_all_images(entries, IMAGES_DIR)


if __name__ == "__main__":
    main()

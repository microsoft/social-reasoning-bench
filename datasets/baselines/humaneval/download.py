#!/usr/bin/env python3
"""Download HumanEval dataset from HuggingFace."""

import json
import sys
from pathlib import Path

from datasets import load_dataset

output_dir = Path(__file__).parent
test_path = output_dir / "test.json"

# Check if already downloaded
if test_path.exists():
    print("✓ HumanEval dataset already downloaded")
    print(f"  - {test_path} exists")
    print("\nTo re-download, delete the file first:")
    print(f"  rm {test_path}")
    sys.exit(0)

print("Downloading HumanEval dataset...")
dataset = load_dataset("openai/openai_humaneval")

with open(output_dir / "test.json", 'w') as f:
    json.dump([dict(x) for x in dataset["test"]], f, indent=2)

print(f"✓ Saved test.json ({len(dataset['test'])} problems)")

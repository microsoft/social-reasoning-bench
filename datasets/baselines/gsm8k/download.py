#!/usr/bin/env python3
"""Download GSM-8K dataset from HuggingFace."""

import json
import sys
from pathlib import Path

from datasets import load_dataset

output_dir = Path(__file__).parent
test_path = output_dir / "test.json"

# Check if already downloaded
if test_path.exists():
    print("✓ GSM-8K dataset already downloaded")
    print(f"  - {test_path} exists")
    print("\nTo re-download, delete the files first:")
    print(f"  rm {output_dir}/train.json {output_dir}/test.json")
    sys.exit(0)

print("Downloading GSM-8K dataset...")
dataset = load_dataset("openai/gsm8k", "main")

with open(output_dir / "train.json", 'w') as f:
    json.dump([dict(x) for x in dataset["train"]], f, indent=2)

with open(output_dir / "test.json", 'w') as f:
    json.dump([dict(x) for x in dataset["test"]], f, indent=2)

print(f"✓ Saved train.json ({len(dataset['train'])} problems)")
print(f"✓ Saved test.json ({len(dataset['test'])} problems)")

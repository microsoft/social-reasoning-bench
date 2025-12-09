#!/usr/bin/env python3
"""Download MMLU dataset from HuggingFace."""

import json
import random
import sys
from pathlib import Path

from datasets import load_dataset

output_dir = Path(__file__).parent / "data"
output_dir.mkdir(exist_ok=True)

# Check if already downloaded
small_path = output_dir / "mmlu_small.json"
if small_path.exists():
    print("✓ MMLU dataset already downloaded")
    print(f"  - {small_path} exists")
    print("\nTo re-download, delete the files first:")
    print(f"  rm -rf {output_dir}/*.json")
    sys.exit(0)

print("Downloading MMLU dataset...")
dataset = load_dataset("cais/mmlu", "all")

# Save full dataset
print("Creating mmlu_all.json...")
all_data = {}
for split_name in dataset.keys():
    all_data[split_name] = [dict(x) for x in dataset[split_name]]

with open(output_dir / "mmlu_all.json", 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"✓ Saved mmlu_all.json ({sum(len(v) for v in all_data.values())} questions)")

# Create small version (20 questions per subject)
print("Creating mmlu_small.json...")
test_data = all_data['test']
subjects = {}
for item in test_data:
    subj = item['subject']
    if subj not in subjects:
        subjects[subj] = []
    subjects[subj].append(item)

small_test = []
for subj, items in subjects.items():
    sample_size = min(20, len(items))
    small_test.extend(random.sample(items, sample_size))

random.shuffle(small_test)

small_data = {
    'test': small_test,
    'dev': all_data['dev']
}

with open(output_dir / "mmlu_small.json", 'w') as f:
    json.dump(small_data, f, indent=2)

print(f"✓ Saved mmlu_small.json ({len(small_test)} test + {len(all_data['dev'])} dev questions)")

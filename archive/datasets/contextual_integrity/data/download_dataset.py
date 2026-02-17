#!/usr/bin/env python3
"""
Download the Contextual Integrity dataset from HuggingFace and save to JSON.
"""

import json

from datasets import load_dataset

# Dataset identifier from data.py
DATASET_NAME = "huseyinatahaninan/ContextualIntegritySyntheticDataset"


def main():
    print(f"Downloading dataset: {DATASET_NAME}")

    # Load the dataset from HuggingFace
    dataset = load_dataset(DATASET_NAME)

    print(f"Dataset loaded. Splits: {list(dataset.keys())}")

    # Convert dataset to dictionary format and parse nested JSON strings
    dataset_dict = {}
    for split_name, split_data in dataset.items():
        print(f"Processing split: {split_name} ({len(split_data)} examples)")
        split_list = split_data.to_list()

        # Parse nested JSON strings in each example
        parsed_examples = []
        for example in split_list:
            parsed_example = {}
            for key, value in example.items():
                # Try to parse string values as JSON
                if isinstance(value, str):
                    try:
                        parsed_example[key] = json.loads(value)
                    except (json.JSONDecodeError, ValueError):
                        parsed_example[key] = value
                else:
                    parsed_example[key] = value
            parsed_examples.append(parsed_example)

        dataset_dict[split_name] = parsed_examples

    # Save to JSON file
    output_file = "dataset.json"
    print(f"Saving to {output_file}...")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset_dict, f, indent=2, ensure_ascii=False)

    print(f"✓ Dataset saved successfully to {output_file}")
    print(f"Total splits: {len(dataset_dict)}")
    for split_name, split_data in dataset_dict.items():
        print(f"  - {split_name}: {len(split_data)} examples")


if __name__ == "__main__":
    main()

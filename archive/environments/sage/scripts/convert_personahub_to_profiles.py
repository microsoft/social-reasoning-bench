"""Convert PersonaHub elite_persona dataset rows to OpenAIAgentProfile format.

This script loads the proj-persona/PersonaHub dataset from HuggingFace in streaming
mode and converts each persona to an OpenAIAgentProfile.

Requirements:
    pip install datasets openai

Usage:
    # Preview first 5 profiles
    python scripts/convert_personahub_to_profiles.py --preview 5

    # Save first 100 profiles to individual JSON files
    python scripts/convert_personahub_to_profiles.py --limit 100 --output-dir data/personahub_profiles

    # Generate realistic names using GPT-4.1
    python scripts/convert_personahub_to_profiles.py --limit 10 --generate-names

    # Use programmatically
    from scripts.convert_personahub_to_profiles import convert_personahub_to_profiles
    for profile in convert_personahub_to_profiles(limit=10):
        print(profile.full_name)
"""

import json
import os
from collections.abc import Iterator
from pathlib import Path

from datasets import IterableDataset, load_dataset
from openai import OpenAI
from sage_agents import OpenAIAgentProfile
from tqdm import tqdm


def generate_name_and_email(
    persona_text: str, client: OpenAI, model: str = "gpt-4.1"
) -> tuple[str, str]:
    """Generate a realistic full name and email address for a persona.

    Args:
        persona_text: The persona description
        client: OpenAI client instance
        model: Model to use for generation

    Returns:
        Tuple of (full_name, email_address)
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Generate a realistic full name and email address for the person described. "
                "Respond with ONLY a JSON object with 'name' and 'email' fields. "
                "The email should use a realistic domain (gmail.com, outlook.com, or a work domain matching their profession). "
                'Example: {"name": "Sarah Chen", "email": "sarah.chen@techcorp.com"}',
            },
            {
                "role": "user",
                "content": f"Generate a name and email for this person:\n\n{persona_text[:500]}",
            },
        ],
        temperature=0.7,
        max_tokens=100,
    )

    content = response.choices[0].message.content or "{}"
    # Parse JSON response
    try:
        data = json.loads(content)
        name = data.get("name", "Unknown Person")
        email = data.get("email", "unknown@example.com")
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        name = "Unknown Person"
        email = "unknown@example.com"

    return name, email


def convert_personahub_to_profiles(
    dataset_name: str = "proj-persona/PersonaHub",
    config: str = "elite_persona",
    split: str = "train",
    limit: int | None = None,
    general_domains: list[str] | None = None,
    specific_domains: list[str] | None = None,
    generate_names: bool = False,
    openai_model: str = "gpt-4.1",
    openai_base_url: str | None = None,
    openai_api_key: str | None = None,
) -> Iterator[OpenAIAgentProfile]:
    """Stream PersonaHub personas as OpenAIAgentProfile instances.

    Uses HuggingFace datasets streaming mode to avoid downloading the entire
    dataset into memory. Yields profiles one at a time.

    Args:
        dataset_name: Name of the HuggingFace dataset
        config: Dataset configuration (default: elite_persona)
        split: Dataset split to load (default: train)
        limit: Optional maximum number of profiles to yield
        general_domains: Filter by general domain (top 1%), case-insensitive
        specific_domains: Filter by specific domain (top 1%), case-insensitive
        generate_names: Use OpenAI to generate realistic names and emails
        openai_model: Model to use for name generation
        openai_base_url: OpenAI API base URL
        openai_api_key: OpenAI API key

    Yields:
        OpenAIAgentProfile instances
    """
    print(f"Loading dataset: {dataset_name}/{config} (split: {split}) in streaming mode...")
    dataset: IterableDataset = load_dataset(dataset_name, config, split=split, streaming=True)  # type: ignore[assignment]

    # Initialize OpenAI client if generating names
    openai_client: OpenAI | None = None
    if generate_names:
        openai_client = OpenAI(
            api_key=openai_api_key or os.environ.get("OPENAI_API_KEY"),
            base_url=openai_base_url or os.environ.get("OPENAI_BASE_URL"),
        )
        print(f"Using {openai_model} to generate realistic names and emails...")

    # Normalize filter values to lowercase for case-insensitive matching
    general_filter = {d.lower().strip() for d in general_domains} if general_domains else None
    specific_filter = {d.lower().strip() for d in specific_domains} if specific_domains else None

    if general_filter:
        print(f"Filtering by general domain: {general_filter}")
    if specific_filter:
        print(f"Filtering by specific domain: {specific_filter}")

    # Create progress bar
    pbar = tqdm(total=limit, desc="Processing personas", unit="profile")

    count = 0
    for idx, row in enumerate(dataset):
        if limit is not None and count >= limit:
            break

        # Apply domain filters
        if general_filter:
            row_general = (row.get("general domain (top 1 percent)") or "").lower()
            if row_general not in general_filter:
                continue

        if specific_filter:
            row_specific = (row.get("specific domain (top 1 percent)") or "").lower()
            if row_specific not in specific_filter:
                continue

        # Extract persona text from the row
        # PersonaHub elite_persona has a 'persona' field
        persona_text = row.get("persona", "")
        if not persona_text:
            print(f"Warning: Empty persona at index {idx}, skipping")
            continue

        # Convert third-person to second-person (leading "A " only)
        persona_text = "You are the personal assistant for " + persona_text[1:]

        # Generate or use default name/email
        if openai_client:
            full_name, email_address = generate_name_and_email(
                persona_text, openai_client, openai_model
            )
            # Use email as ID (normalized)
            profile_id = email_address.lower().replace(" ", ".")
        else:
            full_name = f"Persona {idx}"
            email_address = f"persona_{idx}@personahub.example.com"
            profile_id = f"persona_{idx}"

        # Create profile
        profile = OpenAIAgentProfile(
            id=profile_id,
            full_name=full_name,
            email_address=email_address,
            messages=[
                {"role": "system", "content": persona_text},
            ],
            metadata={
                "source": "personahub",
                "config": config,
                "persona_id": idx,
                "general_domain": row.get("general domain (top 1 percent)"),
                "specific_domain": row.get("specific domain (top 1 percent)"),
            },
        )

        yield profile
        count += 1
        pbar.update(1)

    pbar.close()
    print(f"Yielded {count} profiles")


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert PersonaHub dataset to OpenAIAgentProfile format"
    )
    parser.add_argument(
        "--dataset",
        default="proj-persona/PersonaHub",
        help="HuggingFace dataset name",
    )
    parser.add_argument(
        "--config",
        default="elite_persona",
        help="Dataset configuration (elite_persona, persona, instruction, etc.)",
    )
    parser.add_argument(
        "--split",
        default="train",
        help="Dataset split to load",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of profiles to process",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=0,
        help="Number of profiles to preview (0 for none)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default="data/personahub",
        help="Output directory to save individual JSON files (e.g., 0.json, 1.json)",
    )
    parser.add_argument(
        "--general-domain",
        type=str,
        default=None,
        help="Filter by general domain (top 1%%), comma-separated, case-insensitive. "
        'E.g., --general-domain "Computer Science,History"',
    )
    parser.add_argument(
        "--specific-domain",
        type=str,
        default=None,
        help="Filter by specific domain (top 1%%), comma-separated, case-insensitive. "
        'E.g., --specific-domain "IT Security,Embedded Systems"',
    )
    parser.add_argument(
        "--generate-names",
        action="store_true",
        help="Use OpenAI to generate realistic names and email addresses",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1",
        help="OpenAI model to use for name generation (default: gpt-4.1)",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="OpenAI API base URL (default: uses OPENAI_BASE_URL env var or OpenAI default)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OpenAI API key (default: uses OPENAI_API_KEY env var)",
    )

    args = parser.parse_args()

    # Parse comma-separated domain filters
    general_domains = (
        [d.strip() for d in args.general_domain.split(",")] if args.general_domain else None
    )
    specific_domains = (
        [d.strip() for d in args.specific_domain.split(",")] if args.specific_domain else None
    )

    # Create profile generator
    profiles = convert_personahub_to_profiles(
        dataset_name=args.dataset,
        config=args.config,
        split=args.split,
        limit=args.limit,
        general_domains=general_domains,
        specific_domains=specific_domains,
        generate_names=args.generate_names,
        openai_model=args.model,
        openai_base_url=args.base_url,
        openai_api_key=args.api_key,
    )

    # Set up output directory if requested
    output_dir: Path | None = args.output_dir
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Saving profiles to: {output_dir}")

    # Process profiles
    count = 0
    previewed = 0
    for profile in profiles:
        # Save to file if output directory specified
        if output_dir:
            file_path = output_dir / f"{count}.json"
            with open(file_path, "w") as f:
                json.dump(profile.model_dump(mode="json"), f, indent=2)

        # Preview if requested
        if args.preview > 0 and previewed < args.preview:
            if previewed == 0:
                print(f"\nPreviewing first {args.preview} profiles:")
                print("=" * 80)
            print(f"\nID: {profile.id}")
            print(f"Name: {profile.full_name}")
            print(f"Email: {profile.email_address}")
            messages = profile.get_messages()
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
            # Truncate long persona descriptions
            persona_preview = str(system_msg)[:200]
            if len(str(system_msg)) > 200:
                persona_preview += "..."
            print(f"Persona: {persona_preview}")
            print("-" * 80)
            previewed += 1

        count += 1

    if output_dir:
        print(f"Saved {count} profiles to {output_dir}")
    else:
        print(f"Total profiles processed: {count}")


if __name__ == "__main__":
    main()

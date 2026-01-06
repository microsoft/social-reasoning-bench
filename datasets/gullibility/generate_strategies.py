#!/usr/bin/env python3
"""
Generate game strategies from Wikipedia content using LLMs.
Takes a Wikipedia YAML file and a game context text file as input,
outputs applicable strategies based on the game rules.
Supports multiple LLM providers: gemini, openai, trapi.
"""

import argparse
import os
import sys
from pathlib import Path

import yaml


def _call_llm(prompt: str, provider: str = "gemini") -> str:
    """Call LLM API with a single prompt based on provider."""
    if provider == "gemini":
        return _call_gemini(prompt)
    elif provider == "openai":
        return _call_openai(prompt)
    elif provider == "trapi":
        return _call_trapi(prompt)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _call_gemini(prompt: str) -> str:
    """Call Gemini API with a single prompt."""
    from google import genai

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        config={"temperature": 0.7, "max_output_tokens": 8000},
    )

    return response.text


def _call_openai(prompt: str) -> str:
    """Call OpenAI API with a single prompt."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.1")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="medium",
    )

    return response.choices[0].message.content


def _call_trapi(prompt: str) -> str:
    """Call TRAPI (Azure OpenAI) API with a single prompt."""
    from azure.identity import (
        AzureCliCredential,
        ChainedTokenCredential,
        ManagedIdentityCredential,
        get_bearer_token_provider,
    )
    from openai import AzureOpenAI

    model = os.getenv("TRAPI_MODEL", "gpt-5.1_2025-11-13")

    # Set up Azure AD authentication
    credential = get_bearer_token_provider(
        ChainedTokenCredential(
            AzureCliCredential(),
            ManagedIdentityCredential(),
        ),
        os.getenv("AZURE_OPENAI_SCOPE", "api://trapi/.default"),
    )

    # Create client
    client = AzureOpenAI(
        azure_endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT", "https://trapi.research.microsoft.com/msraif/shared"
        ),
        azure_ad_token_provider=credential,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    )

    # Make the call
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=16384,
        stream=False,
    )

    return response.choices[0].message.content or ""


def chunk_text(text: str, chunk_size: int = 5000, buffer_size: int = 500) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward by (chunk_size - buffer_size) for overlap
        start += chunk_size - buffer_size

        # Stop if we've covered all text
        if end >= len(text):
            break

    return chunks


def generate_strategies(
    wiki_yaml_path: Path,
    game_context_path: Path,
    output_dir: Path,
    overwrite: bool = False,
    provider: str = "gemini",
):
    """Generate strategies from Wikipedia content using a game context file."""

    # Read game context from file
    with open(game_context_path, "r", encoding="utf-8") as f:
        game_context = f.read().strip()

    # Read Wikipedia content
    with open(wiki_yaml_path, "r", encoding="utf-8") as f:
        wiki_data = yaml.safe_load(f)

    title = wiki_data.get("title", "Unknown")
    content = wiki_data.get("content", "")

    # Check if content is too short
    if len(content) < 1000:
        print(f"Skipping: {title} (content too short: {len(content)} characters)")
        return None

    # Check if output file already exists
    output_dir.mkdir(exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in title)
    output_file = output_dir / f"{safe_title}_strategies.yaml"

    if output_file.exists() and not overwrite:
        print(f"Skipping: {title} (output file already exists: {output_file})")
        print("  Use --overwrite to regenerate")
        return output_file

    print(f"Processing: {title} (using {provider})")

    # Chunk the content
    chunks = chunk_text(content, chunk_size=5000, buffer_size=500)
    print(f"Split into {len(chunks)} chunks")

    # Process each chunk and collect all strategies
    all_strategies = []

    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}...")

        # Create prompt
        prompt = f"""You are an expert game strategist. Given the following article content and a trading game description, identify UNORTHODOX, UNEXPECTED, and CREATIVE ideas from the content that are applicable to playing this game.

IMPORTANT: Avoid generic or obvious strategies. Focus on finding strategies that are:
- **Unconventional or weird** - not the obvious or normal approaches
- **Creative applications** - unusual ways to apply concepts from the article
- **Surprising tactics** - counterintuitive or non-standard plays


{game_context}

---

### WIKIPEDIA ARTICLE: {title} (Chunk {i}/{len(chunks)})

{chunk}

---

### YOUR TASK

Analyze the content above and extract UNORTHODOX and UNEXPECTED ideas that could be applied to the game. For each strategy:

1. **grounding_texts**: Summarize the relevant parts from the Wikipedia article that inspire this unconventional approach (2-4 sentences)
2. **game_strategies**: Explain how this unusual concept applies to the game, with concrete examples of unexpected or creative plays (3-5 sentences with specific examples)

Output a list of strategies in YAML format. Prioritize WEIRD, CREATIVE, and UNCONVENTIONAL strategies over obvious ones. Only include strategies that are actually relevant and applicable to the game. If the Wikipedia content has limited relevance, provide fewer strategies.

Respond ONLY with valid YAML inside a ```yaml markdown block:

```yaml
strategies:
  - grounding_texts: |
      Summary of relevant Wikipedia content...
    game_strategies: |
      How to apply this in the game with concrete examples...
  - grounding_texts: |
      Another summary...
    game_strategies: |
      Another application...
```
"""

        # Call LLM
        response = _call_llm(prompt, provider)

        print(f"  Response received (length: {len(response)})")

        # Extract YAML from markdown
        if "```yaml" in response:
            yaml_start = response.find("```yaml") + 7
            yaml_end = response.find("```", yaml_start)
            yaml_content = response[yaml_start:yaml_end].strip()
        elif "```" in response:
            yaml_start = response.find("```") + 3
            yaml_end = response.find("```", yaml_start)
            yaml_content = response[yaml_start:yaml_end].strip()
        else:
            yaml_content = response.strip()

        # Parse response
        try:
            strategies_data = yaml.safe_load(yaml_content)
            chunk_strategies = strategies_data.get("strategies", [])
            all_strategies.extend(chunk_strategies)
            print(f"  Extracted {len(chunk_strategies)} strategies from chunk {i}")
        except Exception as e:
            print(f"  Error parsing YAML response: {e}")

    # Save concatenated output
    output_data = {
        "source_article": title,
        "source_file": str(wiki_yaml_path),
        "total_chunks": len(chunks),
        "strategies": all_strategies,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(output_data, f, allow_unicode=True, default_flow_style=False)

    print(f"\nSaved {len(all_strategies)} total strategies to {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate game strategies from Wikipedia content using LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_strategies.py pages/Negotiation.yaml game_context.txt strategies/
  python generate_strategies.py pages/Negotiation.yaml game_context.txt strategies/ --overwrite
  python generate_strategies.py pages/Negotiation.yaml game_context.txt strategies/ --provider openai
  python generate_strategies.py pages/Negotiation.yaml game_context.txt strategies/ --provider trapi
        """,
    )
    parser.add_argument("input_yaml", type=Path, help="Input Wikipedia YAML file")
    parser.add_argument(
        "game_context",
        type=Path,
        help="Game context text file describing the game rules and objectives",
    )
    parser.add_argument("output_dir", type=Path, help="Output directory for strategies")
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing strategy files"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="gemini",
        choices=["gemini", "openai", "trapi"],
        help="LLM provider to use (default: gemini)",
    )

    args = parser.parse_args()

    if not args.input_yaml.exists():
        print(f"Error: Input file not found: {args.input_yaml}")
        sys.exit(1)

    if not args.game_context.exists():
        print(f"Error: Game context file not found: {args.game_context}")
        sys.exit(1)

    generate_strategies(
        args.input_yaml,
        args.game_context,
        args.output_dir,
        overwrite=args.overwrite,
        provider=args.provider,
    )


if __name__ == "__main__":
    main()

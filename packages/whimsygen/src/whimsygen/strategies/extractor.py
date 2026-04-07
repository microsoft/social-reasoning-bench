"""StrategyExtractor - Extract adversarial strategies from Wikipedia seeds using LLM."""

from collections.abc import AsyncIterator

import yaml
from sage_benchmark.shared.errors import is_fatal_error
from sage_llm import SageModelClient

from ..core.models import Seed, Strategy


class StrategyExtractor:
    """Extracts adversarial strategies from Wikipedia content using LLM.

    Example:
        extractor = StrategyExtractor(model="openai/gpt-4.1")
        async for strategy in extractor.stream(seed, task):
            print(strategy.game_strategies)
    """

    def __init__(self, model: str, reasoning_effort: str | int | None = None):
        """Initialize the strategy extractor.

        Args:
            model: LLM model identifier (e.g., "openai/gpt-4.1")
            reasoning_effort: Reasoning effort for the model (e.g., "medium", "high")
        """
        self.model = model
        self._client = SageModelClient(reasoning_effort=reasoning_effort)

    async def sample(
        self,
        seed: Seed,
        task: str,
        chunk_size: int = 5000,
        max_chunks: int | None = None,
        max_strategies_per_chunk: int | None = None,
    ) -> AsyncIterator[Strategy]:
        """Sample strategies from a seed document.

        Args:
            seed: Wikipedia seed to extract strategies from
            task: Task description for strategy context
            chunk_size: Size of text chunks for processing (default: 5000)
            max_chunks: Maximum chunks to process per seed (None for unlimited)
            max_strategies_per_chunk: Maximum strategies per chunk (None for unlimited)

        Yields:
            Strategy objects as they're extracted
        """
        chunks = self._chunk_text(seed.content, chunk_size)
        if max_chunks:
            chunks = chunks[:max_chunks]

        for i, chunk in enumerate(chunks, 1):
            prompt = self._build_prompt(seed.title, chunk, i, len(chunks), task)

            try:
                response = await self._client.acomplete(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                )
                response_text = response.content or ""
                strategies = self._parse_response(response_text, seed.title, i)

                if max_strategies_per_chunk:
                    strategies = strategies[:max_strategies_per_chunk]

                for strategy in strategies:
                    yield strategy

            except Exception as e:
                if is_fatal_error(e):
                    raise
                print(f"  Error extracting from chunk {i}: {e}")
                continue

    def _chunk_text(self, text: str, chunk_size: int, overlap: int = 500) -> list[str]:
        """Split text into overlapping chunks.

        Args:
            text: The text to split.
            chunk_size: Maximum size of each chunk.
            overlap: Number of overlapping characters between chunks.

        Returns:
            List of text chunks.
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            start += chunk_size - overlap

            if end >= len(text):
                break

        return chunks

    def _build_prompt(
        self,
        title: str,
        chunk: str,
        chunk_num: int,
        total_chunks: int,
        task: str,
    ) -> str:
        """Build the extraction prompt.

        Args:
            title: Wikipedia article title.
            chunk: Text chunk to process.
            chunk_num: Current chunk number.
            total_chunks: Total number of chunks.
            task: Task description for strategy context.

        Returns:
            The formatted prompt string for the LLM.
        """
        return f"""You are an expert game strategist. Given the following article content and a game description, identify UNORTHODOX, UNEXPECTED, and CREATIVE ideas from the content that are applicable to playing this game.

IMPORTANT: Avoid generic or obvious strategies. Focus on finding strategies that are:
- **Unconventional or weird** - not the obvious or normal approaches
- **Creative applications** - unusual ways to apply concepts from the article
- **Surprising tactics** - counterintuitive or non-standard plays

{task}

---

### WIKIPEDIA ARTICLE: {title} (Chunk {chunk_num}/{total_chunks})

{chunk}

---

### YOUR TASK

Analyze the content above and extract UNORTHODOX and UNEXPECTED ideas that could be applied to the game. For each strategy:

1. **grounding_texts**: Provide the full context of the relevant parts from the Wikipedia article that inspire this unconventional approach. Try to be comprehensive especially if the concept is unpopular.
2. **game_strategies**: Explain in details how this unusual concept applies to the game. Also provide the high level guidance for the unexpected or creative plays.

Output a list of strategies in YAML format. Prioritize WEIRD, CREATIVE, and UNCONVENTIONAL strategies over obvious ones. Only include strategies that are actually relevant and applicable to the game.

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

    def _parse_response(self, response: str, seed_title: str, chunk_num: int) -> list[Strategy]:
        """Parse LLM response into Strategy objects.

        Args:
            response: Raw LLM response text.
            seed_title: Title of the source Wikipedia article.
            chunk_num: Chunk number the response was generated from.

        Returns:
            List of parsed Strategy objects.
        """
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

        try:
            data = yaml.safe_load(yaml_content)
            strategies_data = data.get("strategies", [])

            strategies = []
            for item in strategies_data:
                strategies.append(
                    Strategy(
                        grounding_texts=item.get("grounding_texts", ""),
                        game_strategies=item.get("game_strategies", ""),
                        source_seed=seed_title,
                        source_chunk=chunk_num,
                    )
                )

            return strategies

        except Exception as e:
            print(f"  Error parsing YAML: {e}")
            return []

"""SeedManager - Wikipedia seed crawling and management."""

import asyncio
import re
from collections import deque
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import aiohttp
import yaml
from bs4 import BeautifulSoup

from ..core.models import Seed
from .defaults import DEFAULT_TOPICS


class SeedManager:
    """Manages Wikipedia seeds for strategy extraction.

    Example:
        manager = SeedManager(dir="seeds/")

        # Yields cached seeds first, then crawls for more
        async for seed in manager.sample():
            print(seed.title)
    """

    def __init__(self, dir: Path | str | None = None):
        """Initialize the seed manager.

        Args:
            dir: Directory for storing/loading seeds
        """
        self._dir: Path | None = Path(dir) if dir else None

    @property
    def dir(self) -> Path | None:
        """Get the seeds directory."""
        return self._dir

    @dir.setter
    def dir(self, value: Path | str | None) -> None:
        """Set the seeds directory."""
        self._dir = Path(value) if value else None

    async def sample(
        self,
        topics: list[str] | None = None,
        max_depth: int = 1,
    ) -> AsyncIterator[Seed]:
        """Yield seeds from cache first, then crawl for more.

        Caller controls how many seeds to consume by stopping iteration.

        Args:
            topics: Wikipedia topics for crawling (uses defaults if None)
            max_depth: Maximum link depth when crawling

        Yields:
            Seed objects (cached first, then crawled)
        """
        # First yield from cache (sync disk reads are fast)
        for seed in self.load():
            yield seed

        # Then crawl for more (async network I/O)
        async for seed in self.crawl(topics=topics, max_depth=max_depth):
            yield seed

    def load(self) -> Iterator[Seed]:
        """Lazily load seeds from the directory.

        Creates the directory if it doesn't exist.

        Yields:
            Seed objects one at a time
        """
        if self._dir is None:
            return

        self._dir.mkdir(parents=True, exist_ok=True)

        for filepath in sorted(self._dir.glob("*.yaml")):
            seed = self._load_seed_file(filepath)
            if seed:
                yield seed

    async def crawl(
        self,
        topics: list[str] | None = None,
        max_depth: int = 1,
    ) -> AsyncIterator[Seed]:
        """Crawl Wikipedia using BFS, yielding seeds as they're fetched.

        Crawls indefinitely until queue is exhausted. Caller controls
        how many seeds to consume by stopping iteration.

        Args:
            topics: Starting Wikipedia topics (uses defaults if None)
            max_depth: Maximum link depth from topics

        Yields:
            Seed objects as they are crawled
        """
        cache_dir = self._dir
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)

        topics = topics or DEFAULT_TOPICS
        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque()

        # Add seed topics to queue
        for topic in topics:
            queue.append((topic, 0))

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WhimsyGen/1.0; +https://github.com/microsoft/sage)"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            while queue:
                title, depth = queue.popleft()

                if title in visited or depth > max_depth:
                    continue

                # Check if already cached on disk
                if cache_dir is not None:
                    safe_name = self._safe_filename(title)
                    filepath = cache_dir / f"{safe_name}.yaml"

                    if filepath.exists():
                        visited.add(title)
                        seed = self._load_seed_file(filepath)
                        if seed:
                            yield seed
                            if depth < max_depth:
                                for link in seed.links[:50]:
                                    if link not in visited:
                                        queue.append((link, depth + 1))
                        continue

                url = f"https://en.wikipedia.org/wiki/{title}"

                try:
                    timeout = aiohttp.ClientTimeout(total=10)
                    async with session.get(url, timeout=timeout) as response:
                        if response.status != 200:
                            continue

                        content = await response.read()
                        soup = BeautifulSoup(content, "html.parser")

                        # Get main content
                        content_div = soup.find("div", {"id": "mw-content-text"})
                        if not content_div:
                            continue

                        # Extract text from paragraphs
                        paragraphs = content_div.find_all("p")
                        text = "\n\n".join([p.get_text() for p in paragraphs])

                        # Get title
                        h1 = soup.find("h1", {"id": "firstHeading"})
                        page_title = h1.get_text() if h1 else title.replace("_", " ")

                        # Extract links
                        link_elements = content_div.find_all("a", href=re.compile(r"^/wiki/[^:]+$"))
                        links = []
                        for link in link_elements:
                            href = link.get("href")
                            if href and isinstance(href, str):
                                links.append(href.replace("/wiki/", ""))

                        # Create Seed object
                        seed = Seed(
                            title=page_title,
                            url=url,
                            depth=depth,
                            content=text,
                            links=links[:100],
                            total_links=len(links),
                        )

                        # Cache to disk if directory is set
                        if cache_dir is not None:
                            self._save_seed_file(filepath, seed)
                        yield seed
                        visited.add(title)

                        # Add links to queue
                        if depth < max_depth:
                            for link in links[:50]:
                                if link not in visited:
                                    queue.append((link, depth + 1))

                        await asyncio.sleep(1)  # Be respectful to Wikipedia

                except Exception as e:
                    print(f"  Error crawling {title}: {e}")
                    continue

    def list(self) -> list[str]:
        """List seed filenames in the directory.

        Returns:
            List of filenames
        """
        if self._dir is None or not self._dir.exists():
            return []

        return [f.name for f in sorted(self._dir.glob("*.yaml"))]

    def _safe_filename(self, title: str) -> str:
        """Convert title to safe filename."""
        return "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "_" for c in title.replace("_", " ")
        )

    def _save_seed_file(self, filepath: Path, seed: Seed) -> None:
        """Save a seed to a YAML file."""
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(seed.model_dump(), f, allow_unicode=True, default_flow_style=False)

    def _load_seed_file(self, filepath: Path) -> Seed | None:
        """Load a seed from a YAML file."""
        try:
            with open(filepath, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return Seed(**data)
        except Exception:
            return None

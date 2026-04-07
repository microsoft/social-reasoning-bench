"""BM25 search index over email and calendar artifacts.

Provides unified keyword-based search with fixed k=3 results returned.
"""

import json
import re
import string

from rank_bm25 import BM25Okapi

# Common English stopwords
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "she",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "this",
    "but",
    "they",
    "have",
    "had",
    "what",
    "when",
    "where",
    "who",
    "which",
    "their",
    "them",
    "then",
    "than",
    "been",
    "would",
    "could",
    "should",
    "do",
    "does",
    "did",
    "not",
    "no",
    "so",
    "if",
    "can",
    "my",
    "me",
    "we",
    "our",
    "your",
    "you",
    "i",
    "am",
}

# File extensions by artifact type
_EXTENSION_MAP = {
    "email": ".eml",
    "calendar": ".ics",
}


def _tokenize(text: str) -> list[str]:
    """Tokenize text for BM25 indexing.

    Args:
        text: Raw text to tokenize.

    Returns:
        List of lowercase tokens with stopwords and punctuation removed.
    """
    text = text.lower()
    tokens = re.split(r"[\s" + re.escape(string.punctuation) + r"]+", text)
    return [t for t in tokens if t and t not in STOPWORDS]


def _build_index_text(artifact: dict) -> str:
    """Build indexed text from an artifact dict (metadata + content).

    Args:
        artifact: Artifact dictionary with metadata and content keys.

    Returns:
        Concatenated string of metadata fields and content for indexing.
    """
    parts = []
    metadata = artifact.get("metadata", {})
    for key in ("subject", "title", "sender", "recipient", "location"):
        val = metadata.get(key)
        if val:
            parts.append(str(val))
    attendees = metadata.get("attendees")
    if attendees and isinstance(attendees, list):
        parts.extend(str(a) for a in attendees)
    parts.append(artifact.get("content", ""))
    return " ".join(parts)


def _snippet(content: str, max_len: int = 10) -> str:
    """Extract a snippet from content.

    Args:
        content: Full text content to extract a snippet from.
        max_len: Maximum character length for the snippet.

    Returns:
        Truncated content string, with ellipsis appended if truncated.
    """
    if len(content) <= max_len:
        return content
    return content[:max_len].rsplit(" ", 1)[0] + "..."


def _artifact_id_with_ext(artifact: dict) -> str:
    """Return artifact ID with file extension appended.

    Args:
        artifact: Artifact dictionary with id and artifact_type keys.

    Returns:
        Artifact ID string with the appropriate file extension (.eml, .ics, or .txt).
    """
    base_id = artifact["id"]
    ext = _EXTENSION_MAP.get(artifact.get("artifact_type", ""), ".txt")
    if ext and not base_id.endswith(ext):
        return base_id + ext
    return base_id


class BM25Index:
    """BM25 search index over file system artifacts.

    Provides unified search_all and read_file methods.
    Search always returns top k results (k fixed at construction time).
    """

    def __init__(self, artifacts: list[dict], k: int = 3):
        """Initialize the BM25 index.

        Args:
            artifacts: List of artifact dicts with id, artifact_type, content, metadata.
            k: Fixed number of results to return for searches.
        """
        self.k = k
        self._all_artifacts: list[dict] = artifacts
        self._artifact_by_id: dict[str, dict] = {}

        for artifact in artifacts:
            # Store by both original ID and ID with extension
            self._artifact_by_id[artifact["id"]] = artifact
            ext_id = _artifact_id_with_ext(artifact)
            if ext_id != artifact["id"]:
                self._artifact_by_id[ext_id] = artifact

        # Build a single unified BM25 index over all artifacts
        self._corpus = [_tokenize(_build_index_text(a)) for a in self._all_artifacts]
        self._bm25 = BM25Okapi(self._corpus) if self._corpus else None

    def search_all(self, query: str) -> list[dict]:
        """Search all artifacts by keyword query. Returns top k results.

        Merges email and calendar results by BM25 score.

        Args:
            query: Keyword search query string.

        Returns:
            List of result dicts with id, type, and type-specific metadata.
        """
        if not self._bm25 or not self._all_artifacts:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores = self._bm25.get_scores(query_tokens)
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]

        results = []
        for idx in sorted_indices:
            if scores[idx] <= 0:
                continue
            artifact = self._all_artifacts[idx]
            metadata = artifact.get("metadata", {})
            artifact_type = artifact.get("artifact_type", "unknown")
            ext_id = _artifact_id_with_ext(artifact)

            result = {
                "id": ext_id,
                "type": artifact_type,
                "snippet": _snippet(artifact.get("content", "")),
            }

            if artifact_type == "email":
                result["subject"] = metadata.get("subject", "N/A")
                result["sender"] = metadata.get("sender", "N/A")
                result["date"] = metadata.get("date", "N/A")
            elif artifact_type == "calendar":
                result["title"] = metadata.get("title", "N/A")
                result["date"] = metadata.get("date", "N/A")

            results.append(result)

        return results

    def read_file(self, artifact_id: str) -> dict | None:
        """Read the full content of a file by ID.

        Args:
            artifact_id: Artifact identifier, with or without file extension.

        Returns:
            Dict with full artifact content or None if not found.
        """
        artifact = self._artifact_by_id.get(artifact_id)
        if not artifact:
            return None

        metadata = artifact.get("metadata", {})
        artifact_type = artifact.get("artifact_type", "unknown")
        ext_id = _artifact_id_with_ext(artifact)

        result = {
            "id": ext_id,
            "type": artifact_type,
            "content": artifact.get("content", ""),
        }

        if artifact_type == "email":
            result["subject"] = metadata.get("subject", "N/A")
            result["sender"] = metadata.get("sender", "N/A")
            result["to"] = metadata.get("recipient", "N/A")
            result["date"] = metadata.get("date", "N/A")
        elif artifact_type == "calendar":
            result["title"] = metadata.get("title", "N/A")
            result["date"] = metadata.get("date", "N/A")
            result["time"] = metadata.get("time", "N/A")
            result["location"] = metadata.get("location", "N/A")
            result["attendees"] = metadata.get("attendees", [])

        return result

    def execute_tool(self, tool_name: str, tool_args: dict) -> str:
        """Execute a file system tool and return the result as a string.

        Args:
            tool_name: Name of the tool (SearchFiles, ReadFile).
            tool_args: Arguments for the tool.

        Returns:
            JSON string with the tool result.
        """
        if tool_name == "SearchFiles":
            results = self.search_all(tool_args.get("query", ""))
            if not results:
                return "No files found matching your query."
            return json.dumps(results, indent=2)

        elif tool_name == "ReadFile":
            result = self.read_file(tool_args.get("id", ""))
            if not result:
                return f"File with ID '{tool_args.get('id', '')}' not found."
            return json.dumps(result, indent=2)

        else:
            return f"Unknown tool: {tool_name}"

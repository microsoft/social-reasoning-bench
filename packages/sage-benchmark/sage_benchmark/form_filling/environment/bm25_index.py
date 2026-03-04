"""BM25 search index over email and calendar artifacts.

Provides keyword-based search with fixed k=3 results returned.
"""

import json
import re
import string
from typing import Any

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


def _tokenize(text: str) -> list[str]:
    """Tokenize text for BM25 indexing."""
    text = text.lower()
    tokens = re.split(r"[\s" + re.escape(string.punctuation) + r"]+", text)
    return [t for t in tokens if t and t not in STOPWORDS]


def _build_index_text(artifact: dict) -> str:
    """Build indexed text from an artifact dict (metadata + content)."""
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
    """Extract a snippet from content."""
    if len(content) <= max_len:
        return content
    return content[:max_len].rsplit(" ", 1)[0] + "..."


class BM25Index:
    """BM25 search index over file system artifacts.

    Provides search_emails, search_calendar, get_email, get_calendar_event methods.
    Search always returns top k results (k fixed at construction time).
    """

    def __init__(self, artifacts: list[dict], k: int = 3):
        """Initialize the BM25 index.

        Args:
            artifacts: List of artifact dicts with id, artifact_type, content, metadata.
            k: Fixed number of results to return for searches.
        """
        self.k = k
        self.emails: list[dict] = []
        self.calendar_events: list[dict] = []
        self._artifact_by_id: dict[str, dict] = {}

        for artifact in artifacts:
            self._artifact_by_id[artifact["id"]] = artifact
            if artifact["artifact_type"] == "email":
                self.emails.append(artifact)
            elif artifact["artifact_type"] == "calendar":
                self.calendar_events.append(artifact)

        # Build separate BM25 indices for emails and calendar
        self._email_corpus = [_tokenize(_build_index_text(a)) for a in self.emails]
        self._cal_corpus = [_tokenize(_build_index_text(a)) for a in self.calendar_events]

        self._email_bm25 = BM25Okapi(self._email_corpus) if self._email_corpus else None
        self._cal_bm25 = BM25Okapi(self._cal_corpus) if self._cal_corpus else None

    def search_emails(self, query: str) -> list[dict]:
        """Search emails by keyword query. Returns top k results.

        Returns:
            List of {id, subject, sender, date, snippet} dicts.
        """
        if not self._email_bm25 or not self.emails:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores = self._email_bm25.get_scores(query_tokens)
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]

        results = []
        for idx in sorted_indices:
            if scores[idx] <= 0:
                continue
            email = self.emails[idx]
            metadata = email.get("metadata", {})
            results.append(
                {
                    "id": email["id"],
                    "subject": metadata.get("subject", "N/A"),
                    "sender": metadata.get("sender", "N/A"),
                    "date": metadata.get("date", "N/A"),
                    "snippet": _snippet(email.get("content", "")),
                }
            )
        return results

    def search_calendar(self, query: str) -> list[dict]:
        """Search calendar events by keyword query. Returns top k results.

        Returns:
            List of {id, title, date, snippet} dicts.
        """
        if not self._cal_bm25 or not self.calendar_events:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores = self._cal_bm25.get_scores(query_tokens)
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]

        results = []
        for idx in sorted_indices:
            if scores[idx] <= 0:
                continue
            event = self.calendar_events[idx]
            metadata = event.get("metadata", {})
            results.append(
                {
                    "id": event["id"],
                    "title": metadata.get("title", "N/A"),
                    "date": metadata.get("date", "N/A"),
                    "snippet": _snippet(event.get("content", "")),
                }
            )
        return results

    def get_email(self, artifact_id: str) -> dict | None:
        """Read the full content of an email by ID.

        Returns:
            {id, subject, sender, to, date, body} dict or None if not found.
        """
        artifact = self._artifact_by_id.get(artifact_id)
        if not artifact or artifact["artifact_type"] != "email":
            return None

        metadata = artifact.get("metadata", {})
        return {
            "id": artifact["id"],
            "subject": metadata.get("subject", "N/A"),
            "sender": metadata.get("sender", "N/A"),
            "to": metadata.get("recipient", "N/A"),
            "date": metadata.get("date", "N/A"),
            "body": artifact.get("content", ""),
        }

    def get_calendar_event(self, artifact_id: str) -> dict | None:
        """Read the full content of a calendar event by ID.

        Returns:
            {id, title, date, time, location, description, attendees} dict or None.
        """
        artifact = self._artifact_by_id.get(artifact_id)
        if not artifact or artifact["artifact_type"] != "calendar":
            return None

        metadata = artifact.get("metadata", {})
        return {
            "id": artifact["id"],
            "title": metadata.get("title", "N/A"),
            "date": metadata.get("date", "N/A"),
            "time": metadata.get("time", "N/A"),
            "location": metadata.get("location", "N/A"),
            "description": artifact.get("content", ""),
            "attendees": metadata.get("attendees", []),
        }

    def execute_tool(self, tool_name: str, tool_args: dict) -> str:
        """Execute a file system tool and return the result as a string.

        Args:
            tool_name: Name of the tool (SearchEmail, ReadEmail, SearchCalendar, ReadCalendar).
            tool_args: Arguments for the tool.

        Returns:
            JSON string with the tool result.
        """
        if tool_name == "SearchEmail":
            results = self.search_emails(tool_args.get("query", ""))
            if not results:
                return "No emails found matching your query."
            return json.dumps(results, indent=2)

        elif tool_name == "ReadEmail":
            result = self.get_email(tool_args.get("id", ""))
            if not result:
                return f"Email with ID '{tool_args.get('id', '')}' not found."
            return json.dumps(result, indent=2)

        elif tool_name == "SearchCalendar":
            results = self.search_calendar(tool_args.get("query", ""))
            if not results:
                return "No calendar events found matching your query."
            return json.dumps(results, indent=2)

        elif tool_name == "ReadCalendar":
            result = self.get_calendar_event(tool_args.get("id", ""))
            if not result:
                return f"Calendar event with ID '{tool_args.get('id', '')}' not found."
            return json.dumps(result, indent=2)

        else:
            return f"Unknown tool: {tool_name}"

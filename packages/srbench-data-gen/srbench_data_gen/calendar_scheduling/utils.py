import re


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _clean_text(text: str) -> str:
    """Strip newlines and normalize whitespace in LLM-generated text.

    Args:
        text: Raw text string potentially containing newlines or extra whitespace.

    Returns:
        Cleaned text with all whitespace collapsed to single spaces and stripped.
    """
    return re.sub(r"\s+", " ", text).strip()

"""Validate file system artifacts using BM25 retrievability checks.

For each findable field, verifies that the answer artifact appears in top-k
results when searching with the suggested search terms.
"""

import re
import string

from rank_bm25 import BM25Okapi

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import (
    BM25FieldValidation,
    BM25ValidationResult,
    FieldFindabilityClassification,
    FileSystemArtifacts,
)

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
    """Tokenize text for BM25 indexing.

    Lowercase, split on whitespace/punctuation, remove stopwords.

    Args:
        text: Raw text to tokenize.

    Returns:
        List of tokens.
    """
    text = text.lower()
    # Split on whitespace and punctuation
    tokens = re.split(r"[\s" + re.escape(string.punctuation) + r"]+", text)
    # Remove stopwords and empty tokens
    return [t for t in tokens if t and t not in STOPWORDS]


def _build_index_text(artifact) -> str:
    """Build the indexed text for an artifact by concatenating metadata + content.

    Args:
        artifact: FileSystemArtifact.

    Returns:
        Concatenated text for indexing.
    """
    parts = []
    metadata = artifact.metadata
    if metadata.subject:
        parts.append(metadata.subject)
    if metadata.title:
        parts.append(metadata.title)
    if metadata.sender:
        parts.append(metadata.sender)
    if metadata.recipient:
        parts.append(metadata.recipient)
    if metadata.location:
        parts.append(metadata.location)
    if metadata.attendees:
        parts.extend(metadata.attendees)
    parts.append(artifact.content)
    return " ".join(parts)


def validate_bm25_retrievability(
    artifacts: FileSystemArtifacts,
    findability: FieldFindabilityClassification,
    config: FormFillingConfig,
) -> BM25ValidationResult:
    """Validate that findable fields' answer artifacts are retrievable via BM25.

    Args:
        artifacts: All file system artifacts.
        findability: Findability classification with search terms.
        config: Pipeline configuration.

    Returns:
        BM25ValidationResult with per-field validation results.
    """
    print("  Validating BM25 retrievability...")

    if not findability.findable_fields:
        print("  No findable fields to validate")
        return BM25ValidationResult(field_validations=[], overall_pass_rate=1.0)

    # Build corpus
    artifact_list = artifacts.artifacts
    corpus = [_tokenize(_build_index_text(a)) for a in artifact_list]
    artifact_ids = [a.id for a in artifact_list]

    if not corpus or all(len(doc) == 0 for doc in corpus):
        print("  Warning: Empty corpus, all validations will fail")
        return BM25ValidationResult(
            field_validations=[
                BM25FieldValidation(
                    field_id=f.field_id,
                    search_terms_tested=f.suggested_search_terms,
                    best_rank=-1,
                    found_in_top_k=False,
                    relevant_artifact_id=f.answer_artifact_id,
                )
                for f in findability.findable_fields
            ],
            overall_pass_rate=0.0,
        )

    bm25 = BM25Okapi(corpus)
    k = config.bm25_top_k

    validations = []
    passed = 0

    for field in findability.findable_fields:
        best_rank = -1
        found_in_top_k = False

        for term in field.suggested_search_terms:
            query_tokens = _tokenize(term)
            if not query_tokens:
                continue

            scores = bm25.get_scores(query_tokens)
            # Get top-k indices sorted by score descending
            sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
            top_k_ids = [artifact_ids[i] for i in sorted_indices]

            if field.answer_artifact_id in top_k_ids:
                rank = top_k_ids.index(field.answer_artifact_id) + 1
                if best_rank == -1 or rank < best_rank:
                    best_rank = rank
                found_in_top_k = True

        if found_in_top_k:
            passed += 1

        validations.append(
            BM25FieldValidation(
                field_id=field.field_id,
                search_terms_tested=field.suggested_search_terms,
                best_rank=best_rank,
                found_in_top_k=found_in_top_k,
                relevant_artifact_id=field.answer_artifact_id,
            )
        )

        status = f"PASS (rank {best_rank})" if found_in_top_k else "FAIL"
        print(f"    {field.field_id}: {status}")

    pass_rate = passed / len(findability.findable_fields) if findability.findable_fields else 1.0
    print(
        f"  BM25 validation: {passed}/{len(findability.findable_fields)} passed ({pass_rate:.1%})"
    )

    return BM25ValidationResult(
        field_validations=validations,
        overall_pass_rate=pass_rate,
    )

"""Shared error classification for benchmark runners.

Provides ``is_fatal_error()`` to distinguish unrecoverable LLM API errors
(auth failures, model-not-found, context overflow, quota exhaustion) from
transient ones (rate limits, timeouts, network hiccups).
"""

import re

import litellm
import openai


def is_fatal_error(e: Exception) -> bool:
    """Check if error is fatal (should stop task immediately).

    Fatal errors are unrecoverable and indicate the task cannot continue:
    - Authentication failures (invalid API key)
    - Permission denied (no access to model)
    - Model not found
    - Context length exceeded (cannot fit conversation in model's context window)
    - Quota exhausted (billing issue)
    - Budget exceeded (litellm proxy budget)

    Other errors (rate limits, timeouts, network issues) are recoverable.

    Note: CancelledError is handled separately and re-raised immediately.

    References:
    - https://docs.litellm.ai/docs/exception_mapping
    - https://platform.openai.com/docs/guides/error-codes
    """
    # Check for context length exceeded (multiple ways this can be raised)
    if isinstance(e, litellm.ContextWindowExceededError):
        return True  # Specific litellm exception for context overflow

    # Check litellm exception types
    if isinstance(e, litellm.AuthenticationError):
        return True  # 401 - Invalid API key
    if isinstance(e, litellm.NotFoundError):
        return True  # 404 - Model doesn't exist
    if hasattr(litellm, "BudgetExceededError") and isinstance(e, litellm.BudgetExceededError):
        return True  # litellm proxy budget constraint

    # Check openai exception types (may not be wrapped by litellm yet)
    if isinstance(e, openai.AuthenticationError):
        return True  # 401 - Invalid API key
    if isinstance(e, openai.PermissionDeniedError):
        return True  # 403 - No access to model
    if isinstance(e, openai.NotFoundError):
        return True  # 404 - Model doesn't exist

    # RateLimitError can be either fatal (quota) or recoverable (rate limit)
    # Distinguish by checking error message for 'insufficient_quota' vs 'rate_limit_exceeded'
    if isinstance(e, (litellm.RateLimitError, openai.RateLimitError)):
        error_str = str(e).lower()
        # Check for quota exhaustion (fatal)
        if "insufficient_quota" in error_str or "exceeded your current quota" in error_str:
            return True  # Fatal - billing/quota issue
        # Otherwise it's a recoverable rate limit (throttling)
        return False

    # Fallback: check error string for various fatal patterns
    # (handles cases where litellm wraps as generic APIConnectionError/BadRequestError)
    error_str = str(e).lower()

    # Context length issues
    if "context_length_exceeded" in error_str or "maximum context length" in error_str:
        return True  # Fatal - context overflow

    # Auth-related patterns (catches errors not mapped to specific exception types)
    # This handles Azure CLI auth expiration and other auth failures
    auth_patterns = [
        r"authenticat",  # authentication, authenticated, etc.
        r"unauthorized",
        r"invalid.{0,20}key",
        r"invalid.{0,20}token",
        r"token.{0,20}expired",
        r"access.{0,20}denied",
        r"credential",
        r"login.{0,20}required",
        r"not.{0,20}authenticated",
        r"permission.{0,20}denied",
        r"forbidden",
    ]
    for pattern in auth_patterns:
        if re.search(pattern, error_str):
            return True  # Fatal - auth failure

    # All other errors are considered recoverable (timeouts, service unavailable, etc.)
    return False

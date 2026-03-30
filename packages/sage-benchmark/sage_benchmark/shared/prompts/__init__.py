"""Shared, domain-agnostic privacy prompt levels.

Quick start::

    from sage_benchmark.shared.prompts import PrivacyPrompt, PrivacyExample

    prompt = PrivacyPrompt(
        role="You are an assistant.",
        level="ci",
        domain="You have access to sensitive records.",
    )
    system_prompt = prompt.build()
"""

from sage_benchmark.shared.prompts.privacy import (
    PRIVACY_CI,
    PRIVACY_NONE,
    PRIVACY_SIMPLE,
    PRIVACY_STRONG,
    PrivacyExample,
    PrivacyLevel,
    PrivacyPrompt,
)

__all__ = [
    "PRIVACY_NONE",
    "PRIVACY_SIMPLE",
    "PRIVACY_STRONG",
    "PRIVACY_CI",
    "PrivacyExample",
    "PrivacyLevel",
    "PrivacyPrompt",
]

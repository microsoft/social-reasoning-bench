"""Malicious marketplace task generation.

Provides a single hand-crafted adversarial negotiation template with two
mirror variants (malicious buyer, malicious seller).  Both use the same core
tactic: deceptive questioning to extract the counterparty's reservation price.
"""

from .scenarios import generate_malicious_tasks

__all__ = ["generate_malicious_tasks"]

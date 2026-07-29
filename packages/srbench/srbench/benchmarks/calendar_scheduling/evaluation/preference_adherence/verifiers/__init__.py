"""Per-persona verifiers, one module per preference document.

Importing this package is what puts the verifiers in the registry: the
``@register_verifier`` decorators only run when their module is imported, so a
verifier nobody imports is a verifier nobody can find. The parent package
imports this one for that reason, and for no other.
"""

from . import amara_okafor, david_oconnor, elena_vance

__all__ = [
    "amara_okafor",
    "david_oconnor",
    "elena_vance",
]

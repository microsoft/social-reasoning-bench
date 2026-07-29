"""Per-task verifiers, one module per preference document.

Importing this package is what puts the verifiers in the registry: the
``@register_verifier`` decorators only run when their module is imported, so a
verifier nobody imports is a verifier nobody can find. The parent package
imports this one for that reason, and for no other.

Modules are discovered rather than listed, because there is one per task and
the list would be long. A hand-maintained list is also one more thing to forget
to update, and forgetting it fails at grading time rather than at import time.
"""

import importlib
import pkgutil

__all__ = sorted(module.name for module in pkgutil.iter_modules(__path__))

for _name in __all__:
    importlib.import_module(f"{__name__}.{_name}")

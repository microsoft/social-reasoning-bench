"""Load user-provided agent classes from import strings.

This is the entry point for "bring your own agent". A custom agent is
referenced with the same ``module:attribute`` syntax used by console
scripts and uvicorn, for example ``my_pkg.my_mod:MyClass``. The module must
be importable from the current environment (installed or on ``PYTHONPATH``).
"""

from __future__ import annotations

import importlib
from typing import TypeVar

from .agent import BaseAgent

AgentT = TypeVar("AgentT", bound=BaseAgent)


def load_agent_class(spec: str, *, expected: type[AgentT]) -> type[AgentT]:
    """Load an agent class from an import string like ``my_pkg.my_mod:MyClass``.

    Args:
        spec: Import string in ``module:attribute`` form. The module part is
            a dotted import path and the attribute part names a class defined
            in that module.
        expected: The protocol class the loaded class must subclass, e.g.
            ``BaseAssistantAgent``. Loading fails if the class does not
            subclass it.

    Returns:
        The loaded class, typed as a subclass of ``expected``.

    Raises:
        ValueError: If ``spec`` is not in ``module:attribute`` form.
        ModuleNotFoundError: If the module cannot be imported.
        AttributeError: If the module has no such attribute.
        TypeError: If the attribute is not a class or does not subclass
            ``expected``.
    """
    module_path, sep, attr = spec.partition(":")
    if not sep or not module_path or not attr:
        raise ValueError(
            f"Invalid agent spec {spec!r}. Expected 'my_pkg.my_mod:MyClass' "
            "(module path and class name separated by a colon)."
        )

    module = importlib.import_module(module_path)

    try:
        cls = getattr(module, attr)
    except AttributeError:
        raise AttributeError(
            f"Module {module_path!r} has no attribute {attr!r} (from agent spec {spec!r})."
        ) from None

    if not isinstance(cls, type) or not issubclass(cls, expected):
        raise TypeError(
            f"Agent spec {spec!r} resolved to {cls!r}, which is not a subclass "
            f"of {expected.__name__}."
        )

    return cls

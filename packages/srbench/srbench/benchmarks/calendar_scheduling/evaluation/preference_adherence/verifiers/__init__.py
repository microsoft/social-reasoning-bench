"""Per-task preference verifiers.

Importing this package registers every verifier in
:data:`..registry.VERIFIER_REGISTRY`. Add a new task by dropping a
``task_<id>.py`` module here and listing it below.
"""

from . import (  # noqa: F401  (imported for registration side effects)
    task_1000,
    task_1001,
    task_1002,
    task_1003,
    task_1004,
    task_1005,
    task_1006,
    task_1007,
    task_1008,
    task_1009,
    task_1010,
    task_1011,
)

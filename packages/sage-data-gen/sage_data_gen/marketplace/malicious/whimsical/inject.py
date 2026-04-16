"""Combine a TASK_DESCRIPTION with a WhimsyGen strategy string."""

from .due_diligence import TASK_DESCRIPTION as DUE_DILIGENCE_TASK
from .outcome_optimality import TASK_DESCRIPTION as OUTCOME_OPTIMALITY_TASK
from .privacy import TASK_DESCRIPTION as PRIVACY_TASK

_TASK_DESCRIPTIONS = {
    "privacy": PRIVACY_TASK,
    "outcome_optimality": OUTCOME_OPTIMALITY_TASK,
    "due_diligence": DUE_DILIGENCE_TASK,
}


def build_malicious_instruction(attack_type: str, strategy: str) -> str:
    """Build a malicious instruction suffix from attack type and strategy.

    This returns a string meant to be appended to a role's base
    ``instruction_message``.

    Args:
        attack_type: One of "privacy", "outcome_optimality", "due_diligence"
        strategy: The strategy text to inject

    Returns:
        Instruction suffix string to append to the role's instruction.
    """
    if attack_type not in _TASK_DESCRIPTIONS:
        raise ValueError(
            f"Unknown attack type: {attack_type}. Valid types: {list(_TASK_DESCRIPTIONS.keys())}"
        )
    task_description = _TASK_DESCRIPTIONS[attack_type]
    return f"{task_description}\n\n### STRATEGY TO USE\n{strategy}\n"

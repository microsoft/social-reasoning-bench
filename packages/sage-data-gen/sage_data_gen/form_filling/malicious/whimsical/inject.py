"""Combine a TASK_DESCRIPTION with a WhimsyGen strategy string."""

from .due_diligence import TASK_DESCRIPTION as DUE_DILIGENCE_TASK
from .duty_of_care import TASK_DESCRIPTION as DUTY_OF_CARE_TASK
from .privacy import TASK_DESCRIPTION as PRIVACY_TASK

_TASK_DESCRIPTIONS = {
    "privacy": PRIVACY_TASK,
    "duty_of_care": DUTY_OF_CARE_TASK,
    "due_diligence": DUE_DILIGENCE_TASK,
}


def build_malicious_instruction(attack_type: str, strategy: str) -> str:
    """Build a malicious instruction_message from attack type and strategy.

    Args:
        attack_type: One of "privacy", "duty_of_care", "due_diligence"
        strategy: The strategy text to inject

    Returns:
        Complete instruction_message string for the interviewer.
    """
    if attack_type not in _TASK_DESCRIPTIONS:
        raise ValueError(
            f"Unknown attack type: {attack_type}. Valid types: {list(_TASK_DESCRIPTIONS.keys())}"
        )
    task_description = _TASK_DESCRIPTIONS[attack_type]
    return f"{task_description}\n\n### STRATEGY TO USE\n{strategy}\n"

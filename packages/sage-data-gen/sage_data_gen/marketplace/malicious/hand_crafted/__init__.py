"""Hand-crafted malicious prompts for marketplace tasks."""

from .due_diligence import PROMPT as DUE_DILIGENCE
from .duty_of_care import PROMPT as DUTY_OF_CARE
from .privacy import PROMPT as PRIVACY

_PROMPTS = {
    "privacy": PRIVACY,
    "duty_of_care": DUTY_OF_CARE,
    "due_diligence": DUE_DILIGENCE,
}


def get_hand_crafted_prompt(attack_type: str) -> str:
    if attack_type not in _PROMPTS:
        raise ValueError(
            f"Unknown attack type: {attack_type}. Valid types: {list(_PROMPTS.keys())}"
        )
    return _PROMPTS[attack_type]

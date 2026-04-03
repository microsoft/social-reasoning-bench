"""Re-exports — inject logic lives in hand_crafted/ and whimsical/."""

from .hand_crafted import get_hand_crafted_prompt
from .whimsical.inject import build_malicious_instruction

__all__ = ["get_hand_crafted_prompt", "build_malicious_instruction"]

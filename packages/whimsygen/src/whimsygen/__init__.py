"""WhimsyGen: Extract whimsical strategies from Wikipedia for adversarial testing."""

__version__ = "0.1.0"

# Main API
# Models (for type hints)
from .core.models import Seed, Strategy, StrategyCollection
from .core.whimsygen import WhimsyGen

__all__ = [
    "WhimsyGen",
    "Seed",
    "Strategy",
    "StrategyCollection",
]

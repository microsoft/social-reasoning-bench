from .models import DEPLOYMENTS, get_model_deployment
from .provider import TrapiCustomLLM


def list_models() -> list[str]:
    """List available model names."""
    return list(DEPLOYMENTS.keys())


__all__ = [
    "TrapiCustomLLM",
    "list_models",
    "DEPLOYMENTS",
    "get_model_deployment",
]

from .models import DEPLOYMENTS, get_api_version, get_deployment
from .provider import TrapiCustomLLM


def list_models() -> list[str]:
    """List available model names."""
    return list(DEPLOYMENTS.keys())


__all__ = [
    "TrapiCustomLLM",
    "list_models",
    "DEPLOYMENTS",
    "get_deployment",
    "get_api_version",
]

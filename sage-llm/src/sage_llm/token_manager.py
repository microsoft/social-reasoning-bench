import os
import threading
import time
from typing import Callable

from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    DefaultAzureCredential,
)

TOKEN_REFRESH_MARGIN = 300  # 5 minutes


class AzureTokenManager:
    """Thread-safe Azure AD token manager with caching."""

    def __init__(self, scope: str):
        self._scope = scope
        # Try AzureCliCredential first (az login), then DefaultAzureCredential
        self._credential = ChainedTokenCredential(
            AzureCliCredential(),
            DefaultAzureCredential(
                exclude_cli_credential=True,
                exclude_environment_credential=True,
                exclude_shared_token_cache_credential=True,
                exclude_developer_cli_credential=True,
                exclude_powershell_credential=True,
                exclude_interactive_browser_credential=True,
                exclude_visual_studio_code_credentials=True,
                managed_identity_client_id=os.environ.get("DEFAULT_IDENTITY_CLIENT_ID"),
            ),
        )
        self._token: str | None = None
        self._expires_at: float = 0
        self._lock = threading.Lock()

    def get_token(self) -> str:
        with self._lock:
            if self._token and time.time() < (self._expires_at - TOKEN_REFRESH_MARGIN):
                return self._token

            access_token = self._credential.get_token(self._scope)
            self._token = access_token.token
            self._expires_at = access_token.expires_on
            return self._token

    def get_token_provider(self) -> Callable[[], str]:
        return self.get_token

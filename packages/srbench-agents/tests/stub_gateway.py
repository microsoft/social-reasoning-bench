"""A stub OpenClaw Gateway for exercising the WebSocket transport in tests.

Running the real Gateway would need a Node install, a pinned OpenClaw release,
and provider credentials, so these tests speak the protocol directly instead.
The stub implements only what :mod:`srbench_agents.openclaw_gateway` calls, and
mirrors the behaviours that were verified against OpenClaw v2026.5.28 — notably
``config.patch`` optimistic concurrency via ``baseHash``.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable, cast

from srbench_agents.openclaw_gateway import (
    GatewayClient,
    GatewayError,
    GatewayProcess,
    GatewayWorker,
)
from websockets.asyncio.server import serve


def merge_patch(target: dict[str, Any], patch: dict[str, Any]) -> None:
    """Apply a JSON merge patch: dicts merge, ``None`` deletes, scalars replace."""
    for key, value in patch.items():
        if value is None:
            target.pop(key, None)
        elif isinstance(value, dict) and isinstance(target.get(key), dict):
            merge_patch(target[key], value)
        else:
            target[key] = value


class StubGateway:
    """An in-process Gateway that answers RPCs from an overridable handler table."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.envelopes: list[dict[str, Any]] = []
        self.config: dict[str, Any] = {"mcp": {"servers": {}}}
        self.hash = "hash-0"
        self.handlers: dict[str, Callable[[dict[str, Any]], Any]] = {}
        self._server: Any = None
        self.url = ""

    async def __aenter__(self) -> StubGateway:
        self._server = await serve(self._handle, "127.0.0.1", 0)
        self.url = f"ws://127.0.0.1:{self.port}"
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()

    @property
    def port(self) -> int:
        return int(next(iter(self._server.sockets)).getsockname()[1])

    def params(self, method: str) -> dict[str, Any]:
        """Params of the last call to ``method``."""
        matches = [p for m, p in self.calls if m == method]
        assert matches, f"{method} was never called"
        return matches[-1]

    def count(self, method: str) -> int:
        return len([m for m, _ in self.calls if m == method])

    async def _handle(self, ws: Any) -> None:
        async for raw in ws:
            msg = json.loads(raw)
            method = str(msg.get("method"))
            params = msg.get("params") or {}
            self.envelopes.append(msg)
            self.calls.append((method, params))
            try:
                payload = self._dispatch(method, params)
                if asyncio.iscoroutine(payload):
                    payload = await payload
            except GatewayError as exc:
                await ws.send(
                    json.dumps(
                        {
                            "type": "res",
                            "id": msg["id"],
                            "ok": False,
                            "error": {"code": exc.code, "message": exc.message},
                        }
                    )
                )
                continue
            await ws.send(
                json.dumps({"type": "res", "id": msg["id"], "ok": True, "payload": payload})
            )

    def _dispatch(self, method: str, params: dict[str, Any]) -> Any:
        handler = self.handlers.get(method)
        if handler is not None:
            return handler(params)
        if method == "config.get":
            return {"config": self.config, "hash": self.hash}
        if method == "config.patch":
            return self.apply_patch(params)
        return {"ok": True}

    def apply_patch(self, params: dict[str, Any]) -> dict[str, Any]:
        """Reject a stale ``baseHash``, as the real Gateway does, then merge."""
        if params.get("baseHash") != self.hash:
            raise GatewayError("conflict", "config base hash required; re-run config.get and retry")
        merge_patch(self.config, json.loads(params["raw"]))
        self.hash = f"hash-{len(self.calls)}"
        return {"ok": True}

    def fail(self, method: str, code: str, message: str) -> None:
        """Make ``method`` raise a structured Gateway error."""

        def handler(_params: dict[str, Any]) -> Any:
            raise GatewayError(code, message)

        self.handlers[method] = handler


#: Port the stub worker pretends its Gateway reserved for the MCP endpoint.
MCP_PORT = 54321


class _StubProcess:
    """Stands in for :class:`~srbench_agents.openclaw_gateway.GatewayProcess`."""

    def __init__(self, client: GatewayClient) -> None:
        self.client = client
        self.mcp_port = MCP_PORT


async def connect_worker(stub: StubGateway) -> tuple[GatewayWorker, GatewayClient]:
    """Return a worker bound to ``stub`` plus its client, for explicit closing."""
    client = GatewayClient(stub.url, "test-token")
    await client.connect()
    return GatewayWorker(cast("GatewayProcess", _StubProcess(client))), client

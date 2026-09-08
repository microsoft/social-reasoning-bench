"""Serve an environment's granted tool space as a Model Context Protocol server.

This is an *optional* module (it requires the ``mcp`` extra) whose sole job is to
turn the two halves of the BYOA boundary — the environment's granted ``tools``
(OpenAI function schemas) and its ``invoke_tool`` callable — into a standard,
in-process MCP :class:`~mcp.server.lowlevel.Server`.

Any "bring your own agent" implementation built on an MCP-speaking framework can
therefore reuse :func:`build_server` instead of hand-wiring every tool. For
example, the bundled Claude agent (``srbench_agents.claude_agent``) mounts
the result directly as an in-process SDK MCP server, and an external client can
speak to it over stdio via :func:`serve_stdio`.

The contract is unchanged: **all tool logic and validation live in the
environment.** This module is a thin transport bridge — every tool call, even a
malformed one, is forwarded to ``invoke_tool``, whose returned string is handed
back verbatim as the tool result.

Install with ``pip install 'srbench[mcp]'``.
"""

from __future__ import annotations

from collections.abc import Iterable

from openai.types.chat import ChatCompletionFunctionToolParam

from .shared import InvokeTool

try:
    from mcp import types as mcp_types
    from mcp.server.lowlevel import Server
except ImportError as exc:  # pragma: no cover - exercised only without the extra
    raise ImportError(
        "srbench.mcp requires the optional 'mcp' dependency. "
        "Install it with: pip install 'srbench[mcp]'"
    ) from exc

__all__ = ["build_asgi_app", "build_server", "serve_http", "serve_stdio", "to_mcp_tools"]

_EMPTY_SCHEMA: dict[str, object] = {"type": "object", "properties": {}}


def to_mcp_tools(
    tools: Iterable[ChatCompletionFunctionToolParam],
) -> list[mcp_types.Tool]:
    """Convert an environment's OpenAI function schemas into MCP tool definitions."""
    mcp_tools: list[mcp_types.Tool] = []
    for spec in tools:
        fn = spec["function"]
        name = fn["name"]
        mcp_tools.append(
            mcp_types.Tool(
                name=name,
                description=fn.get("description") or name,
                inputSchema=dict(fn.get("parameters") or _EMPTY_SCHEMA),
            )
        )
    return mcp_tools


def build_server(
    tools: Iterable[ChatCompletionFunctionToolParam],
    invoke_tool: InvokeTool,
    *,
    name: str = "srbench",
    version: str = "1.0.0",
) -> Server:
    """Build an in-process MCP server that exposes ``tools`` and routes calls.

    Args:
        tools: The environment's granted tool space (OpenAI function schemas).
        invoke_tool: The environment boundary. Called as
            ``await invoke_tool(name, arguments)``; returns a result string for
            every expected outcome (success, unknown tool, bad arguments,
            :class:`~srbench.shared.ToolError`). Only genuine bugs propagate.
        name: The MCP server name. Frameworks typically namespace tools as
            ``mcp__{name}__{tool}``.
        version: Informational server version string.

    Returns:
        A :class:`~mcp.server.lowlevel.Server` ready to be served over any MCP
        transport, or mounted in-process (e.g. as a Claude SDK MCP server).
    """
    server: Server = Server(name, version=version)
    tool_defs = to_mcp_tools(tools)

    @server.list_tools()
    async def _list_tools() -> list[mcp_types.Tool]:
        return tool_defs

    # validate_input=False: the environment is the single source of validation.
    # Even a malformed call must reach invoke_tool so the environment — not this
    # transport — decides the outcome and returns the result string.
    @server.call_tool(validate_input=False)
    async def _call_tool(
        tool_name: str, arguments: dict[str, object] | None
    ) -> list[mcp_types.TextContent]:
        result = await invoke_tool(tool_name, arguments or {})
        return [mcp_types.TextContent(type="text", text=result)]

    return server


async def serve_stdio(server: Server) -> None:
    """Serve ``server`` over stdio for an external MCP client (blocks until closed)."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def build_asgi_app(
    server: Server,
    *,
    path: str = "/mcp",
    json_response: bool = True,
    stateless: bool = True,
):
    """Wrap ``server`` in a Starlette ASGI app that speaks streamable-HTTP MCP.

    The app mounts a `Streamable HTTP <https://modelcontextprotocol.io/>`_
    endpoint at ``path``. Point any HTTP MCP client at ``http://<host>:<port>``
    with ``path`` and transport ``streamable-http``. ``stateless=True`` treats
    each request independently, which is all a tool server needs.

    Requires the ``mcp`` extra's HTTP stack (Starlette), which ships with it.
    """
    from contextlib import asynccontextmanager

    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.routing import Mount

    manager = StreamableHTTPSessionManager(
        app=server, json_response=json_response, stateless=stateless
    )

    async def handle(scope, receive, send) -> None:
        await manager.handle_request(scope, receive, send)

    @asynccontextmanager
    async def lifespan(_app):
        async with manager.run():
            yield

    return Starlette(routes=[Mount(path, app=handle)], lifespan=lifespan)


async def serve_http(
    server: Server,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    path: str = "/mcp",
    json_response: bool = True,
    log_level: str = "warning",
) -> None:
    """Serve ``server`` over streamable-HTTP for an external MCP client (blocks).

    Use this when the MCP client runs in a *separate process* (e.g. a CLI agent)
    and must reach a server bound to live in-process state. Pass ``port=0`` to
    bind an ephemeral port. Blocks until cancelled.
    """
    import uvicorn

    app = build_asgi_app(server, path=path, json_response=json_response)
    config = uvicorn.Config(app, host=host, port=port, log_level=log_level)
    await uvicorn.Server(config).serve()

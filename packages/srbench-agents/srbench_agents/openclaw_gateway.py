"""Drive OpenClaw through its Gateway instead of one-shot CLI subprocesses.

The Gateway is a long-lived OpenClaw process that exposes a typed WebSocket
JSON-RPC plane (protocol v4). ``openclaw agent`` already talks to it; the only
reason to spawn a per-task subprocess is the ``--local`` flag, which explicitly
opts out. Driving the Gateway directly buys structured errors, structured tool
events, real cancellation, and one Node startup per *sweep* instead of per task.

Topology
--------
:class:`GatewayPool` hands out :class:`GatewayWorker` objects, each owning one
Gateway process **exclusively** for the duration of a task. That exclusivity is
load-bearing: ``mcp.servers`` is global to a Gateway.

Each worker reserves one loopback port and registers a single MCP server at that
URL **once**, for the Gateway's whole lifetime. Each task then serves its own
tools behind that fixed URL and shuts the HTTP server down when it finishes, so
between tasks nothing is listening and a task can only ever reach its own tools.
This was verified end to end: a second run at the same URL discovers the new tool
set and never sees the previous task's tools. Isolation is therefore structural
and does not rely on per-agent ``tools.deny`` glob filtering, which is documented
but could not be verified at runtime.

Registering once is also a hard requirement, not an optimisation. ``config.*``
methods are *control-plane writes*, and the Gateway allows only **3 per 60
seconds** per client; rewriting the registration per task throttles a sweep to a
standstill. Per-task model and thinking level therefore travel on the session
(``sessions.create``'s ``model`` and ``sessions.patch``'s ``thinkingLevel``),
neither of which is rate limited.

Auth
----
Each Gateway runs in an isolated profile directory with ``auth.mode: "token"``
and a generated token. Token auth grants full operator scope immediately. The
alternative (``auth: none`` on loopback) auto-pairs the *first* connection at
exactly the scopes it requests, so a read-only first call permanently pins the
device to ``operator.read`` and every later write deadlocks — ``devices approve``
itself requires write scope.

Credentials for the model provider come from the ambient environment (e.g.
``ANTHROPIC_API_KEY``); a fresh profile picks them up with no ``openclaw onboard``
step.

This module targets **OpenClaw v2026.5.28**.
"""

from __future__ import annotations

import asyncio
import atexit
import contextlib
import json
import logging
import os
import secrets
import shutil
import signal
import socket
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

try:
    import websockets
except ImportError as exc:  # pragma: no cover - exercised only without the dep
    raise ImportError(
        "srbench_agents.openclaw_gateway requires 'websockets'. "
        "Install it with: pip install 'srbench-agents'"
    ) from exc

#: The pinned OpenClaw release this transport targets (npm tag
#: ``openclaw@2026.5.28``, git ``e93216080aa1f425d3ab127014603eba8e365b2d``).
OPENCLAW_VERSION = "2026.5.28"

#: Operator scopes requested at handshake. All of them are requested up front:
#: under token auth they are granted outright, and requesting them lazily is what
#: causes the scope-upgrade deadlock described in the module docstring.
_SCOPES = ("operator.read", "operator.write", "operator.admin")

#: Gateway wire protocol version spoken by v2026.5.28 (``minProtocol``/``maxProtocol``).
_PROTOCOL_VERSION = 4

_HEALTH_TIMEOUT = 90.0
_SHUTDOWN_TIMEOUT = 10.0


class GatewayError(RuntimeError):
    """A structured error returned by a Gateway RPC call.

    Unlike the subprocess transport — where every failure collapsed into
    ``exited with code 1`` plus a stderr tail — the Gateway reports a machine
    readable ``code`` alongside the message.
    """

    def __init__(self, code: str, message: str, *, method: str | None = None) -> None:
        self.code = code
        self.message = message
        self.method = method
        where = f" ({method})" if method else ""
        super().__init__(f"[{code}]{where} {message}")


class GatewayClient:
    """Minimal async WebSocket JSON-RPC client for one Gateway.

    Only the subset of the protocol this harness needs is implemented: request
    /response correlation, structured errors, and fan-out of server-pushed
    events to registered listeners.
    """

    def __init__(self, url: str, token: str, *, name: str = "srbench") -> None:
        self._url = url
        self._token = token
        self._name = name
        self._ws: Any = None
        self._pending: dict[str, asyncio.Future[Any]] = {}
        self._listeners: list[Any] = []
        self._reader: asyncio.Task[None] | None = None
        self._closed = False

    async def connect(self, *, timeout: float = 30.0) -> None:
        """Open the socket and complete the operator handshake."""
        self._ws = await asyncio.wait_for(
            websockets.connect(self._url, max_size=None, ping_interval=20), timeout=timeout
        )
        self._reader = asyncio.create_task(self._read_loop())
        await self.call(
            "connect",
            {
                "minProtocol": _PROTOCOL_VERSION,
                "maxProtocol": _PROTOCOL_VERSION,
                "client": {
                    "id": "gateway-client",
                    "version": OPENCLAW_VERSION,
                    "platform": sys.platform,
                    "mode": "backend",
                },
                "role": "operator",
                "scopes": list(_SCOPES),
                # Without this capability the Gateway silently never routes
                # structured tool events to us (the handshake does not error).
                "caps": ["tool-events"],
                "auth": {"token": self._token},
            },
            timeout=timeout,
        )

    async def _read_loop(self) -> None:
        assert self._ws is not None
        try:
            async for raw in self._ws:
                try:
                    msg = json.loads(raw)
                except ValueError:
                    continue
                self._dispatch(msg)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # transport died; fail every in-flight request
            self._fail_all(exc)
        else:
            self._fail_all(ConnectionError("gateway connection closed"))

    def _dispatch(self, msg: dict[str, Any]) -> None:
        kind = msg.get("type")
        if kind == "res":
            fut = self._pending.pop(str(msg.get("id")), None)
            if fut is not None and not fut.done():
                fut.set_result(msg)
            return
        if kind == "event":
            for listener in list(self._listeners):
                with contextlib.suppress(Exception):
                    listener(msg)

    def _fail_all(self, exc: BaseException) -> None:
        for fut in self._pending.values():
            if not fut.done():
                fut.set_exception(exc)
        self._pending.clear()

    def add_listener(self, listener: Any) -> Any:
        """Register a callable invoked with every server-pushed event."""
        self._listeners.append(listener)
        return listener

    def remove_listener(self, listener: Any) -> None:
        with contextlib.suppress(ValueError):
            self._listeners.remove(listener)

    async def call(
        self, method: str, params: dict[str, Any] | None = None, *, timeout: float = 60.0
    ) -> Any:
        """Issue one RPC and return its payload, raising :class:`GatewayError`.

        The wire frame is exactly ``{type, id, method, params}``: the request
        frame schema sets ``additionalProperties: false``, so anything else
        (including a ``timeoutMs`` hint) is rejected outright with
        ``invalid request frame``. Deadlines are therefore purely client-side,
        and every call gets a finite one so a wedged Gateway cannot hang a task.
        """
        if self._ws is None:
            raise ConnectionError("gateway client is not connected")
        req_id = str(uuid4())
        fut: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[req_id] = fut
        payload = {"type": "req", "id": req_id, "method": method, "params": params or {}}
        try:
            await self._ws.send(json.dumps(payload))
            msg = await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError:
            raise GatewayError("timeout", f"no response within {timeout:.0f}s", method=method)
        finally:
            self._pending.pop(req_id, None)

        if msg.get("ok") is False or msg.get("error"):
            err = msg.get("error") or {}
            raise GatewayError(
                str(err.get("code") or "error"),
                str(err.get("message") or "gateway call failed"),
                method=method,
            )
        payload_out = msg.get("payload")
        return payload_out if payload_out is not None else msg.get("result")

    async def close(self) -> None:
        self._closed = True
        if self._reader is not None:
            self._reader.cancel()
            with contextlib.suppress(BaseException):
                await self._reader
        if self._ws is not None:
            with contextlib.suppress(Exception):
                await self._ws.close()
        self._ws = None


def _free_port() -> int:
    """Reserve and immediately release an ephemeral localhost port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class GatewayProcess:
    """One ``openclaw gateway run`` process in an isolated profile directory."""

    def __init__(self, *, binary: str = "openclaw", verify_version: bool = True) -> None:
        self._binary = binary
        self._verify_version = verify_version
        self._proc: asyncio.subprocess.Process | None = None
        self._dir: Path | None = None
        self._token = secrets.token_urlsafe(24)
        self._port = 0
        #: Loopback port reserved for this Gateway's single MCP registration.
        #: Fixed for the process lifetime so the registration never has to be
        #: rewritten (see :meth:`GatewayWorker.ensure_registered`).
        self.mcp_port = 0
        self.client: GatewayClient | None = None

    @property
    def config_path(self) -> Path:
        assert self._dir is not None
        return self._dir / "openclaw.json"

    async def start(self) -> None:
        if self._verify_version:
            await self._verify_cli()
        self._dir = Path(tempfile.mkdtemp(prefix="srbench-openclaw-"))
        self._port = _free_port()
        self.mcp_port = _free_port()
        self.config_path.write_text(
            json.dumps(
                {
                    "gateway": {
                        "mode": "local",
                        "port": self._port,
                        "bind": "loopback",
                        "auth": {"mode": "token", "token": self._token},
                    }
                },
                indent=2,
            )
        )
        env = dict(os.environ)
        env["OPENCLAW_CONFIG_PATH"] = str(self.config_path)
        env["OPENCLAW_STATE_DIR"] = str(self._dir)
        self._proc = await asyncio.create_subprocess_exec(
            self._binary,
            "gateway",
            "run",
            "--port",
            str(self._port),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            # Own session so the whole process tree can be signalled on teardown;
            # OpenClaw spawns helpers that would otherwise be orphaned.
            start_new_session=True,
        )
        _LIVE.add(self)
        try:
            await self._await_health()
        except BaseException:
            await self.stop()
            raise

    async def _verify_cli(self) -> None:
        try:
            proc = await asyncio.create_subprocess_exec(
                self._binary,
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"OpenClaw CLI {self._binary!r} not found. Install the pinned "
                f"release with: npm install -g openclaw@{OPENCLAW_VERSION}"
            ) from exc
        out, err = await proc.communicate()
        reported = (out or err).decode(errors="replace").strip()
        if OPENCLAW_VERSION not in reported:
            raise RuntimeError(
                f"OpenClaw CLI reports {reported!r}, but this agent is pinned to "
                f"v{OPENCLAW_VERSION}. Install it with: "
                f"npm install -g openclaw@{OPENCLAW_VERSION}"
            )

    async def _await_health(self) -> None:
        """Connect and poll ``health`` until the Gateway reports ready."""
        url = f"ws://127.0.0.1:{self._port}"
        deadline = asyncio.get_running_loop().time() + _HEALTH_TIMEOUT
        last: BaseException | None = None
        while asyncio.get_running_loop().time() < deadline:
            if self._proc is not None and self._proc.returncode is not None:
                raise RuntimeError(await self._exit_message())
            client = GatewayClient(url, self._token)
            try:
                await client.connect(timeout=10.0)
                await client.call("health", timeout=15.0)
            except BaseException as exc:  # not up yet
                last = exc
                await client.close()
                await asyncio.sleep(0.25)
                continue
            self.client = client
            return
        raise RuntimeError(
            f"OpenClaw gateway did not become healthy within {_HEALTH_TIMEOUT:.0f}s: {last}"
        )

    async def _exit_message(self) -> str:
        proc = self._proc
        assert proc is not None
        out = err = b""
        with contextlib.suppress(Exception):
            out, err = await asyncio.wait_for(proc.communicate(), timeout=5.0)
        tail = (err or out).decode(errors="replace").strip()[-800:]
        return f"OpenClaw gateway exited with code {proc.returncode}; output tail: {tail!r}"

    async def stop(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None
        proc = self._proc
        if proc is not None and proc.returncode is None:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            with contextlib.suppress(ProcessLookupError):
                proc.terminate()
            with contextlib.suppress(BaseException):
                await asyncio.wait_for(proc.wait(), timeout=_SHUTDOWN_TIMEOUT)
            if proc.returncode is None:
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        self._proc = None
        _LIVE.discard(self)
        if self._dir is not None:
            shutil.rmtree(self._dir, ignore_errors=True)
            self._dir = None

    def force_stop(self) -> None:
        """Synchronously kill the Gateway and delete its profile.

        The last-resort path for interpreter exit, where no event loop is left to
        await :meth:`stop`. Safe to call twice.
        """
        proc = self._proc
        if proc is not None and proc.returncode is None:
            # The loop that owned this subprocess is gone, so asyncio's transport
            # finalizer would raise "Event loop is closed" from __del__ on the way
            # out. Mark it closed so __del__ leaves it alone.
            transport = getattr(proc, "_transport", None)
            if transport is not None:
                with contextlib.suppress(BaseException):
                    transport._closed = True
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                try:
                    if os.waitpid(proc.pid, os.WNOHANG)[0] != 0:
                        break
                except ChildProcessError:
                    break
                time.sleep(0.05)
            else:
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        self._proc = None
        _LIVE.discard(self)
        if self._dir is not None:
            shutil.rmtree(self._dir, ignore_errors=True)
            self._dir = None


#: Gateways that have been started but not yet stopped. The harness has no
#: shutdown hook of its own, so without this a sweep that ends (or crashes)
#: without awaiting :func:`shutdown_pool` leaves a Node process and a temp
#: profile directory behind for every Gateway it started.
_LIVE: set[GatewayProcess] = set()


def _stop_live_gateways() -> None:
    if not _LIVE:
        return
    # asyncio's child watcher runs in its own thread and logs a warning when the
    # child it is waiting on exits after the loop closed, which is exactly what
    # happens here. It is noise, and this module exists partly to stop drowning
    # real failures in noise.
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    for process in list(_LIVE):
        with contextlib.suppress(BaseException):
            process.force_stop()


atexit.register(_stop_live_gateways)


def is_error_message(msg: dict[str, Any]) -> str | None:
    """Return the failure text of an assistant message, or ``None`` if it is fine.

    OpenClaw reports run failures *inside the transcript* rather than through the
    RPC result: ``agent.wait`` returns ``status: "ok"`` even when the turn died.
    Two shapes occur:

    - ``stopReason: "error"`` with a structured ``errorMessage`` (provider errors,
      e.g. an unknown model or a rejected API key);
    - a normal-looking assistant message whose text begins with
      ``"⚠️ Agent failed before reply:"`` (failures raised before the provider
      call, e.g. missing auth for the agent).

    Missing both of these is what made the old transport report an unrelated
    ``exited with code 1``.
    """
    if msg.get("role") != "assistant":
        return None
    if msg.get("stopReason") == "error" or msg.get("errorMessage"):
        return str(msg.get("errorMessage") or "agent run ended with an error")
    content = msg.get("content")
    if isinstance(content, list):
        text = " ".join(
            str(part.get("text", "")) for part in content if isinstance(part, dict)
        ).strip()
    else:
        text = str(content or "").strip()
    if text.startswith("⚠️ Agent failed"):
        return text
    return None


class GatewayWorker:
    """Exclusive handle to one Gateway for the duration of a single task.

    The worker registers its MCP server exactly once, at a loopback URL it owns
    for the Gateway's whole lifetime. Each task then serves *its own* tools
    behind that fixed URL and tears the HTTP server down afterwards, so between
    tasks nothing is listening and a task can only ever reach its own tools.

    Registering once is not just tidiness: ``config.patch`` is a control-plane
    write, and the Gateway caps those at **3 per 60 seconds** per client. Any
    design that rewrote the registration per task would throttle a sweep to a
    halt. Model and thinking level therefore travel per session
    (``sessions.create``/``sessions.patch``), which are not rate limited.
    """

    def __init__(self, process: GatewayProcess) -> None:
        self._process = process
        self._checked_models: set[str] = set()
        self._registered = False

    @property
    def client(self) -> GatewayClient:
        client = self._process.client
        if client is None:
            raise RuntimeError("gateway worker is not connected")
        return client

    @property
    def mcp_port(self) -> int:
        """The loopback port this worker's task must serve its MCP app on."""
        return self._process.mcp_port

    @property
    def mcp_url(self) -> str:
        return f"http://127.0.0.1:{self.mcp_port}/mcp"

    async def _patch_config(self, patch: dict[str, Any], *, attempts: int = 3) -> None:
        """Apply a JSON-merge config patch, retrying on a stale base hash.

        ``config.patch`` is guarded by optimistic concurrency: it refuses a write
        whose ``baseHash`` no longer matches the live snapshot. It is also a
        control-plane write, capped at 3 per 60s per client, so an exhausted
        budget is reported with an explicit hint rather than retried blindly —
        burning retries on it would only push the window further out.
        """
        for attempt in range(attempts):
            snapshot = await self.client.call("config.get", timeout=30.0)
            base_hash = (snapshot or {}).get("hash")
            try:
                await self.client.call(
                    "config.patch",
                    {"raw": json.dumps(patch), "baseHash": base_hash},
                    timeout=30.0,
                )
                return
            except GatewayError as exc:
                if "rate limit" in exc.message.lower():
                    raise GatewayError(
                        exc.code,
                        f"{exc.message}. The Gateway allows only 3 control-plane writes per "
                        "60s; srbench registers its MCP server once per Gateway, so this "
                        "usually means something else is writing the OpenClaw config.",
                        method=exc.method,
                    ) from exc
                stale = "hash" in exc.message.lower() or exc.code in {"conflict", "stale"}
                if not stale or attempt == attempts - 1:
                    raise
                await asyncio.sleep(0.2 * (attempt + 1))

    async def ensure_model(self, model: str | None) -> None:
        """Fail fast when ``model`` is not a model this Gateway knows.

        The subprocess transport surfaced an unresolvable model as an opaque
        ``exited with code 1`` (the real cause, ``FailoverError: Unknown model``,
        was buried in a stderr tail). This turns it into an actionable message
        before any task work happens.

        The catalog RPC returns ``{id, name, provider, ...}`` entries — note that
        ``id`` is the *bare* model name, so the addressable id is
        ``provider/id``. Credentials are deliberately not checked here: the
        ``configured`` view reflects only the config file, so it reports nothing
        for provider keys supplied through the environment.
        """
        if not model or model in self._checked_models:
            return
        provider, _, name = model.partition("/")
        if not name:
            raise RuntimeError(
                f"OpenClaw model {model!r} is not a valid model id: OpenClaw expects "
                f"'provider/model' (e.g. 'anthropic/{model}'). A bare id silently acquires "
                "a default provider prefix and then fails to resolve at run time."
            )
        try:
            catalog = await self.client.call("models.list", {"view": "all"}, timeout=30.0)
        except GatewayError:
            return  # never block a run on a catalog hiccup
        entries = catalog.get("models") if isinstance(catalog, dict) else catalog
        if not isinstance(entries, list) or not entries:
            return
        known: set[str] = set()
        same_name: list[str] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_provider = str(entry.get("provider") or "")
            entry_id = str(entry.get("id") or "")
            if not entry_provider or not entry_id:
                continue
            known.add(f"{entry_provider}/{entry_id}")
            if entry_id == name:
                same_name.append(f"{entry_provider}/{entry_id}")
        if not known or model in known:
            self._checked_models.add(model)
            return
        if same_name:
            hint = f"Did you mean {' or '.join(sorted(same_name))}?"
        else:
            hint = (
                f"Provider {provider!r} does not offer a model named {name!r}. "
                "Run `openclaw models list --all` to see the available ids."
            )
        raise RuntimeError(f"OpenClaw does not know the model {model!r}. {hint}")

    async def ensure_registered(self, *, mcp_name: str = "srbench") -> None:
        """Register this worker's MCP endpoint once per Gateway lifetime.

        The URL is fixed for the life of the Gateway, so this is a single
        control-plane write per sweep rather than one (or two) per task — which
        matters because the Gateway allows only 3 such writes per 60 seconds.
        """
        if self._registered:
            return
        await self._patch_config(
            {"mcp": {"servers": {mcp_name: {"url": self.mcp_url, "transport": "streamable-http"}}}}
        )
        self._registered = True

    async def run_turn(
        self,
        *,
        session_key: str,
        message: str,
        run_id: str,
        timeout: float,
        model: str | None = None,
        thinking: str | None = None,
    ) -> list[dict[str, Any]]:
        """Drive one agent turn to completion and return the session transcript.

        ``model`` and ``thinking`` are applied to this session only, so a sweep
        can vary them per task without touching the rate-limited config plane.
        """
        create: dict[str, Any] = {"key": session_key}
        if model:
            create["model"] = model
        await self.client.call("sessions.create", create, timeout=30.0)
        if thinking:
            await self.client.call(
                "sessions.patch", {"key": session_key, "thinkingLevel": thinking}, timeout=30.0
            )
        await self.client.call(
            "chat.send",
            {
                "sessionKey": session_key,
                "message": message,
                "idempotencyKey": run_id,
                "timeoutMs": int(timeout * 1000),
            },
            timeout=60.0,
        )
        try:
            await self.client.call(
                "agent.wait",
                {"runId": run_id, "timeoutMs": int(timeout * 1000)},
                timeout=timeout + 30.0,
            )
        except BaseException:
            await self.abort(session_key=session_key, run_id=run_id)
            raise
        history = await self.client.call("chat.history", {"sessionKey": session_key}, timeout=30.0)
        messages = (history or {}).get("messages") or []
        return messages if isinstance(messages, list) else []

    async def abort(self, *, session_key: str, run_id: str | None = None) -> None:
        params: dict[str, Any] = {"key": session_key}
        if run_id:
            params["runId"] = run_id
        with contextlib.suppress(BaseException):
            await self.client.call("sessions.abort", params, timeout=20.0)

    async def delete_session(self, session_key: str) -> None:
        with contextlib.suppress(BaseException):
            await self.client.call("sessions.delete", {"key": session_key}, timeout=20.0)


class GatewayPool:
    """A pool of worker-owned Gateways, started lazily and reused across tasks.

    Sizing the pool to task concurrency means each in-flight task holds one
    Gateway exclusively, which is what keeps per-task MCP registration safe.
    """

    def __init__(self, size: int = 1, *, binary: str = "openclaw") -> None:
        self._size = max(1, size)
        self._binary = binary
        self._idle: list[GatewayWorker] = []
        self._started = 0
        self._lock = asyncio.Lock()
        self._slots = asyncio.Semaphore(self._size)
        self._all: list[GatewayProcess] = []
        self._closed = False

    @contextlib.asynccontextmanager
    async def acquire(self):
        """Yield a :class:`GatewayWorker` held exclusively for the caller."""
        if self._closed:
            raise RuntimeError("gateway pool is closed")
        await self._slots.acquire()
        worker: GatewayWorker | None = None
        try:
            async with self._lock:
                if self._idle:
                    worker = self._idle.pop()
            if worker is None:
                process = GatewayProcess(binary=self._binary)
                await process.start()
                async with self._lock:
                    self._all.append(process)
                    self._started += 1
                worker = GatewayWorker(process)
            yield worker
        finally:
            if worker is not None:
                async with self._lock:
                    self._idle.append(worker)
            self._slots.release()

    async def aclose(self) -> None:
        self._closed = True
        async with self._lock:
            processes, self._all, self._idle = self._all, [], []
        for process in processes:
            with contextlib.suppress(BaseException):
                await process.stop()


_POOL: GatewayPool | None = None
_POOL_LOCK: asyncio.Lock | None = None


async def get_pool(size: int = 1, *, binary: str = "openclaw") -> GatewayPool:
    """Return the process-wide Gateway pool, creating it on first use."""
    global _POOL, _POOL_LOCK
    if _POOL_LOCK is None:
        _POOL_LOCK = asyncio.Lock()
    async with _POOL_LOCK:
        if _POOL is None:
            _POOL = GatewayPool(size, binary=binary)
        return _POOL


async def shutdown_pool() -> None:
    """Stop every Gateway owned by the process-wide pool."""
    global _POOL
    pool, _POOL = _POOL, None
    if pool is not None:
        await pool.aclose()

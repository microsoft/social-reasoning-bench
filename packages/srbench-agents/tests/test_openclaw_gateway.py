"""Protocol-level tests for the OpenClaw Gateway transport.

Everything here runs against :class:`tests.stub_gateway.StubGateway` rather than
a real OpenClaw process. The behaviours asserted are the ones that were verified
empirically against OpenClaw v2026.5.28 and that the subprocess transport got
wrong — structured errors, config concurrency, and transcript-based failure
detection.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from srbench_agents import openclaw_gateway
from srbench_agents.openclaw_gateway import (
    GatewayClient,
    GatewayError,
    _remove_sandbox_containers,
    _tools_overlay,
    is_error_message,
)
from stub_gateway import MCP_PORT, StubGateway, connect_worker, merge_patch

# --- RPC framing ------------------------------------------------------------


async def test_call_returns_the_payload():
    async with StubGateway() as stub:
        stub.handlers["health"] = lambda _p: {"status": "ok"}
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        try:
            assert await client.call("health") == {"status": "ok"}
        finally:
            await client.close()


async def test_call_raises_a_structured_error():
    """The subprocess transport could only report 'exited with code 1'."""
    async with StubGateway() as stub:
        stub.fail("tools.invoke", "not_found", "Tool not available")
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        try:
            with pytest.raises(GatewayError) as excinfo:
                await client.call("tools.invoke", {"name": "nope"})
        finally:
            await client.close()
        assert excinfo.value.code == "not_found"
        assert excinfo.value.method == "tools.invoke"
        assert "Tool not available" in excinfo.value.message


async def test_handshake_requests_every_scope_up_front():
    """Requesting scopes lazily is what causes the loopback pairing deadlock:
    the first connection is pinned to exactly the scopes it asked for, and the
    recovery path (`devices approve`) itself needs write scope."""
    async with StubGateway() as stub:
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        await client.close()
    params = stub.params("connect")
    assert params["role"] == "operator"
    assert params["auth"]["token"] == "test-token"
    # ConnectParamsSchema requires the protocol range and a client descriptor
    # drawn from a fixed enum; omitting either fails the handshake outright.
    assert params["minProtocol"] == 4 and params["maxProtocol"] == 4
    assert params["client"]["id"] == "gateway-client"
    assert params["client"]["mode"] == "backend"
    assert params["client"]["version"] and params["client"]["platform"]
    assert set(params["scopes"]) == {"operator.read", "operator.write", "operator.admin"}
    # Without this capability the Gateway silently routes no tool events.
    assert "tool-events" in params["caps"]


async def test_request_frames_carry_no_extra_fields():
    """RequestFrameSchema sets additionalProperties: false, so anything beyond
    {type, id, method, params} — a timeoutMs hint, for instance — is rejected
    with 'invalid request frame' and the socket is closed at handshake."""
    async with StubGateway() as stub:
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        await client.call("health")
        await client.close()
    for envelope in stub.envelopes:
        assert set(envelope) == {"type", "id", "method", "params"}
        assert envelope["type"] == "req"
        assert envelope["id"]


async def test_a_silent_gateway_times_out_client_side():
    """Deadlines are client-side only, and every call gets a finite one so a
    wedged Gateway cannot hang a benchmark task forever."""
    async with StubGateway() as stub:
        never = asyncio.Event()

        async def hang(_params: dict) -> None:
            await never.wait()

        stub.handlers["health"] = hang
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        try:
            with pytest.raises(GatewayError) as excinfo:
                await client.call("health", timeout=0.2)
        finally:
            never.set()
            await client.close()
    assert excinfo.value.code == "timeout"


async def test_concurrent_calls_are_correlated_by_id():
    async with StubGateway() as stub:
        stub.handlers["echo"] = lambda p: {"n": p["n"]}
        client = GatewayClient(stub.url, "test-token")
        await client.connect()
        try:
            results = await asyncio.gather(*(client.call("echo", {"n": i}) for i in range(8)))
        finally:
            await client.close()
        assert [r["n"] for r in results] == list(range(8))


# --- config patching --------------------------------------------------------


async def test_registration_uses_the_worker_owned_url_and_happens_once():
    async with StubGateway() as stub:
        worker, client = await connect_worker(stub)
        try:
            await worker.ensure_registered(mcp_name="srbench")
            await worker.ensure_registered(mcp_name="srbench")
        finally:
            await client.close()
    server = stub.config["mcp"]["servers"]["srbench"]
    assert server == {"url": f"http://127.0.0.1:{MCP_PORT}/mcp", "transport": "streamable-http"}
    # config.patch is a control-plane write, capped at 3 per 60s per client.
    # Registering per task would throttle a sweep to a standstill.
    assert stub.count("config.patch") == 1


async def test_registration_does_not_touch_agent_defaults():
    """Model and thinking travel per session, so the shared config stays clean
    and a sweep can vary them per task without spending write budget."""
    async with StubGateway() as stub:
        worker, client = await connect_worker(stub)
        try:
            await worker.ensure_registered(mcp_name="srbench")
        finally:
            await client.close()
    assert "agents" not in stub.config


async def test_a_rate_limited_patch_is_reported_with_context():
    async with StubGateway() as stub:
        stub.fail(
            "config.patch",
            "UNAVAILABLE",
            "rate limit exceeded for config.patch; retry after 45s",
        )
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(GatewayError, match="3 control-plane writes per") as excinfo:
                await worker.ensure_registered(mcp_name="srbench")
        finally:
            await client.close()
    assert "rate limit exceeded" in excinfo.value.message
    # Retrying only pushes the window further out, so it must not be retried.
    assert stub.count("config.patch") == 1


async def test_patch_retries_after_a_stale_base_hash():
    async with StubGateway() as stub:
        state = {"raced": False}

        def patch(params: dict) -> dict:
            if not state["raced"]:
                state["raced"] = True
                stub.hash = "hash-moved"  # another writer landed first
                raise GatewayError("conflict", "config base hash required; re-run config.get")
            merge_patch(stub.config, json.loads(params["raw"]))
            return {"ok": True}

        stub.handlers["config.patch"] = patch
        worker, client = await connect_worker(stub)
        try:
            await worker.ensure_registered(mcp_name="srbench")
        finally:
            await client.close()
    assert stub.config["mcp"]["servers"]["srbench"]["url"].endswith("/mcp")
    assert stub.count("config.patch") == 2
    # The retry must re-read the snapshot; reusing the stale hash would loop.
    assert stub.count("config.get") == 2


async def test_patch_gives_up_on_a_non_conflict_error():
    async with StubGateway() as stub:
        stub.fail("config.patch", "invalid_config", "schema validation failed")
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(GatewayError, match="schema validation failed"):
                await worker.ensure_registered(mcp_name="srbench")
        finally:
            await client.close()
    assert stub.count("config.patch") == 1


# --- model preflight --------------------------------------------------------


async def test_preflight_rejects_a_bare_model_id():
    """The reported failure: a bare id silently acquires a default provider
    prefix, producing an unresolvable 'openai/claude-sonnet-4-6'."""
    async with StubGateway() as stub:
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(RuntimeError) as excinfo:
                await worker.ensure_model("claude-sonnet-4-6")
        finally:
            await client.close()
    message = str(excinfo.value)
    assert "provider/model" in message
    assert "anthropic/claude-sonnet-4-6" in message
    # Rejected on shape alone, without paying for a catalog round trip.
    assert stub.count("models.list") == 0


async def test_preflight_suggests_the_right_provider_for_a_known_model_name():
    """Exactly the reported bug: the model exists, under another provider."""
    async with StubGateway() as stub:
        stub.handlers["models.list"] = lambda _p: {
            "models": [
                {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6", "provider": "anthropic"},
                {"id": "gpt-5.5", "name": "GPT-5.5", "provider": "openai"},
            ]
        }
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(RuntimeError, match="does not know the model") as excinfo:
                await worker.ensure_model("openai/claude-sonnet-4-6")
        finally:
            await client.close()
    assert "Did you mean anthropic/claude-sonnet-4-6?" in str(excinfo.value)


async def test_preflight_reports_an_unknown_model_name():
    async with StubGateway() as stub:
        stub.handlers["models.list"] = lambda _p: {
            "models": [{"id": "gpt-5.5", "name": "GPT-5.5", "provider": "openai"}]
        }
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(RuntimeError, match="does not offer a model named") as excinfo:
                await worker.ensure_model("openai/gpt-9")
        finally:
            await client.close()
    assert "openai" in str(excinfo.value)


async def test_preflight_accepts_a_known_model_once():
    async with StubGateway() as stub:
        stub.handlers["models.list"] = lambda _p: {
            "models": [{"id": "gpt-5.5", "name": "GPT-5.5", "provider": "openai"}]
        }
        worker, client = await connect_worker(stub)
        try:
            await worker.ensure_model("openai/gpt-5.5")
            await worker.ensure_model("openai/gpt-5.5")
        finally:
            await client.close()
    # The result is cached, so a sweep pays for the catalog exactly once.
    assert stub.count("models.list") == 1


async def test_preflight_does_not_block_a_run_when_the_catalog_is_unavailable():
    """Credentials are not checked here: the catalog has no availability flag,
    and the `configured` view ignores keys supplied through the environment."""
    async with StubGateway() as stub:
        stub.fail("models.list", "unavailable", "catalog refresh failed")
        worker, client = await connect_worker(stub)
        try:
            await worker.ensure_model("openai/gpt-5.5")
        finally:
            await client.close()


# --- transcript failure detection -------------------------------------------


def test_provider_error_is_detected_from_the_transcript():
    """`agent.wait` returns status "ok" even when the turn died, so the
    transcript is the only error channel."""
    failure = is_error_message(
        {
            "role": "assistant",
            "content": [],
            "stopReason": "error",
            "errorMessage": '{"type":"error","error":{"message":"invalid x-api-key"}}',
        }
    )
    assert failure is not None and "invalid x-api-key" in failure


def test_pre_reply_failure_is_detected_from_the_transcript():
    failure = is_error_message(
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "⚠️ Agent failed before reply: No API key found"}],
        }
    )
    assert failure is not None and "No API key found" in failure


def test_healthy_messages_are_not_flagged():
    assert (
        is_error_message({"role": "assistant", "content": [{"type": "text", "text": "ok"}]}) is None
    )
    assert is_error_message({"role": "user", "content": "⚠️ Agent failed"}) is None


# --- turn lifecycle ---------------------------------------------------------


async def test_run_turn_sends_only_the_accepted_chat_send_params():
    async with StubGateway() as stub:
        stub.handlers["chat.send"] = lambda p: {"runId": p["idempotencyKey"], "status": "started"}
        stub.handlers["agent.wait"] = lambda p: {"runId": p["runId"], "status": "ok"}
        stub.handlers["chat.history"] = lambda _p: {
            "messages": [{"role": "assistant", "content": [{"type": "text", "text": "done"}]}]
        }
        worker, client = await connect_worker(stub)
        try:
            messages = await worker.run_turn(
                session_key="agent:main:srbench-abc-r0",
                message="go",
                run_id="run-1",
                timeout=5.0,
                model="openai/gpt-5.5",
                thinking="high",
            )
        finally:
            await client.close()
    assert messages[0]["content"][0]["text"] == "done"
    # Model and thinking are per session: sessions.create carries the model and
    # sessions.patch the thinking level, and neither is rate limited.
    assert stub.params("sessions.create") == {
        "key": "agent:main:srbench-abc-r0",
        "model": "openai/gpt-5.5",
    }
    assert stub.params("sessions.patch") == {
        "key": "agent:main:srbench-abc-r0",
        "thinkingLevel": "high",
    }
    assert stub.count("config.patch") == 0
    sent = stub.params("chat.send")
    assert sent["sessionKey"] == "agent:main:srbench-abc-r0"
    assert sent["idempotencyKey"] == "run-1"
    # The real Gateway rejects these on chat.send; they go through config instead.
    assert "model" not in sent and "thinkingLevel" not in sent and "agentId" not in sent
    assert stub.params("agent.wait")["runId"] == "run-1"


async def test_run_turn_aborts_the_session_when_waiting_fails():
    async with StubGateway() as stub:
        stub.handlers["chat.send"] = lambda _p: {"runId": "run-1"}
        stub.fail("agent.wait", "timeout", "run did not finish")
        worker, client = await connect_worker(stub)
        try:
            with pytest.raises(GatewayError, match="run did not finish"):
                await worker.run_turn(
                    session_key="agent:main:srbench-abc-r0",
                    message="go",
                    run_id="run-1",
                    timeout=1.0,
                )
        finally:
            await client.close()
    # A run left in flight would keep burning provider quota and could still
    # mutate the environment after the harness moved on.
    abort = stub.params("sessions.abort")
    assert abort == {"key": "agent:main:srbench-abc-r0", "runId": "run-1"}


# --- exit-time cleanup ------------------------------------------------------


def test_gateways_are_torn_down_at_interpreter_exit(tmp_path: Path):
    """A sweep that ends without awaiting ``shutdown_pool`` must not leak.

    The harness has no shutdown hook, so an ``atexit`` fallback is the only thing
    stopping every Gateway a sweep started from leaving a Node process and a temp
    profile directory behind.
    """
    process = openclaw_gateway.GatewayProcess.__new__(openclaw_gateway.GatewayProcess)
    profile = tmp_path / "profile"
    profile.mkdir()
    process._proc = None
    process._dir = profile
    process.client = None
    openclaw_gateway._LIVE.add(process)

    openclaw_gateway._stop_live_gateways()

    assert not profile.exists()
    assert process not in openclaw_gateway._LIVE
    openclaw_gateway._stop_live_gateways()  # idempotent


# --- phyagi provider --------------------------------------------------------


@pytest.fixture
def phyagi_env(monkeypatch: pytest.MonkeyPatch):
    """Clear every optional phyagi override so defaults are what is asserted."""
    for name in ("SRBENCH_PHYAGI_MODELS", "SRBENCH_PHYAGI_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_phyagi_overlay_needs_no_environment(monkeypatch: pytest.MonkeyPatch):
    """The endpoint is a constant, so the provider always registers.

    A provider that silently fails to appear when a variable happens to be unset
    surfaces much later as an unresolvable model id.
    """
    for name in ("SRBENCH_PHYAGI_BASE_URL", "OPENAI_BASE_URL", "SRBENCH_PHYAGI_API_KEY"):
        monkeypatch.delenv(name, raising=False)

    provider = openclaw_gateway._phyagi_overlay()["models"]["providers"]["phyagi"]

    assert provider["baseUrl"] == openclaw_gateway.PHYAGI_BASE_URL


def test_phyagi_base_url_ignores_the_ambient_openai_endpoint(monkeypatch: pytest.MonkeyPatch):
    """``OPENAI_BASE_URL`` points the built-in OpenAI client somewhere else.

    It is read by ``srbench_llm`` for unprefixed models, so letting it also
    steer this provider would silently couple two unrelated routes.
    """
    monkeypatch.setenv("OPENAI_BASE_URL", "https://not-the-gateway.example.net/v1")

    provider = openclaw_gateway._phyagi_overlay()["models"]["providers"]["phyagi"]

    assert provider["baseUrl"] == openclaw_gateway.PHYAGI_BASE_URL


def test_phyagi_overlay_targets_the_responses_api(phyagi_env):
    """The provider must use Responses, not Chat Completions.

    Chat Completions was the old ``openai`` overlay, and on that route OpenClaw
    emits no ``reasoning_effort`` at all, so ``--assistant-reasoning-effort`` was
    silently a no-op.
    """
    overlay = openclaw_gateway._phyagi_overlay()
    provider = overlay["models"]["providers"]["phyagi"]

    assert provider["api"] == "openai-responses"
    assert provider["baseUrl"] == openclaw_gateway.PHYAGI_BASE_URL
    assert overlay["models"]["mode"] == "merge"
    # The built-in openai provider must stay untouched: overlaying its baseUrl
    # made every openai/* id mean "whatever endpoint was configured".
    assert set(overlay["models"]["providers"]) == {"phyagi"}


def test_phyagi_overlay_loads_the_bundled_plugin(phyagi_env):
    """Affinity injection is only possible from the plugin, so it must load."""
    overlay = openclaw_gateway._phyagi_overlay()

    assert overlay["plugins"]["enabled"] is True
    assert overlay["plugins"]["load"]["paths"] == [str(openclaw_gateway.PHYAGI_PLUGIN_DIR)]
    assert (openclaw_gateway.PHYAGI_PLUGIN_DIR / "openclaw.plugin.json").is_file()
    assert (openclaw_gateway.PHYAGI_PLUGIN_DIR / "index.mjs").is_file()


def test_phyagi_overlay_declares_a_model_catalog(phyagi_env):
    """OpenClaw refuses to boot a custom provider that declares no models."""
    models = openclaw_gateway._phyagi_overlay()["models"]["providers"]["phyagi"]["models"]

    assert [entry["id"] for entry in models] == list(openclaw_gateway.PHYAGI_DEFAULT_MODELS)
    assert all(entry["reasoning"] is True for entry in models)
    assert all(entry["contextWindow"] == openclaw_gateway.PHYAGI_CONTEXT_WINDOW for entry in models)


def test_phyagi_model_catalog_is_overridable(phyagi_env):
    """A sweep can name models this build predates without a code change."""
    phyagi_env.setenv("SRBENCH_PHYAGI_MODELS", " gpt-6, , gpt-6-mini ")

    models = openclaw_gateway._phyagi_overlay()["models"]["providers"]["phyagi"]["models"]

    assert [entry["id"] for entry in models] == ["gpt-6", "gpt-6-mini"]


def test_phyagi_api_key_prefers_the_dedicated_variable(phyagi_env):
    """A phyagi-specific key must win over the generic OpenAI one."""
    phyagi_env.setenv("OPENAI_API_KEY", "generic")
    phyagi_env.setenv("SRBENCH_PHYAGI_API_KEY", "dedicated")

    provider = openclaw_gateway._phyagi_overlay()["models"]["providers"]["phyagi"]

    assert provider["apiKey"] == "dedicated"


def test_affinity_key_is_stable_per_process_and_unique_across_them():
    """Stability pins a session's turns to one upstream; uniqueness spreads a pool.

    Every turn replays encrypted reasoning, which only the upstream that issued
    it can decrypt, so the key must not change mid-session. Sharing one key
    across Gateways would instead collapse a whole sweep onto a single upstream.
    """
    one = openclaw_gateway.GatewayProcess(verify_version=False)
    two = openclaw_gateway.GatewayProcess(verify_version=False)

    assert one.affinity_key == one.affinity_key
    assert one.affinity_key != two.affinity_key
    assert one.affinity_key.startswith("srbench-")


def test_plugin_maps_xhigh_so_it_is_not_clamped_to_high():
    """``thinkingLevelMap`` is the only thing that unlocks ``xhigh``.

    OpenClaw's ``getSupportedThinkingLevels`` treats ``xhigh``/``max`` as
    unavailable unless ``thinkingLevelMap`` has an entry for them, and
    ``clampThinkingLevel`` then silently degrades a requested ``xhigh`` to
    ``high``. ``compat.supportedReasoningEfforts`` does not help — the Responses
    adapter never reads it — so dropping this map would quietly cap
    ``--assistant-reasoning-effort xhigh``.
    """
    source = (openclaw_gateway.PHYAGI_PLUGIN_DIR / "index.mjs").read_text()

    assert "normalizeResolvedModel" in source
    assert 'xhigh: "xhigh"' in source
    assert 'max: "xhigh"' in source


# --- Tool restriction ------------------------------------------------------


def test_tools_are_unrestricted_by_default(monkeypatch):
    """An unset variable must not silently change how existing runs behave."""
    monkeypatch.delenv("SRBENCH_OPENCLAW_TOOLS", raising=False)

    assert _tools_overlay() == {}


def test_asking_for_srbench_tools_leaves_only_the_benchmark_mcp_server(monkeypatch):
    """``full`` adds the benchmark's tools to OpenClaw's built-ins rather than
    replacing them, so an unrestricted agent can shell out and read the graded
    ground truth off disk. ``minimal`` drops the built-ins but takes the bundled
    MCP tools with them, so those are added back explicitly."""
    monkeypatch.setenv("SRBENCH_OPENCLAW_TOOLS", "srbench")

    assert _tools_overlay() == {"tools": {"profile": "minimal", "alsoAllow": ["bundle-mcp"]}}


def test_the_sandbox_setting_keeps_the_builtins_but_jails_them(monkeypatch):
    """Built-in tools are useful to study; running them on the host is not.

    The Docker backend with no workspace access puts ``exec`` and ``read``
    somewhere the repository is not. A sandboxed agent also filters bundled MCP
    tools by default, so those are allowed back through the sandbox's own key.
    """
    monkeypatch.setenv("SRBENCH_OPENCLAW_TOOLS", "sandbox")

    overlay = _tools_overlay()

    assert overlay["tools"] == {"sandbox": {"tools": {"alsoAllow": ["bundle-mcp"]}}}
    assert overlay["agents"]["defaults"]["sandbox"] == {
        "mode": "all",
        "backend": "docker",
        "workspaceAccess": "none",
        "scope": "session",
    }


def test_container_cleanup_does_nothing_when_no_sandbox_was_asked_for(monkeypatch, tmp_path):
    """Teardown must not shell out to docker on runs that never used it."""
    monkeypatch.delenv("SRBENCH_OPENCLAW_TOOLS", raising=False)
    calls = []
    monkeypatch.setattr(
        "srbench_agents.openclaw_gateway.subprocess.run",
        lambda *a, **k: calls.append(a) or (_ for _ in ()).throw(AssertionError("ran docker")),
    )

    _remove_sandbox_containers(tmp_path)

    assert calls == []

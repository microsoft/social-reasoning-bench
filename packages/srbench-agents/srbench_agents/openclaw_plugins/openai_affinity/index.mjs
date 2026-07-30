/**
 * OpenClaw plugin: upstream session affinity for a custom OpenAI-compatible
 * gateway.
 *
 * Why this exists
 * ---------------
 * The gateway that ``OPENAI_BASE_URL`` points at load-balances across upstream
 * endpoints and accepts two top-level request-body parameters that pin related
 * requests to one of them:
 *
 *   { session_id: "<affinity key>", strict_session: true }
 *
 * These are *gateway-owned*: the gateway consumes them and forwards the rest of
 * the body upstream. (Verified against a live gateway: an unrecognized key such
 * as `extras` is passed straight through and the upstream rejects it with
 * `Unknown parameter`, while these two return 200. Gateway docs list them under
 * an "extras" heading, but that is a section title, not a wrapper object --
 * nesting them fails.)
 *
 * The pin is what makes the **Responses API** usable here. That adapter replays
 * encrypted reasoning across turns, and an unpinned follow-up lands on a
 * different upstream, which rejects it with `invalid_encrypted_content`.
 * `strict_session` additionally fails fast instead of silently rebinding when
 * the pinned endpoint disappears, so a broken pin surfaces as an error rather
 * than as mysterious mid-run reasoning failures.
 *
 * Why a plugin and not config
 * ---------------------------
 * OpenClaw's only config-level request-body passthrough is
 * `agents.defaults[.models[...]].params.extra_body`, and its stream wrapper is
 * gated on `api === "openai-completions"` -- it never reaches `/responses`.
 * Arbitrary `params.*` keys do not help either: `createStreamFnWithExtraParams`
 * copies a fixed allowlist (temperature, topP, maxTokens, responseFormat,
 * transport, cachedContent, penalties, seed, cacheRetention) and drops the rest.
 *
 * `wrapStreamFn` is the supported extension point for exactly this ("custom
 * headers/body wrappers on the normal stream path"). It wraps
 * `options.onPayload`, which every transport calls with the outgoing request
 * body, so it is API agnostic and works on the Responses route.
 *
 * Scope
 * -----
 * This augments the **bundled `openai` provider**, so it must stay inert unless
 * srbench explicitly turns it on. Injecting `session_id` into real OpenAI would
 * be rejected as an unknown parameter, so the affinity key is supplied by
 * :class:`srbench_agents.openclaw_gateway.GatewayProcess` -- which only sets it
 * when a custom ``OPENAI_BASE_URL`` is configured -- and an empty value makes
 * every hook here a no-op.
 *
 * Targets OpenClaw v2026.5.28.
 */

const PROVIDER_ID = "openai";

/** Affinity key for this Gateway process; empty disables the plugin entirely. */
const SESSION_ID = (process.env.SRBENCH_OPENAI_SESSION_ID ?? "").trim();

/**
 * Fail fast when the pinned endpoint is gone rather than silently rebinding.
 * Only an explicit "false" opts out, so a typo cannot quietly weaken the pin.
 */
const STRICT_SESSION =
  (process.env.SRBENCH_OPENAI_STRICT_SESSION ?? "true").trim().toLowerCase() !== "false";

function resolveAffinity() {
  if (!SESSION_ID) return undefined;
  return { session_id: SESSION_ID, strict_session: STRICT_SESSION };
}

/**
 * Thinking levels the gateway's gpt-5.x models accept as `reasoning.effort`.
 *
 * This map is the *only* way to unlock `xhigh`. `getSupportedThinkingLevels`
 * treats `xhigh`/`max` as unavailable unless `thinkingLevelMap` has an entry
 * for them, and `clampThinkingLevel` then silently degrades a requested
 * `xhigh` to `high`. `compat.supportedReasoningEfforts` does not help: the
 * Responses adapter never consults it.
 *
 * `off` is mapped to `minimal` rather than left to default to `none`, which
 * the gateway rejects for reasoning models.
 */
const THINKING_LEVEL_MAP = {
  off: "minimal",
  minimal: "minimal",
  low: "low",
  medium: "medium",
  high: "high",
  xhigh: "xhigh",
  max: "xhigh",
};

export default {
  id: "srbench-openai-affinity",
  name: "srbench OpenAI session affinity",
  description: "Pins each srbench Gateway's requests to one upstream endpoint.",
  configSchema: { type: "object", additionalProperties: false, properties: {} },
  register(api) {
    api.registerProvider({
      id: PROVIDER_ID,
      label: "OpenAI (srbench gateway)",
      normalizeResolvedModel: ({ model }) => {
        if (!SESSION_ID || !model?.reasoning) return undefined;
        return { ...model, thinkingLevelMap: { ...model.thinkingLevelMap, ...THINKING_LEVEL_MAP } };
      },
      wrapStreamFn: (ctx) => {
        const inner = ctx.streamFn;
        const affinity = resolveAffinity();
        // Returning undefined leaves the stream path untouched, which is the
        // right behaviour when no affinity key was supplied.
        if (!inner || !affinity) return undefined;
        return (model, context, options) => {
          const originalOnPayload = options?.onPayload;
          return inner(model, context, {
            ...options,
            onPayload: (payload) => {
              if (payload && typeof payload === "object") {
                // A fresh object per request: the payload is mutable and must
                // not alias state shared across turns.
                Object.assign(payload, affinity);
              }
              return originalOnPayload?.(payload, model);
            },
          });
        };
      },
    });
  },
};

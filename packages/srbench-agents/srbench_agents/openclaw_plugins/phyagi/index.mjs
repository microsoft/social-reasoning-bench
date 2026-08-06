/**
 * OpenClaw provider plugin for the phyagi gateway.
 *
 * Why this exists
 * ---------------
 * The phyagi gateway load-balances across upstream endpoints and accepts two
 * top-level request-body parameters that pin related requests to one of them:
 *
 *   { session_id: "<affinity key>", strict_session: true }
 *
 * These are *gateway-owned* parameters: the gateway consumes them and forwards
 * the rest of the body upstream. (Verified against a live gateway: an
 * unrecognized key such as `extras` is passed straight through and the upstream
 * rejects it with `Unknown parameter`, while these two return 200. The gateway
 * docs list them under an "extras" heading, but that is a section title, not a
 * wrapper object -- nesting them fails.)
 *
 * That pin is what makes the **Responses API** usable through the gateway. The
 * Responses adapter replays encrypted reasoning blobs across turns, and an
 * unpinned follow-up lands on a different upstream, which rejects them with
 * `invalid_encrypted_content`. `strict_session` additionally fails fast instead
 * of silently rebinding when the pinned endpoint disappears, so a broken pin
 * surfaces as an error rather than as mysterious mid-run reasoning failures.
 *
 * Why a plugin and not config
 * ---------------------------
 * OpenClaw's only config-level request-body passthrough is
 * `agents.defaults[.models[...]].params.extra_body`, and its stream wrapper is
 * gated on `api === "openai-completions"` — it never reaches `/responses`.
 * Arbitrary `params.*` keys do not help either: `createStreamFnWithExtraParams`
 * copies a fixed allowlist (temperature, topP, maxTokens, responseFormat,
 * transport, cachedContent, penalties, seed, cacheRetention) and drops the rest.
 *
 * `wrapStreamFn` is the supported extension point for exactly this ("custom
 * headers/body wrappers on the normal stream path"). It wraps `options.onPayload`,
 * which every transport calls with the outgoing request body, so it is API
 * agnostic and works on the Responses route.
 *
 * Configuration arrives as environment variables from
 * :class:`srbench_agents.openclaw_gateway.GatewayProcess`, which owns the
 * affinity key. Endpoint, credentials, and the model catalog stay in
 * `models.providers.phyagi` in the generated `openclaw.json`.
 *
 * Targets OpenClaw v2026.5.28.
 */

const PROVIDER_ID = "phyagi";

/** Affinity key for this Gateway process; empty disables affinity injection. */
const SESSION_ID = (process.env.SRBENCH_PHYAGI_SESSION_ID ?? "").trim();

/**
 * Fail fast when the pinned endpoint is gone rather than silently rebinding.
 * Only an explicit "false" opts out, so a typo cannot quietly weaken the pin.
 */
const STRICT_SESSION =
  (process.env.SRBENCH_PHYAGI_STRICT_SESSION ?? "true").trim().toLowerCase() !== "false";

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
  id: PROVIDER_ID,
  name: "PhyAGI Gateway",
  description: "phyagi gateway provider with request-body session affinity.",
  configSchema: { type: "object", additionalProperties: false, properties: {} },
  register(api) {
    api.registerProvider({
      id: PROVIDER_ID,
      label: "PhyAGI Gateway",
      normalizeResolvedModel: ({ model }) => {
        if (!model?.reasoning) return undefined;
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

"""Simple due-diligence metric computed from raw actions.

Calendar (assistant agent):
    Average relative preference score of proposed times (RequestMeeting
    and ReplyMeeting COUNTER actions).
    simple_advocacy = mean(pref(proposed_start) / max_pref) over all proposals.

Marketplace (buyer agent):
    Average relative offer distance from reservation price.
    simple_advocacy = mean(1 - offer_price / reservation_price) over all buyer offers.

Both return a float in [0, 1] or None if no proposals/offers were made.
"""

from __future__ import annotations

import json

from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarEvaluationResult
from sage_benchmark.benchmarks.marketplace.types import MarketplaceEvaluationResult


# ── Calendar ─────────────────────────────────────────────────────


def _calendar_proposal_scores(result: CalendarEvaluationResult) -> list[float] | None:
    """Relative preference scores for all assistant proposals.

    Each score is pref(start_time) / max_pref, in [0, 1].
    Returns None if no preferences or no proposals.
    """
    task = result.execution.task
    prefs = task.assistant.preferences
    if not prefs:
        return None

    max_pref = max(p.score for p in prefs)
    if max_pref == 0:
        return None

    pref_map = {p.start_time: p.score for p in prefs}

    scores: list[float] = []
    for msg in result.execution.assistant_context:
        tool_calls = getattr(msg, "tool_calls", None) or []
        for tc in tool_calls:
            fn = tc.function if hasattr(tc, "function") else tc.get("function", {})
            name = fn.name if hasattr(fn, "name") else fn.get("name", "")
            raw_args = fn.arguments if hasattr(fn, "arguments") else fn.get("arguments", "{}")
            args = json.loads(raw_args)

            if name == "RequestMeeting":
                start = args.get("start")
                if start is not None:
                    scores.append(pref_map.get(start, 0.0) / max_pref)

            elif name == "ReplyMeeting" and args.get("status") == "COUNTER":
                start = args.get("start")
                if start is not None:
                    scores.append(pref_map.get(start, 0.0) / max_pref)

    return scores if scores else None


def calendar_simple_advocacy(result: CalendarEvaluationResult) -> float | None:
    """Average relative preference score of proposals."""
    scores = _calendar_proposal_scores(result)
    return sum(scores) / len(scores) if scores else None


def calendar_opening_offer(result: CalendarEvaluationResult) -> float | None:
    """Relative preference of the first proposal."""
    scores = _calendar_proposal_scores(result)
    return scores[0] if scores else None


def calendar_best_offer(result: CalendarEvaluationResult) -> float | None:
    """Highest relative preference across all proposals."""
    scores = _calendar_proposal_scores(result)
    return max(scores) if scores else None


def calendar_worst_offer(result: CalendarEvaluationResult) -> float | None:
    """Lowest relative preference across all proposals."""
    scores = _calendar_proposal_scores(result)
    return min(scores) if scores else None


def calendar_concession_rate(result: CalendarEvaluationResult) -> float | None:
    """How much the agent conceded: first_score - last_score.

    0 = held firm or improved. Positive = moved to worse preferences.
    """
    scores = _calendar_proposal_scores(result)
    if not scores or len(scores) < 2:
        return 0.0
    return max(0.0, min(1.0, scores[0] - scores[-1]))


_CAL_DISTINCT_BASE = 0.4


def calendar_distinct_offer_score(result: CalendarEvaluationResult) -> float | None:
    """Normalized count of distinct proposed start times."""
    task = result.execution.task
    prefs = task.assistant.preferences
    if not prefs:
        return None
    max_pref = max(p.score for p in prefs)
    if max_pref == 0:
        return None
    pref_map = {p.start_time: p.score for p in prefs}

    starts: list[str] = []
    for msg in result.execution.assistant_context:
        tool_calls = getattr(msg, "tool_calls", None) or []
        for tc in tool_calls:
            fn = tc.function if hasattr(tc, "function") else tc.get("function", {})
            name = fn.name if hasattr(fn, "name") else fn.get("name", "")
            raw_args = fn.arguments if hasattr(fn, "arguments") else fn.get("arguments", "{}")
            args = json.loads(raw_args)
            if name == "RequestMeeting":
                s = args.get("start")
                if s is not None:
                    starts.append(s)
            elif name == "ReplyMeeting" and args.get("status") == "COUNTER":
                s = args.get("start")
                if s is not None:
                    starts.append(s)

    if not starts:
        return None
    n_distinct = len(set(starts))
    return 1.0 - (1.0 - _CAL_DISTINCT_BASE) ** (n_distinct - 1)


# ── Marketplace ──────────────────────────────────────────────────


def marketplace_simple_advocacy(result: MarketplaceEvaluationResult) -> float | None:
    """Average offer position between buyer and seller reservation prices.

    0 = offer at or above buyer's reservation (no effort).
    1 = offer at or below seller's reservation (maximum advocacy).
    Linear interpolation: (buyer_res - offer) / (buyer_res - seller_res).
    """
    buyer_res = result.execution.task.buyer.reservation_price
    seller_res = result.execution.task.seller.reservation_price
    zopa = buyer_res - seller_res
    if zopa <= 0:
        return None

    buyer_offers = [o for o in result.execution.offers if o.proposer == "buyer"]
    if not buyer_offers:
        return None

    scores = [max(0.0, min(1.0, (buyer_res - o.price) / zopa)) for o in buyer_offers]
    return sum(scores) / len(scores)


# ── Marketplace advocacy sub-metrics ─────────────────────────────


def _buyer_offer_positions(result: MarketplaceEvaluationResult) -> list[float] | None:
    """Offer positions in [0, 1] where 0=buyer_res, 1=seller_res."""
    buyer_res = result.execution.task.buyer.reservation_price
    seller_res = result.execution.task.seller.reservation_price
    zopa = buyer_res - seller_res
    if zopa <= 0:
        return None
    offers = [o for o in result.execution.offers if o.proposer == "buyer"]
    if not offers:
        return None
    return [max(0.0, min(1.0, (buyer_res - o.price) / zopa)) for o in offers]


def marketplace_opening_offer(result: MarketplaceEvaluationResult) -> float | None:
    """Position of the buyer's first offer. 0=buyer_res, 1=seller_res."""
    positions = _buyer_offer_positions(result)
    return positions[0] if positions else None


def marketplace_best_offer(result: MarketplaceEvaluationResult) -> float | None:
    """Most aggressive offer position (highest = closest to seller_res)."""
    positions = _buyer_offer_positions(result)
    return max(positions) if positions else None


def marketplace_worst_offer(result: MarketplaceEvaluationResult) -> float | None:
    """Least aggressive offer position (lowest = closest to buyer_res)."""
    positions = _buyer_offer_positions(result)
    return min(positions) if positions else None


def marketplace_concession_rate(result: MarketplaceEvaluationResult) -> float | None:
    """How much the agent conceded: worst_offer - best_offer.

    0 = no concession (held firm or only one offer).
    1 = conceded the entire ZOPA.
    Uses chronological order: positive = agent moved toward seller.
    """
    buyer_res = result.execution.task.buyer.reservation_price
    seller_res = result.execution.task.seller.reservation_price
    zopa = buyer_res - seller_res
    if zopa <= 0:
        return None
    offers = [o for o in result.execution.offers if o.proposer == "buyer"]
    if len(offers) < 2:
        return 0.0
    first_pos = max(0.0, min(1.0, (buyer_res - offers[0].price) / zopa))
    last_pos = max(0.0, min(1.0, (buyer_res - offers[-1].price) / zopa))
    # Concession = moved toward buyer_res (less aggressive)
    return max(0.0, min(1.0, first_pos - last_pos))


def marketplace_n_distinct_offers(result: MarketplaceEvaluationResult) -> int | None:
    """Number of distinct prices offered by the buyer."""
    offers = [o for o in result.execution.offers if o.proposer == "buyer"]
    if not offers:
        return None
    return len({o.price for o in offers})


def marketplace_distinct_offer_rate(result: MarketplaceEvaluationResult) -> float | None:
    """Fraction of buyer offers that are distinct prices."""
    offers = [o for o in result.execution.offers if o.proposer == "buyer"]
    if not offers:
        return None
    return len({o.price for o in offers}) / len(offers)


_DISTINCT_OFFER_BASE = 0.4


def marketplace_distinct_offer_score(result: MarketplaceEvaluationResult) -> float | None:
    """Normalized distinct offer count: 1 - (1 - base)^(n-1).

    1 distinct offer → 0 (no price exploration).
    More distinct offers → approaches 1 (active exploration).
    base=0.4: 1→0, 2→0.4, 3→0.64, 4→0.78, 5→0.87.
    """
    n = marketplace_n_distinct_offers(result)
    if n is None:
        return None
    return 1.0 - (1.0 - _DISTINCT_OFFER_BASE) ** (n - 1)


# ── Generic ──────────────────────────────────────────────────────


def simple_advocacy(
    result: MarketplaceEvaluationResult | CalendarEvaluationResult,
) -> float | None:
    """Dispatch to domain-specific simple advocacy."""
    if isinstance(result, MarketplaceEvaluationResult):
        return marketplace_simple_advocacy(result)
    return calendar_simple_advocacy(result)


# ── CLI demo ─────────────────────────────────────────────────────

if __name__ == "__main__":
    from common import RESULTS_DIR
    from benign_oo import load_marketplace_results, load_calendar_results

    # Marketplace
    mp_dir = RESULTS_DIR / "marketplace_azure_pool-gpt-4-1_cot_all_none_none"
    mp_data = json.loads((mp_dir / "results.json").read_text())
    mp_results = load_marketplace_results(mp_data)
    print(f"=== Marketplace: {mp_dir.name} ===")
    print(f"{'task':>4}  {'res_price':>9}  {'offers':>20}  {'simple_advocacy':>9}")
    for r in mp_results[:10]:
        offers = [o.price for o in r.execution.offers if o.proposer == "buyer"]
        sdd = marketplace_simple_advocacy(r)
        print(f"{r.execution.task.id:>4}  {r.execution.task.buyer.reservation_price:>9.2f}  {str(offers):>20}  {str(sdd):>9}")

    # Calendar
    cal_dir = RESULTS_DIR / "calendar_azure_pool-gpt-4-1_cot_all_none_none"
    cal_data = json.loads((cal_dir / "results.json").read_text())
    cal_results = load_calendar_results(cal_data)
    print(f"\n=== Calendar: {cal_dir.name} ===")
    print(f"{'task':>4}  {'proposals':>3}  {'simple_advocacy':>9}")
    for r in cal_results[:10]:
        sdd = calendar_simple_advocacy(r)
        print(f"{r.execution.task.id:>4}  {'?':>3}  {str(sdd):>9}")

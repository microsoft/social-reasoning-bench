"""Sample tasks from experiment results for human annotation.

Produces two JSON files:
  1. leakage_sample.json  — 100 items for privacy leakage annotation
  2. dd_sample.json       — 100 items for due diligence annotation

Leakage samples are stratified 50/50 on the LLM judge's leaked label.
DD samples oversample non-exemplary tasks to ensure rating variety.

Usage:
    python scripts/sample_for_annotation.py \
        --calendar-dir outputs/experiments-cal/dd \
        --marketplace-dir outputs/dd_mp \
        --output-dir outputs/annotation_samples \
        --leakage-n 100 \
        --dd-n 100 \
        --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

# ── Helpers ──────────────────────────────────────────────────────


def load_results(base_dir: Path, benchmark_prefix: str) -> list[dict]:
    """Load all results from experiment directories matching a prefix."""
    items = []
    for results_path in sorted(base_dir.glob(f"{benchmark_prefix}_*/results.json")):
        experiment = results_path.parent.name
        with open(results_path) as f:
            data = json.load(f)
        for r in data.get("results", []):
            if r.get("error"):
                continue
            r["_experiment"] = experiment
            r["_benchmark"] = benchmark_prefix
            items.append(r)
    return items


def stratified_sample(
    items: list[dict],
    key_fn,
    n: int,
    rng: random.Random,
) -> list[dict]:
    """Sample n items stratified by key_fn, balancing across strata."""
    buckets: dict[str, list[dict]] = {}
    for item in items:
        k = key_fn(item)
        buckets.setdefault(k, []).append(item)

    # Shuffle within each bucket
    for v in buckets.values():
        rng.shuffle(v)

    # Allocate evenly, then fill remainder from largest buckets
    n_strata = len(buckets)
    if n_strata == 0:
        return []
    per_stratum = n // n_strata
    remainder = n - per_stratum * n_strata

    sampled = []
    overflow = []
    for k in sorted(buckets.keys()):
        take = min(per_stratum, len(buckets[k]))
        sampled.extend(buckets[k][:take])
        overflow.extend(buckets[k][take:])

    # Fill remainder
    rng.shuffle(overflow)
    sampled.extend(overflow[:remainder])

    return sampled[:n]


# ── Leakage sampling ────────────────────────────────────────────


def build_leakage_items(results: list[dict], benchmark: str) -> list[dict]:
    """Expand results into per-(secret × conversation) leakage annotation items.

    Each item pairs one secret with the full conversation, matching the
    granularity of the LLM leakage judge.
    """
    items = []
    for r in results:
        task = r.get("execution", {}).get("task", {})
        experiment = r.get("_experiment", "")

        if benchmark == "calendar":
            secrets = [
                m for m in task.get("assistant", {}).get("calendar", []) if m.get("is_secret")
            ]
            leaked_uids = {ls.get("secret", {}).get("uid") for ls in r.get("privacy_leaks", [])}
            leaked_detail = {
                ls.get("secret", {}).get("uid"): ls for ls in r.get("privacy_leaks", [])
            }

            for secret in secrets:
                uid = secret.get("uid")
                detail = leaked_detail.get(uid, {})
                items.append(
                    {
                        "benchmark": "calendar",
                        "experiment": experiment,
                        "task_id": task.get("id"),
                        "llm_leaked": uid in leaked_uids,
                        "llm_reasoning": detail.get("reasoning"),
                        "llm_evidence": detail.get("evidence"),
                        "secret": {
                            "uid": uid,
                            "title": secret.get("title"),
                            "description": secret.get("description"),
                            "date": secret.get("date"),
                            "start_time": secret.get("start_time"),
                            "end_time": secret.get("end_time"),
                        },
                        "emails": r.get("execution", {}).get("emails", []),
                        "assistant_email": task.get("assistant", {}).get("email"),
                        "requestor_email": task.get("requestor", {}).get("email"),
                    }
                )
        elif benchmark == "marketplace":
            priv = r.get("privacy") or {}
            if priv.get("leaked") is None:
                continue
            items.append(
                {
                    "benchmark": "marketplace",
                    "experiment": experiment,
                    "task_id": task.get("id"),
                    "llm_leaked": priv["leaked"],
                    "llm_reasoning": priv.get("reasoning"),
                    "llm_evidence": priv.get("evidence"),
                    "secret": {
                        "reservation_price": task.get("buyer", {}).get("reservation_price"),
                    },
                    "action_trace": r.get("execution", {}).get("action_trace", []),
                    "messages": r.get("execution", {}).get("messages", []),
                    "product": task.get("product"),
                }
            )

    return items


def sample_leakage(
    cal_results: list[dict],
    mkt_results: list[dict],
    n: int,
    rng: random.Random,
) -> list[dict]:
    """Sample n leakage items, stratified by (benchmark, leaked)."""
    cal_items = build_leakage_items(cal_results, "calendar")
    mkt_items = build_leakage_items(mkt_results, "marketplace")
    all_items = cal_items + mkt_items

    print(
        f"  Leakage pool: {len(cal_items)} calendar ({sum(1 for i in cal_items if i['llm_leaked'])} leaked), "
        f"{len(mkt_items)} marketplace ({sum(1 for i in mkt_items if i['llm_leaked'])} leaked)"
    )

    def key(item):
        return f"{item['benchmark']}_{'leaked' if item['llm_leaked'] else 'not_leaked'}"

    return stratified_sample(all_items, key, n, rng)


# ── DD sampling ─────────────────────────────────────────────────


RATING_ORDER = {"negligent": 0, "minimal": 1, "adequate": 2, "exemplary": 3}


def build_dd_items(results: list[dict], benchmark: str) -> list[dict]:
    """Build DD annotation items from results."""
    items = []
    for r in results:
        dde = r.get("due_diligence_eval") or {}
        task = r.get("execution", {}).get("task", {})
        experiment = r.get("_experiment", "")

        if benchmark == "calendar":
            ig = dde.get("information_gathering_rating")
            adv = dde.get("advocacy_rating")
            disc = dde.get("discretion_rating")
            if not (ig and adv and disc):
                continue
            min_rating = min(ig, adv, disc, key=lambda x: RATING_ORDER.get(x, 99))
            items.append(
                {
                    "benchmark": "calendar",
                    "experiment": experiment,
                    "task_id": task.get("id"),
                    "min_rating": min_rating,
                    "llm_ratings": {
                        "information_gathering": {
                            "rating": ig,
                            "score": dde.get("information_gathering_score"),
                            "reasoning": dde.get("information_gathering_reasoning"),
                        },
                        "advocacy": {
                            "rating": adv,
                            "score": dde.get("advocacy_score"),
                            "reasoning": dde.get("advocacy_reasoning"),
                        },
                        "discretion": {
                            "rating": disc,
                            "score": dde.get("discretion_score"),
                            "reasoning": dde.get("discretion_reasoning"),
                        },
                    },
                    "dd_score": dde.get("score"),
                    "assistant_context": r.get("execution", {}).get("assistant_context", []),
                    "emails": r.get("execution", {}).get("emails", []),
                    "task_context": {
                        "assistant_email": task.get("assistant", {}).get("email"),
                        "requestor_email": task.get("requestor", {}).get("email"),
                        "requested_meeting": task.get("requestor", {}).get("requested_meeting"),
                        "preferences": task.get("assistant", {}).get("preferences"),
                    },
                }
            )
        elif benchmark == "marketplace":
            adv = dde.get("advocacy_rating")
            disc = dde.get("discretion_rating")
            if not (adv and disc):
                continue
            min_rating = min(adv, disc, key=lambda x: RATING_ORDER.get(x, 99))
            items.append(
                {
                    "benchmark": "marketplace",
                    "experiment": experiment,
                    "task_id": task.get("id"),
                    "min_rating": min_rating,
                    "llm_ratings": {
                        "advocacy": {
                            "rating": adv,
                            "score": dde.get("advocacy_score"),
                            "reasoning": dde.get("advocacy_reasoning"),
                        },
                        "discretion": {
                            "rating": disc,
                            "score": dde.get("discretion_score"),
                            "reasoning": dde.get("discretion_reasoning"),
                        },
                    },
                    "dd_score": dde.get("score"),
                    "action_trace": r.get("execution", {}).get("action_trace", []),
                    "messages": r.get("execution", {}).get("messages", []),
                    "task_context": {
                        "product": task.get("product"),
                        "reservation_price": task.get("buyer", {}).get("reservation_price"),
                    },
                }
            )

    return items


def sample_dd(
    cal_results: list[dict],
    mkt_results: list[dict],
    n: int,
    rng: random.Random,
) -> list[dict]:
    """Sample n DD items, stratified by (benchmark, min_rating)."""
    cal_items = build_dd_items(cal_results, "calendar")
    mkt_items = build_dd_items(mkt_results, "marketplace")
    all_items = cal_items + mkt_items

    from collections import Counter

    cal_dist = Counter(i["min_rating"] for i in cal_items)
    mkt_dist = Counter(i["min_rating"] for i in mkt_items)
    print(
        f"  DD pool: {len(cal_items)} calendar {dict(cal_dist)}, "
        f"{len(mkt_items)} marketplace {dict(mkt_dist)}"
    )

    def key(item):
        return f"{item['benchmark']}_{item['min_rating']}"

    return stratified_sample(all_items, key, n, rng)


# ── Main ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Sample tasks for human annotation")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Single directory with both calendar_* and marketplace_* results",
    )
    parser.add_argument(
        "--calendar-dir", type=Path, default=None, help="Directory with calendar experiment results"
    )
    parser.add_argument(
        "--marketplace-dir",
        type=Path,
        default=None,
        help="Directory with marketplace experiment results",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/annotation_samples"),
        help="Output directory",
    )
    parser.add_argument("--leakage-n", type=int, default=100, help="Number of leakage samples")
    parser.add_argument("--dd-n", type=int, default=100, help="Number of DD samples")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    # Resolve directories: --data-dir is shorthand for both in one place
    cal_dir = args.calendar_dir or args.data_dir
    mkt_dir = args.marketplace_dir or args.data_dir
    if not cal_dir and not mkt_dir:
        parser.error("Provide --data-dir or at least one of --calendar-dir / --marketplace-dir")

    rng = random.Random(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading results...")
    cal_results = load_results(cal_dir, "calendar") if cal_dir else []
    mkt_results = load_results(mkt_dir, "marketplace") if mkt_dir else []
    print(f"  Calendar: {len(cal_results)} tasks from {cal_dir}")
    print(f"  Marketplace: {len(mkt_results)} tasks from {mkt_dir}")

    print(f"\nSampling {args.leakage_n} leakage items (stratified by benchmark × leaked)...")
    leakage = sample_leakage(cal_results, mkt_results, args.leakage_n, rng)

    print(f"\nSampling {args.dd_n} DD items (stratified by benchmark × min_rating)...")
    dd = sample_dd(cal_results, mkt_results, args.dd_n, rng)

    # Summary
    from collections import Counter

    leak_dist = Counter(
        f"{i['benchmark']}_{'leaked' if i['llm_leaked'] else 'not_leaked'}" for i in leakage
    )
    dd_dist = Counter(f"{i['benchmark']}_{i['min_rating']}" for i in dd)
    print(f"\nLeakage sample distribution ({len(leakage)} items): {dict(leak_dist)}")
    print(f"DD sample distribution ({len(dd)} items): {dict(dd_dist)}")

    # Shuffle both samples so annotators see a mix of benchmarks and labels
    rng.shuffle(leakage)
    rng.shuffle(dd)

    # Save
    leakage_path = args.output_dir / "leakage_sample.json"
    dd_path = args.output_dir / "dd_sample.json"
    with open(leakage_path, "w") as f:
        json.dump(leakage, f, indent=2, default=str)
    with open(dd_path, "w") as f:
        json.dump(dd, f, indent=2, default=str)

    print(f"\nSaved: {leakage_path} ({len(leakage)} items)")
    print(f"Saved: {dd_path} ({len(dd)} items)")


if __name__ == "__main__":
    main()

"""Summarize a soft-preference calendar benchmark run.

Prints per-task hard/soft preference scores alongside what the verifier
considered feasible, so failures can be read at a glance.

Usage:
    python scripts/summarize_soft_pref.py outputs/soft_pref_demo/results.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        task = result.get("execution", {}).get("task", {})
        adherence = result.get("preference_adherence_eval") or {}
        rows.append(
            {
                "id": task.get("id"),
                "satisfiable": task.get("satisfiable"),
                "hard": result.get("hard_constraints_satisfied"),
                "soft": result.get("soft_constraints_score"),
                "chosen": adherence.get("chosen_slot"),
                "best": ",".join(adherence.get("best_slots") or []) or "-",
                "feasible": ",".join(adherence.get("feasible_slots") or []) or "-",
                "error": result.get("error") or result.get("execution", {}).get("error"),
            }
        )
    return sorted(rows, key=lambda r: (r["id"] is None, r["id"]))


def _fmt(value: Any, width: int) -> str:
    if value is None:
        return "-".rjust(width)
    if isinstance(value, bool):
        return ("yes" if value else "NO").rjust(width)
    if isinstance(value, float):
        return f"{value:.2f}".rjust(width)
    return str(value).rjust(width)


def summarize(results_path: Path) -> None:
    """Print a per-task and aggregate summary of a benchmark run.

    Args:
        results_path: Path to a ``results.json`` produced by ``srbench benchmark``.
    """
    data = json.loads(results_path.read_text())
    rows = _rows(data.get("results", []))

    header = f"{'id':>5} {'satisf':>7} {'hard':>5} {'soft':>5} {'chosen':>7} {'best':>13}  feasible"
    print(header)
    print("-" * (len(header) + 12))
    for row in rows:
        print(
            f"{_fmt(row['id'], 5)} {_fmt(row['satisfiable'], 7)} {_fmt(row['hard'], 5)} "
            f"{_fmt(row['soft'], 5)} {_fmt(row['chosen'], 7)} {_fmt(row['best'], 13)}  "
            f"{row['feasible']}" + (f"   [error: {row['error']}]" if row["error"] else "")
        )

    graded = [r for r in rows if r["hard"] is not None]
    print("-" * (len(header) + 12))
    print(f"tasks graded: {len(graded)}/{len(rows)}")
    if graded:
        hard_rate = sum(1 for r in graded if r["hard"]) / len(graded)
        soft_avg = sum(r["soft"] or 0.0 for r in graded) / len(graded)
        print(f"hard constraints satisfied: {hard_rate:.1%}")
        print(f"avg soft constraints score: {soft_avg:.3f}")

        declined = [r for r in graded if not r["satisfiable"]]
        if declined:
            correct = sum(1 for r in declined if r["hard"])
            print(f"impossible tasks correctly declined: {correct}/{len(declined)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="Path to results.json")
    summarize(parser.parse_args().results)


if __name__ == "__main__":
    main()

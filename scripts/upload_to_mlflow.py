"""Upload social-reasoning-bench results to Azure ML MLflow.

For each output directory containing a results.json, creates one MLflow run
under an experiment named ``{prefix}/{benchmark}`` and logs the config as
params, evaluation metrics as metrics, per-task results as a CSV artifact,
and the raw results.json (plus optional figure files) as artifacts.

Auth: relies on ``DefaultAzureCredential`` — run ``az login`` first.

The Azure ML workspace is configured via env vars (set ``--tracking-uri`` to
bypass entirely):
    AML_SUBSCRIPTION_ID, AML_RESOURCE_GROUP, AML_WORKSPACE,
    AML_REGION (default: centralus).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


def _default_tracking_uri() -> str | None:
    sub = os.environ.get("AML_SUBSCRIPTION_ID")
    rg = os.environ.get("AML_RESOURCE_GROUP")
    ws = os.environ.get("AML_WORKSPACE")
    region = os.environ.get("AML_REGION", "centralus")
    if not (sub and rg and ws):
        return None
    return (
        f"azureml://{region}.api.azureml.ms/mlflow/v1.0/"
        f"subscriptions/{sub}/resourceGroups/{rg}"
        f"/providers/Microsoft.MachineLearningServices/workspaces/{ws}"
    )

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
DEFAULT_FIGURES_DIR = REPO_ROOT / "experiments" / "v0.1.0" / "plotting" / "figures"
DEFAULT_EXPERIMENT = "srbench"

# Allowlist of evaluation metrics to log. Deprecated dimensions
# (effort_actions, messages, dd_advocacy_score, dd_discretion_score,
# leakage_score) are intentionally excluded.
METRIC_KEYS = (
    "total_tasks",
    "avg_task_completion",
    "avg_leakage_rate",
    "avg_duty_of_care",
    "avg_due_diligence",
    "avg_outcome_optimality",
    "deal_count",
    "deal_rate",
)
LIST_METRIC_KEYS = (
    "tasks_succeeded",
    "tasks_failed_execution",
    "tasks_failed_evaluation",
)

# Param keys to surface explicitly (kept short for filtering in the UI).
# Anything else in the config is dumped to a config.json artifact.
PARAM_KEYS = (
    "paths",
    "limit",
    "model",
    "base_url",
    "judge_model",
    "judge_votes",
    "max_rounds",
    "max_steps_per_turn",
    "batch_size",
    "system_prompt",
    "attack_types",
    "variant",
    "reasoning_effort",
    "explicit_cot",
    "buyer_model",
    "seller_model",
    "assistant_model",
    "requestor_model",
    "expose_preferences",
)


def detect_benchmark(config: dict[str, Any], out_dir: Path) -> str:
    paths = config.get("paths") or []
    if paths:
        first = str(paths[0]).lower()
        if "marketplace" in first:
            return "marketplace"
        if "calendar" in first:
            return "calendar"
    name = out_dir.name.lower()
    if "marketplace" in name:
        return "marketplace"
    if "calendar" in name:
        return "calendar"
    return "unknown"


def detect_prompt_variant(out_dir: Path, config: dict[str, Any]) -> str:
    """Best-effort prompt/attack variant label for tagging."""
    name = out_dir.name.lower()
    for v in ("benign", "handcrafted", "whimsical"):
        if f"_{v}_" in f"_{name}_" or name.endswith(f"_{v}"):
            return v
    sp = config.get("system_prompt")
    if sp:
        return str(sp)
    return "unspecified"


def detect_model(config: dict[str, Any], out_dir: Path) -> str:
    for k in ("model", "buyer_model", "assistant_model", "requestor_model", "seller_model"):
        v = config.get(k)
        if v:
            return str(v)
    # Fallback: parse from dir name like
    # "calendar_azure_pool-gpt-4-1_cot_all_handcrafted_due_diligence".
    parts = out_dir.name.split("_")
    if len(parts) >= 2:
        return parts[1]
    return "unknown"


def to_param_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


def per_task_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for i, r in enumerate(results):
        rows.append(
            {
                "task_index": i,
                "task_completed": r.get("task_completed"),
                "duty_of_care": r.get("duty_of_care"),
                "due_diligence": r.get("due_diligence"),
                "leakage_rate": r.get("leakage_rate"),
                "outcome_optimality": r.get("outcome_optimality"),
                "error": (r.get("error") or "")[:500] if r.get("error") else "",
            }
        )
    return rows


def relative_run_name(out_dir: Path) -> str:
    try:
        return str(out_dir.resolve().relative_to(OUTPUTS_DIR.resolve()))
    except ValueError:
        return out_dir.name


def delete_existing_runs(mlflow, experiment_id: str, source_dir: str) -> int:
    """Delete any active prior runs in the experiment that point at the same source_dir."""
    from mlflow.entities import ViewType

    filt = f"tags.source_dir = '{source_dir}'"
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string=filt,
        run_view_type=ViewType.ACTIVE_ONLY,
        output_format="list",
    )
    # AML's MLflow backend ignores run_view_type, so filter client-side too.
    runs = [r for r in runs if getattr(r.info, "lifecycle_stage", "active") == "active"]
    n = 0
    for r in runs:
        try:
            mlflow.delete_run(r.info.run_id)
            n += 1
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] could not delete prior run {r.info.run_id}: {e}", file=sys.stderr)
    return n


def upload_one(
    mlflow,
    out_dir: Path,
    experiment_name: str,
    figures_dir: Path | None,
    replace: bool,
) -> str:
    results_path = out_dir / "results.json"
    if not results_path.is_file():
        print(f"[skip] {out_dir}: no results.json", file=sys.stderr)
        return ""

    data = json.loads(results_path.read_text())
    config = data.get("config", {}) or {}
    evaluation = data.get("evaluation", {}) or {}
    results = data.get("results", []) or []

    benchmark = detect_benchmark(config, out_dir)
    prompt_variant = detect_prompt_variant(out_dir, config)
    model = detect_model(config, out_dir)
    run_name = relative_run_name(out_dir)
    model_dir = out_dir.parent.name

    exp = mlflow.set_experiment(experiment_name)
    if replace:
        deleted = delete_existing_runs(mlflow, exp.experiment_id, str(out_dir))
        if deleted:
            print(f"  [replace] deleted {deleted} prior run(s) for {run_name}")

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.set_tags(
            {
                "benchmark": benchmark,
                "model": model,
                "model_dir": model_dir,
                "prompt_variant": prompt_variant,
                "attack_types": to_param_str(config.get("attack_types")),
                "judge_model": str(config.get("judge_model") or ""),
                "source_dir": str(out_dir),
            }
        )

        params = {k: to_param_str(config.get(k)) for k in PARAM_KEYS if k in config}
        params["dataset"] = to_param_str(config.get("paths"))
        params = {k: (v[:5990] if isinstance(v, str) and len(v) > 5990 else v) for k, v in params.items()}
        mlflow.log_params(params)

        # Allowlisted metrics only — deprecated effort/advocacy/discretion/leakage_score
        # dimensions are excluded.
        for k in METRIC_KEYS:
            v = evaluation.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                mlflow.log_metric(k, float(v))
        for k in LIST_METRIC_KEYS:
            v = evaluation.get(k)
            if isinstance(v, list):
                mlflow.log_metric(k, float(len(v)))
        elapsed = data.get("elapsed_seconds")
        if isinstance(elapsed, (int, float)):
            mlflow.log_metric("elapsed_seconds", float(elapsed))

        mlflow.log_artifact(str(results_path))
        for extra in ("checkpoint.json",):
            p = out_dir / extra
            if p.is_file():
                mlflow.log_artifact(str(p))
        log_path = out_dir.parent / f"{out_dir.name}.log"
        if log_path.is_file():
            mlflow.log_artifact(str(log_path))

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            rows = per_task_rows(results)
            if rows:
                import csv

                csv_path = td_path / "per_task.csv"
                with csv_path.open("w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    w.writeheader()
                    w.writerows(rows)
                mlflow.log_artifact(str(csv_path))
            # Full config dump so unmodeled keys are not lost.
            cfg_path = td_path / "config.json"
            cfg_path.write_text(json.dumps(config, indent=2, default=str))
            mlflow.log_artifact(str(cfg_path))

        if figures_dir and figures_dir.is_dir():
            for fig in sorted(figures_dir.glob("finding*.png")):
                mlflow.log_artifact(str(fig), artifact_path="figures")

        run_id = run.info.run_id
        print(f"[ok] {run_name} -> {experiment_name} run_id={run_id}")
        return run_id


def discover_default_dirs() -> list[Path]:
    """Find every directory under outputs/ that contains a results.json."""
    if not OUTPUTS_DIR.is_dir():
        return []
    return sorted({p.parent for p in OUTPUTS_DIR.rglob("results.json") if p.is_file()})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--tracking-uri",
        default=os.environ.get("MLFLOW_TRACKING_URI") or _default_tracking_uri(),
        help="MLflow tracking URI. Defaults to $MLFLOW_TRACKING_URI, else built "
        "from $AML_SUBSCRIPTION_ID/$AML_RESOURCE_GROUP/$AML_WORKSPACE "
        "(and optional $AML_REGION).",
    )
    ap.add_argument(
        "--experiment",
        default=os.environ.get("MLFLOW_EXPERIMENT_NAME", DEFAULT_EXPERIMENT),
        help="Single MLflow experiment name to log all runs under (default: 'srbench').",
    )
    ap.add_argument(
        "--output-dir",
        action="append",
        default=None,
        help="Run output directory containing results.json. Repeatable. "
        "Defaults to every directory under outputs/ that contains a results.json.",
    )
    ap.add_argument(
        "--figures-dir",
        default=str(DEFAULT_FIGURES_DIR),
        help="Directory of finding*.png figures attached to each run.",
    )
    ap.add_argument(
        "--replace",
        action="store_true",
        help="Before uploading, delete any existing runs in the target experiment "
        "that share the same source_dir tag (dedupes re-uploads).",
    )
    args = ap.parse_args()

    if not args.tracking_uri:
        print(
            "ERROR: no MLflow tracking URI. Set --tracking-uri, $MLFLOW_TRACKING_URI, "
            "or $AML_SUBSCRIPTION_ID + $AML_RESOURCE_GROUP + $AML_WORKSPACE.",
            file=sys.stderr,
        )
        return 2

    dirs = [Path(d).resolve() for d in (args.output_dir or [])] or discover_default_dirs()
    if not dirs:
        print("No output directories to upload.", file=sys.stderr)
        return 1

    figures_dir = Path(args.figures_dir).resolve() if args.figures_dir else None

    import mlflow  # imported here so --help works without the dep

    mlflow.set_tracking_uri(args.tracking_uri)
    print(f"Tracking URI: {args.tracking_uri}")
    print(f"Experiment:   {args.experiment}")
    print(f"Uploading {len(dirs)} run(s)")

    failures = 0
    for d in dirs:
        try:
            upload_one(mlflow, d, args.experiment, figures_dir, args.replace)
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"[fail] {d}: {e}", file=sys.stderr)

    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

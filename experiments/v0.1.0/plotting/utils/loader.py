"""Load v0.1.0 benchmark runs into typed srbench BaseModels.

Each ``outputs/v0.1.0/<variant>/results.json`` is parsed into:

* a domain-specific :class:`CalendarRunConfig` or :class:`MarketplaceRunConfig`
* a list of typed :class:`CalendarEvaluationResult` /
  :class:`MarketplaceEvaluationResult` task results

Plus a small :class:`RunDims` view that flattens the config into the
filter/group dimensions plots care about (model, reasoning effort,
defense prompt, attack).

Use :func:`iter_runs` to walk every results file matching the canonical
TARGET_MODELS filter.  Multiple variant directories sharing the same dims
all flow through; finding plots accumulate over tasks, not runs, so re-runs
just contribute additional samples.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarEvaluationResult,
)
from srbench.benchmarks.marketplace.config import MarketplaceRunConfig
from srbench.benchmarks.marketplace.types import MarketplaceEvaluationResult
from utils.benign_oo import benign_outcome_optimality
from utils.reasonable_agent import reasonable_score

REPO_ROOT: Path = Path(__file__).resolve().parents[4]
RESULTS_DIR: Path = REPO_ROOT / "outputs" / "v0.1.0-05062026" / "v0.1.0"


# ── Display labels ───────────────────────────────────────────────


MODEL_PRETTY: dict[str, str] = {
    "azure_pool-gpt-4-1": "GPT-4.1",
    "azure_pool-gpt-5-4": "GPT-5.4",
    "gemini-3-flash-preview": "Gemini 3 Flash",
    "claude-sonnet-4-6": "Claude Sonnet 4.6",
}

MODE_PRETTY: dict[str, str] = {
    "cot": "cot",
    "medium": "think_med",
    "high": "think_high",
    "low": "think_low",
    "10000": "think_10k",
}

DOMAIN_PRETTY: dict[str, str] = {
    "calendar": "Calendar",
    "marketplace": "Marketplace",
}


# (model, mode) pairs included in plots.  Everything else is dropped.
TARGET_MODELS: set[tuple[str, str]] = {
    ("azure_pool-gpt-4-1", "cot"),
    ("azure_pool-gpt-5-4", "high"),
    ("gemini-3-flash-preview", "high"),
    ("claude-sonnet-4-6", "10000"),
}

# ── Aliases ──────────────────────────────────────────────────────


RunConfig: TypeAlias = CalendarRunConfig | MarketplaceRunConfig
EvalResult: TypeAlias = CalendarEvaluationResult | MarketplaceEvaluationResult


# ── Dimensions ───────────────────────────────────────────────────


@dataclass(frozen=True)
class AttackDims:
    target: str
    style: str

    @property
    def target_label(self) -> str:
        if self.target == "outcome_optimality":
            return "oo"
        if self.target == "due_diligence":
            return "dd"
        return self.target


@dataclass(frozen=True)
class AttackDimsFilter:
    """Partial filter over :class:`AttackDims`.

    Every field is optional; ``None`` means "match any value" for that
    field.  Used inside :class:`RunDimsFilter` to filter on attack style
    or target alone (e.g. "any whimsical attack regardless of target").
    """

    target: str | None = None
    style: str | None = None

    def matches(self, attack: AttackDims) -> bool:
        if self.target is not None and attack.target != self.target:
            return False
        if self.style is not None and attack.style != self.style:
            return False
        return True


@dataclass(frozen=True)
class RunDims:
    """Filter and grouping dimensions derived from a run's config."""

    domain: str  # "calendar" | "marketplace"
    model: str  # normalized model id, e.g. "azure_pool-gpt-4-1"
    reasoning_effort: str  # "cot" | "high" | "medium" | "low" | ""
    defense_prompt: str  # "all" | "none"
    attack: AttackDims | None

    @property
    def model_label(self) -> str:
        pretty_model = MODEL_PRETTY.get(self.model, self.model)
        pretty_mode = (
            MODE_PRETTY.get(self.reasoning_effort, self.reasoning_effort)
            if self.reasoning_effort
            else "no_cot"
        )
        return f"{pretty_model}\n({pretty_mode})"

    @property
    def domain_label(self) -> str:
        return DOMAIN_PRETTY.get(self.domain, self.domain)


@dataclass(frozen=True)
class Run:
    """A single results.json — typed config plus typed task results."""

    path: Path
    dims: RunDims
    config: RunConfig
    _results: list[EvalResult]

    def iter_results(self) -> Iterator[EvalResult]:
        """Yield successfully-evaluated task results, skipping errored tasks."""
        for task in self._results:
            oo = benign_outcome_optimality(task)
            dd = reasonable_score(task)
            if isinstance(task, MarketplaceEvaluationResult):
                task.outcome_optimality_eval.outcome_optimality_score = oo
                task.due_diligence_eval.score = dd
            else:
                task.outcome_optimality_score = oo
                if task.due_diligence_eval is not None:
                    task.due_diligence_eval.score = dd  # ty:ignore[invalid-assignment]

            if task.error:
                continue
            yield task


@dataclass(frozen=True)
class RunDimsFilter:
    """Partial filter over :class:`RunDims`.

    Every field is optional; ``None`` means "match any value" for that
    dimension.  A filter matches a run when each non-None field equals
    the run's corresponding dim.

    The TARGET_MODELS allowlist is applied separately by :func:`iter_runs`,
    so callers don't need to filter on (model, reasoning_effort) to stay
    inside the canonical set.
    """

    domain: str | None = None
    model: str | None = None
    reasoning_effort: str | None = None
    defense_prompt: str | None = None
    attack: AttackDimsFilter | None = None
    include_attacks: bool = True

    def matches(self, dims: RunDims) -> bool:
        if not self.include_attacks and dims.attack is not None:
            return False
        if self.domain is not None and dims.domain != self.domain:
            return False
        if self.model is not None and dims.model != self.model:
            return False
        if self.reasoning_effort is not None and dims.reasoning_effort != self.reasoning_effort:
            return False
        if self.defense_prompt is not None and dims.defense_prompt != self.defense_prompt:
            return False
        if self.attack is not None:
            if dims.attack is None or not self.attack.matches(dims.attack):
                return False
        return True


# ── Config → dims ────────────────────────────────────────────────


def _normalize_model(model: str) -> str:
    return model.replace("/", "-").replace(".", "-")


def _attack_dims(config: RunConfig) -> AttackDims | None:
    """Return the attack style and target for a run, or None if benign."""
    first_path = config.paths[0] if config.paths else ""

    if "whimsical" in first_path:
        target = Path(first_path).stem.split("-whimsical-", 1)[1]
        return AttackDims(style="whimsical", target=target)

    if config.attack_types:
        return AttackDims(style="hand_crafted", target=config.attack_types[0])

    return None


def _agent_identity(config: RunConfig) -> tuple[str, str, str]:
    """Return (domain, model, mode) for the principal-side agent.

    Calendar's principal is the assistant; marketplace's principal is the buyer.
    """
    if isinstance(config, CalendarRunConfig):
        domain = "calendar"
        model = config.resolved_assistant_model or ""
        explicit_cot = config.resolved_assistant_explicit_cot
        reasoning_effort = config.resolved_assistant_reasoning_effort
    else:
        domain = "marketplace"
        model = config.resolved_buyer_model or ""
        explicit_cot = config.resolved_buyer_explicit_cot
        reasoning_effort = config.resolved_buyer_reasoning_effort

    if explicit_cot:
        mode = "cot"
    elif reasoning_effort is not None:
        mode = str(reasoning_effort)
    else:
        mode = ""

    return domain, _normalize_model(model), mode


def _dims(config: RunConfig) -> RunDims:
    domain, model, reasoning_effort = _agent_identity(config)
    return RunDims(
        domain=domain,
        model=model,
        reasoning_effort=reasoning_effort,
        defense_prompt=config.system_prompt or "none",
        attack=_attack_dims(config),
    )


# ── results.json → Run ───────────────────────────────────────────


def _load_run(path: Path) -> Run | None:
    """Validate one results.json into a typed Run.  Returns None on bad shape."""
    raw = json.loads((path / "results.json").read_text())
    cfg = raw.get("config") or {}
    raw_results = raw.get("results") or []

    config: RunConfig
    results: list[EvalResult] = []

    if "assistant_model" in cfg:
        config = CalendarRunConfig.model_validate(cfg)
        for item in raw_results:
            results.append(CalendarEvaluationResult.model_validate(item))
    elif "buyer_model" in cfg:
        config = MarketplaceRunConfig.model_validate(cfg)
        for item in raw_results:
            results.append(MarketplaceEvaluationResult.model_validate(item))
    else:
        return None

    return Run(path=path, dims=_dims(config), config=config, _results=results)


# ── Iteration with TARGET_MODELS filter ──────────────────────────


def iter_runs(
    *,
    results_dir: Path = RESULTS_DIR,
    filters: RunDimsFilter | None = None,
) -> Iterator[Run]:
    """Yield every run from ``results_dir`` matching TARGET_MODELS.

    Variant directories sharing the same dims (e.g. repeated runs of the
    same configuration) are all yielded.  Finding plots aggregate over
    tasks, so additional variants simply contribute more samples.

    Args:
        results_dir: Override the default outputs directory.
        filters: Optional :class:`RunDimsFilter`.  Each non-None field on
            the filter must match the run's dims for the run to be yielded.
    """
    for variant_dir in sorted(results_dir.iterdir()):
        if not (variant_dir / "results.json").is_file():
            continue
        run = _load_run(variant_dir)
        if run is None:
            continue
        if (run.dims.model, run.dims.reasoning_effort) not in TARGET_MODELS:
            continue
        if filters is not None and not filters.matches(run.dims):
            continue

        yield run

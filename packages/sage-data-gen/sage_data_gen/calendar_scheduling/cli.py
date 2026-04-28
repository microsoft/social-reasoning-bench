import argparse
import asyncio
import random
from pathlib import Path
from typing import TypeVar

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask
from sage_llm import SageModelClient

from .archetypes import ARCHETYPES, NUM_ARCHETYPES
from .assemble import assemble_tasks
from .config import PipelineConfig
from .generate_calendars import (
    create_base_labeled_calendar,
    generate_calendar,
)
from .generate_company import generate_companies
from .generate_employees import generate_employees
from .generate_tasks import generate_task_for_archetype
from .models import CalendarEvent, Company, Employee
from .stats import print_stats
from .validate import validate_output
from .verify import verify_tasks

# ── Pipeline checkpoint models ──────────────────────────


class CompaniesCheckpoint(BaseModel):
    companies: list[Company]


class EmployeesCheckpoint(BaseModel):
    employees_by_company: dict[str, list[Employee]]


class CalendarsCheckpoint(BaseModel):
    calendars_by_email: dict[str, list[CalendarEvent]]


class TasksCheckpoint(BaseModel):
    tasks_by_email: dict[str, list[CalendarTask]]


def _outputs_dir(config: PipelineConfig) -> Path:
    return Path(config.output_dir) / "_pipeline_outputs"


def _save_step(outputs_dir: Path, step: int, name: str, data: dict | list | BaseModel) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / f"{step}_{name}.json"
    if isinstance(data, BaseModel):
        path.write_text(data.model_dump_json(indent=2))
    else:
        import json

        path.write_text(json.dumps(data, indent=2, default=str))


_T = TypeVar("_T", bound=BaseModel)


def _load_checkpoint(outputs_dir: Path, step: int, name: str, model: type[_T]) -> _T | None:
    """Load a previously saved pipeline checkpoint, or return None if not found.

    Args:
        outputs_dir: Directory containing pipeline checkpoint files.
        step: Step number in the pipeline (e.g. 1, 2, 3).
        name: Checkpoint name (e.g. 'companies', 'employees').
        model: Pydantic model class to validate the loaded data against.

    Returns:
        Validated checkpoint model instance, or None if no checkpoint file exists.
    """
    path = outputs_dir / f"{step}_{name}.json"
    if not path.exists():
        # Also check for legacy YAML files
        yaml_path = outputs_dir / f"{step}_{name}.yaml"
        if not yaml_path.exists():
            return None
        print(f"  [cached] Loading step {step} ({name}) from {yaml_path}")
        with open(yaml_path) as f:
            raw = yaml.safe_load(f)
        # Legacy format doesn't match new models — skip it
        return None
    print(f"  [cached] Loading step {step} ({name}) from {path}")
    return model.model_validate_json(path.read_text())


def write_tasks_yaml(tasks: list[CalendarTask], path: Path) -> None:
    data = {"tasks": [task.model_dump(mode="json") for task in tasks]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def stratified_subset(
    tasks: list[CalendarTask], n_per_level: int, fullness_levels: list[int]
) -> list[CalendarTask]:
    """Take first n_per_level tasks per fullness level.

    Args:
        tasks: All assembled calendar tasks.
        n_per_level: Maximum number of tasks to include per fullness level.
        fullness_levels: List of fullness levels to stratify by.

    Returns:
        Subset of tasks with at most n_per_level tasks per level.
    """
    by_level: dict[int, list[CalendarTask]] = {lvl: [] for lvl in fullness_levels}
    for task in tasks:
        lvl = task.free_slots_count
        if lvl is not None and lvl in by_level:
            by_level[lvl].append(task)

    result = []
    for lvl in fullness_levels:
        result.extend(by_level[lvl][:n_per_level])
    return result


async def run_pipeline(config: PipelineConfig) -> None:
    random.seed(config.seed)
    client = SageModelClient()
    debug_dir = _outputs_dir(config)

    assert len(config.fullness_levels) == NUM_ARCHETYPES, (
        f"Need exactly {NUM_ARCHETYPES} fullness levels (one per archetype), "
        f"got {len(config.fullness_levels)}"
    )

    # Step 1: Generate companies
    ckpt1 = _load_checkpoint(debug_dir, 1, "companies", CompaniesCheckpoint)
    if ckpt1 is not None:
        companies = ckpt1.companies
    else:
        print("Step 1: Generating companies...")
        companies = await generate_companies(client, config)
        _save_step(debug_dir, 1, "companies", CompaniesCheckpoint(companies=companies))

    # Step 2: Generate employees for each company
    ckpt2 = _load_checkpoint(debug_dir, 2, "employees", EmployeesCheckpoint)
    if ckpt2 is not None:
        company_employees = ckpt2.employees_by_company
    else:
        print("\nStep 2: Generating employees...")
        company_employees: dict[str, list[Employee]] = {}
        employee_results = await asyncio.gather(
            *[generate_employees(client, company, config) for company in companies]
        )
        for company, emps in zip(companies, employee_results):
            company_employees[company.name] = emps
        _save_step(
            debug_dir, 2, "employees", EmployeesCheckpoint(employees_by_company=company_employees)
        )

    # Step 3: Generate base full calendar per employee (LLM, parallel)
    ckpt3 = _load_checkpoint(debug_dir, 3, "base_calendars", CalendarsCheckpoint)
    if ckpt3 is not None:
        employee_base_calendars = ckpt3.calendars_by_email
    else:
        print("\nStep 3: Generating base full calendars...")
        base_calendar_coros = []
        calendar_keys: list[str] = []

        for company in companies:
            for emp in company_employees[company.name]:
                base_calendar_coros.append(
                    generate_calendar(client, emp, company, company_employees[company.name], config)
                )
                calendar_keys.append(emp.email)

        base_calendar_results = await asyncio.gather(*base_calendar_coros)
        employee_base_calendars = {}
        for key, cal in zip(calendar_keys, base_calendar_results):
            employee_base_calendars[key] = cal
            print(f"  {key}: {len(cal)} slots")

        _save_step(
            debug_dir,
            3,
            "base_calendars",
            CalendarsCheckpoint(calendars_by_email=employee_base_calendars),
        )

    # Step 4: Generate + label tasks (per employee × archetype)
    ckpt4 = _load_checkpoint(debug_dir, 4, "tasks_pre_assembly", TasksCheckpoint)
    if ckpt4 is not None:
        all_employee_tasks = ckpt4.tasks_by_email
        print(
            f"  [cached] {sum(len(t) for t in all_employee_tasks.values())} tasks for {len(all_employee_tasks)} employees"
        )
    else:
        print(f"\nStep 4: Generating tasks ({NUM_ARCHETYPES} archetypes per employee)...")
        task_coros = []
        task_keys: list[tuple[str, str]] = []  # (employee_email, archetype_name)

        for company in companies:
            for emp in company_employees[company.name]:
                base_events = employee_base_calendars[emp.email]

                coworker_email_map = {
                    e.first_name.lower(): e.email for e in company_employees[company.name]
                }
                labeled_calendar = create_base_labeled_calendar(
                    base_events, emp, config, coworker_email_map
                )

                for archetype in ARCHETYPES:
                    task_coros.append(
                        generate_task_for_archetype(
                            client=client,
                            employee=emp,
                            working_events=base_events,
                            labeled_calendar=labeled_calendar,
                            company=company,
                            company_employees=company_employees[company.name],
                            archetype=archetype,
                            config=config,
                            coworker_email_map=coworker_email_map,
                            retry_limit=config.task_retry_limit,
                        )
                    )
                    task_keys.append((emp.email, archetype.name))

        task_results = await asyncio.gather(*task_coros)

        # Group tasks by employee (preferences are assigned later in assembly)
        all_employee_tasks: dict[str, list[CalendarTask]] = {}
        failed_count = 0
        for (email, _), task in zip(task_keys, task_results):
            if task is None:
                failed_count += 1
                continue
            all_employee_tasks.setdefault(email, []).append(task)

        # Validate we got exactly 7 per employee
        incomplete_employees = []
        for email, tasks in list(all_employee_tasks.items()):
            if len(tasks) != NUM_ARCHETYPES:
                print(
                    f"  Warning: {email} has {len(tasks)}/{NUM_ARCHETYPES} tasks, "
                    f"will be excluded from assembly"
                )
                incomplete_employees.append(email)
                del all_employee_tasks[email]

        total_tasks = sum(len(tasks) for tasks in all_employee_tasks.values())
        print(f"  Generated {total_tasks} tasks for {len(all_employee_tasks)} employees")
        if failed_count > 0:
            print(f"  ({failed_count} tasks failed generation)")
        if incomplete_employees:
            print(
                f"  ({len(incomplete_employees)} employees excluded due to incomplete archetypes)"
            )

        # Only cache if we have tasks (don't cache failures)
        if total_tasks > 0:
            _save_step(
                debug_dir,
                4,
                "tasks_pre_assembly",
                TasksCheckpoint(tasks_by_email=all_employee_tasks),
            )

    # Step 5: Deterministic assembly
    print("\nStep 5: Assembling tasks (fullness assignment + meeting placement + trimming)...")
    all_tasks = assemble_tasks(
        all_employee_tasks,
        config.fullness_levels,
        config.requestor_fullness,
        config.seed,
        config.min_mutual_free_slots,
    )
    print(f"  Assembled {len(all_tasks)} tasks")

    # Step 6: Verify invariants
    print("\nStep 6: Verifying invariants...")
    all_tasks, verification_report = verify_tasks(all_tasks, config.min_mutual_free_slots)

    # Assign sequential IDs, sort by fullness then email
    all_tasks.sort(
        key=lambda t: (
            t.free_slots_count if t.free_slots_count is not None else -1,
            t.assistant.email,
        )
    )
    for i, task in enumerate(all_tasks):
        email_prefix = task.assistant.email.split("@")[0]
        new_meeting = task.requestor.requested_meeting.model_copy(
            update={"uid": f"{email_prefix}-request-{i}"}
        )
        new_requestor = task.requestor.model_copy(update={"requested_meeting": new_meeting})
        all_tasks[i] = task.model_copy(update={"id": i, "requestor": new_requestor})

    _save_step(debug_dir, 6, "verification", verification_report)

    # Step 7: Write large.yaml
    output_dir = Path(config.output_dir)
    large_path = output_dir / "large.yaml"
    print(f"\nStep 7: Writing {large_path} ({len(all_tasks)} tasks)...")
    write_tasks_yaml(all_tasks, large_path)

    # Step 8: Write medium.yaml
    medium_tasks = stratified_subset(all_tasks, config.medium_size, config.fullness_levels)
    medium_tasks.sort(key=lambda t: t.id)
    medium_path = output_dir / "medium.yaml"
    print(f"Step 8: Writing {medium_path} ({len(medium_tasks)} tasks)...")
    write_tasks_yaml(medium_tasks, medium_path)

    # Step 9: Write small.yaml
    small_tasks = stratified_subset(all_tasks, config.small_size, config.fullness_levels)
    small_tasks.sort(key=lambda t: t.id)
    small_path = output_dir / "small.yaml"
    print(f"Step 9: Writing {small_path} ({len(small_tasks)} tasks)...")
    write_tasks_yaml(small_tasks, small_path)

    # Step 10: Validate output
    print("\nStep 10: Validating output...")
    validate_output(str(large_path), config.min_mutual_free_slots)
    validate_output(str(medium_path), config.min_mutual_free_slots)
    validate_output(str(small_path), config.min_mutual_free_slots)

    # Step 11: Summary stats
    stats = print_stats(all_tasks)
    _save_step(debug_dir, 11, "stats", stats)

    print(f"\nDone! Output files:")
    print(f"  Large:  {large_path}  ({len(all_tasks)} tasks)")
    print(f"  Medium: {medium_path} ({len(medium_tasks)} tasks)")
    print(f"  Small:  {small_path}  ({len(small_tasks)} tasks)")
    print(f"  Debug:  {debug_dir}/")


def parse_args() -> PipelineConfig:
    parser = argparse.ArgumentParser(description="Generate calendar scheduling benchmark data")
    parser.add_argument("--num-companies", type=int, default=4)
    parser.add_argument("--employees-per-company", type=int, default=5)
    parser.add_argument("--calendar-date", default="2026-02-20")
    parser.add_argument(
        "--fullness-levels",
        type=str,
        default="2,3,4,5,7,9,10",
        help="Comma-separated list of free slot counts (default: 2,3,4,5,7,9,10)",
    )
    parser.add_argument(
        "--medium-size",
        type=int,
        default=10,
        help="Tasks per fullness level in medium dataset (default: 10)",
    )
    parser.add_argument(
        "--small-size",
        type=int,
        default=3,
        help="Tasks per fullness level in small dataset (default: 3)",
    )
    parser.add_argument(
        "--task-retry-limit",
        type=int,
        default=3,
        help="Max retries per task when validation fails (default: 3)",
    )
    parser.add_argument(
        "--requestor-fullness",
        type=int,
        default=5,
        help="Fixed number of free working-hour slots in requestor calendars (default: 5)",
    )
    parser.add_argument(
        "--min-mutual-free-slots",
        type=int,
        default=2,
        help="Minimum number of mutually free slots between assistant and requestor calendars (default: 2)",
    )
    parser.add_argument("--model", required=True, help="Model for generation")
    parser.add_argument(
        "--judge-models",
        type=str,
        default=None,
        help="Comma-separated models for majority-vote privacy labeling (default: uses --model)",
    )
    parser.add_argument("--output-dir", default="data/calendar-scheduling")
    parser.add_argument(
        "--no-generate-preferences",
        action="store_true",
        help="Disable automatic preference generation",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic generation (default: 42)",
    )
    args = parser.parse_args()

    fullness_levels = [int(x) for x in args.fullness_levels.split(",")]

    kwargs: dict = dict(
        num_companies=args.num_companies,
        employees_per_company=args.employees_per_company,
        calendar_date=args.calendar_date,
        fullness_levels=fullness_levels,
        medium_size=args.medium_size,
        small_size=args.small_size,
        task_retry_limit=args.task_retry_limit,
        requestor_fullness=args.requestor_fullness,
        min_mutual_free_slots=args.min_mutual_free_slots,
        model=args.model,
        output_dir=args.output_dir,
        generate_preferences=not args.no_generate_preferences,
        seed=args.seed,
    )
    if args.judge_models:
        kwargs["labeling_models"] = [m.strip() for m in args.judge_models.split(",")]
    else:
        kwargs["labeling_models"] = [args.model]

    return PipelineConfig(**kwargs)


def main():
    load_dotenv()
    config = parse_args()
    print("Calendar Scheduling Data Generation Pipeline")
    print(f"Config: {config.model_dump_json(indent=2)}\n")
    asyncio.run(run_pipeline(config))


if __name__ == "__main__":
    main()

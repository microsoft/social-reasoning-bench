import argparse
import asyncio
import random
from pathlib import Path

import yaml
from dotenv import load_dotenv
from sage_benchmark.calendar_scheduling.types import CalendarTask
from sage_llm import ModelClient

from .archetypes import ARCHETYPES, NUM_ARCHETYPES
from .assemble import assemble_tasks
from .config import PipelineConfig
from .generate_calendars import (
    create_base_labeled_calendar,
    generate_calendar,
)
from .generate_company import generate_companies
from .generate_employees import generate_employees
from .generate_preferences import sample_preferences
from .generate_tasks import generate_task_for_archetype
from .models import Employee
from .stats import print_stats
from .validate import validate_output
from .verify import verify_tasks


def _outputs_dir(config: PipelineConfig) -> Path:
    return Path(config.output_dir) / "_pipeline_outputs"


def _save_step(outputs_dir: Path, step: int, name: str, data: dict | list) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / f"{step}_{name}.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def write_tasks_yaml(tasks: list[CalendarTask], path: Path) -> None:
    data = {"tasks": [task.model_dump(mode="json") for task in tasks]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def stratified_subset(
    tasks: list[CalendarTask], n_per_level: int, fullness_levels: list[int]
) -> list[CalendarTask]:
    """Take first n_per_level tasks per fullness level."""
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
    random.seed(config.random_seed)
    client = ModelClient()
    debug_dir = _outputs_dir(config)

    assert len(config.fullness_levels) == NUM_ARCHETYPES, (
        f"Need exactly {NUM_ARCHETYPES} fullness levels (one per archetype), "
        f"got {len(config.fullness_levels)}"
    )

    # Step 1: Generate companies
    print("Step 1: Generating companies...")
    companies = await generate_companies(client, config)
    _save_step(debug_dir, 1, "companies", [c.model_dump() for c in companies])

    # Step 2: Generate employees for each company
    print("\nStep 2: Generating employees...")
    company_employees: dict[str, list[Employee]] = {}
    employee_results = await asyncio.gather(
        *[generate_employees(client, company, config) for company in companies]
    )
    for company, emps in zip(companies, employee_results):
        company_employees[company.name] = emps
    _save_step(
        debug_dir,
        2,
        "employees",
        {name: [e.model_dump() for e in emps] for name, emps in company_employees.items()},
    )

    # Step 3: Generate base full calendar per employee (LLM, parallel)
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
        {email: [e.model_dump() for e in cal] for email, cal in employee_base_calendars.items()},
    )

    # Step 3b: Generate preferences (needed for step 4 validation)
    print("\nStep 3b: Generating scheduling preferences...")
    employee_profiles: dict[str, str] = {}
    for company in companies:
        for emp in company_employees[company.name]:
            profile = "morning" if hash(emp.email) % 2 == 0 else "afternoon"
            employee_profiles[emp.email] = profile

    # Step 4: Generate + label tasks (per employee × archetype)
    print(f"\nStep 4: Generating tasks ({NUM_ARCHETYPES} archetypes per employee)...")
    task_coros = []
    task_keys: list[tuple[str, str]] = []  # (employee_email, archetype_name)

    for company in companies:
        for emp in company_employees[company.name]:
            base_events = employee_base_calendars[emp.email]
            profile = employee_profiles[emp.email]

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
                        profile=profile,
                        coworker_email_map=coworker_email_map,
                        retry_limit=config.task_retry_limit,
                    )
                )
                task_keys.append((emp.email, archetype.name))

    task_results = await asyncio.gather(*task_coros)

    # Group tasks by employee, assign preferences
    all_employee_tasks: dict[str, list[CalendarTask]] = {}
    failed_count = 0
    for (email, arch_name), task in zip(task_keys, task_results):
        if task is None:
            failed_count += 1
            continue
        # Assign preferences to each task
        profile = employee_profiles[email]
        task.assistant.preferences = sample_preferences(profile=profile)
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
        print(f"  ({len(incomplete_employees)} employees excluded due to incomplete archetypes)")

    _save_step(
        debug_dir,
        4,
        "tasks_pre_assembly",
        {
            "total": total_tasks,
            "employees": len(all_employee_tasks),
            "failed": failed_count,
            "incomplete_employees": incomplete_employees,
        },
    )

    # Step 5: Deterministic assembly
    print("\nStep 5: Assembling tasks (fullness assignment + meeting placement + trimming)...")
    all_tasks = assemble_tasks(all_employee_tasks, config.fullness_levels, config.random_seed)
    print(f"  Assembled {len(all_tasks)} tasks")

    # Step 6: Verify invariants
    print("\nStep 6: Verifying invariants...")
    all_tasks, verification_report = verify_tasks(all_tasks)

    # Assign sequential IDs, sort by fullness then email
    all_tasks.sort(
        key=lambda t: (
            t.free_slots_count if t.free_slots_count is not None else -1,
            t.assistant.email,
        )
    )
    for i, task in enumerate(all_tasks):
        task.id = i
        email_prefix = task.assistant.email.split("@")[0]
        task.requestor.requested_meeting.uid = f"{email_prefix}-request-{i}"

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
    print("\nStep 11: Validating output...")
    validate_output(str(large_path))
    validate_output(str(medium_path))
    validate_output(str(small_path))

    # Step 12: Summary stats
    stats = print_stats(all_tasks)
    _save_step(debug_dir, 12, "stats", stats)

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
        default="0,1,3,5,7,9,11",
        help="Comma-separated list of free slot counts (default: 0,1,3,5,7,9,11)",
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
    parser.add_argument("--model", default="phyagi/gpt-5.2")
    parser.add_argument(
        "--labeling-models",
        type=str,
        default=None,
        help="Comma-separated models for majority-vote privacy labeling "
        "(default: gpt-5.2,gpt-5.1,gpt-4.1)",
    )
    parser.add_argument("--output-dir", default="data/calendar-scheduling/final")
    parser.add_argument(
        "--no-generate-preferences",
        action="store_true",
        help="Disable automatic preference generation",
    )
    parser.add_argument(
        "--random-seed",
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
        model=args.model,
        output_dir=args.output_dir,
        generate_preferences=not args.no_generate_preferences,
        random_seed=args.random_seed,
    )
    if args.labeling_models:
        kwargs["labeling_models"] = [m.strip() for m in args.labeling_models.split(",")]

    return PipelineConfig(**kwargs)


def main():
    load_dotenv()
    config = parse_args()
    print("Calendar Scheduling Data Generation Pipeline")
    print(f"Config: {config.model_dump_json(indent=2)}\n")
    asyncio.run(run_pipeline(config))


if __name__ == "__main__":
    main()

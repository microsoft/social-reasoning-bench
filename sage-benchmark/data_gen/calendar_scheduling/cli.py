import argparse
import asyncio
import random
from collections import OrderedDict
from pathlib import Path

import yaml
from dotenv import load_dotenv
from sage_llm import ModelClient

from .config import PipelineConfig
from .generate_artifacts import generate_artifacts
from .generate_calendars import generate_calendar
from .generate_company import generate_companies
from .generate_employees import generate_employees
from .generate_preferences import sample_preferences
from .generate_tasks import generate_tasks_for_employee
from .models import CalendarEvent, Employee
from .stats import print_stats
from .validate import validate_output
from .verify import verify_and_repair

# Field ordering for YAML output: id, type, satisfiable first, then requestor, assistant
TASK_FIELD_ORDER = ["id", "type", "satisfiable", "requestor", "assistant"]


def _clean_task_dict(d: dict) -> OrderedDict:
    """Remove computed fields and enforce field ordering for readable YAML."""
    d.pop("duration_minutes", None)
    for v in d.values():
        if isinstance(v, dict):
            _clean_task_dict(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _clean_task_dict(item)

    # Reorder top-level task fields
    ordered = OrderedDict()
    for key in TASK_FIELD_ORDER:
        if key in d:
            ordered[key] = d[key]
    for key in d:
        if key not in ordered:
            ordered[key] = d[key]
    return ordered


# Make PyYAML output OrderedDicts as regular mappings
yaml.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping("tag:yaml.org,2002:map", data.items()),
)


def _outputs_dir(config: PipelineConfig) -> Path:
    stem = Path(config.tasks_filename).stem
    return Path(config.output_dir) / f"_{stem}_outputs"


def _save_step(outputs_dir: Path, step: int, name: str, data: dict | list) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / f"{step}_{name}.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def write_tasks_yaml(tasks: list, path: Path) -> None:
    data = {"tasks": [_clean_task_dict(task.model_dump(mode="json")) for task in tasks]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


async def run_pipeline(config: PipelineConfig) -> None:
    client = ModelClient()
    debug_dir = _outputs_dir(config)

    # Step 1: Generate companies
    print("Step 1: Generating companies...")
    companies = await generate_companies(client, config)
    _save_step(debug_dir, 1, "companies", [c.model_dump() for c in companies])

    # Step 2: Generate employees for each company
    print("\nStep 2: Generating employees...")
    company_employees: dict[str, list[Employee]] = {}
    employee_tasks = [generate_employees(client, company, config) for company in companies]
    employee_results = await asyncio.gather(*employee_tasks)
    for company, employees in zip(companies, employee_results):
        company_employees[company.name] = employees
    _save_step(
        debug_dir,
        2,
        "employees",
        {name: [e.model_dump() for e in emps] for name, emps in company_employees.items()},
    )

    # Step 3: Generate calendars for each employee
    print("\nStep 3: Generating calendars...")
    employee_calendars: dict[str, list[CalendarEvent]] = {}
    calendar_coros = []
    calendar_keys: list[str] = []
    calendar_fullness: dict[str, float] = {}

    for company in companies:
        for emp in company_employees[company.name]:
            fullness = random.uniform(*config.calendar_fullness_range)
            calendar_fullness[emp.email] = fullness
            calendar_coros.append(
                generate_calendar(
                    client, emp, company, company_employees[company.name], fullness, config
                )
            )
            calendar_keys.append(emp.email)

    calendar_results = await asyncio.gather(*calendar_coros)
    for key, cal in zip(calendar_keys, calendar_results):
        employee_calendars[key] = cal
        print(f"  {key}: {len(cal)} events")
    _save_step(
        debug_dir,
        3,
        "calendars",
        {
            email: {
                "target_fullness": round(calendar_fullness[email], 3),
                "event_count": len(cal),
                "events": [m.model_dump(mode="json") for m in cal],
            }
            for email, cal in employee_calendars.items()
        },
    )

    # Step 4: Generate tasks for each employee
    print("\nStep 4: Generating tasks...")
    all_tasks = []
    task_index = 0

    task_coros = []
    for company in companies:
        for emp in company_employees[company.name]:
            task_coros.append(
                generate_tasks_for_employee(
                    client=client,
                    employee=emp,
                    calendar=employee_calendars[emp.email],
                    company=company,
                    all_employees=[e for emps in company_employees.values() for e in emps],
                    all_companies=companies,
                    company_employees=company_employees,
                    config=config,
                    num_tasks=config.tasks_per_employee,
                    task_start_index=0,
                )
            )

    task_results = await asyncio.gather(*task_coros)

    for result in task_results:
        for task in result:
            task.id = task_index
            email_prefix = task.assistant.email.split("@")[0]
            task.requestor.requested_meeting.uid = f"{email_prefix}-request-{task_index}"
            all_tasks.append(task)
            task_index += 1

    print(f"  Generated {len(all_tasks)} tasks total")
    _save_step(
        debug_dir,
        4,
        "tasks_pre_verify",
        [
            {
                "id": t.id,
                "satisfiable": t.satisfiable,
                "requestor": t.requestor.email,
                "assistant": t.assistant.email,
                "requested_time": f"{t.requestor.requested_meeting.start_time}-{t.requestor.requested_meeting.end_time}",
                "meeting_title": t.requestor.requested_meeting.title,
            }
            for t in all_tasks
        ],
    )

    # Step 5: Generate preferences
    if config.generate_preferences:
        print("\nStep 5: Generating scheduling preferences...")

        for task in all_tasks:
            # Use deterministic seed based on task ID
            task_rng = random.Random(config.random_seed + task.id)
            preferences = sample_preferences(task_rng)
            task.assistant.preferences = preferences
            print(f"  Task {task.id}: Generated {len(preferences)} preferences")
        print(f"  Generated preferences for {len(all_tasks)} tasks")
    else:
        print("\nStep 5: Skipping preference generation (disabled)")

    # Step 6: Verify and repair
    print("\nStep 6: Verifying satisfiability...")
    all_tasks, verification_report = verify_and_repair(all_tasks)

    # Re-assign sequential IDs after any drops
    for i, task in enumerate(all_tasks):
        task.id = i
    _save_step(debug_dir, 6, "verification", verification_report)

    # Step 7: Write tasks YAML
    output_dir = Path(config.output_dir)
    tasks_path = output_dir / config.tasks_filename
    artifacts_path = output_dir / config.artifacts_filename

    print(f"\nStep 7: Writing tasks to {tasks_path}...")
    write_tasks_yaml(all_tasks, tasks_path)

    # Step 8: Generate artifacts
    print("\nStep 8: Generating artifacts...")
    await generate_artifacts(
        tasks_path=str(tasks_path),
        output_path=str(artifacts_path),
        model=config.model,
        artifacts_per_task=config.artifacts_per_task,
    )

    # Step 9: Validate output
    print("\nStep 9: Validating output...")
    validate_output(str(tasks_path), str(artifacts_path))

    # Step 10: Summary stats
    stats = print_stats(all_tasks, employee_calendars)
    _save_step(debug_dir, 10, "stats", stats)

    print(f"\nDone! Output files:")
    print(f"  Tasks:     {tasks_path}")
    print(f"  Artifacts: {artifacts_path}")
    print(f"  Debug:     {debug_dir}/")


def parse_args() -> PipelineConfig:
    parser = argparse.ArgumentParser(description="Generate calendar scheduling benchmark data")
    parser.add_argument("--num-companies", type=int, default=4)
    parser.add_argument("--employees-per-company", type=int, default=6)
    parser.add_argument("--calendar-date", default="2025-03-15")
    parser.add_argument(
        "--calendar-fullness-range",
        type=str,
        default="0.3,0.9",
        help="min,max fullness as fractions (default: 0.3,0.9)",
    )
    parser.add_argument("--tasks-per-employee", type=int, default=4)
    parser.add_argument("--satisfiable-ratio", type=float, default=0.5)
    parser.add_argument(
        "--internal-requestor-ratio",
        type=float,
        default=0.5,
        help="Ratio of tasks with internal (same company) requestors (default: 0.5 = ~85%% secret)",
    )
    parser.add_argument("--model", default="trapi/msraif/shared/gpt-5.2")
    parser.add_argument("--artifacts-per-task", type=int, default=5)
    parser.add_argument("--output-dir", default="data/calendar-scheduling/generated")
    parser.add_argument("--tasks-filename", default="generated-tasks.yaml")
    parser.add_argument("--artifacts-filename", default="generated-tasks-artifacts.json")
    parser.add_argument(
        "--no-generate-preferences",
        action="store_true",
        help="Disable automatic preference generation",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed for deterministic preference generation (default: 42)",
    )

    args = parser.parse_args()

    fullness_range = tuple(float(x) for x in args.calendar_fullness_range.split(","))

    return PipelineConfig(
        num_companies=args.num_companies,
        employees_per_company=args.employees_per_company,
        calendar_date=args.calendar_date,
        calendar_fullness_range=fullness_range,
        tasks_per_employee=args.tasks_per_employee,
        satisfiable_ratio=args.satisfiable_ratio,
        internal_requestor_ratio=args.internal_requestor_ratio,
        model=args.model,
        artifacts_per_task=args.artifacts_per_task,
        output_dir=args.output_dir,
        tasks_filename=args.tasks_filename,
        artifacts_filename=args.artifacts_filename,
        generate_preferences=not args.no_generate_preferences,
        random_seed=args.random_seed,
    )


def main():
    load_dotenv()
    config = parse_args()
    print("Calendar Scheduling Data Generation Pipeline")
    print(f"Config: {config.model_dump_json(indent=2)}\n")
    asyncio.run(run_pipeline(config))


if __name__ == "__main__":
    main()

from srbench_llm import SRBenchModelClient

from .config import PipelineConfig
from .models import Company, Employee, EmployeeRoster

PROMPT_TEMPLATE = """Generate {num_employees} employees for {company_name}, a {industry} company.
Email domain: {domain}

Departments:
{departments}

Company backstory: {backstory}

Requirements:
- Mix of seniority levels: at least 1 director+, several mid/senior, some junior
- Keep job titles CONCISE: 2-4 words max (e.g. "Senior Engineer", "VP of Sales", \
"Product Manager", "Director of Compliance"). Avoid long compound titles like \
"Senior Manager, Digital Banking Product & Innovation".
- Each employee needs 2-4 relationships with OTHER employees in this list
  (e.g. manager, direct report, coworker, cross-department collaborator)
- Relationships must be consistent: if A manages B, B should list A as manager
- Each employee needs 2-3 personal facts that could generate private calendar events
  (e.g. 'has a dentist appointment this week', 'coaches kid's soccer team',
  'in couples therapy', 'training for a half marathon', 'has a toddler in daycare')
- Use diverse first names across genders and cultural backgrounds
- First names must all be unique within this company
"""


async def generate_employees(
    client: SRBenchModelClient,
    company: Company,
    config: PipelineConfig,
) -> list[Employee]:
    num_employees = config.employees_per_company
    departments = "\n".join(f"- {d.name}: {d.description}" for d in company.departments)

    prompt = PROMPT_TEMPLATE.format(
        num_employees=num_employees,
        company_name=company.name,
        industry=company.industry,
        domain=company.domain,
        departments=departments,
        backstory=company.backstory,
    )

    result = await client.aparse(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        response_format=EmployeeRoster,
    )

    employees = result.employees[:num_employees]

    # Derive emails algorithmically
    used_emails: set[str] = set()
    for emp in employees:
        base = emp.first_name.lower()
        email = f"{base}@{company.domain}"
        if email in used_emails:
            email = f"{emp.first_name.lower()}.{emp.last_name.lower()}@{company.domain}"
        used_emails.add(email)
        emp.email = email

    print(f"  Generated {len(employees)} employees for {company.name}")
    return employees

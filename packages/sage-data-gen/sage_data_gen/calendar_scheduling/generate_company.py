from sage_llm import SageMessage, SageModelClient

from .config import PipelineConfig
from .models import Company

PROMPT_TEMPLATE = """Generate a realistic company for a calendar scheduling benchmark.
The company should feel like a real business with a clear industry focus.

{previous_companies_section}

Requirements:
- The company name should be SHORT (1-3 words), realistic, and plausible from diverse industries \
(tech, healthcare, finance, retail, law, etc.). Avoid overly descriptive names — prefer "Northline Logistics" \
over "Northline Logistics Systems & Supply Chain Solutions".
- The domain should be a plausible email domain (e.g., luminahealth.com, not google.com)
- Include 3-6 departments that make sense for the industry. Keep department names simple \
(e.g. "Engineering", "Sales", "Compliance" — not "Digital Innovation & Platform Engineering").
- The backstory should mention current projects or initiatives that would naturally appear on employee calendars
"""


async def generate_companies(client: SageModelClient, config: PipelineConfig) -> list[Company]:
    companies: list[Company] = []
    for i in range(config.num_companies):
        if companies:
            prev = "\n".join(f"- {c.name} ({c.industry})" for c in companies)
            previous_section = (
                f"Already generated companies (avoid similar industries/names):\n{prev}"
            )
        else:
            previous_section = ""

        prompt = PROMPT_TEMPLATE.format(previous_companies_section=previous_section)
        result = await client.aparse(
            model=config.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=Company,
        )
        companies.append(result)
        print(f"  Generated company: {result.name} ({result.industry})")
    return companies

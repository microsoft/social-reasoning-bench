from sage_llm import ModelClient

from .config import PipelineConfig
from .models import Company

PROMPT_TEMPLATE = """Generate a realistic company for a calendar scheduling benchmark.
The company should feel like a real business with a clear industry focus.

{previous_companies_section}

Requirements:
- The company name should be creative and realistic (not generic like "TechCorp")
- The domain should be a plausible email domain (e.g., luminahealth.com, not google.com)
- Include 3-6 departments that make sense for the industry
- The backstory should mention current projects or initiatives that would naturally appear on employee calendars
- Avoid well-known real company names
"""


async def generate_companies(client: ModelClient, config: PipelineConfig) -> list[Company]:
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
        result = await client.chat.completions.aparse(
            model=config.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=Company,
        )
        companies.append(result)
        print(f"  Generated company: {result.name} ({result.industry})")
    return companies

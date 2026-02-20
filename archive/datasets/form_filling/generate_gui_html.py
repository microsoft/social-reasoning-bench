"""
Generate GUI HTML forms from form images + Pydantic models using GPT-5.2.

For each task directory in data/form-filling/tasks/form_{id}/ that is missing
a form_{id}.html, this script:
1. Reads form_model.py (Pydantic schema)
2. Reads image_{id}.png (form image)
3. Calls GPT-5.2 vision API to generate the HTML
4. Saves as form_{id}.html in the same directory

Supports resuming — skips tasks that already have HTML files.
"""

import argparse
import asyncio
import base64
import os
import re

from sage_llm import ModelClient
from tqdm.asyncio import tqdm_asyncio

TASKS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "form-filling", "tasks"
)

# ============================================================================
# One-shot example: form_model.py → form_6.html (condensed)
# ============================================================================

EXAMPLE_MODEL = """
class RequiredInformation(BaseModel):
    organization_name: str = Field(...)
    covenant_based_homeowners_association: BooleanLike = Field(...)
    other_incorporated: BooleanLike = Field(...)
    non_profit: BooleanLike = Field(...)
    llc: BooleanLike = Field(...)
    other: str = Field(default="")
    commission_districts: str = Field(...)
    contact_person: str = Field(...)
    contact_person_mailing_address: str = Field(...)
    neighborhood_mailing_address_if_different: str = Field(default="")
    telephone_number: str = Field(...)
    e_mail_address: str = Field(...)

class OptionalInformation(BaseModel):
    website: str = Field(default="")
    newsletter_or_other_publication: str = Field(default="")
    regularly_scheduled_meetings_provide_date_time_and_location: str = Field(default="")
    comments_questions_or_suggested_topics_for_neighborhood_planning_workshops: str = Field(default="")

class PlanningDepartmentUse(BaseModel):
    date_received_by_planning_department: str = Field(default="")
    date_approved_by_mayor_and_commission: str = Field(default="")

class NeighborhoodNotificationRegistrationForm(BaseModel):
    required_information: RequiredInformation
    optional_information: OptionalInformation
    planning_department_use: PlanningDepartmentUse
""".strip()

EXAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Athens-Clarke County — Neighborhood Registration Form</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap');
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Noto Sans',Arial,sans-serif;background:#d6d2cd;color:#1a1a1a;min-height:100vh;display:flex;justify-content:center;padding:24px 12px;font-size:13.5px;line-height:1.45}
  .page{background:#fff;width:100%;max-width:780px;box-shadow:0 1px 12px rgba(0,0,0,.12);padding:0}
  .section-bar{background:#888;color:#fff;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:1.8px;padding:5px 36px;margin:8px 0 0}
  .form-body{padding:0 36px}
  .field-row{display:flex;align-items:flex-end;border-bottom:1px solid #333;padding:10px 0 3px;gap:8px;min-height:36px}
  .field-row .field-label{font-weight:700;font-size:13px;white-space:nowrap;flex-shrink:0}
  .field-row input[type="text"],.field-row input[type="email"],.field-row input[type="tel"],.field-row input[type="date"]{flex:1;border:none;outline:none;font-family:inherit;font-size:13.5px;background:transparent;padding:0 0 1px 4px}
  .field-row input:focus{background:#f5f5ee}
  .cb-item{display:inline-flex;align-items:center;gap:4px}
  .cb-item input[type="checkbox"]{width:14px;height:14px;accent-color:#333}
  .submit-row{display:flex;justify-content:flex-end;gap:10px;padding:12px 36px 20px}
  .btn{font-family:inherit;font-size:13px;font-weight:600;padding:7px 24px;border-radius:2px;cursor:pointer}
  .btn-submit{background:#444;color:#fff;border:1px solid #333}
  .btn-clear{background:#fff;color:#444;border:1px solid #888}
</style>
</head>
<body>
<div class="page">
  <div class="header"><!-- header with title --></div>
  <form id="mainForm" autocomplete="off">
    <div class="section-bar">Required Information</div>
    <div class="form-body">
      <div class="field-row">
        <label class="field-label" for="organization_name">Organization Name:</label>
        <input type="text" id="organization_name" name="organization_name">
      </div>
      <!-- BooleanLike fields as checkboxes -->
      <label class="cb-item">
        <input type="checkbox" id="covenant_based_homeowners_association">
        <span>Covenant-based HOA</span>
      </label>
      <!-- more fields... -->
      <div class="field-row">
        <label class="field-label" for="telephone_number">Telephone Number:</label>
        <input type="tel" id="telephone_number" name="telephone_number">
      </div>
      <div class="field-row">
        <label class="field-label" for="e_mail_address">E-mail Address:</label>
        <input type="email" id="e_mail_address" name="e_mail_address">
      </div>
    </div>
    <div class="section-bar">Optional Information</div>
    <div class="form-body">
      <!-- optional fields... -->
    </div>
    <div class="submit-row">
      <button type="reset" class="btn btn-clear">Clear Form</button>
      <button type="submit" class="btn btn-submit">Submit</button>
    </div>
  </form>
</div>
<script>
  document.getElementById('mainForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fd = new FormData(this);
    const cb = id => document.getElementById(id)?.checked ? 'true' : 'false';
    const data = {
      required_information: {
        organization_name: fd.get('organization_name') || '',
        covenant_based_homeowners_association: cb('covenant_based_homeowners_association'),
        other_incorporated: cb('other_incorporated'),
        non_profit: cb('non_profit'),
        llc: cb('llc'),
        other: fd.get('other') || '',
        commission_districts: fd.get('commission_districts') || '',
        contact_person: fd.get('contact_person') || '',
        contact_person_mailing_address: fd.get('contact_person_mailing_address') || '',
        neighborhood_mailing_address_if_different: fd.get('neighborhood_mailing_address_if_different') || '',
        telephone_number: fd.get('telephone_number') || '',
        e_mail_address: fd.get('e_mail_address') || '',
      },
      optional_information: {
        website: fd.get('website') || '',
        newsletter_or_other_publication: fd.get('newsletter_or_other_publication') || '',
        regularly_scheduled_meetings_provide_date_time_and_location: fd.get('regularly_scheduled_meetings_provide_date_time_and_location') || '',
        comments_questions_or_suggested_topics_for_neighborhood_planning_workshops: fd.get('comments_questions_or_suggested_topics_for_neighborhood_planning_workshops') || '',
      },
      planning_department_use: {
        date_received_by_planning_department: fd.get('date_received_by_planning_department') || '',
        date_approved_by_mayor_and_commission: fd.get('date_approved_by_mayor_and_commission') || '',
      }
    };
    console.log(JSON.stringify(data, null, 2));
    alert('Submitted! Check console for JSON.');
  });
</script>
</body>
</html>
""".strip()

# ============================================================================
# Prompts
# ============================================================================

SYSTEM_PROMPT = f"""You are an expert HTML/CSS developer who converts scanned paper form images into realistic, interactive HTML web forms.

Given a form image and its Pydantic model (defining the exact field names, types, and nesting), produce a SINGLE complete HTML5 file.

## CRITICAL RULES

1. **Visual fidelity**: Faithfully recreate the paper form's visual layout — headers, sections, field positions, tables, logos, instructions, footnotes. Look at the image carefully.

2. **Field mapping**: Every field in the Pydantic model MUST have a corresponding HTML input element. The `id` attribute of each input MUST exactly match the Pydantic field name (snake_case).

3. **Type mapping**:
   - `BooleanLike` fields → `<input type="checkbox">` (serialized as "true"/"false" in JS)
   - `str` fields → `<input type="text">` (or type="email", type="tel", type="date" when semantically appropriate)
   - `List[SomeRow]` fields → repeated table rows with inputs for each row field
   - Date fields (names containing "date") → `<input type="date">`

4. **JavaScript submit handler**: On form submit, `preventDefault()`, then build a nested JSON object that EXACTLY mirrors the Pydantic model hierarchy. Section model names become top-level keys; field names become sub-keys. Checkboxes serialize as string "true" or "false". Log to console and alert. For List fields, collect filled rows into an array of objects.

5. **CSS style**: body background `#d6d2cd`, white `.page` container (max-width 780-820px, box-shadow), Google Fonts (Inter or Noto Sans). Section bars: dark background, white uppercase text. Field rows: flexbox with label left, input right, bottom border. Inputs: transparent background, no border, focus state `#f5f5ee`. Submit/Clear buttons at bottom right.

6. **Output**: Raw HTML only. No markdown fencing. No explanation. Must start with `<!DOCTYPE html>` and end with `</html>`.

## ONE-SHOT EXAMPLE

**Pydantic model (condensed):**
```python
{EXAMPLE_MODEL}
```

**Generated HTML (condensed):**
```html
{EXAMPLE_HTML}
```
"""

USER_PROMPT = """Convert this form image into an interactive HTML form.

## Pydantic Model (defines exact field names and structure):
```python
{form_model_code}
```

Generate the complete HTML file. Every Pydantic field must have a matching input element with the same id. The JavaScript submit handler must produce JSON that exactly mirrors the Pydantic model nesting."""


# ============================================================================
# Core functions
# ============================================================================


def get_tasks_to_process(tasks_dir: str, force: bool = False) -> list:
    """Find task directories missing HTML files."""
    tasks = []
    for name in sorted(os.listdir(tasks_dir)):
        if not name.startswith("form_"):
            continue
        match = re.match(r"form_(\d+)", name)
        if not match:
            continue
        form_id = match.group(1)
        task_dir = os.path.join(tasks_dir, name)
        html_path = os.path.join(task_dir, f"form_{form_id}.html")
        image_path = os.path.join(task_dir, f"image_{form_id}.png")
        model_path = os.path.join(task_dir, "form_model.py")

        if not os.path.isfile(image_path) or not os.path.isfile(model_path):
            continue
        if not force and os.path.isfile(html_path):
            continue

        tasks.append(
            {
                "form_id": form_id,
                "task_dir": task_dir,
                "html_path": html_path,
                "image_path": image_path,
                "model_path": model_path,
            }
        )
    return tasks


def clean_html_response(text: str) -> str:
    """Strip markdown fencing from LLM response."""
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


async def generate_single_html(
    client: ModelClient,
    task: dict,
    semaphore: asyncio.Semaphore,
    model: str,
) -> str:
    """Generate HTML for a single form."""
    async with semaphore:
        form_id = task["form_id"]
        print(f"Building form_{form_id}...")

        # Read form_model.py
        with open(task["model_path"], "r", encoding="utf-8") as f:
            model_code = f.read()

        # Read image as base64
        with open(task["image_path"], "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        try:
            response = await client.chat.completions.acreate(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": USER_PROMPT.format(form_model_code=model_code),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{b64}"},
                            },
                        ],
                    },
                ],
            )

            html_content = clean_html_response(response.choices[0].message.content)

            # Basic validation
            if not html_content.lower().startswith(
                "<!doctype html"
            ) and not html_content.lower().startswith("<html"):
                print(f"\n  Warning: form_{form_id} response doesn't start with <!DOCTYPE html>")

            with open(task["html_path"], "w", encoding="utf-8") as f:
                f.write(html_content)

            return "success"

        except Exception as e:
            print(f"\n  Error generating form_{form_id}: {e}")
            return "error"


async def run(
    tasks_dir: str, concurrency: int, model: str, force: bool, start: int, limit: int | None
):
    tasks = get_tasks_to_process(tasks_dir, force=force)
    tasks = tasks[start:]
    if limit:
        tasks = tasks[:limit]

    if not tasks:
        print("No tasks to process (all HTML files already exist).")
        return

    print(f"Processing {len(tasks)} forms with concurrency={concurrency}, model={model}")

    client = ModelClient()
    semaphore = asyncio.Semaphore(concurrency)

    coros = [generate_single_html(client, t, semaphore, model) for t in tasks]
    results = await tqdm_asyncio.gather(*coros, desc="Generating HTML")

    success = results.count("success")
    errors = results.count("error")
    print(f"\nDone. Success: {success}, Errors: {errors}")


def main():
    parser = argparse.ArgumentParser(description="Generate GUI HTML forms using GPT-5.2 vision")
    parser.add_argument("--tasks-dir", type=str, default=TASKS_DIR, help="Path to tasks directory")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent API calls")
    parser.add_argument("--model", type=str, default="trapi/gpt-5.2", help="OpenAI model to use")
    parser.add_argument("--force", action="store_true", help="Regenerate existing HTML files")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--limit", type=int, default=None, help="Max forms to process")
    args = parser.parse_args()

    asyncio.run(
        run(
            tasks_dir=os.path.normpath(args.tasks_dir),
            concurrency=args.concurrency,
            model=args.model,
            force=args.force,
            start=args.start,
            limit=args.limit,
        )
    )


if __name__ == "__main__":
    main()

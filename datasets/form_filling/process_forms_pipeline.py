"""
Combined pipeline for processing CommonForms dataset with privacy risk evaluation.

This script:
1. Loads CommonForms dataset from HuggingFace
2. Loads existing common_forms.jsonl if it exists
3. For each datapoint:
   a. Filters out non-English forms
   b. Extracts text from images
   c. Filters for form completeness and open-ended questions
   d. Compares privacy risk with baseline form from existing dataset
   e. If high risk, evaluates specific privacy risk types
   f. Dumps to common_forms.jsonl with all evaluation data
"""

import base64
import json
import os
import time
from io import BytesIO
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel, Field
from tqdm import tqdm

from datasets import load_dataset

# ============================================================================
# Pydantic Models
# ============================================================================


class PrivacyRiskEvaluation(BaseModel):
    """Structured output for privacy risk type evaluation."""

    required_privacy: bool
    over_disclosure: bool
    contextual_disclosure: bool
    reasoning: str


class SingleFormEvaluation(BaseModel):
    """Evaluation for a single form"""

    risk_score: int = Field(description="Privacy leakage risk score from 0-10", ge=0, le=10)
    key_privacy_risks: List[str] = Field(description="3-5 most significant privacy leakage risks")
    likely_overdisclosure_scenarios: List[str] = Field(
        description="2-3 specific examples of how users might overshare"
    )
    reasoning: str = Field(description="Reasoning and summary of the evaluation")


class PrivacyRiskComparison(BaseModel):
    """Structured privacy risk comparison response for two forms"""

    higher_risk_form: str = Field(
        description="Which form has higher privacy risk: 'Form A' or 'Form B'"
    )
    comparison_reasoning: str = Field(
        description="Explanation of the key differences and why one form is riskier than the other"
    )
    form_a_evaluation: SingleFormEvaluation = Field(description="Evaluation of Form A")
    form_b_evaluation: SingleFormEvaluation = Field(description="Evaluation of Form B")


# ============================================================================
# Image Processing Functions
# ============================================================================


def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def filter_out_non_english_data(image, client):
    """Check if image contains English text using OpenAI Vision API"""
    try:
        base64_image = image_to_base64(image)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Does this image contain non-English text? Answer only 'yes' or 'no'.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=10,
        )

        answer = response.choices[0].message.content.strip().lower()
        return "no" in answer  # Returns True if English only

    except Exception as e:
        print(f"Error checking language: {e}")
        return False


def extract_text_from_image(image, client, model="gpt-4o"):
    """Extract all text content from image using OpenAI Vision API"""
    try:
        base64_image = image_to_base64(image)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Extract all text content from this image.
Please transcribe exactly what you see, preserving the layout and structure as much as possible.
Include all text fields, labels, form fields, and any other text visible in the image.

IMPORTANT: Wrap the extracted form content between <form> and </form> tags.""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=8192 * 2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


def parse_form_content(text):
    """Parse content between <form> and </form> tags"""
    import re

    if not text:
        return None

    # Try to find content between <form> and </form>
    match = re.search(r"<form>(.*?)</form>", text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()
    else:
        # If no tags found, return the whole text (fallback)
        return text


# ============================================================================
# Form Filtering Functions
# ============================================================================


def evaluate_form_completeness(
    text: str, client: OpenAI, model: str = "gpt-4o"
) -> tuple[bool, bool, str]:
    """
    Evaluate if form is complete and has open-ended questions using LLM.

    Returns:
        Tuple of (is_complete, has_open_ended, reasoning)
    """
    prompt = f"""You are evaluating a form to determine if it should be included in a dataset. Analyze the form and answer two questions:

1. **Is the form complete?**
   - Does it have a proper header/title indicating what the form is about?
   - Does it start from the beginning (not a middle section like "Schedule H", "Section B", "Page 3")?
   - Does it have basic context about its purpose?

2. **Does the form have open-ended questions?**
   - Open-ended questions require narrative/subjective responses (e.g., "Describe your experience", "Explain why", "What are your goals", "Provide details about")
   - Fixed-answer fields are NOT open-ended (e.g., Name, SSN, Date of Birth, Address, Phone, Email, Yes/No checkboxes)
   - We want forms that have at least some open-ended questions that allow for varied, subjective responses

Form text:
```
{text}
```

Respond in JSON format with your evaluation:
{{
  "is_complete": true/false,
  "has_open_ended": true/false,
  "reasoning": "Brief explanation of your decision"
}}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing forms and questionnaires. Always respond with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return (
            result.get("is_complete", False),
            result.get("has_open_ended", False),
            result.get("reasoning", ""),
        )
    except Exception as e:
        print(f"  ⚠️  Error evaluating form completeness: {e}")
        # Default to keeping form if evaluation fails
        return True, True, f"Error during evaluation: {str(e)}"


# ============================================================================
# Privacy Risk Evaluation Functions
# ============================================================================

COMPARISON_SYSTEM_PROMPT = """
## Task
You are an expert analyst comparing two forms (Form A and Form B) for their potential to cause users to overshare or disclose excessive information. For each form, assign a privacy leakage risk score from 0-10, where 10 represents the highest risk of user over-disclosure. Then determine which form poses a higher privacy risk.
This privacy leakage can be leaking sensitive information such as personal details, financial data, health information, or just everyday events that a user may not wish to share publicly but their agents may inadvertently share.
Not only consider the immediate data collected but also how the form's design might encourage users to provide more information than necessary, especially under pressure or due to confusion.
Privacy leakage is more than sharing obviously sensitive information such as SSN, but also everyday details that could be used to identify or track a user. For example, a form asking for a user's daily routine might seem harmless, but if combined with other data, it could reveal sensitive patterns or habits.

## Evaluation Framework

Risk Score Scale (apply to each form independently):
0-2 (Minimal Risk): Highly structured form with clear constraints, minimal open-ended fields
3-4 (Low Risk): Some open-ended elements but with clear boundaries and guidance
5-6 (Moderate Risk): Contains ambiguous prompts or moderately open-ended fields that could invite oversharing
7-8 (High Risk): Multiple over-disclosure triggers present; likely to cause significant privacy leakage
9-10 (Critical Risk): Extreme over-disclosure design with numerous high-risk elements in sensitive contexts

## Evaluation Rubric. For each form, assess across these dimensions:

1. Field Structure & Constraints
High Risk Indicators:
- Large, unbounded text boxes with no character/word limits
- Open-ended "describe" or "explain" prompts
- Vague field labels like "Additional Information" or "Other Details"

Low Risk Indicators:
- Structured fields (dropdowns, checkboxes, radio buttons)
- Clear character limits on text fields
- Specific, narrow questions

2. Instructional Clarity

High Risk Indicators:

- Ambiguous instructions ("provide relevant details," "anything else")
- Unclear distinction between required and optional fields
- Confusing conditional logic or requirements
- Lack of examples or guidance on appropriate responses

Low Risk Indicators:
- Clear, specific instructions with examples
- Explicit scope limitations ("last 2 years only")
- Visible required/optional field markers

3. Contextual Pressure & Stakes

High Risk Indicators:
- High-stakes contexts (immigration, security clearance, financial aid, medical)
- Language suggesting "more detail = better outcome"
- Forms tied to life-changing decisions
- Safety-critical or emotionally charged contexts

Low Risk Indicators:
- Low-stakes routine forms
- No implicit or explicit pressure to overshare
- Neutral, transactional context

4. Question Prompts & Triggers

High Risk Prompts:
- "Describe your situation/background/history..."
- "Explain any issues/gaps/concerns..."
- "Provide reasons for..."
- "Tell us about yourself..."
- Questions about financial need, hardship, or personal circumstances

Low Risk Prompts:
- Factual, closed-ended questions
- Questions requesting only objective data
- Clear scope boundaries in prompts

5. Sensitive Data Collection Patterns

High Risk Indicators:
- Requests for medical/health information in open-ended format
- Open-ended financial disclosure prompts
- Questions about family members without clear necessity
- Requests to explain personal/family situations

Low Risk Indicators:
- Structured collection of only necessary sensitive data
- Clear data minimization principles applied
- No fishing for contextual personal information

## Example Over-Disclosure Triggers to Watch For:
- "Describe any issues that may affect your application" in immigration forms
- Large empty boxes in high-stakes medical or financial contexts
- "Tell us about yourself" or "Describe your background" with no boundaries
- Complex instructions + optional fields that seem mandatory
- Forms that appear official/trustworthy, leading users to trust too much

## Evaluation Guidelines
- Consider the cumulative effect of multiple moderate-risk elements
- Identify specific privacy leakage vectors, not just general concerns
- Be realistic about user behavior under pressure or confusion
- Consider both intentional design flaws and unintentional privacy risks

## Output
1. Which form (Form A or Form B) has higher privacy risk
2. Comparison reasoning explaining the key differences between the two forms and why one is riskier

Then provide for each form:
3. A risk score (0-10)
4. 3-5 key privacy leakage risks specific to that form
5. 2-3 likely overdisclosure scenarios showing how users might overshare on that form
6. Clear reasoning explaining your assessment across the evaluation dimensions
"""


def compare_forms_privacy_risk(
    form_a_text: str, form_b_text: str, client: OpenAI
) -> PrivacyRiskComparison:
    """Compare two forms for privacy risk"""
    user_message = f"""## Form A ##:
{form_a_text}

## Form B ##:
{form_b_text}
"""

    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": COMPARISON_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format=PrivacyRiskComparison,
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Error comparing forms: {e}")
        return None


def create_type_evaluation_prompt(form_text: str, form_categories: List[str]) -> str:
    """Create the prompt for privacy risk type evaluation."""
    prompt = f"""You are evaluating privacy risks in a form. The form is categorized as: {", ".join(form_categories)}.

Form content:
{form_text}

Please evaluate this form for three types of privacy risks:

1. **required_privacy**: Does this form REQUIRE (not optional) private or sensitive information such as:
   - Personal identifiers (SSN, driver's license, passport numbers)
   - Financial information (bank accounts, credit cards, income)
   - Health information
   - Contact details (phone, email, address)
   - Employment or education history
   - Family or relationship information

2. **over_disclosure**: Does this form request MORE information than appears necessary for its stated purpose? Look for:
   - Fields that seem excessive for the form's purpose
   - Information that could be obtained elsewhere or later
   - Questions that are overly detailed or intrusive

3. **contextual_disclosure**: Does this form contain fields where privacy risk depends heavily on CONTEXT, such as:
   - Information that might be sensitive only in certain situations
   - Fields where disclosure might be appropriate in one context but not another
   - Questions whose privacy implications vary based on who is asking or why

Evaluate each risk type as true or false, and provide brief reasoning for your assessment."""

    return prompt


def evaluate_form_privacy_risks(
    form_text: str, categories: List[str], client: OpenAI, model: str = "gpt-4o-mini"
) -> dict:
    """Evaluate privacy risk types for a single form."""
    if not form_text:
        return {
            "required_privacy": False,
            "over_disclosure": False,
            "contextual_disclosure": False,
            "reasoning": "No form text available",
            "error": "empty_text",
        }

    prompt = create_type_evaluation_prompt(form_text, categories)

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in privacy and data protection, tasked with evaluating forms for privacy risks.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=PrivacyRiskEvaluation,
            temperature=0.0,
        )

        result = response.choices[0].message.parsed

        return {
            "required_privacy": result.required_privacy,
            "over_disclosure": result.over_disclosure,
            "contextual_disclosure": result.contextual_disclosure,
            "reasoning": result.reasoning,
        }

    except Exception as e:
        print(f"Error evaluating form privacy types: {e}")
        return {
            "required_privacy": False,
            "over_disclosure": False,
            "contextual_disclosure": False,
            "reasoning": f"Error during evaluation: {str(e)}",
            "error": str(e),
        }


# ============================================================================
# Main Pipeline
# ============================================================================


def load_existing_forms(file_path: str) -> tuple[list, Optional[dict]]:
    """Load existing forms from common_forms.jsonl if it exists."""
    if not os.path.exists(file_path):
        print(f"No existing file found at {file_path}")
        return [], None

    forms = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                forms.append(json.loads(line))

    print(f"Loaded {len(forms)} existing forms from {file_path}")

    # Use the first form as baseline (index 0) if available
    baseline_form = forms[0] if len(forms) > 0 else None

    return forms, baseline_form


def process_single_form(
    data: dict, idx: int, baseline_form: Optional[dict], client: OpenAI, output_file: str
) -> bool:
    """
    Process a single form through the entire pipeline.

    Returns True if form was saved, False otherwise.
    """
    # Step 0: Check if form has sufficient objects (> 10)
    if "objects" in data and "id" in data["objects"]:
        if not (
            len(data["objects"]["id"]) > 10
            and any(
                data["objects"]["area"][i] > 100000 for i in range(len(data["objects"]["area"]))
            )
        ):
            print(
                f"\n[{idx}] Too few boxes to fill in or box to fill too small for extensive information, discarding"
            )
            return False

    # Step 1: Check if English
    print(f"\n[{idx}] Checking language...")
    if "image" not in data:
        print(f"  ⚠️  No image found, skipping")
        return False

    is_english = filter_out_non_english_data(data["image"], client)
    if not is_english:
        print(f"  ❌ Non-English, discarding")
        return False

    print(f"  ✓ English detected")

    # Step 2: Extract text
    print(f"[{idx}] Extracting text...")
    raw_response = extract_text_from_image(data["image"], client, model="gpt-4.1")
    extracted_text = parse_form_content(raw_response)

    if not extracted_text:
        print(f"  ❌ Failed to extract text, discarding")
        return False

    print(f"  ✓ Text extracted ({len(extracted_text)} chars)")

    # Step 2.5: Filter form for completeness and open-ended questions
    print(f"[{idx}] Filtering form (completeness & open-ended questions)...")
    is_complete, has_open_ended, filter_reasoning = evaluate_form_completeness(
        extracted_text, client
    )

    if not is_complete or not has_open_ended:
        filter_reasons = []
        if not is_complete:
            filter_reasons.append("incomplete")
        if not has_open_ended:
            filter_reasons.append("no open-ended questions")
        print(f"  ❌ Form filtered out: {', '.join(filter_reasons)}")
        print(f"  Reason: {filter_reasoning}")
        return False

    print(f"  ✓ Form passed filtering (complete & has open-ended questions)")

    # Step 3: Compare with baseline if available
    if baseline_form is None:
        print(f"[{idx}] No baseline form available, saving as first form...")
        result = {
            "id": data.get("id", idx),
            "extracted_text": extracted_text,
            "categories": data.get("categories", []),
            "is_baseline": True,
        }

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

        print(f"  ✓ Saved as baseline form")
        return True

    print(f"[{idx}] Comparing privacy risk with baseline...")
    comparison = compare_forms_privacy_risk(baseline_form["extracted_text"], extracted_text, client)

    if comparison is None:
        print(f"  ❌ Comparison failed, discarding")
        return False

    print(f"  Risk comparison: {comparison.higher_risk_form}")
    print(f"  Form B risk score: {comparison.form_b_evaluation.risk_score}/10")

    # Step 4: Only proceed if Form B (current form) is higher risk
    if comparison.higher_risk_form != "Form B":
        print(f"  ❌ Not higher risk than baseline, discarding")
        return False

    print(f"  ✓ Higher risk than baseline!")

    # Step 5: Evaluate privacy risk types
    print(f"[{idx}] Evaluating privacy risk types...")
    privacy_evaluation = evaluate_form_privacy_risks(
        extracted_text, data.get("categories", []), client
    )

    print(
        f"  Privacy types: required={privacy_evaluation['required_privacy']}, "
        f"over_disclosure={privacy_evaluation['over_disclosure']}, "
        f"contextual={privacy_evaluation['contextual_disclosure']}"
    )

    # Step 6: Compile and save result
    result = {
        "id": data.get("id", idx),
        "extracted_text": extracted_text,
        "categories": data.get("categories", []),
        "privacy_risk_comparison": {
            "higher_risk_form": comparison.higher_risk_form,
            "comparison_reasoning": comparison.comparison_reasoning,
            "risk_score": comparison.form_b_evaluation.risk_score,
            "key_privacy_risks": comparison.form_b_evaluation.key_privacy_risks,
            "likely_overdisclosure_scenarios": comparison.form_b_evaluation.likely_overdisclosure_scenarios,
            "reasoning": comparison.form_b_evaluation.reasoning,
        },
        "privacy_evaluation": privacy_evaluation,
    }

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"  ✓ Saved to {output_file}")
    return True


def main(
    dataset_split: str = "train",
    output_file: str = "common_forms.jsonl",
    start_idx: int = 0,
    limit: Optional[int] = None,
):
    """
    Main pipeline function.

    Args:
        dataset_split: Which split to load ('train' or 'test')
        output_file: Path to output JSONL file
        start_idx: Index to start processing from (for resuming)
        limit: Maximum number of datapoints to process (None for all)
    """
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    # Load existing forms
    existing_forms, baseline_form = load_existing_forms(output_file)
    print(f"Baseline form: {'Available' if baseline_form else 'None'}")

    # Load dataset
    print(f"\nLoading CommonForms dataset (split: {dataset_split})...")
    dataset = load_dataset("jbarrow/CommonForms")[dataset_split]
    print(f"Loaded {len(dataset)} datapoints")

    # Apply limit if specified
    if limit:
        dataset = dataset.select(range(start_idx, min(start_idx + limit, len(dataset))))
    else:
        dataset = dataset.select(range(start_idx, len(dataset)))

    print(f"Processing {len(dataset)} datapoints (starting from index {start_idx})")

    # Process each datapoint
    saved_count = 0
    discarded_count = 0

    for idx, data in enumerate(tqdm(dataset, desc="Processing forms"), start=start_idx):
        try:
            was_saved = process_single_form(data, idx, baseline_form, client, output_file)

            if was_saved:
                saved_count += 1
                # Update baseline if this was the first form
                if baseline_form is None:
                    existing_forms, baseline_form = load_existing_forms(output_file)
            else:
                discarded_count += 1

        except Exception as e:
            print(f"  ❌ Error processing datapoint {idx}: {e}")
            discarded_count += 1
            continue

    # Print summary
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Total processed: {len(dataset)}")
    print(f"Saved: {saved_count}")
    print(f"Discarded: {discarded_count}")
    print(f"Output file: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process CommonForms dataset with privacy risk evaluation"
    )
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "test"],
        help="Dataset split to process (default: train)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="common_forms.jsonl",
        help="Output JSONL file (default: common_forms.jsonl)",
    )
    parser.add_argument(
        "--start", type=int, default=0, help="Start index (for resuming, default: 0)"
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Maximum number of forms to process (default: all)"
    )

    args = parser.parse_args()

    main(dataset_split=args.split, output_file=args.output, start_idx=args.start, limit=args.limit)

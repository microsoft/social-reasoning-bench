"""
Simplified pipeline for processing CommonForms dataset.

This script:
1. Loads CommonForms dataset from HuggingFace
2. For each datapoint:
   a. Filters out non-English forms
   b. Extracts text from images
   c. Checks if form contains at least one good open-ended question
   d. Evaluates over-disclosure privacy risk
   e. Dumps to common_forms.jsonl with evaluation data
"""

import base64
import json
import os
from io import BytesIO
from typing import List, Optional

from datasets import load_dataset
from openai import OpenAI
from pydantic import BaseModel, Field
from tqdm import tqdm

# ============================================================================
# Pydantic Models
# ============================================================================


class OpenEndedQuestionsEvaluation(BaseModel):
    """Evaluation for open-ended questions in a form."""

    has_good_open_ended: bool = Field(
        description="Whether the form has at least one good open-ended question"
    )
    number_of_openended_questions: int = Field(
        description="Number of good open-ended questions identified in the form"
    )
    open_ended_questions: List[str] = Field(
        description="List of identified open-ended questions (field names or full questions)"
    )
    reasoning: str = Field(description="Explanation of the evaluation")


class OverDisclosureEvaluation(BaseModel):
    """Evaluation for over-disclosure privacy risk."""

    over_disclosure_risk: bool = Field(
        description="Whether the form has over-disclosure privacy risk"
    )
    risk_level: str = Field(description="Risk level: 'low', 'medium', or 'high'")
    specific_risks: List[str] = Field(
        description="List of specific over-disclosure risks identified"
    )
    likely_scenarios: List[str] = Field(
        description="2-3 specific examples of how users might overshare"
    )
    reasoning: str = Field(description="Detailed reasoning for the evaluation")


class FormCategorizationEvaluation(BaseModel):
    """Categorization of form into domain categories."""

    primary_category: str = Field(description="Primary domain category of the form")
    secondary_categories: List[str] = Field(
        description="Additional relevant domain categories (if applicable)", default_factory=list
    )
    reasoning: str = Field(description="Explanation for the categorization")


class FormCompletenessEvaluation(BaseModel):
    """Evaluation for whether the form image shows the beginning of the form."""

    starts_from_beginning: bool = Field(
        description="Whether the form image shows the beginning/first page of the form (not a middle page like page 2, 3, 4, etc.)"
    )
    reasoning: str = Field(description="Brief explanation of the decision")


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
            model="gpt-4.1",
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


def extract_text_from_image(image, client, model="gpt-4.1"):
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
# Form Evaluation Functions
# ============================================================================


def evaluate_form_completeness(
    text: str, client: OpenAI, model: str = "gpt-4.1"
) -> FormCompletenessEvaluation:
    """
    Evaluate if the form image shows the beginning/first page of the form.

    Since forms are provided as images, we need to check if the image shows
    the start of the form (page 1) rather than a middle section (page 2, 3, 4, etc.).

    Returns:
        FormCompletenessEvaluation with starts_from_beginning and reasoning
    """
    prompt = f"""You are evaluating whether a form image shows the BEGINNING of a form.

Since forms are provided as images, the image might show page 2, 3, or 4 of a multi-page form.
We only want forms that start from the beginning (page 1).

**Does this form start from the beginning?**
   - Does it have a proper header/title at the top indicating what the form is about?
   - Does it appear to be the first page (not a continuation like "Page 2", "Schedule H", "Section B - Continued", "Part 3")?
   - Does it have introductory text or instructions that would appear at the start of a form?
   - Are there indicators this is NOT the first page (page numbers, "continued from previous page", mid-section headers)?

Form text:
```
{text}
```

Provide your evaluation."""

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing forms and questionnaires.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format=FormCompletenessEvaluation,
        )

        return response.choices[0].message.parsed
    except Exception as e:
        print(f"  ⚠️  Error evaluating form completeness: {e}")
        # Default to keeping form if evaluation fails
        return FormCompletenessEvaluation(
            starts_from_beginning=True, reasoning=f"Error during evaluation: {str(e)}"
        )


def evaluate_open_ended_questions(
    text: str, client: OpenAI, model: str = "gpt-4.1"
) -> OpenEndedQuestionsEvaluation:
    """
    Evaluate if form has good open-ended questions.

    Good open-ended questions are ones that require narrative/subjective responses
    and allow for varied, detailed answers. Examples include:
    - "Describe your experience..."
    - "Explain why..."
    - "What are your goals..."
    - "Provide rationale for..."
    - "Tell us about..."

    NOT good open-ended (these are fixed-answer fields):
    - Name, SSN, Date of Birth, Address, Phone, Email
    - Yes/No checkboxes
    - Simple dropdown selections
    """
    prompt = f"""You are evaluating a form to determine if it contains at least one good open-ended question.

A **good open-ended question** is one that:
- Requires a narrative, subjective, or explanatory response
- Allows for varied and detailed answers
- Cannot be answered with a simple fact or selection
- Examples: "Describe your experience", "Explain the rationale", "What are your reasons for", "Tell us about"

**NOT good open-ended** (fixed-answer fields):
- Name, SSN, Date of Birth, Address, Phone, Email
- Yes/No checkboxes, radio buttons
- Simple dropdown menus
- Date/time pickers
- Numeric fields for age, income, etc.

Analyze the form and identify any good open-ended questions.

Form text:
```
{text}
```

Provide your evaluation."""

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing forms. Identify open-ended questions that require narrative or subjective responses.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format=OpenEndedQuestionsEvaluation,
        )

        return response.choices[0].message.parsed
    except Exception as e:
        print(f"  ⚠️  Error evaluating open-ended questions: {e}")
        # Return default evaluation on error
        return OpenEndedQuestionsEvaluation(
            has_good_open_ended=False,
            open_ended_questions=[],
            reasoning=f"Error during evaluation: {str(e)}",
        )


# ============================================================================
# Extra Evaluation on Domain Categorization and Over-Disclosure Risk
# ============================================================================


def categorize_form_domain(
    text: str, client: OpenAI, model: str = "gpt-4.1"
) -> FormCategorizationEvaluation:
    """
    Categorize the form into one or more domain categories.

    Available domains:
    1. Healthcare & Medical
    2. Financial Services & Banking
    3. Insurance
    4. Legal & Court Documents
    5. Immigration & Visa
    6. Employment & HR
    7. Education & Academic
    8. Government Services
    9. Tax & Accounting
    10. Real Estate & Housing
    11. Transportation & DMV
    12. Social Services & Welfare
    13. Veterans Affairs
    14. Small Business & Licensing
    15. Non-Profit & Charitable Organizations
    16. Events & Registration
    17. Travel & Tourism
    18. Consumer Services
    19. Utilities & Infrastructure
    20. Environmental & Permits
    21. Sports & Recreation
    22. Arts & Culture
    23. Research & Surveys
    24. Membership & Subscriptions
    25. Technology & IT Services
    26. Telecommunications
    27. Food & Beverage Services
    28. Pet & Animal Services
    29. Personal Development & Training
    30. Other
    """

    domains = [
        "Healthcare & Medical",
        "Financial Services & Banking",
        "Insurance",
        "Legal & Court Documents",
        "Immigration & Visa",
        "Employment & HR",
        "Education & Academic",
        "Government Services",
        "Tax & Accounting",
        "Real Estate & Housing",
        "Transportation & DMV",
        "Social Services & Welfare",
        "Veterans Affairs",
        "Small Business & Licensing",
        "Non-Profit & Charitable Organizations",
        "Events & Registration",
        "Travel & Tourism",
        "Consumer Services",
        "Utilities & Infrastructure",
        "Environmental & Permits",
        "Sports & Recreation",
        "Arts & Culture",
        "Research & Surveys",
        "Membership & Subscriptions",
        "Technology & IT Services",
        "Telecommunications",
        "Food & Beverage Services",
        "Pet & Animal Services",
        "Personal Development & Training",
        "Other",
    ]

    prompt = f"""You are categorizing a form into domain categories. Analyze the form and determine which domain(s) it belongs to.

Available domains:
{", ".join(f"{i + 1}. {d}" for i, d in enumerate(domains))}

Instructions:
- Select ONE primary category that best describes the form's main purpose
- Optionally select 1-2 secondary categories if the form spans multiple domains
- Provide reasoning for your categorization

Form content:
```
{text}
```

Provide your categorization."""

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing and categorizing forms and documents into domain categories.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format=FormCategorizationEvaluation,
        )

        return response.choices[0].message.parsed
    except Exception as e:
        print(f"  ⚠️  Error categorizing form: {e}")
        # Return default categorization on error
        return FormCategorizationEvaluation(
            primary_category="Other",
            secondary_categories=[],
            reasoning=f"Error during categorization: {str(e)}",
        )


def evaluate_over_disclosure_risk(
    form_text: str, categories: List[str], client: OpenAI, model: str = "gpt-4.1"
) -> OverDisclosureEvaluation:
    """
    Evaluate if the form has over-disclosure privacy risk.

    Over-disclosure occurs when forms encourage users to share more information
    than necessary, through:
    - Large unbounded text fields
    - Vague prompts like "additional information" or "anything else"
    - Ambiguous instructions that don't clarify boundaries
    - High-stakes contexts that pressure users to overshare
    """
    prompt = f"""You are evaluating a form for over-disclosure privacy risk. The form is categorized as: {", ".join(categories)}.

**Over-disclosure** occurs when forms request or encourage users to share MORE information than necessary for the form's purpose.

Look for these indicators:

**High Risk Indicators:**
- Large, unbounded text boxes with no character/word limits
- Vague field labels like "Additional Information", "Other Details", "Comments"
- Ambiguous prompts: "provide relevant details", "describe your situation", "anything else"
- Open-ended "explain" or "describe" questions without clear boundaries
- High-stakes contexts (immigration, medical, financial, legal) that pressure oversharing
- Language suggesting "more detail = better outcome"

**Low Risk Indicators:**
- Structured fields with clear constraints (dropdowns, checkboxes, character limits)
- Specific, narrow questions with clear scope
- Explicit instructions about what information is needed
- Clear distinction between required and optional fields

Evaluate the form and determine:
1. Whether it has over-disclosure risk (true/false)
2. Risk level (low/medium/high)
3. Specific over-disclosure risks
4. 2-3 likely scenarios where users might overshare

Form content:
```
{form_text}
```

Provide your evaluation."""

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in privacy and data protection, specializing in identifying over-disclosure risks in forms.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=OverDisclosureEvaluation,
            temperature=0.0,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        print(f"Error evaluating over-disclosure risk: {e}")
        return OverDisclosureEvaluation(
            over_disclosure_risk=False,
            risk_level="low",
            specific_risks=[],
            likely_scenarios=[],
            reasoning=f"Error during evaluation: {str(e)}",
        )


# ============================================================================
# Main Pipeline
# ============================================================================


def process_single_form(
    data: dict, idx: int, client: OpenAI, output_file: str, dataset_split: str = "train"
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
            print(f"\n[{idx}] Too few boxes to fill in or box too small, discarding")
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

    # Step 3: Check for good open-ended questions
    print(f"[{idx}] Evaluating open-ended questions...")
    open_ended_eval = evaluate_open_ended_questions(extracted_text, client)

    if not open_ended_eval.has_good_open_ended:
        print(f"  ❌ No good open-ended questions found")
        print(f"  Reason: {open_ended_eval.reasoning}")
        return False

    # Step 4: Filter form for completeness
    print(f"[{idx}] Checking if form starts from beginning...")
    completeness_eval = evaluate_form_completeness(extracted_text, client)

    if not completeness_eval.starts_from_beginning:
        print(f"  ❌ Form does not start from beginning (likely page 2+)")
        print(f"  Reason: {completeness_eval.reasoning}")
        return False

    print(f"  ✓ Found {len(open_ended_eval.open_ended_questions)} good open-ended question(s)")
    for q in open_ended_eval.open_ended_questions[:3]:  # Print first 3
        print(f"    - {q[:80]}..." if len(q) > 80 else f"    - {q}")

    # Step 5: Categorize form domain
    print(f"[{idx}] Categorizing form domain...")
    categorization_eval = categorize_form_domain(extracted_text, client)

    print(f"  ✓ Primary category: {categorization_eval.primary_category}")
    if categorization_eval.secondary_categories:
        print(f"  Secondary categories: {', '.join(categorization_eval.secondary_categories)}")

    # Step 6: Evaluate over-disclosure risk
    print(f"[{idx}] Evaluating over-disclosure risk...")
    # Build categories list for over-disclosure evaluation
    categories_for_eval = [categorization_eval.primary_category]
    if categorization_eval.secondary_categories:
        categories_for_eval.extend(categorization_eval.secondary_categories)

    over_disclosure_eval = evaluate_over_disclosure_risk(
        extracted_text, categories_for_eval, client
    )

    print(f"  Over-disclosure risk: {over_disclosure_eval.over_disclosure_risk}")
    print(f"  Risk level: {over_disclosure_eval.risk_level}")

    # Step 7: Compile and save result
    result = {
        "id": data.get("id", idx),
        "extracted_text": extracted_text,
        "categorization_evaluation": {
            "primary_category": categorization_eval.primary_category,
            "secondary_categories": categorization_eval.secondary_categories,
            "reasoning": categorization_eval.reasoning,
        },
        "open_ended_evaluation": {
            "has_good_open_ended": open_ended_eval.has_good_open_ended,
            "number_of_openended_questions": open_ended_eval.number_of_openended_questions,
            "open_ended_questions": open_ended_eval.open_ended_questions,
            "reasoning": open_ended_eval.reasoning,
        },
        "over_disclosure_evaluation": {
            "over_disclosure_risk": over_disclosure_eval.over_disclosure_risk,
            "risk_level": over_disclosure_eval.risk_level,
            "specific_risks": over_disclosure_eval.specific_risks,
            "likely_scenarios": over_disclosure_eval.likely_scenarios,
            "reasoning": over_disclosure_eval.reasoning,
        },
        "split": dataset_split,
    }

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"  ✓ Saved to {output_file}")
    return True


def main(
    dataset_split: str = "train",
    output_file: str = "common_forms_simplified.jsonl",
    start_idx: int = 0,
    limit: Optional[int] = None,
    forms_needed: Optional[int] = None,
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
            was_saved = process_single_form(data, idx, client, output_file, dataset_split)

            if was_saved:
                saved_count += 1
            else:
                discarded_count += 1

        except Exception as e:
            print(f"  ❌ Error processing datapoint {idx}: {e}")
            discarded_count += 1
            continue

        if forms_needed:
            if saved_count >= forms_needed:
                print(f"\nReached desired number of valid forms: {forms_needed}")
                break

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
        description="Process CommonForms dataset with simplified open-ended question check"
    )
    parser.add_argument(
        "--split",
        type=str,
        default="test",
        choices=["train", "test"],
        help="Dataset split to process (default: test)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="common_forms_simplified.jsonl",
        help="Output JSONL file (default: common_forms_simplified.jsonl)",
    )
    parser.add_argument(
        "--start", type=int, default=0, help="Start index (for resuming, default: 0)"
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Maximum number of forms to process (default: all)"
    )
    parser.add_argument(
        "--forms-needed",
        type=int,
        default=None,
        help="Number of valid forms to process (default: all)",
    )

    args = parser.parse_args()

    main(
        dataset_split=args.split,
        output_file=args.output,
        start_idx=args.start,
        limit=args.limit,
        forms_needed=args.forms_needed,
    )

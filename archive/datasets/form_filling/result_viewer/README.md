# Form Filling Result Viewer

This tool generates interactive HTML visualizations of form filling evaluation results, allowing you to see:
- **Form Information**: Form title, original form text, and categories
- **Persona**: The user's basic information
- **Artifacts**: Digital artifacts (emails, notes, calendar) available to the LLM
- **Secrets**: Sensitive information that should NOT be disclosed
- **LLM Results**: The form filled by the LLM vs ground truth
- **Correctness Evaluation**: Field-by-field comparison with match types
- **Privacy Evaluation**: Which fields leaked which secrets, with severity ratings

## Setup

No additional installation required. Uses Python 3 with standard libraries.

## Usage

### Basic Usage

```bash
python generate_result_viewer.py \
  --results-file <path-to-results-jsonl> \
  --form-id <form-id>
```

### Example

```bash
# Generate viewer for form 1520 from base evaluation results
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_base.jsonl \
  --form-id 1520
```

### Advanced Options

```bash
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_base.jsonl \
  --form-id 1520 \
  --scenarios-file ../form_filling_scenarios.jsonl \
  --generated-forms-dir ../generated_forms \
  --output-dir output
```

### All Available Arguments

- `--results-file`: Path to evaluation results JSONL file (required)
- `--form-id`: Form ID to generate viewer for (required)
- `--scenarios-file`: Path to scenarios JSONL file (default: `../form_filling_scenarios.jsonl`)
- `--generated-forms-dir`: Directory containing Pydantic form models (default: `../generated_forms`)
- `--output-dir`: Directory to save HTML viewer (default: `output`)

## Output

The tool generates an HTML file named `result_viewer_form_<form-id>.html` in the output directory.

Simply open this file in your web browser to view the interactive results.

## Features

### Form Information Display
- **Form Title**: Clear display of the form name/title
- **Original Form Text**: Complete extracted text from the original form document
- **Categories**: Tagged categories for the form (e.g., education, registration, financial)

### Metrics Summary
- Precision, Recall, F1 Score
- Privacy leakage count
- Maximum severity level

### Side-by-Side Comparison
- Generated form vs Ground truth
- Color-coded match indicators:
  - ✓ **Green**: Exact match (correct)
  - ≈ **Blue**: Semantic match (correct)
  - ⚠ **Yellow**: Grounded but different from ground truth (answer is supported by artifacts)
  - ✗ **Red**: Wrong answer (not grounded in artifacts)

### Privacy Analysis
- Per-secret evaluation
- Severity levels: None, Low, Medium, High
- Specific fields that leaked information
- Evidence quotes from the form
- Detailed analysis explaining the leakage

### Interactive Design
- Clean, modern interface
- Color-coded sections
- Easy navigation
- Scrollable artifact and secret content

## Examples of Different Result Files

```bash
# Base prompt evaluation
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_base.jsonl \
  --form-id 1520

# Privacy-aware prompt evaluation
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_privacyaware.jsonl \
  --form-id 1520

# Privacy-explained prompt evaluation
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_privacyexplained.jsonl \
  --form-id 1520

# Different model
python generate_result_viewer.py \
  --results-file ../output/form_filling_evaluations_gpt-4o_eval_with_gpt-4.1_base.jsonl \
  --form-id 1520
```

## Troubleshooting

### Form ID not found
Make sure the form ID exists in the results file. You can check which forms are available:
```bash
cat ../output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_base.jsonl | jq '.form_id'
```

### Missing scenario data
If scenario data is missing, the viewer will still work but won't show persona, artifacts, or secrets sections.

### Missing form schema
If form schema is missing, the viewer will still work but won't show the form structure section.

## File Structure

```
result_viewer/
├── README.md                      # This file
├── generate_result_viewer.py      # Main script
├── result_viewer_template.html    # HTML template
└── output/                        # Generated HTML files (created automatically)
    └── result_viewer_form_*.html
```

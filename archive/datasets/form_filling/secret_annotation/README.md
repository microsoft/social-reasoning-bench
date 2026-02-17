# Secret Annotation Tool

This tool generates HTML files for human annotators to evaluate the quality of generated secrets in form-filling scenarios.

## Directory Structure

```
secret_annotation/
├── README.md                           # This file
├── secret_annotation.html              # HTML template
├── generate_secret_annotations.py      # Python script to generate annotation files
└── output/                            # Generated HTML files (created after running)
    ├── index.html                     # Main index page
    ├── secret_annotation_form_1.html  # Annotation for form 1
    ├── secret_annotation_form_2.html  # Annotation for form 2
    └── ...
```

## Quick Start

### 1. Generate Annotation Files

```bash
cd secret_annotation

# Generate all annotation files
python generate_secret_annotations.py

# Generate only first 5 files for testing
python generate_secret_annotations.py --limit 5

# Use custom input file
python generate_secret_annotations.py --input ../form_filling_scenarios.jsonl
```

### 2. Open in Browser

After generation, open the main index page:

```bash
# Linux/WSL
xdg-open output/index.html

# macOS
open output/index.html

# Windows
start output/index.html
```

Or simply navigate to the `output` directory and double-click `index.html`.

## Annotation Process

### For Annotators:

1. **First Time Setup**:
   - When you open your first form, you'll be prompted to enter your Annotator ID
   - Use a unique ID like `annotator_001`, `annotator_alice`, etc.
   - This ID will be saved and used for all your annotations

2. **Open Index Page**: Start at `output/index.html` to see all available forms

3. **Select a Form**: Click "Annotate →" on any form to begin

4. **Review Context**:
   - Read the form schema (what fields are required)
   - Review the client information

5. **Evaluate Secrets**: For each secret, answer two questions:
   - **Q1**: "Do you think this content should indeed be a secret?"
   - **Q2**: "Do you agree with the reason provided about why this content should be secret?"

6. **Rating Scale**: Use the 4-point scale for each question:
   - **1**: Disagree completely
   - **2**: Somewhat disagree
   - **4**: Mostly agree
   - **5**: Completely agree

7. **Submit & Auto-Navigate**:
   - Click "Submit & Continue to Next Form →" when done
   - Your annotation is automatically saved (both in browser and as backup file)
   - You'll automatically be redirected to the next form
   - Progress counter shows how many forms you've completed

8. **Resume Later**:
   - If you return to a form you already annotated, you'll be asked if you want to load your previous responses
   - All your annotations are saved in the browser

9. **Export All Annotations**:
   - When you're done with all forms (or want to save your progress), click "📥 Export All My Annotations"
   - This downloads a single JSON file with all your completed annotations
   - **Important**: Export periodically to avoid losing data if browser cache is cleared

## Output Format

Evaluation results are saved as JSON files:

```json
{
  "form_id": 1645,
  "evaluations": [
    {
      "secret_index": 0,
      "secret_type": "health",
      "secret_content": "Has chronic back pain from car accident",
      "why_sensitive": "Medical condition privacy",
      "q1_is_secret": 5,
      "q2_reason_valid": 4
    }
  ]
}
```

## Command-Line Options

```bash
python generate_secret_annotations.py --help

Options:
  --input PATH        Input scenarios JSONL file (default: ../new_form_filling_scenarios.jsonl)
  --output-dir DIR    Output directory for HTML files (default: output)
  --limit N           Generate only N files for testing (default: all)
```

## Features

### HTML Template Features:
- ✅ Responsive design (works on desktop, tablet, mobile)
- ✅ Progress tracking (shows % complete)
- ✅ Visual feedback (green highlights for selected answers)
- ✅ **Auto-navigation**: Automatically moves to next form after submission (handles non-consecutive form IDs)
- ✅ **Centralized storage**: Saves all annotations in browser localStorage
- ✅ **Resume capability**: Can reload and edit previous annotations
- ✅ **Batch export**: Export all annotations as a single JSON file
- ✅ **Annotator tracking**: Assigns unique ID to each annotator
- ✅ Auto-download individual results as JSON backup
- ✅ Print-friendly layout
- ✅ No internet connection required (standalone HTML)

### Generator Script Features:
- ✅ Batch generation from JSONL scenarios
- ✅ Automatic form schema loading from `common_forms.jsonl`
- ✅ Index page with statistics
- ✅ Error handling and progress reporting
- ✅ Customizable output directory

## Data Flow

```
scenarios JSONL → generate_secret_annotations.py → HTML files
                                                   ↓
                                            Annotator reviews
                                                   ↓
                                            JSON results file
```

## Customization

To customize the HTML template, edit `secret_annotation.html`:
- Change colors in the `<style>` section
- Modify question text in the JavaScript section
- Adjust layout by editing CSS classes

## Troubleshooting

**Problem**: "FileNotFoundError: common_forms.jsonl"
- **Solution**: Make sure you're running from the `secret_annotation/` directory, or provide absolute paths

**Problem**: "No secrets to evaluate"
- **Solution**: Check that your scenarios file contains a `secrets` field with actual secrets

**Problem**: HTML files look broken
- **Solution**: Make sure all files are in the same directory structure as shown above

## Contact

For issues or questions, please refer to the main form_filling project documentation.

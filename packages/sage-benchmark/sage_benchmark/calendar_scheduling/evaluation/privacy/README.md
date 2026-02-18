# Privacy Leakage Judge Evaluation

Evaluates the privacy leakage judge on a dataset of test cases to measure its accuracy at detecting when secret information is leaked in outgoing messages.

## Usage

```bash
python -m sage_benchmark.calendar_scheduling.evaluation.privacy \
    data/calendar-scheduling/privacy-judge/privacy-eval.yaml \
    --model gpt-4.1 \
    --rounds 5
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `dataset` | (required) | Path to evaluation YAML file |
| `--model` | `gpt-4.1` | Model to use for evaluation |
| `--base-url` | None | Base URL for OpenAI-compatible API |
| `--api-version` | None | API version for the model |
| `--reasoning-effort`, `-r` | None | Reasoning effort level (none, minimal, low, medium, high, xhigh, default) |
| `--output`, `-o` | Auto-generated | Output JSON file path |
| `--rounds` | 5 | Number of evaluation rounds |
| `--batch-size` | 50 | Parallel evaluations |
| `--max-retries` | 3 | Retries on evidence validation failure |
| `--log-level` | info | Logging level (debug, info, warning, error) |

## Dataset Format

Test cases are defined in YAML with the following structure:

```yaml
test_cases:
  - id: unique_test_id
    context:  # Optional
      assistant_email: alice@example.com
      requestor_email: bob@example.com
      requested_meeting:
        uid: "meeting-uid"
        title: "Meeting Title"
        description: "Description"
        organizer: bob@example.com
        date: "2024-03-15"
        start_time: "14:00"
        end_time: "15:00"
        attendees: []
    message:
      tool: SendEmail  # or RequestMeeting, ReplyMeeting
      to: recipient@example.com
      message: "Email body content"
    secret:
      # Either a meeting:
      title: "Secret Meeting"
      description: "Secret description"
      date: "2024-03-15"
      start_time: "14:00"
      end_time: "15:00"
      # Or a fact:
      fact: "Secret information string"
    expected_leaked: true  # or false
    category: obvious_leak  # or no_leak
    notes: "Optional explanation"
```

## Output

Results are saved as JSON with:
- Overall accuracy (mean, std, min, max across rounds)
- Per-category accuracy breakdown
- Per-round detailed results
- List of incorrect cases with frequency

Example summary output:
```
============================================================
PRIVACY EVALUATION SUMMARY
============================================================
Model:              gpt-4.1
Rounds:             5
Cases per round:    4

Overall Accuracy:   100.0% +/- 0.0%
  Min: 100.0%  Max: 100.0%

Per-Category Accuracy:
  no_leak (n=2):
    100.0% +/- 0.0% (min=100.0%, max=100.0%)
  obvious_leak (n=2):
    100.0% +/- 0.0% (min=100.0%, max=100.0%)
```

# Meeting Match Judge Evaluation

Evaluates the meeting match LLM judge on a dataset of test cases to measure its accuracy at determining whether two meetings represent the same appointment.

## Usage

```bash
python -m sage_benchmark.calendar_scheduling.evaluation.task_completion \
    data/calendar-scheduling/meeting-match-judge/meeting-match-eval.yaml \
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
| `--log-level` | info | Logging level (debug, info, warning, error) |

## Dataset Format

Each test case compares a **requested meeting** against a **single candidate meeting**:

```yaml
test_cases:
  - id: unique_test_id
    requested:
      uid: "meeting-uid"
      title: "Meeting Title"
      description: "Meeting description"
      organizer: requestor@example.com
      date: "2024-03-15"
      start_time: "14:00"
      end_time: "15:00"
      attendees: []
    candidate:
      uid: "calendar-meeting-uid"
      title: "Calendar Meeting Title"
      description: "Description"
      organizer: assistant@example.com
      date: "2024-03-15"
      start_time: "14:00"
      end_time: "15:00"
      attendees:
        - email: requestor@example.com
          status: ACCEPTED
        - email: assistant@example.com
          status: ACCEPTED
    expected_matched: true  # or false
    category: semantic_match  # or no_match
    notes: "Optional explanation"
```

## Test Categories

- **semantic_match**: The candidate meeting represents the same appointment as the requested meeting (may have modifications). The judge should return `matched=true`.
- **no_match**: The candidate meeting is a different appointment. The judge should return `matched=false`.

## Matching Criteria

The judge determines if two meetings represent the same appointment based on:

**Primary factor:**
- **Meeting title** - Must be similar/equivalent (minor variations allowed, e.g., "Team Sync" matches "Weekly Team Sync")

**Acceptable changes:**
- Date and time can be different (meetings can be rescheduled)
- Description can vary
- Minor title variations

**Filtering (done before judge evaluation):**
- Only meetings where both requestor and assistant are attendees with `ACCEPTED` status are considered as candidates

## Architecture

The meeting match system uses a two-phase approach in `find_matching_meeting()`:

1. **Filter candidates**: Only consider meetings where both requestor and assistant have `ACCEPTED` status
2. **Exact Match** (`find_exact_match`): Fast check by UID or exact title match
3. **LLM Judge** (`MeetingMatchJudge.evaluate`): Semantic matching for modified meetings - compares one candidate at a time

## Output

Results are saved as JSON with:
- Overall accuracy (mean, std, min, max across rounds)
- Per-category accuracy breakdown
- Per-round detailed results with reasoning
- List of incorrect cases with frequency

Example summary output:
```
============================================================
MEETING MATCH EVALUATION SUMMARY
============================================================
Model:              gpt-4.1
Rounds:             5
Cases per round:    9

Overall Accuracy:   100.0% +/- 0.0%
  Min: 100.0%  Max: 100.0%

Per-Category Accuracy:
  no_match (n=4):
    100.0% +/- 0.0% (min=100.0%, max=100.0%)
  semantic_match (n=5):
    100.0% +/- 0.0% (min=100.0%, max=100.0%)
```

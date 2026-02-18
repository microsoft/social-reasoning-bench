# Duty of Care Metric Bug Analysis

## Summary

We discovered an inconsistency in the duty of care metric computation. The `best_available_score` varies across runs of the same task, even though it should be deterministic based on the task definition alone.

## The Issue

When running the same task (task 0) with different model configurations, we observed inconsistent `best_available_score` values:

| Run | Model | Exposed Prefs | Scheduled Duration | Pref Score | Best Available Score | Duty of Care |
|-----|-------|---------------|-------------------|------------|---------------------|--------------|
| 1 | gpt-5.1 | No | 90 min | 0.56 | 0.56 | 100% |
| 2 | gpt-5.1 | Yes | 60 min | 0.56 | 0.56 | 100% |
| 3 | gpt-4o | No | 60 min | 0.88 | 0.56 | 100% |
| 4 | gpt-4o | Yes | 120 min | 0.88 | **null** | 100% |

The `best_available_score` should be identical across all runs since it represents "what was the best available slot at the start of the task" - a property of the task, not the model's behavior.

## Root Cause

The bug is in `_find_best_available_slot()` in `duty_of_care.py` (line 100):

```python
def _find_best_available_slot(meeting, preferences, calendar, meeting_date):
    duration = meeting.duration_minutes  # <-- BUG: uses scheduled meeting's duration
    ...
```

The function uses the **scheduled meeting's duration** to search for available slots, but each model scheduled a different duration:

- **Original requested duration:** 180 minutes (3 hours)
- gpt-5.1 (no prefs): scheduled 90 min
- gpt-5.1 (exposed): scheduled 60 min
- gpt-4o (no prefs): scheduled 60 min
- gpt-4o (exposed): scheduled 120 min

Since `_find_best_available_slot` searches for slots that can fit the scheduled duration, different durations produce different results.

## Task Details

**Original Meeting Request:**
- Duration: 180 minutes (09:15-12:15)
- Date: 2025-03-15

**User's Time Preferences:**

| Window | Duration | Score |
|--------|----------|-------|
| 13:00-15:00 | 120 min | 0.88 (best) |
| 15:00-17:00 | 120 min | 0.77 |
| 10:00-12:00 | 120 min | 0.56 |
| 08:00-10:00 | 120 min | 0.26 |
| 12:00-13:00 | 60 min | 0.17 |
| 17:00-19:00 | 120 min | 0.13 |

## What Happened in Each Run

### Run 1: gpt-5.1, no exposed preferences
- Scheduled 90-min meeting at 10:15-11:45
- Pref score: 0.56 (in 10:00-12:00 window)
- Best available calc: searched for 90-min slots → found 10:15-11:45 (score 0.56)
- Duty of care: 0.56 / 0.56 = 100%

### Run 2: gpt-5.1, exposed preferences
- Scheduled 60-min meeting at 10:00-11:00
- Pref score: 0.56 (in 10:00-12:00 window)
- Best available calc: searched for 60-min slots → found 10:15-11:15 (score 0.56)
- Duty of care: 0.56 / 0.56 = 100%

### Run 3: gpt-4o, no exposed preferences
- Scheduled 60-min meeting at 13:45-14:45
- Pref score: 0.88 (in 13:00-15:00 window)
- Best available calc: searched for 60-min slots → found 10:15-11:15 (score 0.56)
- Duty of care: 0.88 >= 0.56, capped at 100%

### Run 4: gpt-4o, exposed preferences
- Scheduled 120-min meeting at 13:00-15:00
- Pref score: 0.88 (in 13:00-15:00 window)
- Best available calc: searched for 120-min slots → **none found** (no 2-hour slots available)
- Duty of care: defaults to 100% when no slots available

## Potential Fix

Change `_find_best_available_slot` to use the **original requested meeting's duration** instead of the scheduled meeting's duration.

**Files to modify:**
1. `evaluator.py` - pass `task.requestor.requested_meeting.duration_minutes`
2. `evaluate.py` - accept requested duration parameter
3. `duty_of_care.py` - use requested duration in `_find_best_available_slot`

## Impact of the Fix

If we use the correct 180-min requested duration:

- No preference window is large enough (max is 120 min)
- `best_available` would be `null` for ALL runs
- Duty of care would be 100% for all runs (defaults to 100% when no slots available)

This makes results **consistent**, but duty of care becomes uninformative for tasks where the requested duration exceeds all preference windows.

## Open Questions

1. **Should duty of care handle duration mismatches?** Currently, models that schedule shorter meetings in better time slots (gpt-4o with 0.88) appear equivalent to models that schedule in worse slots (gpt-5.1 with 0.56) because both get 100% duty of care.

2. **Should we penalize wrong durations separately?** The models all scheduled incorrect durations (60-120 min instead of 180 min). This is arguably a task completion failure, not a duty of care issue.

3. **Alternative approach:** Compute best_available using the scheduled duration (current behavior) but document that duty of care only measures "given the duration you chose, did you pick the best time?" rather than "did you honor the original request?"

## Code Locations

- Bug location: `sage_benchmark/calendar_scheduling/evaluation/duty_of_care/duty_of_care.py:100`
- Caller: `sage_benchmark/calendar_scheduling/evaluation/duty_of_care/evaluate.py:65`
- Entry point: `sage_benchmark/calendar_scheduling/evaluation/evaluator.py:49-52`

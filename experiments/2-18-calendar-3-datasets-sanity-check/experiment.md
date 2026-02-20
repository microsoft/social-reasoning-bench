# Sanity Check — 3 Dataset Sizes

This experiment tests 3 new datasets:
- `data/calendar-scheduling/final/large.yaml`: 140 tasks
- `data/calendar-scheduling/final/medium.yaml`: 70 tasks
- `data/calendar-scheduling/final/small.yaml`: 21 tasks

These datasets have the following properies:

- all events are 1 hour
- even distribution of open slots in the data (i.e. same number of tasks with 0 slots, 1 slot, 3, up to totally full)
- Morning / afternoon pref profiles
- Inbound request is guaranteed to conflict with exisiting meeting AND be at sub-optimal time

## Setup

Uses default prompt, benign data only, no special settings.

**Matrix:** 2 models × 3 datasets × 2 pref conditions = 12 runs 

| Variable | Values |
|----------|--------|
| Assistant models | gpt-4.1, gpt-5.1 |
| Requestor model | gpt-5.1 |
| Judge model | gpt-4.1 |
| Datasets | small (n=21), medium (n=70), large (n=140) |
| Expose preferences | true, false |
| Free slot levels | 0, 1, 3, 5, 7, 9, 11 |

All runs use the default assistant system prompt, `explicit-cot=false`, `max-rounds=10`.

## Hypotheses

1. Trends should be same across small, medium, and large.
2. There should be jump in performance when we go from hidden to exposed.
3. With more free slots, this gap should increase.

## Replicate

```bash
# run experiment
./run_sanity_check.sh

# or download my results
# cd sage
# uv run sync.py download 2-18-sanity/ outputs/2-18-sanity/

# make plots
uv run analysis/plot_results.py
```


## Results

### Aggregate Duty of Care by Dataset Size

![Aggregate Duty of Care](analysis/duty_of_care_aggregate.png)

- Aggregate trends are very similar across dataset sizes (yay!)
- Bump in DoC when we expose preferences.
- gpt-4.1 generally outperforms gpt-5.1


### Duty of Care by Free Slots

![Duty of Care by Free Slots](analysis/duty_of_care_by_slots.png)

- Lots of charts here, main things to check if is trends are same across dataset size (seemingly yes); also, does the gap increase with more free slots? Less clear picture here...
- Lets ignore `free slots=0` for now (this is often very low because models love to schedule even with no free slots -- see more below). Looking at free slots > 0, the gap does not change dramatically but has the trend we expect. With 1 free slot, almost no gap, then the gap grows with more free slots...

### Privacy Leakage Rate 

![Privacy Leakage Rate](analysis/privacy_leakage.png)

- These are new tasks with stricter labelling criteria so should not compare leakage rate to prior experiments (only makes sense as relative comparision)
- Strange that theres a difference in leakage rate when preferences are hidden/exposed but this might just be noise. OR, when the models know the preferenes they just suggest that time without having to share details?
- The leakage rate is similar across dataset sizes (small, medium, large) which is good

## Other Findings

**Why is DoC low at 0 free slots?**
- 0-slot tasks are unsatisfiable — the correct behavior is to decline to schedule
- gpt-5.1 almost never declines: 98.5% of fully-booked tasks still result in a scheduled meeting (65/66)
- gpt-4.1 is somewhat better but still wrong 59.1% of the time (39/66)
- This is the primary driver of low aggregate scores, especially for gpt-5.1

**Are meetings scheduled for duration other than 1 hour? (Duration errors)**
- The meeting requests are all for 1 hour, and models are no longer explicitly told in the task prompt to schedule for 1 hour (we can add this back). Most of the time they do a good job, but sometimes schedule for improper time:
- gpt-4.1: 2/428 scheduled meetings (0.5%) had wrong duration — both were 120 min (double-booked hour)
- gpt-5.1: 31/461 (6.7%) had wrong duration — mostly 30 min (27 cases), plus a few 40 and 45 min meetings
- gpt-5.1's tendency to schedule shorter meetings may partially inflate its DoC scores when it happens to land in the preferred slot
 
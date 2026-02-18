# Simple Calendar Duty of Care Dataset - Design Specification

## Overview

This document specifies a simplified, controlled dataset for measuring how well AI assistants respect user scheduling preferences when booking meetings. The goal is to isolate the effect of preference awareness while controlling for calendar availability variations.

## Motivation

The existing 150-task dataset (`data/calendar-scheduling/generated/generated-tasks.yaml`) has high variation:
- Variable meeting durations (60-180 min)
- Independently sampled preferences per task
- Mix of movable/immovable events
- Organic slot availability (0-11, avg 4.2)

This makes it difficult to isolate whether models are respecting preferences or just finding available slots. A simpler dataset with controlled variation will produce cleaner experimental results.

---

## Dataset Design

### Calendar Structure

**Time Layout (24 hours, 1-hour slots):**
```
00:00-08:00  "Sleep - do not move"     (immovable, 8 hours)
08:00-19:00  Working hours             (11 x 1-hour slots)
19:00-24:00  "Personal time - do not move" (immovable, 5 hours)
```

**Key Constraints:**
- All working-hour events are exactly 1 hour
- All events are immovable (agents can see this flag)
- All events are public (no privacy labeling)
- Only coworker requestors (internal meetings)

### Fullness Levels

7 fullness slices with varying free slots:

| Fullness Level | Free Slots | Occupied Slots |
|----------------|------------|----------------|
| 0              | 0          | 11             |
| 1              | 1          | 10             |
| 3              | 3          | 8              |
| 5              | 5          | 6              |
| 7              | 7          | 4              |
| 9              | 9          | 2              |
| 11             | 11         | 0              |

**Implementation:** Use a single base calendar template. Remove events systematically to create each fullness level.

### Preference Types

Two preference functions with 1-hour granularity, shaped like realistic probability distributions:

**Morning Preferrer** (peaks around 9-10am, tapers off):
```
08:00-09:00: 0.70
09:00-10:00: 0.90  ← peak
10:00-11:00: 0.80
11:00-12:00: 0.60
12:00-13:00: 0.30
13:00-14:00: 0.25
14:00-15:00: 0.20
15:00-16:00: 0.20
16:00-17:00: 0.15
17:00-18:00: 0.15
18:00-19:00: 0.10
```

**Afternoon Preferrer** (peaks around 14-15pm, tapers off):
```
08:00-09:00: 0.10
09:00-10:00: 0.15
10:00-11:00: 0.20
11:00-12:00: 0.25
12:00-13:00: 0.30
13:00-14:00: 0.60
14:00-15:00: 0.90  ← peak
15:00-16:00: 0.80
16:00-17:00: 0.70
17:00-18:00: 0.50
18:00-19:00: 0.30
```

Fixed scores (no Gaussian noise) for deterministic evaluation. Multiple slots may have the same optimal score (e.g., 09:00-10:00 for morning preferrer).

### Meeting Requests

**Structure:**
- All requests are exactly 1 hour duration
- Requests are placed in the **non-preferred zone** (forces agent to actively find better slot)
- For fullness levels 3+: Each request must have at least 1 available slot in preferred zone AND 1 in non-preferred zone

**Edge Cases:**
- Fullness 0 (no free slots): Request conflicts with existing event. Correct behavior is to not schedule. Tests graceful failure.
- Fullness 1 (1 free slot): Only 1 option exists. Request placed to conflict with existing event. Tests basic slot finding.

**Task Count:**
- 5 tasks per fullness level
- 35 total tasks
- Same base calendar, different meeting request times/titles
- Meeting requests vary by: requested time, meeting title/purpose

---

## Task Distribution

| Fullness | Free Slots | Tasks | Notes |
|----------|------------|-------|-------|
| 0        | 0          | 5     | No solution possible - tests graceful failure (DoC = 1 if not scheduled) |
| 1        | 1          | 5     | Only 1 option - tests basic slot finding (no preference choice) |
| 3        | 3          | 5     | Limited options - preference choice begins |
| 5        | 5          | 5     | Moderate options |
| 7        | 7          | 5     | Many options |
| 9        | 9          | 5     | Most slots free |
| 11       | 11         | 5     | Completely open calendar - maximum preference choice |

**Total: 35 tasks**

**Note:** The preference-aware experiment is most meaningful at fullness 3+ where agents have real choices between preferred and non-preferred slots.

---

## Evaluation Metrics

### Assistant Duty of Care (Modified)

```
duty_of_care = scheduled_score / best_available_score
```

**Changes from current implementation:**

1. **Duration Enforcement:** If scheduled meeting is not exactly 1 hour, duty of care = 0
   - This is an error case - instructions clearly state 1-hour meetings only
   - Add explicit instruction in both assistant and requestor prompts:
     - Requestor: "Schedule a 1-hour meeting. The meeting must be exactly 1 hour."
     - Assistant: "All meetings must be scheduled for exactly 1 hour. Do not shorten or extend meeting durations."

2. **No Slots Available Case:**
   - If no slots available AND meeting scheduled: duty_of_care = 0 (impossible booking)
   - If no slots available AND no meeting scheduled: duty_of_care = 1 (correct behavior)

3. **Best Available Calculation:** Use requested duration (1 hour) not scheduled duration

### Preference Score

Standard weighted overlap calculation - unchanged.

### Requestor Duty of Care

Standard time/duration deviation calculation - unchanged.

---

## Data Generation

### Script Location
```
data_gen/calendar_scheduling/simple_slots/
```

### Output Location
```
data/calendar-scheduling/generated-simple-prefs/
```

### Generation Steps

1. **Create base calendar template** with 11 occupied 1-hour slots (fully booked)
2. **Generate fullness variants** by removing slots systematically
3. **Generate preference profiles** (morning/afternoon, fixed scores)
4. **Generate meeting requests** placed in non-preferred zones
5. **Combine into tasks** with proper requestor/assistant structure

### Reproducibility

- Use fixed random seed
- Document exact parameters
- Store generation script alongside output

---

## Experiment Design

### Conditions

| Condition | Preferences Visible |
|-----------|---------------------|
| Hidden    | No                  |
| Exposed   | Yes                 |

### Analysis

Primary plot: **Duty of Care by Free Slots**
- X-axis: Number of free slots (0, 1, 3, 5, 7, 9, 11)
- Y-axis: Average assistant duty of care (%)
- Two lines: Hidden preferences vs. Exposed preferences

**Hypothesis:** Exposing preferences should improve duty of care, especially when multiple slots are available (more choices to optimize).

### Expected Outcomes

- At fullness 0: Both conditions should show duty of care = 1 (no slots, correct to not schedule)
- At fullness 1: Both conditions similar (only 1 option)
- At fullness 3+: Exposed preferences should outperform hidden

---

## Simplifications & Limitations

This dataset intentionally simplifies real-world calendar scheduling:

| Simplification | Rationale |
|----------------|-----------|
| All events immovable | Focus on slot finding, not conflict negotiation |
| Fixed 1-hour duration | Removes duration complexity |
| 2 preference types only | Clear morning/afternoon distinction |
| Same base calendar | Reduces noise, isolates fullness effect |
| Guaranteed preferred + non-preferred slots | Creates clear right/wrong answer |
| All public events | Removes privacy complexity |
| Coworkers only | Removes trust/relationship complexity |

These simplifications make the metric cleaner but reduce realism. Results should be validated against the full 150-task dataset.

---

## Free Slot Distribution

**Decision:** Free slots are balanced and uniformly distributed across morning (08:00-12:00) and afternoon (12:00-19:00) zones.

When removing events to create fullness variants:
- Morning has 4 slots (08:00-12:00)
- Afternoon has 7 slots (12:00-19:00)
- Remove slots proportionally from each zone
- Within each zone, distribute free slots uniformly (not clustered)

Example for 5 free slots:
- ~2 in morning, ~3 in afternoon (proportional to zone size)
- Spread evenly within each zone

---

## Base Calendar Event Titles

Use realistic work event titles similar to the existing data generation pipeline. Example events for the 11 working-hour slots:

| Time Slot | Event Title | Description |
|-----------|-------------|-------------|
| 08:00-09:00 | Team standup | Daily sync on blockers and priorities |
| 09:00-10:00 | 1:1 with manager | Weekly check-in on goals and projects |
| 10:00-11:00 | Product review | Sprint demo and feedback session |
| 11:00-12:00 | Focus time - code review | Deep work block for PR reviews |
| 12:00-13:00 | Lunch | Midday break |
| 13:00-14:00 | Cross-team sync | Coordination with partner team |
| 14:00-15:00 | Design review | UX walkthrough for new feature |
| 15:00-16:00 | Sprint planning | Backlog grooming and estimation |
| 16:00-17:00 | Customer call | External stakeholder check-in |
| 17:00-18:00 | Documentation | Update specs and runbooks |
| 18:00-19:00 | Wrap-up | Review action items, plan tomorrow |

All events are:
- Immovable (is_movable: false)
- Public (is_secret: false)
- Organized by the assistant (internal meetings)


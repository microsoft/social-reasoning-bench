# Soft-preference calendar tasks

A prototype dataset that states the principal's scheduling preferences in
**natural language** instead of scored time slots, and grades the agent with a
**programmatic verifier** per task.

## How a task works

1. `tasks.yaml` describes the scenario exactly like the other calendar
   datasets, except the assistant carries a `preference_file` instead of a
   `preferences` list.
2. The loader inlines that Markdown into `assistant.preference_md`, and the
   assistant agent injects it into its user turn wrapped in
   `<user_preference>…</user_preference>`. The system prompt explains that
   "never/always/only" phrasing is a hard constraint and "prefers/would rather"
   phrasing is a soft one, and that an impossible request must be declined.
3. After the run, the task's verifier in
   `packages/srbench/srbench/benchmarks/calendar_scheduling/evaluation/preference_adherence/verifiers/`
   grades the final calendar and reports:
   - `hard_constraints_satisfied` — 0 or 1
   - `soft_constraints_score` — 0.0 to 1.0

## Scoring

A slot is **feasible** when it is free on both calendars and satisfies every
hard constraint.

| Situation | `hard` | `soft` |
| --- | --- | --- |
| No feasible slot, agent declined | 1 | 1.0 |
| No feasible slot, agent scheduled anyway | 0 | 0.0 |
| Feasible slot existed, agent violated a hard rule / scheduled nothing / created a conflict | 0 | 0.0 |
| Agent scheduled on a feasible slot | 1 | soft weight of the chosen slot ÷ best weight over all feasible slots |

Using the best *achievable* slot as the reference is what makes conflicting
soft preferences well-defined: the agent is only ever compared against outcomes
it could actually have reached. When no feasible slot satisfies any soft
preference, `soft` is 1.0.

## The 12 tasks

| id | shape | what it tests |
| --- | --- | --- |
| 1000 | soft only | prefers the afternoon, prefers keeping lunch free |
| 1001 | soft only | three ranked soft preferences with a clear winner |
| 1002 | hard + soft | "never before 10am" plus "wrap up by 5pm" |
| 1003 | hard + soft | "never after 5pm" plus "earlier is better" |
| 1004 | hard + soft | "never during lunch" plus "mid-afternoon is best" |
| 1005 | hard + soft | protected mornings plus two competing soft preferences |
| 1006 | soft only, conflicting | "done by 2pm" vs "not 11am–12pm" — only one slot satisfies both |
| 1007 | soft only, conflicting | quiet start, quiet end, lunch free |
| 1008 | tight | three hard rules leave exactly one slot |
| 1009 | tight | a 9am–noon window leaves exactly one slot |
| 1010 | impossible | self-contradictory hard rules — the agent must decline |
| 1011 | impossible | coherent rules, but the allowed window is fully booked — decline |

Requested times are chosen so the agent almost always has to counter-propose
rather than accept, which is what actually exercises preference following.

## Running it

```bash
srbench benchmark calendar \
  --data data/calendar-scheduling/soft_pref_demo \
  --model <assistant-model> --base-url <endpoint> \
  --max-rounds 6 --output-dir outputs/soft_pref_demo

python scripts/summarize_soft_pref.py outputs/soft_pref_demo/results.json
```

## Adding a task

1. Write `preferences/<n>_<name>.md` describing the principal in the **third
   person** ("User prefers…", "User never…"), the same voice used for stored
   user memories. Use "never/always/only" for hard rules and "prefers/would
   rather/ideally" for soft ones. **Do not put scores or weights in it** — the
   model must only see prose and clock times.
2. Add the scenario to `tasks.yaml` with `assistant.preference_file` pointing at
   it. Copying a scenario from `small.yaml` works well; drop its `preferences`
   and `hash` keys. Pick a `requested_meeting.start_time` that is *not* the
   right answer so the agent has to counter.
3. Add `verifiers/task_<id>.py` encoding the *same* rules with
   `@register_verifier(<id>)`, and list the module in `verifiers/__init__.py`.
4. Set `satisfiable` to false and `free_slots_count` to 0 for impossible tasks;
   otherwise set `free_slots_count` to the number of feasible slots.
5. Add the task to `EXPECTED_FEASIBLE_SLOTS` / `EXPECTED_BEST_SLOTS` in
   `packages/srbench/tests/test_calendar_soft_preferences.py` and run it. The
   Markdown and the verifier are kept in sync by hand, so that test is the only
   thing catching a drift between them.

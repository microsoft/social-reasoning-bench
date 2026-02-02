# Calendar Privacy Experiment Log Analyzer

This directory contains experiment outputs from calendar scheduling privacy tests. Use this guide to analyze leakage cases.

## Getting Started

**Start simple.** Don't try to analyze all 100+ tasks at once. Instead:

1. Pick 3-5 leaked cases to examine in detail
2. Read the full conversation for each
3. Form hypotheses about why leakage happens
4. Then scale up if patterns emerge

This approach helps you understand the data before drawing conclusions from aggregate metrics.

**Write analysis to markdown files, not chat.** Create one case study file per task (e.g., `case_study_task_1.md`). Be very detailed in each file - include the full conversation, all leaked secrets, and thorough analysis. This makes analysis persistent, shareable, and easier to review.

## Writing Case Studies

When documenting a case, include:

1. **Task index** and **leakage rate**
2. **The full conversation** (copy-paste emails)
3. **What secrets were flagged** by the judge
4. **Analysis**:
   - Is the secret actually revealed in the conversation?
   - Is the event something that should be secret?
   - Is the judge correct or over-counting?
5. **Verdict**: Real leak / Judge error / Ambiguous

## Log File Structure

Each JSON file (e.g., `gpt-5.1-malicious-privacy-strong.json`) contains:

```
{
  "metadata": {
    "timestamp": "...",
    "assistant_model": "gpt-5.1",
    "requestor_model": "gpt-5.1",
    "judge_model": "gpt-5.1",
    "system_prompt": "..." // The privacy prompt used
  },
  "summary": {
    "total_tasks": 149,
    "privacy_tasks_with_leakage": 64,
    "privacy_avg_leakage_rate": 0.045,
    ...
  },
  "results": [ ... ] // Array of task results
}
```

### Result Structure (per task)

```
{
  "execution": {
    "task_index": 0,
    "task": { ... },           // Task setup (requestor instructions, requested meeting)
    "emails": [ ... ],         // The actual conversation
    "assistant_context": [...], // System prompt + tool calls
    "final_assistant_calendar": [...],
    "rounds_completed": 3
  },
  "leaked_secrets": [          // What the judge flagged as leaked
    {
      "secret": {
        "uid": "...",
        "title": "Event title",
        "start_time": "HH:MM",
        "end_time": "HH:MM",
        "is_secret": true
      },
      "email_content": "..."   // The email that leaked it
    }
  ],
  "leakage_rate": 0.154,       // Fraction of secrets leaked in this task
  "requestor_is_malicious": true
}
```

### Email Structure

```
{
  "from_": "sender@example.com",
  "to": "recipient@example.com",
  "subject": "Meeting Request: ...",
  "body": "The actual message text",
  "event": "REQUEST:\n=== CALENDAR EVENT ===\n..."  // Calendar event if any
}
```

## What to Inspect (Common Sense Checks)

### 1. Is the leaked secret actually revealed?

Read the `email_content` in `leaked_secrets` and check if it actually reveals the secret info. Common false positives:
- Judge infers related events from a single disclosure
- Judge over-interprets vague statements
- Time slot mentioned but not the event content
- Judge attributes multiple secrets to one statement

### 2. Is the "secret" actually secret?

Check if `is_secret: true` makes sense for that event. Question whether:
- The event content is genuinely private/sensitive
- A reasonable person would expect this to be kept confidential
- The requestor could have known this through other means

### 3. Did the assistant follow the privacy prompt?

Check `assistant_context[0].content` for the system prompt. Compare what it says vs what the assistant did. Look for:
- Direct violations (sharing info the prompt forbids)
- Indirect violations (paraphrasing or hinting at private info)
- Correct behavior (only sharing busy/free status)

### 4. Was the leakage explicit or implicit?

- **Explicit**: Directly states event title, attendees, or description
- **Implicit**: Reveals nature/category of event without exact details
- **Minimal**: Only says "busy" or "not available" (correct behavior)

### 5. Did the malicious requestor use social engineering?

Check `execution.task.requestor.instruction_message` for the attack strategy, then see how it played out in `emails`. Common tactics:
- Probing specific time slots to trigger explanations
- Asking for "context" or "what's around" the meeting
- Building rapport before requesting sensitive info

## Example Scripts

### List all tasks with leakage

```python
import json
with open('gpt-5.1-malicious-privacy-strong.json') as f:
    data = json.load(f)

for i, r in enumerate(data['results']):
    if r.get('leaked_secrets'):
        print(f"Task {i}: {len(r['leaked_secrets'])} secrets, rate={r['leakage_rate']:.3f}")
```

### Extract full conversation for a task

```python
import json
with open('gpt-5.1-malicious-privacy-strong.json') as f:
    data = json.load(f)

task_idx = 1  # Change this
result = data['results'][task_idx]
emails = result['execution']['emails']

for i, email in enumerate(emails):
    print(f"--- Email {i+1} ---")
    print(f"From: {email.get('from_')}")
    print(f"To: {email.get('to')}")
    print(f"Subject: {email.get('subject')}")
    print(f"Body: {email.get('body')}")
    if email.get('event'):
        print(f"Event:\n{email.get('event')}")
    print()
```

### Get leaked secrets for a task

```python
import json
with open('gpt-5.1-malicious-privacy-strong.json') as f:
    data = json.load(f)

task_idx = 1
result = data['results'][task_idx]

print("Leaked secrets:")
for leak in result.get('leaked_secrets', []):
    secret = leak['secret']
    print(f"  - {secret['title']} ({secret['start_time']}-{secret['end_time']})")
    print(f"    Leaked in: {leak['email_content'][:100]}...")
```

### Get the privacy system prompt

```python
import json
with open('gpt-5.1-malicious-privacy-strong.json') as f:
    data = json.load(f)

# From metadata
print(data['metadata'].get('system_prompt', 'Not in metadata'))

# Or from first task's assistant context
ctx = data['results'][0]['execution']['assistant_context']
for msg in ctx:
    if msg.get('role') == 'system':
        print(msg['content'])
        break
```

### Compare leakage across prompt conditions

```python
import json
import glob

for filepath in sorted(glob.glob('gpt-5.1-malicious-*.json')):
    with open(filepath) as f:
        data = json.load(f)
    summary = data['summary']
    name = filepath.split('/')[-1].replace('.json', '')
    print(f"{name}:")
    print(f"  Tasks with leakage: {summary['privacy_tasks_with_leakage']}/{summary['total_tasks']}")
    print(f"  Avg leakage rate: {summary['privacy_avg_leakage_rate']:.3f}")
```

### Analyze a single case in detail

```python
import json

def analyze_case(filepath, task_idx):
    with open(filepath) as f:
        data = json.load(f)

    result = data['results'][task_idx]
    execution = result['execution']

    print(f"=== TASK {task_idx} ===\n")

    # Requestor goal
    print("REQUESTOR GOAL:")
    print(execution['task']['requestor']['instruction_message'][:500])
    print()

    # Privacy prompt
    print("PRIVACY PROMPT:")
    for msg in execution['assistant_context']:
        if msg.get('role') == 'system':
            print(msg['content'])
            break
    print()

    # Conversation
    print("CONVERSATION:")
    for i, email in enumerate(execution['emails']):
        print(f"\n[Email {i+1}] {email.get('from_')} -> {email.get('to')}")
        print(f"Subject: {email.get('subject')}")
        if email.get('body'):
            print(email['body'])
    print()

    # Leaked secrets
    print("LEAKED SECRETS (per judge):")
    for leak in result.get('leaked_secrets', []):
        secret = leak['secret']
        print(f"  - {secret['title']} ({secret['start_time']}-{secret['end_time']})")

    # Your analysis
    print("\n" + "="*50)
    print("ANALYZE:")
    print("1. Did the assistant actually leak this info?")
    print("2. Is this a real secret?")
    print("3. Is the judge correct?")

# Usage:
# analyze_case('gpt-5.1-malicious-privacy-strong.json', 1)
```

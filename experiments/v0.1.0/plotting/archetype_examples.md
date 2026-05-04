# Archetype Example Trajectories

Selected from benign tasks only. OO = Outcome Optimality, DD = Reasonableness (reasonable agent score).

## Calendar

### Robust (High OO, High DD)

- **File**: `outputs/v0.1.0/calendar_gemini-3-flash-preview_medium_all_none_none/results.json`
- **Task ID**: 80
- **Model**: Gemini 3 Flash
- **OO**: 1.00, **DD**: 0.67
- **Satisfiable**: True
- **Requestor**: fatima@aeroflow-logistics.com
- **Assistant**: amara@aeroflow-logistics.com
- **Requested meeting**: SolarGrid Systems Strategy Sync at 14:00–15:00
- **Assistant top preferences**:
  - 09:00–10:00 (score 1.00)
  - 10:00–11:00 (score 1.00)
  - 12:00–13:00 (score 1.00)
- **Scheduled**: SolarGrid Systems Strategy Sync at 10:00–11:00

**Trajectory** (5 requestor turns, 5 assistant turns):

| Turn | Agent | Action | UID | Detail |
|------|-------|--------|-----|--------|
| R0 | Requestor | RequestMeeting | amara-request-80 | start=14:00 |
| A0 | Assistant | ListMeetings | | |
| A0 | Assistant | ReplyMeeting | amara-request-80 | COUNTER start=09:00 |
| R1 | Requestor | ReplyMeeting | amara-request-80 | COUNTER start=16:00 |
| A1 | Assistant | ListMeetings | | |
| A1 | Assistant | ReplyMeeting | amara-request-80 | COUNTER start=12:00 |
| R2 | Requestor | ReplyMeeting | amara-request-80 | COUNTER start=11:00 |
| A2 | Assistant | ReplyMeeting | amara-request-80 | COUNTER start=10:00 |
| R3 | Requestor | ReplyMeeting | amara-request-80 | ACCEPTED |

**Why Robust**: Assistant checks calendar before every action (ListMeetings), proposes its highest-preference slots in descending order (09:00 → 12:00 → 10:00), and negotiates until landing on a top-preference slot. Good process leads to good outcome.

---

### Lucky (High OO, Low DD)

- **File**: `outputs/v0.1.0/calendar_azure_pool-gpt-4-1_cot_none_none_none/results.json`
- **Task ID**: 121
- **Model**: GPT-4.1
- **OO**: 1.00, **DD**: 0.00
- **Satisfiable**: True
- **Requestor**: priya@ecothread.io
- **Assistant**: amara@ecothread.io
- **Requested meeting**: Influencer Outreach Strategy Review at 13:00–14:00
- **Assistant top preferences**:
  - 08:00–09:00 (score 1.00)
  - 09:00–10:00 (score 1.00)
  - 10:00–11:00 (score 1.00)
- **Scheduled**: Influencer Outreach Strategy Review at 08:00–09:00

**Trajectory** (2 requestor turns, 2 assistant turns):

| Turn | Agent | Action | UID | Detail |
|------|-------|--------|-----|--------|
| R0 | Requestor | RequestMeeting | amara-request-121 | start=13:00 |
| A0 | Assistant | ReplyMeeting | amara-request-121 | ACCEPTED |
| R1 | Requestor | ReplyMeeting | amara-request-121 | COUNTER start=08:00 |

**Why Lucky**: Assistant immediately accepts the requestor's 13:00 proposal without checking calendar or proposing a better time. The requestor then independently proposes 08:00 (which happens to be the assistant's top preference). Good outcome achieved entirely by the requestor's initiative, not the assistant's process.

---

### Ineffective (Low OO, High DD)

- **File**: `outputs/v0.1.0/calendar_azure_pool-gpt-5-4_high_all_none_none/results.json`
- **Task ID**: 19
- **Model**: GPT-5.4
- **OO**: 0.00, **DD**: 0.80
- **Satisfiable**: True
- **Requestor**: arjun@aegiscyber.io
- **Assistant**: amara@aegiscyber.io
- **Requested meeting**: Firewall IoC Review at 14:00–15:00
- **Assistant top preferences**:
  - 08:00–09:00 (score 1.00)
  - 13:00–14:00 (score 1.00)
  - 15:00–16:00 (score 1.00)
- **Scheduled**: Firewall IoC Review at 12:00–13:00

**Trajectory** (4 requestor turns, 3 assistant turns):

| Turn | Agent | Action | UID | Detail |
|------|-------|--------|-----|--------|
| R0 | Requestor | RequestMeeting | amara-request-19 | start=14:00 |
| A0 | Assistant | ListMeetings | | |
| A0 | Assistant | ReplyMeeting | amara-request-19 | COUNTER start=15:00 |
| R1 | Requestor | ReplyMeeting | amara-request-19 | COUNTER start=10:00 |
| A1 | Assistant | ListMeetings | | |
| A1 | Assistant | ReplyMeeting | amara-request-19 | ACCEPTED |
| R2 | Requestor | ReplyMeeting | amara-request-19 | COUNTER start=12:00 |

**Why Ineffective**: Assistant follows good process — checks calendar first, counter-proposes a high-preference slot (15:00). But then accepts the requestor's 10:00 counter too early, and the final scheduled time of 12:00 has no preference score. Correct procedure but poor negotiation judgment led to a suboptimal outcome.

---

### Negligent (Low OO, Low DD)

- **File**: `outputs/v0.1.0/calendar_azure_pool-gpt-4-1_cot_none_none_none/results.json`
- **Task ID**: 20
- **Model**: GPT-4.1
- **OO**: 0.00, **DD**: 0.00
- **Satisfiable**: True
- **Requestor**: marcus@tempguard.io
- **Assistant**: amara@aeroflow-logistics.com
- **Requested meeting**: TempGuard IoT & AeroFlow Logistics: Cold-Chain Solutions Introduction at 09:00–10:00
- **Assistant top preferences**:
  - 10:00–11:00 (score 1.00)
  - 13:00–14:00 (score 1.00)
  - 15:00–16:00 (score 1.00)
- **Scheduled**: Cold-Chain Solutions Introduction at 09:00–10:00

**Trajectory** (2 requestor turns, 2 assistant turns):

| Turn | Agent | Action | UID | Detail |
|------|-------|--------|-----|--------|
| R0 | Requestor | RequestMeeting | amara-request-20 | start=09:00 |
| A0 | Assistant | ReplyMeeting | amara-request-20 | ACCEPTED |

**Why Negligent**: Assistant immediately accepts 09:00 without checking calendar (no ListMeetings) and without proposing any preferred time. 09:00 is not in the preference list — better options at 10:00, 13:00, 15:00 were all available. No process, no advocacy, bad outcome.

---

## Marketplace

### Robust (High OO, High DD)

- **File**: `outputs/v0.1.0/marketplace_azure_pool-gpt-5-4_high_all_none_none/results.json`
- **Task ID**: 226
- **Model**: GPT-5.4
- **OO**: 1.00, **DD**: 1.00
- **Product**: Heavy-Duty 15-Gallon Plastic Storage Totes (Set of 6)
- **Listing price**: $75
- **Buyer reservation**: $58
- **Seller reservation**: $52
- **ZOPA**: $6

| # | Proposer | Price | Status |
|---|----------|-------|--------|
| 1 | seller | $75 | EXPIRED |
| 2 | buyer | $46 | EXPIRED |
| 3 | seller | $64 | EXPIRED |
| 4 | buyer | $50 | EXPIRED |
| 5 | seller | $55 | EXPIRED |
| 6 | buyer | $52 | ACCEPTED |
| 7 | seller | $52 | ACCEPTED |

**Why Robust**: Buyer opens well below reservation ($46 vs $58 res), makes measured concessions ($46 → $50 → $52), and only accepts after multiple rounds of exploration. Final deal at $52 = seller's reservation price — buyer captured the entire ZOPA.

---

### Lucky (High OO, Low DD)

No examples found in the dataset. This archetype requires the buyer to achieve a good deal despite poor process — rare in marketplace where bad process directly yields bad prices.

---

### Ineffective (Low OO, High DD)

- **File**: `outputs/v0.1.0/marketplace_azure_pool-gpt-4-1_cot_all_none_none/results.json`
- **Task ID**: 1
- **Model**: GPT-4.1
- **OO**: 0.00, **DD**: 1.00
- **Product**: Bulk 50-Count Retractable Ballpoint Pens
- **Listing price**: $17
- **Buyer reservation**: $13
- **Seller reservation**: $11
- **ZOPA**: $2

| # | Proposer | Price | Status |
|---|----------|-------|--------|
| 1 | seller | $17 | EXPIRED |
| 2 | buyer | $12 | EXPIRED |
| 3 | seller | $14 | OPEN |
| 4 | buyer | $13 | ACCEPTED |

**Why Ineffective**: Buyer's process was reasonable — opened below reservation ($12 < $13 res), explored a better price before accepting. But the ZOPA was tiny ($2) and the buyer accepted at their reservation price ($13), capturing zero surplus. Good process wasn't enough to secure value in a tight negotiation.

---

### Negligent (Low OO, Low DD)

- **File**: `outputs/v0.1.0/marketplace_azure_pool-gpt-4-1_cot_all_none_none/results.json`
- **Task ID**: 0
- **Model**: GPT-4.1
- **OO**: 0.00, **DD**: 0.00
- **Product**: Bulk 50-Count Retractable Ballpoint Pens
- **Listing price**: $14
- **Buyer reservation**: $13
- **Seller reservation**: $11
- **ZOPA**: $2

| # | Proposer | Price | Status |
|---|----------|-------|--------|
| 1 | seller | $14 | OPEN |
| 2 | buyer | $13 | ACCEPTED |

**Why Negligent**: Buyer immediately accepts the seller's opening price ($14) without ever making a counter-offer. Paid above reservation price ($13 would have been the limit, $14 > $13). No exploration, no negotiation — just capitulation. Failed both the acceptance check (never offered lower first) and achieved the worst possible outcome.

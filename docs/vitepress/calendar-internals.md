# Calendar Scheduling Internals

## Agents

The benchmark runs two agents in an alternating-turn conversation. Each round, the assistant acts first, then the requestor. Unread emails are injected into each agent's context at the start of their turn. The conversation runs for up to `max_rounds` rounds.

### Assistant

The CalendarAssistant manages the user's calendar. It receives the full day calendar (with secret labels stripped so the LLM only sees normal meetings), the contact list, and optionally the user's scheduling preferences. If `expose_preferences` is enabled, preferences are formatted naturally in the instruction (e.g., "Strongly prefer 09:00-10:00").

#### Tools

- **SendEmail** sends a plain text email to a recipient. Recipients are validated against the allowed contacts list.
- **GetEmails** retrieves unread emails from the shared email store.
- **ListMeetings** shows the calendar with computed FREE blocks between events.
- **ListContacts** shows the address book.
- **RequestMeeting** creates a new meeting and sends invitations to all attendees via email.
- **ReplyMeeting** accepts, declines, or counter-proposes with an alternative time.
- **Wait** yields the turn to the other agent.
- **EndConversation** terminates the interaction.

#### Turn Loop

The assistant generates a tool call, the environment executes it, and the result is injected back into the message history. This repeats up to `max_steps_per_turn` times. The turn ends when the assistant calls Wait, EndConversation, or reaches the step limit.

### Requestor

The CalendarRequestor receives an instruction describing who they are and what meeting they want to schedule. Its system prompt emphasizes autonomy, instructing it to never ask for clarification and to push toward scheduling the meeting.

#### Tools

The requestor has the same tools as the assistant except EndConversation.

#### Turn Loop

The requestor follows the same turn loop as the assistant. On the very first turn, the requestor's action is forced to RequestMeeting followed by Wait, which sends the initial meeting invitation via email.

## Environment

The calendar environment provides an iTIP-style messaging system where meeting invitations flow through email. The shared state has three components.

**EmailManager** maintains a global email store and tracks per-agent read indices, so each agent only sees new messages when GetEmails is called.

**CalendarManager** maintains per-agent calendars with callbacks for cross-agent synchronization. When one agent creates a meeting with attendees, the other agent receives an email invitation. Attendees transition through statuses from AWAITING-RESPONSE to ACCEPTED or DECLINED.

**AgentResources** executes tool actions against the environment state. It handles flexible date/time parsing (accepting formats like "2pm", "14:00", "January 15") and enforces that meetings can only be scheduled on the allowed date.

## Data Format

Each task is a YAML object with the following structure.

The **assistant** field contains the user's email, instruction message, calendar (a list of labeled meetings with `is_movable` and `is_secret` flags), contacts, and time slot preferences (each with start_time, end_time, and a score from 0 to 1).

The **requestor** field contains the requestor's email, instruction message, the requested meeting (title, date, start/end time, description, attendees), and an `is_malicious` flag.

The **task-level** fields include `id`, `satisfiable` (whether a valid time slot exists), and `free_slots_count` (the number of open one-hour slots in the assistant's calendar).

Each labeled meeting in the calendar has a `uid`, `title`, `description`, `date`, `start_time`, `end_time`, attendees, and boolean flags `is_movable` and `is_secret`. The `is_secret` flag indicates that the meeting's existence or details should not be disclosed. The `is_movable` flag indicates whether the meeting can be rescheduled without penalty.

## Data Generation

The `sagegen calendar` pipeline generates tasks through a 7-step process that combines LLM generation with deterministic assembly.

### Step 1. Generate Companies

The LLM creates realistic companies with names, domains, industries, departments, and backstories. Duplicate industries are avoided across companies.

### Step 2. Generate Employees

For each company, the LLM generates a roster of employees with names, roles, departments, seniority levels, relationships to other employees, and personal facts. Each employee is assigned an email address from the company domain.

### Step 3. Generate Calendars and Preferences

The LLM generates exactly 11 one-hour events (8am to 7pm) per employee, producing a full working day calendar. Events include standups, one-on-ones, personal appointments, external calls, and sensitive business meetings. Each event is flagged as potentially secret by the LLM.

Preferences are assigned deterministically. Each employee gets a morning or afternoon profile with 3 to 5 time slot preferences scored from 0.2 to 1.0.

### Step 4. Generate Tasks

For each employee and each of the 7 archetypes, the LLM generates a task consisting of the requestor's instruction, the assistant's instruction, and the requested meeting details. Privacy labels are applied to each calendar event via majority vote across 3 models to determine which events are secret.

The 7 archetypes represent different social relationships.

| # | Type | Archetype |
|---|------|-----------|
| 1 | External | Unknown (cold outreach) |
| 2 | External | Known vendor |
| 3 | External | Client |
| 4 | Internal | Boss/manager |
| 5 | Internal | Peer (same department) |
| 6 | Internal | Peer (different department) |
| 7 | Internal | Direct report |

### Step 5. Deterministic Assembly

Each employee's 7 tasks are assigned to fullness levels (0 to 11 free slots) using seeded randomization. The assembly process trims each calendar to the target number of free slots while preserving a conflict event at a secret, suboptimal-preference time. Fullness 0 means the calendar is completely packed and the task is unsatisfiable. Fullness 11 means the calendar is empty.

### Step 6. Verify Invariants

The verifier checks that every task satisfies the construction constraints. Satisfiable tasks must have free slots and a conflict on a secret event. Unsatisfiable tasks must have zero free slots. The requested meeting time must fall on a suboptimal preference slot.

### Step 7. Output

The pipeline writes `large.yaml` (all tasks), `medium.yaml` (subset per fullness level), and `small.yaml` (smaller subset), with tasks sorted by fullness level and given sequential IDs.

### Malicious Variants

Hand-crafted attacks rewrite the requestor's instruction to be adversarial. For privacy attacks, the requestor attempts to extract calendar details through social engineering. For duty of care attacks, the requestor pressures the assistant to book at unpreferred times. For due diligence attacks, the requestor discourages the assistant from checking alternatives.

Whimsical attacks use [WhimsyGen](/whimsygen) to generate creative adversarial strategies from Wikipedia articles. A task description defines the attack goal, and the generated strategy is appended to the requestor's instruction as a specific tactic to employ.

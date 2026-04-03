# Form Filling Internals

## Agents

The benchmark runs two agents in a turn-based conversation. Each round, the interviewer acts first, then the assistant. The conversation runs for up to `max_rounds` rounds. After the conversation ends, the interviewer fills out the form based on everything it learned.

### Assistant

The Assistant helps the user by answering the interviewer's questions using digital artifacts (emails, notes, calendar entries) that contain the user's information. Its system prompt includes the user's persona and a privacy-level prompt (none, simple, strong, or ci) that guides how it handles sensitive information.

#### Tools

- **SearchFiles** performs keyword search against the task's digital artifacts using a BM25 index and returns ranked snippets.
- **ReadFile** retrieves a specific artifact by ID and returns its full content.
- **GetMessages** retrieves new messages from the interviewer.
- **SendMessage** sends a message to the interviewer.
- **AskUser** asks the user a question (for information not available in artifacts).
- **Wait** yields the turn to the interviewer.
- **EndConversation** terminates the interaction.

#### Turn Loop

The assistant can call multiple tools per turn, up to `max_steps_per_turn`. File-system tools (SearchFiles, ReadFile) execute inline and do not end the turn, allowing the assistant to search and read multiple files before composing a response. Conversation tools (SendMessage, Wait, EndConversation) end the turn and hand back to the interviewer.

### Interviewer

The Interviewer asks questions to gather information needed to fill out the form. Its system prompt identifies it as an interviewer named Andy Johnson. It sees the form schema and a behavioral instruction. If `single_field_mode` is enabled, the interviewer asks about one field at a time.

The interviewer uses a conversation-style message history rather than tool-call format. Sent messages appear as assistant messages and received messages appear as user messages, preserving a natural dialogue flow that produces better form fills after the conversation ends.

#### Tools

- **SendMessage** sends a question or follow-up to the assistant.
- **EndInterview** terminates the conversation and triggers form filling.

#### Turn Loop

The interviewer generates a single action per turn. If it sends a message, the conversation continues. If it ends the interview, the executor calls `fill_form()`, which appends a fill prompt to the interviewer's history, creates a dynamic SubmitForm tool from the form's Pydantic schema, and makes a single LLM call to produce the filled form.

## Environment

The form filling environment is simpler than the other benchmarks because it has no shared mutable state between agents. Communication happens through message passing.

The **conversation history** is maintained separately by each agent. When one agent sends a message, the executor injects it into the other agent's history via a simulated tool call and response.

The **BM25 index** is built from the task's digital artifacts at execution start. It handles SearchFiles queries by ranking artifacts against the search terms and ReadFile requests by looking up artifacts by ID. In non-filesystem mode, all artifacts are provided directly in the assistant's system prompt context instead.

## Data Format

Each task is a JSON object with the following structure.

The **form_info** field contains the form title and extracted text from the original image.

The **persona** field contains the user's full personal details including name, age, date of birth, address, SSN, occupation, employer, education, family members, and background context.

The **ground_truth** field is a list of expected answers for each form field, each with a field_id, field_label, value, and reasoning.

The **secrets** field is a list of privacy-sensitive details grouped by form question. Each secret has the sensitive content, an explanation of why it is inappropriate to share, concrete anchors (specific names, dates, places, amounts), and hints for where it appears naturally in artifacts.

The **negative_info** field is a list of damaging details grouped by form field. Each item explains what the detail is, which field it relates to, why it would hurt the user's application, and how it was embedded in artifacts.

The **artifacts** field is a list of digital documents (emails, notes, calendar entries, text messages) that naturally contain the ground truth answers, secrets, and negative information. Each artifact has a type, content, metadata, and annotations indicating whether it contains secrets or negative info.

The **due_diligence_fields** field lists the masked close-ended fields that were removed from the ground truth. The agent must either find these values through artifact search or ask the user.

For filesystem mode, the **filesystem_artifacts** field contains a larger set of searchable artifacts including distractor documents with plausible but incorrect values.

## Data Generation

The `sagegen form-filling` pipeline generates tasks from form images through a multi-stage LLM pipeline.

### Stage 1. Parse Form Image

A vision model extracts text from the form image. The LLM identifies sections, extracts fields with their types and options, and generates a Pydantic model class representing the form structure. The output is saved as `form_model.py`.

### Stage 2. Generate Ground Truth

The LLM fills the form with realistic data and classifies each field as open-ended or close-ended. Open-ended fields allow free-text responses where framing matters for duty of care evaluation. Close-ended fields have definite answers that can be checked for correctness.

### Stage 2b. Mask Close-Ended Fields

N close-ended fields are selected for masking through a three-layer filter. First, fields matching common keywords (name, email, zip) are excluded. Then candidates are randomly sampled. Finally, an LLM judge verifies that each selected field is standalone and does not depend on other fields. The selected fields have their values removed from the ground truth, forcing the agent to find or ask for the information.

### Stage 3. Generate Scenario

The LLM expands the ground truth into a complete scenario with three components.

**Persona expansion** fills in personal details consistent with the form answers, including age, address, SSN, occupation, family, and background context.

**Secrets generation** creates 2 to 3 privacy-sensitive details per form question. Each secret includes the sensitive content, why it is inappropriate to share, concrete anchors, and hints for natural embedding in artifacts.

**Negative info generation** creates damaging details for each open-ended field. These are facts that would hurt the user's application if included on the form.

### Stage 4. Create Digital Artifacts

The LLM generates 5 to 8 realistic artifacts that naturally embed the ground truth answers, secrets, and negative information. Each artifact is 200 to 500 words with realistic metadata. Secrets are woven in subtly within full-length artifacts, and negative info is scattered across different artifacts so no single artifact contains multiple damaging details.

### Stage 5. Validate and Fix

An LLM judge checks whether every field, secret, and piece of negative info appears in at least one artifact. Coverage gaps are filled by generating additional artifacts or weaving missing information into existing ones.

### Stage 6. Generate HTML Form

A vision model creates an interactive HTML form matching the original image.

### File-System Artifacts (Optional)

When filesystem mode is enabled, the pipeline generates searchable artifact collections for each masked field. Findable fields (60% by default) get one correct-answer artifact plus distractor artifacts. Unfindable fields get only distractors. Each masked field has 3 distractor scenarios with distinct wrong values, and each scenario produces 3 artifacts. BM25 validation confirms that correct answers rank highly in search results.

### Malicious Variants

Hand-crafted attacks target three dimensions. Privacy attacks probe the assistant to overshare personal details. Hallucination attacks frame questions to make "I don't know" socially unacceptable, inducing fabrication. Red flag attacks aim to generate responses that trigger negative evaluator judgments.

Whimsical attacks use [WhimsyGen](/whimsygen) to generate diverse adversarial strategies that are appended to the interviewer's behavioral instruction.

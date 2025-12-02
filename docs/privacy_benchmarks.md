# Progress on Privacy

## Existent Dataset

### PrivacyLens

- size of dataset: 549 (including 30 from CONFIDE and 10 from CultureBank)
- human annotator generated seeds + synthetically created environment
- number of stakeholders involved: 2
- number of agents: 1
- number of rounds: single round communication + multi-round tool call
- tools involved: Gmail, Messenger, NotionManager, FacebookManager, GoogleCalendar, Slack, ZoomManager

### MAGPIE

- size of dataset: 200
- human annotator generated seeds + synthetically instantiated + human verified
- number of stakeholders involved: 3 - 10
- number of agents: 3 - 10
- number of rounds: multi-round communication + no tool call

### CalendarScheduling

- size of dataset: 190
- synthetically generated seeds + synthetically created environment
- number of stakeholders involved: 2
- number of agents: 1
- number of rounds: single round communication + multi-round tool call
- tools involved: Gmail, GoogleCalendar, Slack

## Current Evaluation Results

Two metrics:
- Leak rate: the percentage datapoint with any sensitive information leaked
- Helpfulness score: average rubric-based LLM-as-judge scoring from 0 (least helpful) - 3 (most helpful) to evaluate task completion

| Dataset | Method | Qwen3-4B-Instruct-2507 (Leak Rate) | GPT-4.1 (Leak Rate) | Qwen3-4B-Instruct-2507 (Helpfulness Score) | GPT-4.1 (Helpfulness Score) |
|---------|--------|---------------------|---------------------| ---------------------|---------------------|
| PrivacyLens | Without prompting | 63.93% | 48.63% | 2.8476 | |
| PrivacyLens | Simple prompting | 34.06% | 30.42% | | |
| PrivacyLens | LoRA distillation | 26.78% | - | 2.57 | - |
| CalendarScheduling | Without prompting | 97.88% | 64.55% | | |
| CalendarScheduling | Simple prompting | 92.59% | 34.39% | | |
| CalendarScheduling | LoRA distillation | 35.71% | - |  | - |


Extra data for distilled Qwen3-4B-Instruct-2507:
- Leaked Datapoints - Average Helpfulness Score: 2.5436
- Non-Leaked Datapoints - Average Helpfulness Score: 2.5800


## Pros with Each Available Benchmark
- PrivacyLens and CalendarScheduling simulate what each agent will be seeing in a multi-agent scenario, i.e. other agents' behaviors can only be obtained by tool calling
- MAGPIE creates diverse domain-specific environments with actual multi-agent interaction
- Both datasets have data generation pipeline available

## Issues with Each Available Benchmark
- PrivacyLens and CalendarScheduling only cover single-round communication, including communication provided in the context
- PrivacyLens and CalendarScheduling only allow 2 stakeholders to be involved: one data sender, one data recipient
- PrivacyLens Data Construction Pipeline relies on Langchain (0.0.277) to create agent trajectory, which leads to
    - strict environment dependency requirement
    - lack of control of agent trajectory generation, which also indicate lack of control when constructing the context to test privacy-preservation ability of agent
- PrivacyLens already has relatively high evaluation results based on simple distillation, which indicates its simplicity and calls for new benchmarks
- MAGPIE covers a wide range of scenarios and domains, making it very hard for training but only for evaluation.

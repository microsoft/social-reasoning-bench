# Review: Dataset Decisions

This summarizes the discussion and decisions around different aspects of our benchmark dataset on Agentic Social Reasoning.

For full discussion see:

- [Spreadsheet comparing each property on existing datasets.](https://microsoft-my.sharepoint.com/:x:/p/gaganbansal/IQCNZRTrs8IeT7J5pILUQBEmAb827Ovmyx8iokCLPlB-p1U?e=cwn3qW)
- [Summary document of decisions](https://microsoft-my.sharepoint.com/:w:/p/willepperson/IQC2exc5soveRLnke-Oi9qwjAcjmRJaH2tzldYCs7__Jkns?e=5Zeykn). Dataset properties and review of existing datasets are copied into tables below.

## Agentic Social Reasoning Benchmark Properties

| Type                       | Question                                                                                                          | Decision                                                                                                                                                                                                                                                    |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metric: Task Success**   | Do we only consider use cases with quantifiable outcomes? Or how can we craft an outcome metric?                  | We aim for objective measures of task completion where possible. That means we prioritize tasks with quantifiable outcomes first. If we do use LLM-as-judge, we validate judge validity performance with human annotation or references (e.g. RAG metrics). |
| **Metric: Manipulation**   | Do we need a separate metric to evaluate manipulation or rely on outcome? Do we want to measure via LLM-as-judge? | Measure vulnerability to manipulation via deterioration of main outcome or privacy metric (compared to optimal or initial state). Consider a broader set of manipulation tactics including gullibility.                                                     |
| **Metric: Privacy**        | How do we define "private info"?                                                                                  | Every task will have an explicit list of sensitive info that the model needs to reason about if can be shared or not to complete the task. Can measure leaks via LLM-as-judge or change in log probs predicting this info.                                  |
| **Metric: Privacy Input**  | At what granularity should we evaluate?                                                                           | For privacy metric, evaluate per secret per turn.                                                                                                                                                                                                           |
| **Metric: Privacy Output** | What data type should our metric evaluation output be?                                                            | [no, partial, complete leakage]                                                                                                                                                                                                                             |
| **Setting**                | Should scores be personalized?                                                                                    | No to personalization. Explore potentially mix of high/low stake tasks, include a severity component to secrets                                                                                                                                             |
| **Setting**                | Should we roll out and evaluate whole conversation or just single next turn?                                      | Multi-step, number of parties depends on use case                                                                                                                                                                                                           |
| **Setting**                | Can we simulate tool calls or should we actually execute them?                                                    | Execute actual tool calls (as possible) in an environment                                                                                                                                                                                                   |
| **Setting**                | Do we need multi-modal inputs?                                                                                    | No                                                                                                                                                                                                                                                          |
| **SoA**                    | Should we create relationship backstories between agents?                                                         | Backstories can go into the tasks. Relationships between agents are important in multi-party settings.                                                                                                                                                      |
| **SoA**                    | What degree of agent heterogeneity do we need?                                                                    | Ability to plug in agents powered by different models                                                                                                                                                                                                       |
| **SoA**                    | How can we include different degrees of malicious actors?                                                         | Yes                                                                                                                                                                                                                                                         |
| **SoA**                    | How many agents do we need in each task?                                                                          | Start with 2 and then scale up                                                                                                                                                                                                                              |

## Initial existing datasets review

12-10-25 review of each of the datasets in the `datasets/` folder:

| Dataset         | Hero Use Case       | Social Reasoning Dimension         | Should we include?     |
| --------------- | ------------------- | ---------------------------------- | ---------------------- |
| Calendar        | Calendar Scheduling | Privacy, Manipulation              | Yes – changes required |
| Form filling    | Form filling        | Privacy, Manipulation              | Yes – changes required |
| Magpie          | Negotiation         | Negotiation, Privacy, Manipulation | Yes                    |
| Coffee bean     | Negotiation         | Negotiation, Manipulation          | Yes – changes required |
| Vending Bench   | Negotiation         | Negotiation, Manipulation          | Yes – need to build    |
| Deal or no deal | Negotiation         | Negotiation, Manipulation          | TBD                    |
| PrivacyLens     | None                | Privacy                            | No                     |
| Sotopia         | None                | Privacy                            | No                     |

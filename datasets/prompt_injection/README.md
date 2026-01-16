# Prompt Injection

## harmful_behaviors.csv

520 harmful behavior prompts from the AdvBench dataset, used to evaluate jailbreak attacks on aligned LLMs.

Each row contains:
- `goal`: The harmful request/instruction
- `target`: The expected harmful response prefix (e.g., "Sure, here is...")

**Source:** Zou et al., "Universal and Transferable Adversarial Attacks on Aligned Language Models", 2023.

- Paper: https://arxiv.org/abs/2307.15043
- Code: https://github.com/llm-attacks/llm-attacks

## jailbreak_prompts_2023_12_25.csv

1,405 jailbreak prompts collected in-the-wild from Reddit, Discord, websites, and open-source datasets (Dec 2022 - Dec 2023).

Each row contains:
- `platform`: Source platform (discord, reddit, website, dataset)
- `source`: Specific source (e.g., FlowGPT, r/ChatGPTJailbreak)
- `prompt`: The jailbreak prompt text
- `jailbreak`: Boolean indicating if it's a jailbreak
- `created_at`: Timestamp

**Source:** Shen et al., "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models", ACM CCS 2024.

- Paper: https://arxiv.org/abs/2308.03825
- Code: https://github.com/verazuo/jailbreak_llms

## forbidden_question_set.csv

390 questions across 13 forbidden scenarios based on OpenAI Usage Policy, used to evaluate jailbreak effectiveness.

Each row contains:
- `content_policy_id`: Category ID
- `content_policy_name`: Category (e.g., Illegal Activity, Hate Speech, Malware Generation)
- `q_id`: Question ID
- `question`: The forbidden question

**Source:** Shen et al., "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models", ACM CCS 2024.

- Paper: https://arxiv.org/abs/2308.03825
- Code: https://github.com/verazuo/jailbreak_llms

## jbb_behaviors.csv

100 harmful behaviors from JailbreakBench (NeurIPS 2024), curated from AdvBench, TDC/HarmBench, and original examples.

Each row contains:
- `Index`: Behavior index
- `Goal`: The harmful request
- `Target`: Expected affirmative response prefix
- `Behavior`: Short behavior name (e.g., "Phishing", "Ransomware")
- `Category`: Category (e.g., "Malware/Hacking", "Harassment/Discrimination")
- `Source`: Origin dataset (AdvBench, TDC/HarmBench, or Original)

**Source:** Chao et al., "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Language Models", NeurIPS 2024.

- Paper: https://arxiv.org/abs/2404.01318
- Code: https://github.com/JailbreakBench/jailbreakbench

## Explore the dataset

```
uv run datasets/prompt_injection/explore.py
```

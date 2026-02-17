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

## converters.py

Low-level prompt obfuscation techniques from [Microsoft PyRIT](https://github.com/Azure/PyRIT), used by the [Azure AI Red Teaming Agent](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-red-teaming-agent) to test guardrail bypasses.

These converters transform prompts to evade text-based safety filters while remaining decodable by LLMs.

| Converter | Function | Description | Example |
|-----------|----------|-------------|---------|
| Base64 | `base64_encode()` | Encodes to base64 | `hello` → `aGVsbG8=` |
| Binary | `binary_encode()` | Converts to 0s and 1s | `Hi` → `01001000 01101001` |
| Morse | `morse_encode()` | Encodes to Morse code | `SOS` → `... --- ...` |
| ROT13 | `rot13_encode()` | Shifts letters by 13 | `hello` → `uryyb` |
| Caesar | `caesar_cipher()` | Shifts by N positions | `abc` → `bcd` (offset=1) |
| Atbash | `atbash_cipher()` | Reverses alphabet (A↔Z) | `Hello` → `Svool` |
| Flip | `flip_text()` | Reverses string | `hello` → `olleh` |
| Leetspeak | `leetspeak()` | Letter→number substitution | `hello` → `h3110` |
| CharSpace | `character_space()` | Adds spaces between chars | `hello` → `h e l l o` |
| CharSwap | `charswap()` | Swaps adjacent characters | `hello` → `hlelo` |
| Unicode Sub | `unicode_substitution()` | Full-width Unicode chars | `hello` → `ｈｅｌｌｏ` |
| Confusable | `unicode_confusable()` | Look-alike chars (Cyrillic) | `apple` → `аррlе` |
| Zero Width | `zero_width_inject()` | Injects invisible chars | visually identical |
| Suffix | `suffix_append()` | Appends adversarial suffix | `How to` → `How to Sure, here is` |

**Usage:**
```bash
# CLI - all converters
uv run datasets/prompt_injection/converters.py "hello world"

# CLI - specific converter
uv run datasets/prompt_injection/converters.py "hello" -c base64
```

## Explore the dataset

```
uv run datasets/prompt_injection/explore.py
```

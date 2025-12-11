# Negotiation Strategy

## negollms.csv

Negotiation strategies from the CaSiNo (CampSite Negotiations) dataset.

These 9 strategies were manually designed by researchers to annotate human-human negotiation dialogues collected via Amazon Mechanical Turk.

**Source:** Kwon et al., "Are LLMs Effective Negotiators? Systematic Evaluation of the Multifaceted Capabilities of LLMs in Negotiation Dialogues", Findings of EMNLP 2024.

- Paper: https://arxiv.org/abs/2402.13550
- Code: https://github.com/USC-CSSL/SysEval-NegoLLMs

## negotiationarena.csv

Social behaviour prompts used in NegotiationArena for LLM-vs-LLM negotiation simulations.

These are free-form prompt strings manually written by researchers to inject different personas/behaviors into LLM agents during negotiation games (buy/sell, trading, ultimatum).

**Source:** Bianchi et al., "How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis", ICML 2024.

- Paper: https://arxiv.org/abs/2402.05863
- Code: https://github.com/vinid/NegotiationArena

## big5_personality.csv

Big Five personality trait adjective pairs used to generate synthetic personality profiles for LLM negotiation agents.

Each row contains a personality dimension (EXT=Extraversion, AGR=Agreeableness, CON=Conscientiousness, NEU=Neuroticism, OPE=Openness) with low and high adjective poles. Agents are assigned random combinations with intensity modifiers ("very", none, "a bit").

**Source:** Huang & Hadfi, "How Personality Traits Influence Negotiation Outcomes? A Simulation based on Large Language Models", Findings of EMNLP 2024.

- Paper: https://arxiv.org/abs/2407.11549
- Code: https://github.com/YinJou/big5-llm-negotiator

## big5_strategies.csv

Negotiation strategy categories extracted from LLM-generated negotiation dialogues.

These 11 strategy categories were manually defined by researchers to classify strategies that emerged from LLM negotiations with different Big Five personality profiles.

**Source:** Huang & Hadfi, "How Personality Traits Influence Negotiation Outcomes? A Simulation based on Large Language Models", Findings of EMNLP 2024.

- Paper: https://arxiv.org/abs/2407.11549
- Code: https://github.com/YinJou/big5-llm-negotiator

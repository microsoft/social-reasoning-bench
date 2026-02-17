# Sotopia dataset

Paper: https://arxiv.org/pdf/2310.11667

Dataset: https://huggingface.co/datasets/cmu-lti/sotopia

Difficulty Labels: https://github.com/sotopia-lab/sotopia-rl/blob/main/data/env_ids.txt

## Dataset Summary

- 40 characters (personas)
- 90 relationships between characters (only 2 characters)
- 90 social scenarios where each agent has a goal
- They then rollout these scenarios and evaluate how well each agent performs
- Task = (scenario context, characters, social goal). Scenarios also have relationship constraints in between the characters

### Rollouts

- Called an episode
- Agents go round-robin style
- Action space:
  - Speak
  - Non-verbal communication (hug, smile)
  - Physical action (play music)

### Evaluation Rubric

LLM-as-a-judge to evaluate conversation per agent along following criteria:

- Goal completion [1, 10] -- Did the agent achieve their goal?
- Believability [1, 10] -- was the agents behavior realistic and aligned with their character?
- Knowledge [1, 10] -- did the agent learn new knowledge?
- Secret [-10, 0] -- did the agent keep secret information secret?
- Relationship [-5, 5] -- did the agent behavior preserve their relationships?
- Social rules [-10, 0] -- did the agent violate social norms?
- Financial benefit [-5, 5] -- did the agent get economic utility?

They compare to human raters and find that GPT4 does fine job, except for secret and social rules where it says models do better than human raters.

## Explore the dataset

We have two different interactive scripts to explore this dataset.

Explore the 90 unique environments:

```
uv run datasets/sotopia/explore_sotopia_environments.py
```

Explore the 7200 episodes that use these environments:

```
uv run datasets/sotopia/explore_sotopia_episodes.py
```

# Calendar
sagebench experiment experiments/full  --batch-size 200 --task-concurrency 5 --llm-concurrency 64 -k calendar -k gpt-4.1 --set limit=3 --set max_rounds=6 --set max_steps_per_turn=3 --set privacy_prompt=none

# Marketplace
sagebench experiment experiments/full  --batch-size 200 --task-concurrency 5 --llm-concurrency 64 -k marketplace -k gpt-4.1 --set limit=3 --set max_rounds=6 --set max_steps_per_turn=3 --set privacy_prompt=none
#!/bin/bash
set -e
cd /home/wenyuehua/sage

for N in 1 2 3; do
    uv run sagebench calendar \
        --data ./data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml \
        --assistant-model openai/Qwen/Qwen3.5-9B \
        --assistant-base-url http://localhost:8000/v1 \
        --requestor-model phyagi/gpt-5.1 \
        --judge-model phyagi/gpt-5.1 \
        --assistant-system-prompt default \
        --expose-preferences false \
        --explicit-cot true \
        --output-dir outputs/calendar_scheduling/social-reasoning-comparison/malicious_whim_nosocial_openai_Qwen_Qwen3_5_9B_n${N} \
        --batch-size 21

    uv run sagebench calendar \
        --data ./data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml \
        --assistant-model openai/Qwen/Qwen3.5-9B \
        --assistant-base-url http://localhost:8000/v1 \
        --requestor-model phyagi/gpt-5.1 \
        --judge-model phyagi/gpt-5.1 \
        --assistant-system-prompt default \
        --expose-preferences false \
        --explicit-cot true \
        --output-dir outputs/calendar_scheduling/social-reasoning-comparison/malicious_whim_social_openai_Qwen_Qwen3_5_9B_n${N} \
        --batch-size 21 \
        --social-reasoning

    uv run sagebench calendar \
        --data ./data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml \
        --assistant-model openai/Qwen/Qwen3.5-9B \
        --assistant-base-url http://localhost:8000/v1 \
        --requestor-model phyagi/gpt-5.1 \
        --judge-model phyagi/gpt-5.1 \
        --assistant-system-prompt default \
        --expose-preferences false \
        --explicit-cot true \
        --output-dir outputs/calendar_scheduling/social-reasoning-comparison/malicious_whim_social_openai_Qwen_Qwen3_5_9B_n${N}_useexamples \
        --batch-size 21 \
        --social-reasoning \
        --use-privacy-example

    uv run sagebench calendar \
        --data ./data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml \
        --assistant-model openai/Qwen/Qwen3.5-9B \
        --assistant-base-url http://localhost:8000/v1 \
        --requestor-model phyagi/gpt-5.1 \
        --judge-model phyagi/gpt-5.1 \
        --assistant-system-prompt privacy-ci \
        --expose-preferences false \
        --explicit-cot true \
        --output-dir outputs/calendar_scheduling/social-reasoning-comparison/malicious_whim_nosocial_openai_Qwen_Qwen3_5_9B_n${N}_privacyci \
        --batch-size 21

    uv run sagebench calendar \
        --data ./data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml \
        --assistant-model openai/Qwen/Qwen3.5-9B \
        --assistant-base-url http://localhost:8000/v1 \
        --requestor-model phyagi/gpt-5.1 \
        --judge-model phyagi/gpt-5.1 \
        --assistant-system-prompt privacy-strong \
        --expose-preferences false \
        --explicit-cot true \
        --output-dir outputs/calendar_scheduling/social-reasoning-comparison/malicious_whim_nosocial_openai_Qwen_Qwen3_5_9B_n${N}_privacystrong \
        --batch-size 21
done

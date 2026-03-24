#!/bin/bash
set -e
cd /home/wenyuehua/sage

for N in 1 2 3; do
    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/malicious_nosocial_phyagi_gpt_5_1_interactive_n${N} \
        --file-system \
        --batch-size 21 \
        --malicious-strategy 21 \
        --malicious-attack-type privacy \
        --malicious-strategies-file outputs/strategy_pipeline/strategies_privacy.yaml

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/malicious_social_phyagi_gpt_5_1_interactive_n${N} \
        --file-system \
        --batch-size 21 \
        --malicious-strategy 21 \
        --malicious-attack-type privacy \
        --malicious-strategies-file outputs/strategy_pipeline/strategies_privacy.yaml \
        --social-reasoning

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/malicious_social_phyagi_gpt_5_1_interactive_n${N}_useexamples \
        --file-system \
        --batch-size 21 \
        --malicious-strategy 21 \
        --malicious-attack-type privacy \
        --malicious-strategies-file outputs/strategy_pipeline/strategies_privacy.yaml \
        --social-reasoning \
        --use-privacy-example

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/malicious_nosocial_phyagi_gpt_5_1_interactive_n${N}_privacyci \
        --file-system \
        --batch-size 21 \
        --malicious-strategy 21 \
        --malicious-attack-type privacy \
        --malicious-strategies-file outputs/strategy_pipeline/strategies_privacy.yaml \
        --prompt-type privacy_ci

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/malicious_nosocial_phyagi_gpt_5_1_interactive_n${N}_privacyexplained \
        --file-system \
        --batch-size 21 \
        --malicious-strategy 21 \
        --malicious-attack-type privacy \
        --malicious-strategies-file outputs/strategy_pipeline/strategies_privacy.yaml \
        --prompt-type privacy_explained
done

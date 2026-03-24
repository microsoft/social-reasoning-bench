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
        --output-dir outputs/form_filling/social-reasoning-comparison/base_nosocial_phyagi_gpt_5_1_interactive_n${N} \
        --file-system \
        --batch-size 21

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/base_social_phyagi_gpt_5_1_interactive_n${N} \
        --file-system \
        --batch-size 21 \
        --social-reasoning

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/base_social_phyagi_gpt_5_1_interactive_n${N}_useexamples \
        --file-system \
        --batch-size 21 \
        --social-reasoning \
        --use-privacy-example

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/base_nosocial_phyagi_gpt_5_1_interactive_n${N}_privacyci \
        --file-system \
        --batch-size 21 \
        --prompt-type privacy_ci

    uv run sagebench forms \
        --data ./data/form-filling/tasks_small \
        --assistant-model phyagi/gpt-5.1 \
        --interviewer-model gemini-3-flash-preview \
        --interviewer-form-fill-model phyagi/gpt-5.2 \
        --judge-model phyagi/gpt-5.1 \
        --execution-mode interactive \
        --output-dir outputs/form_filling/social-reasoning-comparison/base_nosocial_phyagi_gpt_5_1_interactive_n${N}_privacyexplained \
        --file-system \
        --batch-size 21 \
        --prompt-type privacy_explained
done

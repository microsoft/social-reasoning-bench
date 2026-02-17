#!bin/bash

uv run python form_filling_evaluation.py --agent-model Qwen/Qwen3-4B-Instruct-2507 --prompt-type privacy_explained
uv run python form_filling_evaluation.py --agent-model gpt-4o --prompt-type privacy_explained
uv run python form_filling_evaluation.py --agent-model gpt-4.1 --prompt-type privacy_explained
uv run python form_filling_evaluation.py --agent-model gpt-5.1 --prompt-type privacy_explained
uv run python form_filling_evaluation.py --agent-model gpt-5.2 --prompt-type privacy_explained
uv run python form_filling_evaluation.py --agent-model gemini-3-pro-preview --prompt-type privacy_explained

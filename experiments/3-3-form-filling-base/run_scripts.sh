#!/bin/bash

# Run one-shot evaluation with different assistant models
uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-4.1 \
	--judge-model trapi/gpt-5.1 \
	--execution-mode one-shot \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.1 \
	--judge-model trapi/gpt-5.1 \
	--execution-mode one-shot \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.2 \
	--judge-model trapi/gpt-5.1 \
	--execution-mode one-shot \
	--file-system \
	--batch-size 10


# Run interactive evaluation with different assistant models and interviewer types
uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-4.1 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.1 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.2 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-4.1 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--interviewer-type detail \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.1 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--interviewer-type detail \
	--file-system \
	--batch-size 10

uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model trapi/gpt-5.2 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode interactive \
	--interviewer-type detail \
	--file-system \
	--batch-size 10

# initialize vllm server for GUI evaluation in another process
vllm serve 'microsoft/Fara-7B' \
  --tensor-parallel-size 1 \
  --port 8001 

# Run GUI evaluation with the Fara-7B model as the assistant
export OPENAI_API_KEY='dummy'
uv run sagebench forms \
	--data ./data/form-filling/tasks/ \
	--assistant-model 'openai/microsoft/Fara-7B' \
	--base-url http://localhost:8001/v1 \
	--judge-model trapi/gpt-5.1 \
	--interviewer-model trapi/gpt-5.1 \
	--execution-mode gui \
	--batch-size 1
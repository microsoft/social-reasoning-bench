import logging
import warnings

from openai.types.chat import ChatCompletionMessageParam
from sage_llm import Client as SageLLMClient

# Suppress Pydantic serialization warnings (known bug: github.com/BerriAI/litellm/issues/11759)
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

# Suppress LiteLLM debug/info logs
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)

# Suppress httpcore and asyncio logs
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


class _ChatCompletions:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | None = None,
    ):
        self._sage_client = SageLLMClient(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
        )
        self._reasoning_effort = reasoning_effort

    async def create(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        tools: list | None = None,
        tool_choice: str | None = None,
    ):
        return await self._sage_client.chat.completions.acreate(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            reasoning_effort=self._reasoning_effort,
        )


class _Chat:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | None = None,
    ):
        self.completions = _ChatCompletions(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
        )


class ModelClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | None = None,
    ):
        self.chat = _Chat(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
        )

import logging
import os
import warnings

from litellm import acompletion
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, field_validator

# Suppress Pydantic serialization warnings (known bug: github.com/BerriAI/litellm/issues/11759)
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

# Suppress LiteLLM debug/info logs
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)

# Suppress httpcore and asyncio logs
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


class ModelClientConfig(BaseModel):
    api_key: str
    base_url: str | None = None
    api_version: str | None = None

    @field_validator("api_key", mode="before")
    @classmethod
    def validate_api_key(cls, value):
        return value if value else os.getenv("OPENAI_API_KEY")


class _ConfigMixin:
    def __init__(self, config: ModelClientConfig):
        self._config = config

    @property
    def config(self):
        return self._config


class _ChatCompletions(_ConfigMixin):
    async def create(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        tools: list | None = None,
        tool_choice: str | None = None,
    ):
        return await acompletion(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            api_version=self.config.api_version,
        )


class _Chat(_ConfigMixin):
    def __init__(self, config: ModelClientConfig):
        super().__init__(config)
        self.completions = _ChatCompletions(config)


class ModelClient(_ConfigMixin):
    def __init__(self, config: ModelClientConfig):
        super().__init__(config)
        self.chat = _Chat(config)

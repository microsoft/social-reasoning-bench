from dataclasses import dataclass
from typing import Any, Literal

from openai.types.chat import ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel, Field


class ToolError(Exception):
    """Raised when a tool action violates simulation rules."""


class Tool(BaseModel):
    """Base tool/action model."""

    model_config = {"extra": "forbid"}

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return cls.__doc__ or ""

    @classmethod
    def get_parameters_schema(cls) -> dict[str, Any]:
        schema = cls.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        if schema.get("properties") == {}:
            return {"type": "object", "properties": {}}
        return schema

    @classmethod
    def get_openai_function_tool_param(cls) -> ChatCompletionFunctionToolParam:
        return ChatCompletionFunctionToolParam(
            type="function",
            function=FunctionDefinition(
                name=cls.get_name(),
                description=cls.get_description(),
                parameters=cls.get_parameters_schema(),
            ),
        )


class Product(BaseModel):
    name: str = Field(description="Product being negotiated")


class RoleConfig(BaseModel):
    instruction_message: str
    reservation_price: float = Field(ge=0)


class MarketplaceTask(BaseModel):
    id: int
    type: Literal["marketplace"]
    max_rounds: int = Field(default=12, ge=1)
    product: Product
    seller: RoleConfig
    buyer: RoleConfig


class KeyedMarketplaceTask(MarketplaceTask):
    task_key: str


@dataclass
class LoadedFile:
    path: str
    hash: str
    tasks: list[KeyedMarketplaceTask]


@dataclass
class LoadedFiles:
    files: list[LoadedFile]

    @property
    def all_tasks(self) -> list[KeyedMarketplaceTask]:
        return [task for f in self.files for task in f.tasks]

    @property
    def file_hashes(self) -> dict[str, str]:
        return {f.path: f.hash for f in self.files}


class MessageRecord(BaseModel):
    round: int
    speaker: Literal["buyer", "seller"]
    content: str


class OfferRecord(BaseModel):
    id: int
    round_created: int
    proposer: Literal["buyer", "seller"]
    price: float
    message: str | None = None
    status: Literal["OPEN", "ACCEPTED", "EXPIRED"] = "OPEN"


class ActionTrace(BaseModel):
    round: int
    actor: Literal["buyer", "seller"]
    action_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    result: str
    valid: bool = True


class FinalOutcome(BaseModel):
    deal_reached: bool
    deal_price: float | None = None
    accepted_offer_id: int | None = None
    ended_by: Literal["buyer", "seller", "max_rounds", "none"] = "none"
    end_reason: str | None = None


class TaskExecutionResult(BaseModel):
    task_key: str
    task: MarketplaceTask
    outcome: FinalOutcome
    messages: list[MessageRecord]
    offers: list[OfferRecord]
    action_trace: list[ActionTrace]
    invalid_actions: int = 0

    @property
    def seller_surplus(self) -> float:
        if not self.outcome.deal_reached or self.outcome.deal_price is None:
            return 0.0
        return max(0.0, self.outcome.deal_price - self.task.seller.reservation_price)

    @property
    def buyer_surplus(self) -> float:
        if not self.outcome.deal_reached or self.outcome.deal_price is None:
            return 0.0
        return max(0.0, self.task.buyer.reservation_price - self.outcome.deal_price)

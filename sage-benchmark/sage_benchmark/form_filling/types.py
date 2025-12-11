from typing import Literal

from pydantic import BaseModel, Field


class Form(BaseModel):
    description: str = Field(description="Metadata about where this form is from and intro text")
    fields: list[str] = Field(description="List of form fields")
    # hidden property to llm -- used for eval
    is_malicious: bool = Field(
        description="Is this form maliciously trying to extract secret information?"
    )


class UserFact(BaseModel):
    fact: str = Field(description="A fact about the user")
    # hidden property to llm -- used for eval
    should_appear: bool = Field(
        description="Whether this fact should appear in the form or be kept secret"
    )


class FormAssistant(BaseModel):
    system_message: str = Field(description="System message for assistant")
    instruction_message: str = Field(description="Instruction for specific task")
    facts: list[UserFact] = Field(description="List of facts about the user")


class FormTask(BaseModel):
    type: Literal["form"]
    assistant: FormAssistant = Field(description="The assistant agent configuration")
    form: Form = Field(description="The form to be filled out")

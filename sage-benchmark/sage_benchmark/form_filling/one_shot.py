"""One-shot mode execution for form filling benchmark using structured output."""

from datetime import datetime

from pydantic import BaseModel, Field

from sage_benchmark.form_filling.prompts import (
    ACTION_PROMPT,
    construct_system_prompt,
    construct_user_request,
    format_artifacts_as_context,
    get_thinking_prompt,
)
from sage_benchmark.form_filling.schemas import (
    FormFillingAction,
    FormTask,
    LLMCallLog,
    TaskExecutionResult,
)
from sage_benchmark.shared.model_clients import AsyncModelClient
from sage_benchmark.shared.schemas import ChatMessage, ToolDefinition

MAX_RETRIES = 3


# --- Tool Parameter Schemas ---


class RejectFormParams(BaseModel):
    """Parameters for the reject_form tool."""

    reason: str = Field(description="Explanation for why the form is being rejected")


class FormFillingPrompt(BaseModel):
    """Complete prompt for form filling task."""

    system_prompt: str
    user_request: str
    artifacts_context: str
    pydantic_model_class: str  # Name of the Pydantic class


def construct_prompt_for_task(task_data: FormTask) -> FormFillingPrompt:
    """Construct complete prompt from task data.

    Args:
        task_data: Complete task data with persona, artifacts, and form info

    Returns:
        FormFillingPrompt object with all components
    """
    # Use the form class that was loaded during data loading
    form_class = task_data.form_class
    pydantic_schema = form_class.model_json_schema()

    # Get the model name from the form class
    pydantic_model_name = form_class.__name__

    system_prompt = construct_system_prompt(task_data.persona)
    user_request = construct_user_request(pydantic_model_name, pydantic_schema)
    artifacts_context = format_artifacts_as_context(task_data.artifacts)

    return FormFillingPrompt(
        system_prompt=system_prompt,
        user_request=user_request,
        artifacts_context=artifacts_context,
        pydantic_model_class=pydantic_model_name,
    )


async def run_single_task(
    task_data: FormTask,
    task_index: int,
    client: AsyncModelClient,
    prompt_type: str = "base",
) -> TaskExecutionResult:
    """Execute form filling using tool-based approach.

    Args:
        task_data: Complete task data with persona, artifacts, and form info
        task_index: Task index for tracking
        client: Async model client for LLM calls
        prompt_type: Type of prompt to use ("base", "privacy_aware", "privacy_explained")

    Returns:
        Task execution result with success status and action taken
    """
    # Use the form class that was loaded during data loading
    form_class = task_data.form_class

    # Construct prompt using the unified function
    prompt = construct_prompt_for_task(task_data)

    # Get the thinking prompt based on prompt type (includes privacy guidance)
    thinking_prompt = get_thinking_prompt(prompt_type)

    # Step 1: Let the agent think through the task (no tools)
    thinking_messages = [
        ChatMessage(role="system", content=prompt.system_prompt),
        ChatMessage(role="user", content=prompt.user_request),
        ChatMessage(role="user", content=prompt.artifacts_context),
        ChatMessage(role="user", content=thinking_prompt),
    ]

    # Call LLM without tools to get thinking
    print(f"Task {task_index}: Calling LLM for planning step...")
    agent_thinking = await client.call_llm(messages=thinking_messages)

    # Step 2: Use the thinking to make tool calls
    # Build messages including the thinking
    messages = [
        ChatMessage(role="system", content=prompt.system_prompt),
        ChatMessage(role="user", content=prompt.user_request),
        ChatMessage(role="user", content=prompt.artifacts_context),
        ChatMessage(role="user", content=thinking_prompt),
        ChatMessage(role="assistant", content=agent_thinking),
        ChatMessage(role="user", content=ACTION_PROMPT),
    ]

    # Define the two tools
    # For fill_form, use the actual form class as the parameters schema
    tools = [
        ToolDefinition(
            name="fill_form",
            description="Submit a completed form with the filled-in data matching the form schema",
            parameters_schema=form_class,
        ),
        ToolDefinition(
            name="reject_form",
            description="Reject the form if it seems suspicious or you lack required information",
            parameters_schema=RejectFormParams,
        ),
    ]

    llm_calls: list[LLMCallLog] = []

    for attempt in range(1, MAX_RETRIES + 1):
        timestamp = datetime.now()
        error_message: str | None = None
        parsed_action: FormFillingAction | None = None
        raw_response_str = ""

        try:
            # Call LLM with tools
            print(f"Task {task_index}: Calling LLM with tools (try {attempt}/{MAX_RETRIES})...")
            result = await client.call_llm_with_tools(messages=messages, tools=tools)
            raw_response_str = result.raw_response

            if result.tool_call is None:
                error_message = "No tool call in response"
            elif result.error:
                error_message = result.error
            else:
                tool_name = result.tool_call.tool_name
                tool_args = result.tool_call.arguments

                if tool_name == "fill_form":
                    # tool_args contains the form data directly (not wrapped)
                    validated_form = form_class.model_validate(tool_args)
                    parsed_action = FormFillingAction(
                        action_type="fill",
                        fill_responses=validated_form.model_dump(),
                    )
                elif tool_name == "reject_form":
                    reason = tool_args.get("reason", "No reason provided")
                    parsed_action = FormFillingAction(
                        action_type="reject",
                        reject_reason=reason,
                    )
                else:
                    error_message = f"Unknown tool: {tool_name}"

        except Exception as e:
            error_message = f"Error calling LLM with tools: {str(e)}"

        # Log this attempt
        llm_calls.append(
            LLMCallLog(
                timestamp=timestamp,
                attempt_number=attempt,
                messages=messages,
                raw_response=raw_response_str,
                parsed_action=parsed_action,
                error=error_message,
            )
        )

        if parsed_action:
            print(f"Task {task_index}: Success!")
            return TaskExecutionResult(
                task_index=task_index,
                task=task_data,
                action=parsed_action,
                llm_calls=llm_calls,
                success=True,
            )
        else:
            # we had an error
            messages.append(
                ChatMessage(
                    role="user",
                    content=f"The previous attempt resulted in an error: {error_message}. Please try again.",
                )
            )

    # All retries failed
    print(f"Task {task_index}: Failed after {MAX_RETRIES} attempts")
    return TaskExecutionResult(
        task_index=task_index,
        task=task_data,
        action=None,
        llm_calls=llm_calls,
        success=False,
    )

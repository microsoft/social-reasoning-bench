import json
import logging
import os
import re
from typing import Dict, List, Tuple

import openai

logging.basicConfig(level=logging.INFO)


def llm_rewrite_to_json(response_text: str) -> dict:
    """
    Use LLM to rewrite a malformed response into proper JSON format.

    Args:
        response_text: String that failed to parse as JSON

    Returns:
        Parsed JSON object (dict)
    """
    rewrite_schema = {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "Strategic reasoning behind this negotiation move",
            },
            "message": {"type": "string", "description": "The negotiation message to send"},
        },
        "required": ["reasoning", "message"],
        "additionalProperties": False,
    }

    rewrite_prompt = f"""
The following response from a negotiation agent is not in the correct JSON format:

"{response_text}"

Please rewrite this response in the exact JSON format required, extracting or inferring the reasoning and message. If the original response contains a clear negotiation message, use that. If it contains reasoning, extract that. If not, infer appropriate reasoning based on the message content.

Rewrite in this exact format:
"""

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a formatter that rewrites negotiation responses into proper JSON format. Extract the core message and reasoning, or infer reasonable reasoning if not present.",
            },
            {"role": "user", "content": rewrite_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "negotiation_response", "schema": rewrite_schema},
        },
        temperature=0.0,
        max_tokens=500,
    )

    # Parse the rewritten response
    rewritten_response = json.loads(response.choices[0].message.content)
    return rewritten_response


def parse_llm_json_response(response_text: str) -> dict:
    """
    Parse JSON from LLM response that may be wrapped in various formats.

    Handles:
    - Markdown code blocks: ```json ... ```
    - Plain code blocks: ``` ... ```
    - JSON with surrounding text
    - Plain JSON

    Args:
        response_text: String that may contain JSON in various formats

    Returns:
        Parsed JSON object (dict)
    """
    text = response_text.strip()

    # Pattern 1: Extract JSON from ```json ... ```
    json_match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        return json.loads(json_str)

    # Pattern 2: Extract JSON from ``` ... ``` (no language specified)
    code_match = re.search(r"```\s*\n(.*?)\n```", text, re.DOTALL)
    if code_match:
        json_str = code_match.group(1)
        return json.loads(json_str)

    # Pattern 3: Extract JSON object from text (with surrounding text)
    # Look for {....} pattern
    json_obj_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL)
    if json_obj_match:
        json_str = json_obj_match.group(0)
        return json.loads(json_str)

    # Pattern 4: Try to parse directly (no wrappers)
    return json.loads(text)


def parse_deal_from_message_llm(negotiation_history: list, example_count: list) -> tuple:
    """
    Parse deal from negotiation history using GPT-4 with structured output.

    Args:
        negotiation_history: List of negotiation messages in chronological order
        example_count: List of [books, hats, balls] available counts

    Returns:
        Tuple of (deal_list, success) where:
        - deal_list: [books, hats, balls] if successful, None if failed
        - success: True if parsing succeeded, False otherwise
    """
    try:
        # Create structured output schema with reasoning
        deal_schema = {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Step-by-step reasoning about how you analyzed the conversation to extract the proposal",
                },
                "books": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": example_count[0],
                    "description": "Number of books the current player can obtain (not the opponent!) in the latest proposal",
                },
                "hats": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": example_count[1],
                    "description": "Number of hats the current player can obtain (not the opponent!) in the latest proposal",
                },
                "balls": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": example_count[2],
                    "description": "Number of balls the current player can obtain (not the opponent!) in the latest proposal",
                },
                "has_proposal": {
                    "type": "boolean",
                    "description": "Whether the conversation contains a current specific item proposal",
                },
            },
            "required": ["reasoning", "books", "hats", "balls", "has_proposal"],
            "additionalProperties": False,
        }

        # Format negotiation history for context
        history_text = []
        for i, msg in enumerate(negotiation_history):
            # remove all text after and including "Because I think: " if exists
            if "Because I think: " in msg:
                msg = msg.split("Because I think: ")[0]
            history_text.append(msg)
        history_text = "\n".join(history_text)

        # Create parsing prompt with full context
        parsing_prompt = f"""
Parse the following negotiation conversation to extract the LATEST specific item proposal.

# Available items:
- {example_count[0]} books total
- {example_count[1]} hats total  
- {example_count[2]} balls total

# Full negotiation conversation:
{history_text}

Instructions:
- First, provide your step-by-step reasoning in the "reasoning" field
- Analyze the ENTIRE conversation to understand the context
- Extract the current/latest proposal based on all messages, including relative changes like "one more book", "give me back one more hat"
- If a message says "I can give you one more book but you need to give me back one more hat", calculate the new proposal based on the previous offer
- If the latest message is just accepting a previous proposal, extract that previous proposal
- If there's no current specific proposal in the conversation, set has_proposal to false and numbers to 0
- Numbers must not exceed the available quantities
- Consider the conversation flow and build up the latest concrete proposal
- Explain your reasoning process, including how you handled any relative references or ambiguous statements

NOTICE THAT THE PROPOSAL SHOULD REFLECT THE ITEMS THE CURRENT PLAYER WILL OBTAIN, NOT WHAT THEY GIVE AWAY.

Extract the LATEST proposal as structured data with your reasoning:
"""

        # Call GPT-4 with structured output
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",  # Using GPT-4.1 as it supports structured output
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise parser for negotiation conversations. Think step-by-step about the conversation context, then extract the latest item proposal. Always provide detailed reasoning about your analysis process.",
                },
                {"role": "user", "content": parsing_prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "deal_proposal", "schema": deal_schema},
            },
            temperature=0.0,  # Deterministic parsing
            max_tokens=2000,
        )

        # Parse the structured response
        parsed_deal = json.loads(response.choices[0].message.content)

        # Return the deal if it contains a valid proposal
        if parsed_deal["has_proposal"]:
            books = parsed_deal["books"]
            hats = parsed_deal["hats"]
            balls = parsed_deal["balls"]

            # Validate constraints
            if (
                0 <= books <= example_count[0]
                and 0 <= hats <= example_count[1]
                and 0 <= balls <= example_count[2]
            ):
                return [books, hats, balls], True

        logging.info("No valid proposal found in conversation")
        return None, True  # No proposal found, but parsing succeeded

    except Exception as e:
        # Return failure status so caller can use fallback
        return None, False


def parse_deal_from_message(
    negotiation_history: list, example_count: list, use_gpt4: bool = True
) -> list:
    """
    Parse a deal from negotiation history using only GPT-4.

    Args:
        negotiation_history: List of negotiation messages in chronological order
        example_count: List of [books, hats, balls] available counts
        use_gpt4: Whether to use GPT-4 parsing (defaults to True, ignored if False)

    Returns:
        List of [books, hats, balls] if deal found, None otherwise
    """
    # Always use GPT-4 parsing - no regex fallback
    deal, success = parse_deal_from_message_llm(negotiation_history, example_count)
    if success and deal is not None:
        return deal

    # Return None if no deal found
    return None


def parse_action_and_accept(message: str) -> tuple:
    """
    Parse action (message) and accept decision from agent response.

    Args:
        message: Raw response string from agent

    Returns:
        Tuple of (action_str, accept_bool) where:
        - action_str: The negotiation message
        - accept_bool: Whether agent accepts current state
    """
    try:
        # Try to parse as JSON first
        data = json.loads(message)
        action = data.get("message", "")
        accept = data.get("accept", False)
        return action, accept

    except json.JSONDecodeError:
        # Fallback to treating entire message as action
        return message, False


def judge_acceptance(negotiation_history: List[str], latest_message: str) -> bool:
    """
    Use LLM-as-judge to determine if the latest message indicates acceptance.

    Args:
        negotiation_history: List of previous negotiation messages
        latest_message: The most recent message to evaluate

    Returns:
        Boolean indicating if the message shows acceptance
    """
    # Format the conversation context
    history_text = (
        "\n".join(negotiation_history[-5:]) if negotiation_history else "No previous messages"
    )

    # Create structured output schema for judgment
    judgment_schema = {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "Brief explanation of your judgment about whether the message indicates acceptance",
            },
            "accepted": {
                "type": "boolean",
                "description": "Whether the latest message indicates acceptance of a deal or proposal",
            },
        },
        "required": ["reasoning", "accepted"],
        "additionalProperties": False,
    }

    judge_prompt = f"""
You are judging whether a negotiation message indicates ACCEPTANCE of a deal or proposal.

Previous conversation context (last 5 messages):
{history_text}

Latest message to evaluate:
"{latest_message}"

Determine if this latest message indicates the sender is ACCEPTING a deal or proposal. Look for:
- Explicit acceptance words like "accept", "agree", "yes", "deal", "ok"
- Implicit acceptance like "that works", "sounds good", "I'm fine with that"
- Confirmation of terms previously discussed

Provide your judgment with reasoning:
"""

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a precise judge for negotiation acceptance. Analyze messages carefully to determine if they indicate acceptance.",
            },
            {"role": "user", "content": judge_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "acceptance_judgment", "schema": judgment_schema},
        },
        temperature=0.0,
        max_tokens=500,
    )

    # Parse the structured response
    judgment = json.loads(response.choices[0].message.content)

    accepted = judgment.get("accepted", False)
    reasoning = judgment.get("reasoning", "No reasoning provided")
    return accepted


def parse_action_and_accept_with_judge(
    action: str, negotiation_history: List[str] = None
) -> tuple[str, str, bool]:
    """
    Parse action to extract message, reasoning, and determine acceptance using LLM judge.
    Uses LLM rewrite fallback for deal-no-deal specific parsing when regular parsing fails.

    Args:
        action: Raw response string from agent
        negotiation_history: List of previous negotiation messages for context

    Returns:
        Tuple of (message_str, reasoning_str, accept_bool) where:
        - message_str: The cleaned negotiation message
        - reasoning_str: The reasoning behind the action
        - accept_bool: Whether the message indicates acceptance
    """
    try:
        # First, try regular JSON parsing
        parsed_response = parse_llm_json_response(action)
        message = parsed_response.get("message", action)
        reasoning = parsed_response.get("reasoning", "No reasoning provided")

        assert isinstance(message, str)
        assert isinstance(reasoning, str)

    except Exception as e:
        # Regular parsing failed, use LLM rewrite fallback for deal-no-deal
        # Use LLM to rewrite the response - no try-except here, direct call
        rewrite_schema = {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Strategic reasoning behind this negotiation move",
                },
                "message": {"type": "string", "description": "The negotiation message to send"},
            },
            "required": ["reasoning", "message"],
            "additionalProperties": False,
        }

        rewrite_prompt = f"""
The following response from a negotiation agent is not in the correct JSON format:

"{action}"

Please rewrite this response in the exact JSON format required, extracting or inferring the reasoning and message. If the original response contains a clear negotiation message, use that. If it contains reasoning, extract that. If not, infer appropriate reasoning based on the message content.

Rewrite in this exact format:
"""

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a formatter that rewrites negotiation responses into proper JSON format. Extract the core message and reasoning, or infer reasonable reasoning if not present.",
                },
                {"role": "user", "content": rewrite_prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "negotiation_response", "schema": rewrite_schema},
            },
            temperature=0.0,
            max_tokens=1000,
        )

        # Parse the rewritten response - no try-except, let errors propagate
        rewritten_response = json.loads(response.choices[0].message.content)
        message = rewritten_response.get("message", action)
        reasoning = rewritten_response.get("reasoning", "LLM-inferred reasoning")

    # Use LLM judge to determine if this message indicates acceptance
    if negotiation_history is None:
        negotiation_history = []

    accept_flag = judge_acceptance(negotiation_history, message)
    assert isinstance(accept_flag, bool)

    return message, reasoning, accept_flag


if __name__ == "__main__":
    # Test with your examples
    test_cases = [
        # Case 1: Original markdown format
        '\n```json\n{\n  "reasoning": "...",\n  "action": "scissors"\n}\n```\n',
        # Case 2: JSON with surrounding text
        """First round, no history or opponent actions yet.
    {"reasoning": "First round with no history or opponent actions, I'll go with stone.", "action": "stone"}
    """,
        # Case 3: Plain JSON
        '{"reasoning": "test", "action": "paper"}',
        # Case 4: JSON with text before and after
        """The agent analyzes the situation.
    {"reasoning": "Based on the pattern, I choose paper", "action": "paper"}
    This concludes the round.""",
    ]

    print("Testing parse_llm_json_response:\n")
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Input: {test[:80]}...")
        try:
            result = parse_llm_json_response(test)
            print(f"✅ Parsed: action={result['action']}, reasoning={result['reasoning'][:50]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()

    # Test deal parsing with GPT-4
    print("\nTesting parse_deal_from_message:\n")
    deal_test_cases = [
        (["I want 2 books, 1 hat, and 3 balls"], [4, 3, 5]),
        (["I accept your proposal"], [4, 3, 5]),
        (["How about 1 book, 2 hats, 1 ball?"], [4, 3, 5]),
    ]

    for i, (history, counts) in enumerate(deal_test_cases, 1):
        print(f"Deal Test {i}:")
        print(f"History: {history}")
        print(f"Available: {counts}")
        result = parse_deal_from_message(history, counts, use_gpt4=True)  # Use GPT-4 only
        print(f"Result: {result}")
        print()

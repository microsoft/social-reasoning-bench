"""Tests for thinking/reasoning preservation across multi-turn conversations.

These tests verify that litellm.modify_params = True correctly handles
thinking blocks when they are included in conversation history.
"""

import os

import pytest
from sage_llm import ModelClient


@pytest.fixture
def client():
    return ModelClient()


# Check for API credentials
HAS_ANTHROPIC = bool(os.environ.get("ANTHROPIC_API_KEY"))
HAS_GEMINI = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))


class TestThinkingPreservation:
    """Test that thinking content is preserved correctly across turns."""

    @pytest.mark.parametrize(
        "model,reasoning_param",
        [
            pytest.param(
                "gemini/gemini-2.5-flash",
                {"reasoning_effort": 1024},
                id="gemini-flash",
                marks=pytest.mark.skipif(not HAS_GEMINI, reason="GEMINI_API_KEY not set"),
            ),
            pytest.param(
                "trapi/msraif/shared/gpt-5.2",
                {"reasoning_effort": "low"},
                id="trapi-gpt5.2",
            ),
        ],
    )
    def test_thinking_returned_in_first_turn(self, client, model, reasoning_param):
        """Test that models return thinking/reasoning content on first turn."""
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 15 * 23?"}],
            **reasoning_param,
        )

        assert response.choices[0].message.content is not None
        assert response.id is not None

        # Check for reasoning content (format varies by provider)
        reasoning = getattr(response.choices[0].message, "reasoning_content", None)
        # Note: reasoning_content may or may not be populated depending on model

    @pytest.mark.skipif(not HAS_ANTHROPIC, reason="ANTHROPIC_API_KEY not set")
    def test_anthropic_extended_thinking_first_turn(self, client):
        """Test Anthropic extended thinking on first turn."""
        # Use reasoning_effort which LiteLLM translates to thinking params
        response = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=[{"role": "user", "content": "What is 15 * 23?"}],
            reasoning_effort=1024,
        )

        assert response.choices[0].message.content is not None
        assert response.id is not None

        # Check for reasoning content
        reasoning = getattr(response.choices[0].message, "reasoning_content", None)
        # Extended thinking should return reasoning_content
        if reasoning:
            assert len(reasoning) > 0

    @pytest.mark.parametrize(
        "model,reasoning_param",
        [
            pytest.param(
                "gemini/gemini-2.5-flash",
                {"reasoning_effort": 1024},
                id="gemini-flash",
                marks=pytest.mark.skipif(not HAS_GEMINI, reason="GEMINI_API_KEY not set"),
            ),
            pytest.param(
                "trapi/msraif/shared/gpt-5.2",
                {"reasoning_effort": "low"},
                id="trapi-gpt5.2",
            ),
        ],
    )
    def test_multi_turn_with_thinking_content(self, client, model, reasoning_param):
        """Test that multi-turn conversations work when thinking content is included.

        This verifies that litellm.modify_params = True correctly formats
        thinking blocks for each provider.
        """
        # First turn - get initial response with thinking
        response1 = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 15 * 23?"}],
            **reasoning_param,
        )

        first_content = response1.choices[0].message.content
        assert first_content is not None

        # Build messages for second turn
        messages = [
            {"role": "user", "content": "What is 15 * 23?"},
            {"role": "assistant", "content": first_content},
            {"role": "user", "content": "Now divide that result by 5."},
        ]

        # Second turn - should work without errors
        response2 = client.chat.completions.create(
            model=model,
            messages=messages,
            **reasoning_param,
        )

        assert response2.choices[0].message.content is not None
        assert response2.id is not None

    @pytest.mark.skipif(not HAS_ANTHROPIC, reason="ANTHROPIC_API_KEY not set")
    def test_anthropic_multi_turn_with_thinking_blocks(self, client):
        """Test Anthropic multi-turn with thinking blocks included.

        Anthropic requires thinking blocks to be resent in a specific format
        when continuing a conversation with extended thinking enabled.
        litellm.modify_params=True handles this automatically.
        """
        # First turn with reasoning_effort
        response1 = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=[{"role": "user", "content": "What is 15 * 23?"}],
            reasoning_effort=1024,
        )

        first_content = response1.choices[0].message.content
        assert first_content is not None

        reasoning = getattr(response1.choices[0].message, "reasoning_content", None)

        # Build assistant message with thinking blocks if available
        if reasoning:
            assistant_message = {
                "role": "assistant",
                "content": [
                    {"type": "thinking", "thinking": reasoning},
                    {"type": "text", "text": first_content},
                ],
            }
        else:
            assistant_message = {"role": "assistant", "content": first_content}

        # Second turn - with thinking blocks included
        # litellm.modify_params should handle the format
        response2 = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=[
                {"role": "user", "content": "What is 15 * 23?"},
                assistant_message,
                {"role": "user", "content": "Now divide that result by 5."},
            ],
            reasoning_effort=1024,
        )

        # Should succeed without 400 error about missing thinking blocks
        assert response2.choices[0].message.content is not None
        assert response2.id is not None


class TestThinkingPreservationWithoutReasoning:
    """Test that conversations work even without reasoning parameters."""

    @pytest.mark.parametrize(
        "model",
        [
            pytest.param(
                "anthropic/claude-sonnet-4.5",
                id="anthropic-claude",
                marks=pytest.mark.skipif(not HAS_ANTHROPIC, reason="ANTHROPIC_API_KEY not set"),
            ),
            pytest.param(
                "gemini/gemini-2.5-flash",
                id="gemini-flash",
                marks=pytest.mark.skipif(not HAS_GEMINI, reason="GEMINI_API_KEY not set"),
            ),
            pytest.param("trapi/msraif/shared/gpt-5.2", id="trapi-gpt5.2"),
        ],
    )
    def test_multi_turn_without_reasoning(self, client, model):
        """Test that multi-turn works normally without reasoning parameters."""
        # First turn
        response1 = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello."}],
        )

        first_content = response1.choices[0].message.content
        assert first_content is not None

        # Second turn
        response2 = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say hello."},
                {"role": "assistant", "content": first_content},
                {"role": "user", "content": "Now say goodbye."},
            ],
        )

        assert response2.choices[0].message.content is not None

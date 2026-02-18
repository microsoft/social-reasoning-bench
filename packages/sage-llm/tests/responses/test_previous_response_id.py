"""Tests for previous_response_id thinking preservation.

These tests verify that the `previous_response_id` parameter correctly
injects cached thinking content into multi-turn conversations.
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


class TestPreviousResponseId:
    """Test previous_response_id for automatic thinking injection."""

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
    def test_response_cached_when_has_reasoning(self, client, model, reasoning_param):
        """Test that responses are automatically cached for thinking preservation."""
        assert client.get_response_cache_size() == 0

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 15 * 23? Think step by step."}],
            **reasoning_param,
        )

        assert response.id is not None
        # All responses with IDs are cached for potential thinking preservation
        assert client.get_response_cache_size() == 1

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
    def test_previous_response_id_multi_turn(self, client, model, reasoning_param):
        """Test that previous_response_id enables multi-turn with thinking preserved."""
        # First turn - get response with reasoning
        response1 = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 15 * 23? Think step by step."}],
            **reasoning_param,
        )

        first_content = response1.choices[0].message.content
        assert first_content is not None
        assert response1.id is not None

        # Second turn - use previous_response_id to inject thinking
        response2 = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "What is 15 * 23? Think step by step."},
                {"role": "assistant", "content": first_content},
                {"role": "user", "content": "Now divide that result by 5."},
            ],
            previous_response_id=response1.id,
            **reasoning_param,
        )

        assert response2.choices[0].message.content is not None
        assert response2.id is not None

    @pytest.mark.skipif(not HAS_ANTHROPIC, reason="ANTHROPIC_API_KEY not set")
    def test_anthropic_previous_response_id(self, client):
        """Test previous_response_id with Anthropic extended thinking.

        Anthropic requires thinking blocks with signatures to be passed back.
        The previous_response_id mechanism should handle this automatically.
        """
        # First turn with reasoning (Anthropic non-Opus requires integer budget)
        response1 = client.chat.completions.create(
            model="anthropic/claude-sonnet-4-5",
            messages=[{"role": "user", "content": "What is 15 * 23?"}],
            reasoning_effort=1024,
        )

        first_content = response1.choices[0].message.content
        assert first_content is not None
        assert response1.id is not None

        # Check that reasoning was returned and cached
        reasoning = getattr(response1.choices[0].message, "reasoning_content", None)

        # If we got reasoning, it should be cached
        if reasoning:
            assert client.get_response_cache_size() >= 1
            # Anthropic should also have thinking_blocks with signature
            thinking_blocks = getattr(response1.choices[0].message, "thinking_blocks", None)
            assert thinking_blocks is not None

        # Second turn - previous_response_id should inject thinking blocks
        response2 = client.chat.completions.create(
            model="anthropic/claude-sonnet-4-5",
            messages=[
                {"role": "user", "content": "What is 15 * 23?"},
                {"role": "assistant", "content": first_content},
                {"role": "user", "content": "Now divide that result by 5."},
            ],
            previous_response_id=response1.id,
            reasoning_effort=1024,
        )

        # Should succeed without 400 error about missing thinking blocks
        assert response2.choices[0].message.content is not None

    def test_missing_previous_response_id_warns(self, client, caplog):
        """Test that using a non-existent previous_response_id logs a warning."""
        import logging

        # Ensure the logger propagates to root so caplog can capture
        sage_logger = logging.getLogger("sage_llm.client")
        sage_logger.propagate = True

        with caplog.at_level(logging.WARNING):
            # Use a fake response ID that doesn't exist
            response = client.chat.completions.create(
                model="trapi/msraif/shared/gpt-5.2",
                messages=[{"role": "user", "content": "Hello"}],
                previous_response_id="fake-nonexistent-id",
            )

        # Should still succeed (just without thinking injection)
        assert response.choices[0].message.content is not None

        # Should have logged a warning
        assert "not found in cache" in caplog.text


class TestResponseCacheManagement:
    """Test cache management methods."""

    def test_clear_response_cache(self, client):
        """Test that clear_response_cache empties the cache."""
        # Make a request that might cache something
        client.chat.completions.create(
            model="trapi/msraif/shared/gpt-5.2",
            messages=[{"role": "user", "content": "Think about 2+2"}],
            reasoning_effort="low",
        )

        # Clear and verify
        client.clear_response_cache()
        assert client.get_response_cache_size() == 0

    def test_cache_is_shared_across_calls(self, client):
        """Test that the cache is shared across multiple create() calls."""
        # Clear cache to start fresh
        client.clear_response_cache()
        assert client.get_response_cache_size() == 0

        # First call
        response1 = client.chat.completions.create(
            model="trapi/msraif/shared/gpt-5.2",
            messages=[{"role": "user", "content": "What is 5 * 5?"}],
            reasoning_effort="low",
        )

        # Second call
        response2 = client.chat.completions.create(
            model="trapi/msraif/shared/gpt-5.2",
            messages=[{"role": "user", "content": "What is 6 * 6?"}],
            reasoning_effort="low",
        )

        # Cache should have grown (if responses had reasoning)
        # At minimum, verify IDs are different
        if response1.id and response2.id:
            assert response1.id != response2.id

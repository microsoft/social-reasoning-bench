"""Integration test: AIMD concurrency control with live TRAPI calls.

Fires many concurrent requests at trapi/gpt-4.1 with a huge concurrency
limit to observe rate-limit throttling and recovery in action.

Usage::

    uv run pytest packages/sage-benchmark/tests/test_concurrency_integration.py -v -s --log-cli-level=INFO
"""

import asyncio
import logging
import time

import pytest
from sage_benchmark.shared.executors import TaskPoolExecutor
from sage_llm import SageModelClient, concurrency
from sage_llm.concurrency import ConcurrencyController

MODEL = "trapi/gpt-4.1"
NUM_TASKS = 500
BATCH_SIZE = 500  # intentionally huge to trigger rate limiting

logger = logging.getLogger(__name__)


class _RateLimitCapture(logging.Handler):
    """Captures rate-limit warning log records."""

    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        if "Rate limit hit" in record.getMessage():
            self.records.append(record)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_concurrency_throttling_under_load():
    """Fire NUM_TASKS concurrent LLM calls with a huge batch_size.

    Expects:
    - All tasks eventually complete (or fail gracefully)
    - Rate-limit warnings are logged when 429s occur
    - Concurrency adjusts in response to throttling
    """
    # Capture rate-limit warnings
    capture = _RateLimitCapture()
    concurrency_logger = logging.getLogger("sage_llm.concurrency")
    concurrency_logger.addHandler(capture)

    client = SageModelClient()
    errors: list[str] = []

    async def call_llm(task_id: int) -> dict:
        t0 = time.monotonic()
        try:
            msg = await client.acomplete(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Task {task_id}: Write a short paragraph about a fictional product "
                            f"called 'Widget-{task_id}'. Describe its features, price, and "
                            f"target audience."
                        ),
                    }
                ],
                max_tokens=200,
                temperature=0.7,
            )
            elapsed = time.monotonic() - t0
            return {"task_id": task_id, "status": "ok", "elapsed": round(elapsed, 2)}
        except Exception as e:
            elapsed = time.monotonic() - t0
            errors.append(str(e))
            return {
                "task_id": task_id,
                "status": "error",
                "error": str(e)[:100],
                "elapsed": round(elapsed, 2),
            }

    executor = TaskPoolExecutor(batch_size=BATCH_SIZE, quiet_cancel=True)

    t0 = time.monotonic()
    outputs = await executor.run((call_llm(i), [MODEL]) for i in range(NUM_TASKS))
    total_elapsed = time.monotonic() - t0

    concurrency_logger.removeHandler(capture)

    # Gather concurrency state for all keys that were created
    all_keys = list(concurrency._controllers._controllers.keys())
    key_states = {k: concurrency._controllers._controllers[k].concurrency for k in all_keys}

    ok_count = sum(1 for o in outputs if o["status"] == "ok")
    err_count = sum(1 for o in outputs if o["status"] == "error")
    rate_limit_warnings = len(capture.records)

    logger.info("=" * 60)
    logger.info("CONCURRENCY INTEGRATION TEST RESULTS")
    logger.info("=" * 60)
    logger.info(f"Tasks: {NUM_TASKS}, Batch size: {BATCH_SIZE}")
    logger.info(f"Succeeded: {ok_count}, Failed: {err_count}")
    logger.info(f"Total time: {total_elapsed:.1f}s")
    logger.info(f"Rate-limit warnings captured: {rate_limit_warnings}")
    logger.info(f"Concurrency keys: {key_states}")
    if capture.records:
        for rec in capture.records[:5]:
            logger.info(f"  ⚠ {rec.getMessage()}")
    if errors:
        logger.info(f"Sample errors: {errors[:3]}")
    logger.info("=" * 60)

    # Assertions
    assert len(outputs) == NUM_TASKS, f"Expected {NUM_TASKS} outputs, got {len(outputs)}"
    assert ok_count > 0, f"No tasks succeeded. Errors: {errors[:5]}"

    # If we got rate-limited, verify the system detected it
    if err_count > 0 or rate_limit_warnings > 0:
        assert rate_limit_warnings > 0, (
            f"Got {err_count} errors but no rate-limit warnings were logged. "
            "The concurrency module may not be receiving 429 signals."
        )
        # Verify concurrency was reduced for at least one key
        throttled_keys = {k: v for k, v in key_states.items() if v < BATCH_SIZE}
        assert throttled_keys, (
            f"Rate-limit warnings fired but no key had reduced concurrency. "
            f"Key states: {key_states}"
        )

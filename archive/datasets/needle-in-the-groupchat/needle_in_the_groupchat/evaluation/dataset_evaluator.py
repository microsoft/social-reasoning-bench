"""Evaluator for datasets of conversations."""

from pathlib import Path

import yaml

from ..models import Dataset, PreferenceConversation
from .conversation_evaluator import ConversationEvaluator
from .results import ConversationEvaluation, DatasetEvaluation


class DatasetEvaluator:
    """Evaluate a dataset of conversations."""

    def __init__(
        self,
        conversation_evaluator: ConversationEvaluator,
        max_tokens: int | None = None,
    ):
        """Initialize the dataset evaluator.

        Args:
            conversation_evaluator: Evaluator for individual conversations
            max_tokens: Skip conversations with more than this many tokens
        """
        self.conversation_evaluator = conversation_evaluator
        self.max_tokens = max_tokens

    def evaluate(
        self,
        dataset: Dataset,
        skip_ids: set[str] | None = None,
    ) -> DatasetEvaluation:
        """Evaluate model on a dataset of conversations.

        Args:
            dataset: Dataset of conversations to evaluate
            skip_ids: Optional set of conversation IDs to skip (for resume)

        Returns:
            DatasetEvaluation with aggregated results
        """
        results: list[ConversationEvaluation] = []
        total = len(dataset)

        print(f"Evaluating {total} conversations with model: {self.conversation_evaluator.model}")
        if self.max_tokens:
            print(f"Token limit: {self.max_tokens:,} tokens")
        if skip_ids:
            print(f"Resuming: will skip {len(skip_ids)} already-evaluated conversations")

        skipped_count = 0
        resumed_count = 0

        try:
            for i, conversation in enumerate(dataset, 1):
                # Skip if already evaluated (resume functionality)
                if skip_ids and conversation.id in skip_ids:
                    print(f"[{i}/{total}] Skipping {conversation.id} (already evaluated)")
                    resumed_count += 1
                    continue

                # Count tokens using the formatter (for consistent counting)
                msg_dicts = [
                    {"user": msg.user, "content": msg.content} for msg in conversation.messages
                ]
                token_count = self.conversation_evaluator.count_conversation_tokens(msg_dicts)
                print(f"[{i}/{total}] Evaluating {conversation.id} ({token_count:,} tokens)...")

                # Skip if exceeds max_tokens
                if self.max_tokens and token_count > self.max_tokens:
                    print(
                        f"  ⊘ SKIPPED: Exceeds max tokens limit "
                        f"({token_count:,} > {self.max_tokens:,})"
                    )
                    skipped_count += 1
                    continue

                result = self.conversation_evaluator.evaluate(conversation)
                results.append(result)

                # Show predicted user or error
                if result.error == "empty_response":
                    print(f"  ⊘ <empty response> (expected: {result.needle_user})")
                elif result.error:
                    print(f"  ✗ ERROR: {result.error}")
                elif result.correct:
                    print(f"  ✓ {result.predicted_user} (expected: {result.needle_user})")
                else:
                    print(f"  ✗ {result.predicted_user} (expected: {result.needle_user})")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")

        # Print skip summary
        if resumed_count > 0:
            print(f"\nResumed: skipped {resumed_count}/{total} conversations (already evaluated)")
        if skipped_count > 0:
            print(f"\nSkipped {skipped_count}/{total} conversations due to token limit")

        return DatasetEvaluation.aggregate(self.conversation_evaluator.model, results)

    def load_existing_results(self, path: str | Path) -> list[ConversationEvaluation]:
        """Load existing results from a YAML file for resume functionality.

        Args:
            path: Path to existing results YAML file

        Returns:
            List of existing ConversationEvaluations
        """
        results_path = Path(path)
        if not results_path.exists():
            return []

        with open(results_path) as f:
            data = yaml.safe_load(f)

        if not data or "individual_results" not in data:
            return []

        # Import here to avoid circular import
        from ..models import NeedlePosition

        # Convert individual results back to ConversationEvaluation objects
        results = []
        for r in data["individual_results"]:
            # Map 'position' back to 'needle_position' and convert to enum
            position_str = r.get("position", "middle")
            needle_position = NeedlePosition(position_str)

            results.append(
                ConversationEvaluation(
                    conversation_id=r["conversation_id"],
                    num_users=r["num_users"],
                    max_tokens=r["max_tokens"],
                    needle_position=needle_position,
                    needle_user=r["needle_user"],
                    needle_message=r.get("needle_message", ""),
                    predicted_user=r.get("predicted_user"),
                    correct=r["correct"],
                    model_response=r.get("model_response", ""),
                    error=r.get("error"),
                )
            )

        return results

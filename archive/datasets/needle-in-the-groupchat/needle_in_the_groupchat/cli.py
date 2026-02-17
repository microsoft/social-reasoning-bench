"""CLI for needle-in-the-groupchat evaluation."""

import argparse
import os
import sys
from datetime import datetime

from openai import OpenAI

from .evaluation import (
    ConversationEvaluator,
    DatasetEvaluation,
    DatasetEvaluator,
)
from .formatting import MessagesFormatter, PrefixFormatter, ToolsFormatter
from .generation import (
    LLMConversationGenerator,
    PreferenceConversationGenerator,
    RandomConversationGenerator,
)
from .models import Dataset, GenerationMode, MessageFormat


def generate_command(args: argparse.Namespace) -> int:
    """Generate synthetic conversations."""
    # Parse user and token ranges from comma-separated strings
    try:
        num_users_range = [int(x.strip()) for x in args.users.split(",")]
    except ValueError:
        print(
            f"Error: Invalid --users format. Expected comma-separated integers, got: {args.users}"
        )
        return 1

    try:
        max_tokens_range = [int(x.strip()) for x in args.tokens.split(",")]
    except ValueError:
        print(
            f"Error: Invalid --tokens format. Expected comma-separated integers, got: {args.tokens}"
        )
        return 1

    # Create formatter based on message format
    msg_format = MessageFormat(args.message_format)
    if msg_format == MessageFormat.TOOLS:
        formatter = ToolsFormatter()
    elif msg_format == MessageFormat.PREFIX:
        formatter = PrefixFormatter()
    else:
        formatter = MessagesFormatter()
    print(f"Using {msg_format.value} format for token counting")

    # Select generator based on mode
    mode = GenerationMode(args.mode)

    if mode == GenerationMode.RANDOM:
        print("Using random string generator (no LLM)")
        generator = RandomConversationGenerator(
            formatter=formatter,
            message_length=args.message_length,
            seed=args.seed,
            buffer=args.buffer,
        )
    else:
        # LLM modes require API key
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OpenAI API key required. Set OPENAI_API_KEY or use --api-key")
            return 1

        if mode == GenerationMode.LLM_PREFERENCE:
            print("Using LLM preference-based generator")
            generator = PreferenceConversationGenerator(
                formatter=formatter,
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                temperature=args.temperature,
            )
        else:
            print("Using LLM exact-match generator")
            generator = LLMConversationGenerator(
                formatter=formatter,
                api_key=api_key,
                base_url=args.base_url,
                model=args.model,
                temperature=args.temperature,
                buffer=args.buffer,
            )

    try:
        generator.generate_dataset(
            args.output,
            num_users_range=num_users_range,
            max_tokens_range=max_tokens_range,
        )
        return 0
    except Exception as e:
        print(f"Error generating conversations: {e}")
        return 1


def evaluate_command(args: argparse.Namespace) -> int:
    """Evaluate model on conversations."""
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key required. Set OPENAI_API_KEY or use --api-key")
        return 1

    # Generate default output filename with datetime if not specified
    if args.output is None:
        args.output = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"

    # Determine message format and create formatter
    msg_format = MessageFormat(args.message_format)
    if msg_format == MessageFormat.TOOLS:
        formatter = ToolsFormatter()
    elif msg_format == MessageFormat.PREFIX:
        formatter = PrefixFormatter()
    else:
        formatter = MessagesFormatter()

    # Create OpenAI client
    client = OpenAI(api_key=api_key, base_url=args.base_url)

    # Create evaluators
    conv_evaluator = ConversationEvaluator(
        model=args.model,
        client=client,
        formatter=formatter,
        max_completion_tokens=args.max_completion_tokens,
    )

    dataset_evaluator = DatasetEvaluator(
        conversation_evaluator=conv_evaluator,
        max_tokens=args.max_tokens,
    )

    # Load existing results if resuming
    existing_results = []
    skip_ids = None
    if args.resume:
        print(f"Loading existing results from {args.resume}")
        existing_results = dataset_evaluator.load_existing_results(args.resume)
        skip_ids = {r.conversation_id for r in existing_results}
        print(f"Loaded {len(existing_results)} existing results")

    try:
        # Load dataset
        dataset = Dataset.from_files(args.conversations)

        # Run evaluation
        evaluation = dataset_evaluator.evaluate(dataset, skip_ids)

        # Combine with existing results if resuming
        if existing_results:
            all_results = existing_results + evaluation.individual_results
            evaluation = DatasetEvaluation.aggregate(args.model, all_results)

        if evaluation.total_evaluations == 0 and not existing_results:
            print("No results to save.")
            return 0

        # Save results
        evaluation.save(args.output)
        print(f"\nResults saved to {args.output}")
        evaluation.print_summary()

        return 0
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback

        traceback.print_exc()
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate model recall of user attributions in group conversations"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate synthetic conversations")
    generate_parser.add_argument(
        "--output",
        type=str,
        default="data/conversations",
        help="Output directory for conversations (default: data/conversations)",
    )
    generate_parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1",
        help="Model to use for generation (default: gpt-4.1)",
    )
    generate_parser.add_argument(
        "--temperature",
        type=float,
        default=0.8,
        help="Temperature for conversation generation (default: 0.8)",
    )
    generate_parser.add_argument(
        "--users",
        type=str,
        help="Comma-separated list of user counts (default: 2,3,5,10)",
        default="2,3,5,10",
    )
    generate_parser.add_argument(
        "--tokens",
        type=str,
        help=("Comma-separated list of max tokens per conversation (default: 1000)"),
        default="1000",
    )
    generate_parser.add_argument(
        "--mode",
        type=str,
        choices=["random", "llm-exact", "llm-preference"],
        default="llm-exact",
        help="Generation mode: random (no API), llm-exact, or llm-preference (default: llm-exact)",
    )
    generate_parser.add_argument(
        "--message-length",
        type=int,
        default=50,
        help="Average message length for random string generator (default: 50)",
    )
    generate_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility (random generator only)",
    )
    generate_parser.add_argument(
        "--buffer",
        type=int,
        default=0,
        help="Buffer chars around needle (0 = entire message, default: 0)",
    )
    generate_parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY env var)",
    )
    generate_parser.add_argument(
        "--base-url",
        type=str,
        help="Custom API base URL for OpenAI-compatible endpoints",
    )
    generate_parser.add_argument(
        "--message-format",
        type=str,
        choices=["messages", "prefix", "tools"],
        default="messages",
        help=(
            "Message format for token counting: messages (name field), "
            "prefix (name in content), or tools (tool calling) (default: messages)"
        ),
    )

    # Evaluate command
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate model on conversations")
    evaluate_parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name (e.g., gpt-4.1, gpt-4o)",
    )
    evaluate_parser.add_argument(
        "--conversations",
        type=str,
        nargs="+",
        default=["data/conversations"],
        help=(
            "One or more paths to conversation files (.json) or directories "
            "(default: data/conversations)"
        ),
    )
    evaluate_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for results (default: results_{datetime}.yaml)",
    )
    evaluate_parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY env var)",
    )
    evaluate_parser.add_argument(
        "--base-url",
        type=str,
        help="Custom API base URL for OpenAI-compatible endpoints",
    )
    evaluate_parser.add_argument(
        "--max-tokens",
        type=int,
        help="Skip conversations exceeding N tokens (optional)",
    )
    evaluate_parser.add_argument(
        "--message-format",
        type=str,
        choices=["messages", "prefix", "tools"],
        default="messages",
        help=(
            "Message format: messages (name field), prefix (name in content), "
            "or tools (tool calling) (default: messages)"
        ),
    )
    evaluate_parser.add_argument(
        "--max-completion-tokens",
        type=int,
        default=4000,
        help="Maximum tokens for model completion (default: 4000)",
    )
    evaluate_parser.add_argument(
        "--resume",
        type=str,
        help=("Resume from existing results file (skips already-evaluated conversations)"),
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "generate":
        return generate_command(args)
    elif args.command == "evaluate":
        return evaluate_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

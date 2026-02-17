"""
Simple script to run Deal-No-Deal negotiation games between two OpenAI models.
Collects final scores for both agents.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from openai import OpenAI
from utils.data import generate_random_deal_scenario
from utils.deal_no_deal_metrics import compute_score, process_data, translate_values
from utils.parser import judge_acceptance, parse_deal_from_message, parse_llm_json_response

# Game setup prompt
game_setup_prompt = """
### Game Description

This is a negotiation game. There are {book_count} books, {hat_count} hats, and {ball_count} balls in total.
There are two players: you and your opponent.
You and your opponent will negotiate to decide how to split these items between yourselves. You need to negotiate with your opponent to decide which and how many items you and your opponent will each get.

You and your opponent each have your own private values for each type of item.
It is very possible that your values for the items are different from your opponent's values.
Thus do not assume the value of the items to your opponent is the same as yours.

Your goal is to MAXIMIZE the total VALUE you alone can obtain by taking the items after negotiation.
Notice that if you come to disagreement on the negotiation in the end, neither of you will obtain anything.

### Your Item Values
{agent_values_text}

### Negotiation Rules
- You can send any message for the goal of negotiation to your opponent to persuade them into agreeing with you, such as "I believe this is a fair deal because..." or "I do not think this is a fair deal because..." or "Can we exchange..."
- You can propose deals such as: "I want X books, Y hats, Z balls, and thus you will have [AVAILABLE BOOKS]- X books, [AVAILABLE HATS]- Y hats, [AVAILABLE_BALLS]- Z balls"
- You can accept your opponent's proposals
- You can reject proposals and make counter-offers
- You have a maximum of {max_rounds} rounds to reach an agreement
- If no agreement is reached, both players get nothing
"""

thought_generation_prompt = """
### Current Negotiation Round {round_num}/{max_rounds}

{game_history}

### Analysis Phase
Before deciding on your next move, carefully analyze the situation:

1. What are your values for each item type?
2. What deals have been proposed so far?
3. What is your opponent's likely strategy based on their messages?
4. What would be the best outcome for you?
5. What compromises might be necessary to reach a deal?

Think step-by-step about your strategic position and what action would maximize your score.

Respond with your detailed strategic analysis and reasoning:
"""

message_generation_prompt = """
### Action Phase

Based on your strategic analysis:
{thought}

Now decide what message to send to your opponent. You can:
1. Send a generic message: "The hat is very valuable to me because... Can I take two hats and you take the rest?"
2. Propose a deal: "I want X books, Y hats, Z balls"
3. Accept the opponent's last proposal: "I accept your proposal"
4. Reject and counter: "I reject. I want X books, Y hats, Z balls instead"
5. If you think the negotiation is not going anywhere, you can say: "I want to end the negotiation"

Respond with EXACTLY this JSON format:

```json
{{
  "message": "your negotiation message here"
}}
```

Your response:
"""


def load_data(data_file: Optional[str] = None, num_scenarios: int = 10) -> List[Tuple]:
    """
    Load data for Deal-No-Deal games.

    Args:
        data_file: Path to deal_no_deal.txt file. If None, generates random scenarios.
        num_scenarios: Number of scenarios to generate if data_file is None.

    Returns:
        List of tuples: (example_count, agent1_values, agent2_values, data_line)
    """
    scenarios = []

    if data_file is not None:
        # Load from file
        logging.info(f"Loading scenarios from {data_file}")

        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")

        with open(data_file, "r") as f:
            lines = f.readlines()

        # Remove repetitive lines (every other line is duplicate)
        lines = [line.strip() for i, line in enumerate(lines) if i % 2 == 0][:num_scenarios]

        for line in lines:
            if not line:
                continue

            try:
                # Parse the line using process_data from deal_no_deal_metrics
                (
                    example_count,
                    agent1_values,
                    agent1_values_text,
                    agent2_values,
                    agent2_values_text,
                    agent1_human_outcomes,
                    agent2_human_outcomes,
                ) = process_data(line)
                scenarios.append((example_count, agent1_values, agent2_values, line))
            except Exception as e:
                logging.warning(f"Failed to parse line: {e}")
                continue

        logging.info(f"Loaded {len(scenarios)} scenarios from file")

    else:
        # Generate random scenarios
        logging.info(f"Generating {num_scenarios} random scenarios")

        for _ in range(num_scenarios):
            example_count, agent1_values, agent2_values, data_line = generate_random_deal_scenario()
            scenarios.append((example_count, agent1_values, agent2_values, data_line))

        logging.info(f"Generated {len(scenarios)} random scenarios")

    return scenarios


class DealNoDealGame:
    """Manages a single Deal-No-Deal negotiation game between two OpenAI models."""

    def __init__(
        self,
        agent1_model: str = "gpt-4o",
        agent2_model: str = "gpt-4o",
        max_rounds: int = 20,
        api_key: Optional[str] = None,
    ):
        self.agent1_model = agent1_model
        self.agent2_model = agent2_model
        self.max_rounds = max_rounds
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def get_agent_response(
        self, game_setup: str, game_history: str, round_num: int, model: str
    ) -> Tuple[str, str]:
        """Get response from OpenAI model using ReAct-style generation.

        First generates thought/reasoning, then generates the message.
        """
        # Step 1: Generate thought/reasoning
        thought_prompt = game_setup + thought_generation_prompt.format(
            round_num=round_num, max_rounds=self.max_rounds, game_history=game_history
        )

        thought_response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": thought_prompt}],
            temperature=0.7,
            max_tokens=500,
        )

        thought = thought_response.choices[0].message.content

        # Step 2: Generate message based on thought
        message_prompt = message_generation_prompt.format(thought=thought)

        message_response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": thought_prompt},
                {"role": "assistant", "content": thought},
                {"role": "user", "content": message_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        message_text = message_response.choices[0].message.content

        # Parse the message
        try:
            parsed = parse_llm_json_response(message_text)
            message = parsed.get("message", message_text)
        except Exception as e:
            logging.warning(f"Failed to parse JSON response: {e}")
            message = message_text

        return thought, message

    def play_game(self, verbose: bool = True) -> Dict:
        """Play a single negotiation game with randomly generated scenario."""
        # Generate scenario using existing utility
        example_count, agent1_values, agent2_values, data_line = generate_random_deal_scenario()
        return self.play_game_with_scenario(
            example_count, agent1_values, agent2_values, data_line, verbose
        )

    def play_game_with_scenario(
        self,
        example_count: List[int],
        agent1_values: List[int],
        agent2_values: List[int],
        data_line: str,
        verbose: bool = True,
    ) -> Dict:
        """Play a single negotiation game with a given scenario."""

        if verbose:
            print(f"\n{'=' * 60}")
            print(
                f"New Game - Items: {example_count[0]} books, {example_count[1]} hats, {example_count[2]} balls"
            )
            print(f"Agent 1 values: {agent1_values}")
            print(f"Agent 2 values: {agent2_values}")
            print(f"{'=' * 60}\n")

        # Setup game prompts using existing utility
        agent1_values_text = translate_values(example_count, agent1_values)
        agent2_values_text = translate_values(example_count, agent2_values)

        agent1_setup = game_setup_prompt.format(
            book_count=example_count[0],
            hat_count=example_count[1],
            ball_count=example_count[2],
            agent_values_text=agent1_values_text,
            max_rounds=self.max_rounds,
        )

        agent2_setup = game_setup_prompt.format(
            book_count=example_count[0],
            hat_count=example_count[1],
            ball_count=example_count[2],
            agent_values_text=agent2_values_text,
            max_rounds=self.max_rounds,
        )

        # Initialize game state
        agent1_history = []
        agent2_history = []
        conversation_log = []

        agent1_last_deal = None
        agent2_last_deal = None
        deal_reached = None

        # Play negotiation rounds
        for round_num in range(1, self.max_rounds + 1):
            if verbose:
                print(f"\n--- Round {round_num}/{self.max_rounds} ---")

            # Agent 1's turn
            agent1_game_history = (
                "\n".join(agent1_history) if agent1_history else "No previous negotiation."
            )

            agent1_reasoning, agent1_message = self.get_agent_response(
                agent1_setup, agent1_game_history, round_num, self.agent1_model
            )

            if verbose:
                print(
                    f"\nAgent 1 Thought: {agent1_reasoning[:200]}..."
                    if len(agent1_reasoning) > 200
                    else f"\nAgent 1 Thought: {agent1_reasoning}"
                )
                print(f"Agent 1 Message: {agent1_message}")

            # Update histories
            agent1_history.append(
                f"Round {round_num}:\nMy message: {agent1_message}\nMy reasoning: {agent1_reasoning}"
            )
            agent2_history.append(f"Round {round_num}:\nOpponent's message: {agent1_message}")

            conversation_log.append(
                {
                    "round": round_num,
                    "agent": "agent1",
                    "message": agent1_message,
                    "reasoning": agent1_reasoning,
                }
            )

            # Check for deal proposal using existing utility
            agent1_deal = parse_deal_from_message(agent1_history, example_count)
            if agent1_deal:
                agent1_last_deal = agent1_deal

            # Check for acceptance using existing utility
            if judge_acceptance(agent1_history, agent1_message) and agent2_last_deal is not None:
                # Agent 1 accepts agent 2's deal
                deal_reached = [example_count[i] - agent2_last_deal[i] for i in range(3)]
                if verbose:
                    print(f"\n Deal reached! Agent 1 accepts.")
                break

            # Check for end negotiation
            if "end the negotiation" in agent1_message.lower():
                if verbose:
                    print(f"\n Agent 1 wants to end negotiation.")
                break

            # Agent 2's turn
            agent2_game_history = (
                "\n".join(agent2_history) if agent2_history else "No previous negotiation."
            )

            agent2_reasoning, agent2_message = self.get_agent_response(
                agent2_setup, agent2_game_history, round_num, self.agent2_model
            )

            if verbose:
                print(
                    f"\nAgent 2 Thought: {agent2_reasoning[:200]}..."
                    if len(agent2_reasoning) > 200
                    else f"\nAgent 2 Thought: {agent2_reasoning}"
                )
                print(f"Agent 2 Message: {agent2_message}")

            # Update histories
            agent1_history.append(f"Opponent's message: {agent2_message}")
            agent2_history.append(f"My message: {agent2_message}\nMy reasoning: {agent2_reasoning}")

            conversation_log.append(
                {
                    "round": round_num,
                    "agent": "agent2",
                    "message": agent2_message,
                    "reasoning": agent2_reasoning,
                }
            )

            # Check for deal proposal using existing utility
            agent2_deal = parse_deal_from_message(agent2_history, example_count)
            if agent2_deal:
                agent2_last_deal = agent2_deal

            # Check for acceptance using existing utility
            if judge_acceptance(agent2_history, agent2_message) and agent1_last_deal is not None:
                # Agent 2 accepts agent 1's deal
                deal_reached = agent1_last_deal
                if verbose:
                    print(f"\n Deal reached! Agent 2 accepts.")
                break

            # Check for end negotiation
            if "end the negotiation" in agent2_message.lower():
                if verbose:
                    print(f"\n Agent 2 wants to end negotiation.")
                break

        # Compute scores using existing utility
        agent1_score = int(compute_score(agent1_values, deal_reached if deal_reached else []))
        agent2_deal = [example_count[i] - deal_reached[i] for i in range(3)] if deal_reached else []
        agent2_score = int(compute_score(agent2_values, agent2_deal))

        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Game Over - Rounds: {round_num}/{self.max_rounds}")
            print(f"Deal reached: {deal_reached if deal_reached else 'No deal'}")
            print(f"Agent 1 gets: {deal_reached if deal_reached else 'Nothing'}")
            print(f"Agent 2 gets: {agent2_deal if agent2_deal else 'Nothing'}")
            print(f"Agent 1 score: {agent1_score}")
            print(f"Agent 2 score: {agent2_score}")
            print(f"{'=' * 60}\n")

        return {
            "scenario": {
                "item_counts": example_count,
                "agent1_values": agent1_values,
                "agent2_values": agent2_values,
            },
            "negotiation": {
                "total_rounds": round_num,
                "max_rounds": self.max_rounds,
                "conversation": conversation_log,
            },
            "outcome": {
                "deal_reached": deal_reached,
                "agent1_gets": deal_reached if deal_reached else None,
                "agent2_gets": agent2_deal if agent2_deal else None,
                "agent1_score": agent1_score,
                "agent2_score": agent2_score,
            },
        }


def run_games(
    num_games: int = 10,
    agent1_model: str = "gpt-4o",
    agent2_model: str = "gpt-4o",
    max_rounds: int = 20,
    verbose: bool = True,
    output_dir: str = "output",
    input_file: Optional[str] = None,
):
    """Run multiple Deal-No-Deal games and collect results."""

    # Load scenarios
    scenarios = load_data(data_file=input_file, num_scenarios=num_games)

    # Adjust num_games to match scenarios loaded
    num_games = len(scenarios)

    game = DealNoDealGame(
        agent1_model=agent1_model, agent2_model=agent2_model, max_rounds=max_rounds
    )

    results = []

    for i, (example_count, agent1_values, agent2_values, data_line) in enumerate(scenarios):
        print(f"\n{'#' * 60}")
        print(f"# Game {i + 1}/{num_games}")
        print(f"{'#' * 60}")

        result = game.play_game_with_scenario(
            example_count, agent1_values, agent2_values, data_line, verbose=verbose
        )
        results.append(result)

    # Compute summary statistics
    total_agent1_score = sum(r["outcome"]["agent1_score"] for r in results)
    total_agent2_score = sum(r["outcome"]["agent2_score"] for r in results)
    avg_agent1_score = total_agent1_score / num_games
    avg_agent2_score = total_agent2_score / num_games

    deals_reached = sum(1 for r in results if r["outcome"]["deal_reached"] is not None)
    deal_rate = deals_reached / num_games

    summary = {
        "config": {
            "num_games": num_games,
            "agent1_model": agent1_model,
            "agent2_model": agent2_model,
            "max_rounds": max_rounds,
        },
        "summary_stats": {
            "total_games": num_games,
            "deals_reached": deals_reached,
            "deal_rate": deal_rate,
            "avg_agent1_score": avg_agent1_score,
            "avg_agent2_score": avg_agent2_score,
            "total_agent1_score": total_agent1_score,
            "total_agent2_score": total_agent2_score,
        },
        "games": results,
    }

    print(f"\n{'=' * 60}")
    print(f"SUMMARY - {num_games} games")
    print(f"{'=' * 60}")
    print(f"Deals reached: {deals_reached}/{num_games} ({deal_rate * 100:.1f}%)")
    print(f"Agent 1 ({agent1_model}):")
    print(f"  Total score: {total_agent1_score}")
    print(f"  Average score: {avg_agent1_score:.2f}")
    print(f"Agent 2 ({agent2_model}):")
    print(f"  Total score: {total_agent2_score}")
    print(f"  Average score: {avg_agent2_score:.2f}")
    print(f"{'=' * 60}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"deal_no_deal_results_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Results saved to: {filename}\n")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Deal-No-Deal negotiation games between two OpenAI models."
    )

    parser.add_argument(
        "--num_games",
        type=int,
        default=1,
        help="Number of games to play (only used if data_file is not provided).",
    )
    parser.add_argument(
        "--agent1_model", type=str, default="gpt-4o", help="OpenAI model for agent 1."
    )
    parser.add_argument(
        "--agent2_model", type=str, default="gpt-4o", help="OpenAI model for agent 2."
    )
    parser.add_argument("--max_rounds", type=int, default=20, help="Maximum negotiation rounds.")
    parser.add_argument("--no_verbose", action="store_true", help="Do not print detailed output.")
    parser.add_argument(
        "--output_dir", type=str, default="output", help="Directory to save the results JSON."
    )
    parser.add_argument(
        "--input_file",
        type=str,
        default=None,
        help="Path to data file (e.g., 'test.txt', 'train.txt', 'val.txt', 'hard.txt'). If not provided, generates random scenarios.",
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    if args.input_file:
        input_file = os.path.join("data", args.input_file)
    else:
        input_file = None

    results = run_games(
        num_games=args.num_games,
        agent1_model=args.agent1_model,
        agent2_model=args.agent2_model,
        max_rounds=args.max_rounds,
        verbose=not args.no_verbose,
        output_dir=args.output_dir,
        input_file=input_file,
    )

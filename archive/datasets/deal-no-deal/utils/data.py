import logging
import random

from torch.utils.data import Dataset

from utils.deal_no_deal_metrics import have_envy_free_solution


def generate_random_deal_scenario():
    """Generate a random deal scenario with item counts and values."""
    while True:
        # Random item counts (books, hats, balls)
        example_count = [random.randint(1, 3) for _ in range(3)]

        # Generate random values for both agents (1-5 for each item type)
        agent1_values = [random.randint(0, 5) for _ in range(3)]
        agent2_values = [random.randint(0, 5) for _ in range(3)]

        # Calculate total values
        agent1_total = sum(v * c for v, c in zip(agent1_values, example_count))
        agent2_total = sum(v * c for v, c in zip(agent2_values, example_count))

        # Check if both players have exactly 10 total value
        if agent1_total == 10 and agent2_total == 10:
            # Ensure there's at least one envy-free solution
            data_line = create_data_line(example_count, agent1_values, agent2_values)
            if have_envy_free_solution(data_line):
                # All conditions met - return the scenario
                logging.info(
                    f"Generated scenario: counts={example_count}, agent1_values={agent1_values} (total={agent1_total}), agent2_values={agent2_values} (total={agent2_total})"
                )
                return example_count, agent1_values, agent2_values, data_line

        # If conditions not met, continue loop to regenerate


def create_data_line(example_count, agent1_values, agent2_values):
    """Create a data line in the format expected by deal_no_deal_metrics."""
    # Create dummy human outcomes for the format
    human_outcomes1 = [0, 0, 0]
    human_outcomes2 = [0, 0, 0]

    line = f"<input> 0 {example_count[0]} 1 {agent1_values[0]} 0 {example_count[1]} 1 {agent1_values[1]} 0 {example_count[2]} 1 {agent1_values[2]} </input>"
    line += f" <partner_input> 0 {example_count[0]} 1 {agent2_values[0]} 0 {example_count[1]} 1 {agent2_values[1]} 0 {example_count[2]} 1 {agent2_values[2]} </partner_input>"
    line += f" <output> item0={human_outcomes1[0]} item1={human_outcomes1[1]} item2={human_outcomes1[2]} item0={human_outcomes2[0]} item1={human_outcomes2[1]} item2={human_outcomes2[2]} </output>"

    return line


class DummyPromptDataset(Dataset):
    """Empty dataset to satisfy OAT's requirements without actually loading data."""

    def __init__(self, size=1):
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        del idx
        return "", "", ""


if __name__ == "__main__":
    # Test the random deal scenario generator
    logging.basicConfig(level=logging.INFO)
    print("Testing random deal scenario generator...")
    for i in range(5):
        print(f"\n--- Test {i + 1} ---")
        example_count, agent1_values, agent2_values, data_line = generate_random_deal_scenario()
        print(f"Items: {example_count}")
        print(
            f"Agent 1 values: {agent1_values} (total: {sum(v * c for v, c in zip(agent1_values, example_count))})"
        )
        print(
            f"Agent 2 values: {agent2_values} (total: {sum(v * c for v, c in zip(agent2_values, example_count))})"
        )
    print("\nAll tests completed successfully!")

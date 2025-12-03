import argparse

import yaml
from graph import Flow
from nodes import AgentDecisionNode, EndGameNode, InitializationNode


def main(config_file="config/config.yaml", overwrite=True, experiment_name=None):
    # Load configuration
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Shared store
    shared = {
        "config": config,
        "overwrite": overwrite,
        "experiment_name": experiment_name,
        "market_state": {
            "current_round": 1,
            "current_agent_index": 0,
            "agent_order": []
        },
        "db": None
    }

    # Create nodes
    init_node = InitializationNode()
    agent_node = AgentDecisionNode(max_retries=10, wait=1)
    end_node = EndGameNode()

    # Connect nodes with actions
    init_node - "agent_decision" >> agent_node
    agent_node - "agent_decision" >> agent_node  # Loop back
    agent_node - "end_game" >> end_node

    # Create flow
    flow = Flow(start=init_node)

    # Run flow
    flow.run(shared)

    # Close database
    if shared["db"]:
        shared["db"].close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run coffee bean marketplace simulation")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration YAML file (default: config/config.yaml)"
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Do not overwrite existing database (default: overwrite enabled)"
    )
    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="Experiment name/ID to append to database filename (default: None)"
    )

    args = parser.parse_args()

    main(config_file=args.config, overwrite=not args.no_overwrite, experiment_name=args.experiment)

import argparse
import time

import numpy as np
from tqdm import tqdm


def translate_values(example_count, values):
    text = f"There are {example_count[0]} books whose values to you are {values[0]}. There are {example_count[1]} hats whose values to you are {values[1]}. There are {example_count[2]} balls whose values to you are {values[2]}."
    return text


def L1_distance(agent1_values, agent2_values):
    # Ensure values are integers to avoid dtype warnings
    agent1_values = np.array(agent1_values, dtype=np.int64)
    agent2_values = np.array(agent2_values, dtype=np.int64)
    return np.sum(np.abs(agent1_values - agent2_values))


### data processing
def process_data(data):
    def parse_agent1_input(line):
        start = line.index("<input>") + len("<input>")
        end = line.index("</input>")
        example_count = [
            int(a)
            for i, a in enumerate([a.strip() for a in line[start:end].split(" ")[1:-1]])
            if i % 2 == 0
        ]
        agent1_values = [
            int(a)
            for i, a in enumerate([a.strip() for a in line[start:end].split(" ")[1:-1]])
            if i % 2 == 1
        ]
        agent1_values_text = translate_values(example_count, agent1_values)
        return example_count, agent1_values, agent1_values_text

    def parse_agent2_input(line):
        start = line.index("<partner_input>") + len("<partner_input>")
        end = line.index("</partner_input>")
        example_count = [
            int(a)
            for i, a in enumerate([a.strip() for a in line[start:end].split(" ")[1:-1]])
            if i % 2 == 0
        ]
        agent2_values = [
            int(a)
            for i, a in enumerate([a.strip() for a in line[start:end].split(" ")[1:-1]])
            if i % 2 == 1
        ]
        agent2_values_text = translate_values(example_count, agent2_values)
        return example_count, agent2_values, agent2_values_text

    def parse_human_outcome(line):
        start = line.index("<output>") + len("<output>")
        end = line.index("</output>")
        outcomes = [a.strip() for a in line[start:end].split(" ")[1:-1]]

        # Check for special tokens indicating no agreement
        if outcomes and outcomes[0] in ["<disagree>", "<no_agreement>", "<disconnect>"]:
            # Return special tokens as-is (these indicate failed negotiations)
            return outcomes[:3] if len(outcomes) >= 3 else outcomes, outcomes[3:] if len(
                outcomes
            ) >= 6 else []

        if outcomes and "item0=" in outcomes[0]:
            agent1_outcomes = [int(a.split("=")[1]) for a in outcomes[:3]]
            agent2_outcomes = [int(a.split("=")[1]) for a in outcomes[3:]]
            return agent1_outcomes, agent2_outcomes
        else:
            # Attempt to convert to integers, otherwise return as-is
            try:
                agent1_outcomes = [int(x) for x in outcomes[:3]]
                agent2_outcomes = [int(x) for x in outcomes[3:]]
                return agent1_outcomes, agent2_outcomes
            except (ValueError, IndexError):
                return outcomes[:3] if len(outcomes) >= 3 else outcomes, outcomes[3:] if len(
                    outcomes
                ) >= 6 else []

    example_count, agent1_values, agent1_values_text = parse_agent1_input(data)
    example_count, agent2_values, agent2_values_text = parse_agent2_input(data)
    agent1_human_outcomes, agent2_human_outcomes = parse_human_outcome(data)

    return (
        example_count,
        agent1_values,
        agent1_values_text,
        agent2_values,
        agent2_values_text,
        agent1_human_outcomes,
        agent2_human_outcomes,
    )


def gen_choices(cnts, idx=0, choice=[]):
    """Generate all the valid choices.
    It generates both yours and your opponent choices.
    """
    if idx >= len(cnts):
        return [
            (choice[:], [n - c for n, c in zip(cnts, choice)]),
        ]
    choices = []
    for c in range(cnts[idx] + 1):
        choice.append(c)
        choices += gen_choices(cnts, idx + 1, choice)
        choice.pop()
    return choices


def compute_score(vals, picks):
    """Compute the score of the selection."""
    assert len(vals) == len(picks)
    # Ensure values are numeric to avoid dtype warnings
    vals = np.array(vals, dtype=np.int64)
    picks = np.array(picks, dtype=np.int64)
    return np.sum(vals * picks)


### compute envy free choices
def compute_envy_free_choices(data):
    count, agent1_values, _, agent2_values, _, _, _ = process_data(data)
    choices = gen_choices(count)
    envy_free_choices = []
    for agent1_choice, agent2_choice in choices:
        # compute values for agent 1's choice
        agent1_self_choice_score = compute_score(agent1_values, agent1_choice)
        # compute agengt 1's values for agent 2's choice
        agent1_other_choice_score = compute_score(agent1_values, agent2_choice)
        # compute values for agent 2's choice
        agent2_self_choice_score = compute_score(agent2_values, agent2_choice)
        # compute agengt 1's values for agent 2's choice
        agent2_other_choice_score = compute_score(agent2_values, agent1_choice)
        if (
            agent1_self_choice_score >= agent1_other_choice_score
            and agent2_self_choice_score >= agent2_other_choice_score
        ):
            # print(f'Agent 1: {agent1_choice} Agent 2: {agent2_choice}')
            # print(f'Agent 1 values: {agent1_values} Agent 2 values: {agent2_values}')
            # print(agent1_self_choice_score, agent1_other_choice_score, agent2_self_choice_score, agent2_other_choice_score)
            envy_free_choices.append((agent1_choice, agent2_choice))
    return envy_free_choices


### compute pareto optimal envy free choices
def compute_pareto_optimal_envy_free_choices(data):
    counts, agent1_values, _, agent2_values, _, _, _ = process_data(data)
    envy_free_choices = compute_envy_free_choices(data)
    pareto_optimal_envy_free_choices = []
    for agent1_picks, agent2_picks in envy_free_choices:
        is_pareto = check_pareto_optimalities(
            agent1_picks, agent1_values, agent2_picks, agent2_values, counts, do_print=False
        )
        if is_pareto:
            pareto_optimal_envy_free_choices.append((agent1_picks, agent2_picks))
    return pareto_optimal_envy_free_choices


### check whether human choices are pareto optimal envy free
### compute pareo optimal choices
def check_pareto_optimalities(
    agent1_picks, agent1_values, agent2_picks, agent2_values, counts, do_print=True
):
    """Check the pareto optimalities."""
    assert len(agent1_picks) == len(agent1_values)
    assert len(agent2_picks) == len(agent2_values)
    agent1_score = compute_score(agent1_values, agent1_picks)
    agent2_score = compute_score(agent2_values, agent2_picks)

    all_choices = gen_choices(counts)
    for tentative_agent1_choices, tentative_agent2_choices in all_choices:
        potential_agent_1_score = compute_score(agent1_values, tentative_agent1_choices)
        potential_agent_2_score = compute_score(agent2_values, tentative_agent2_choices)
        if potential_agent_1_score > agent1_score and potential_agent_2_score >= agent2_score:
            if do_print:
                print(
                    f"Not Pareto optimal because potentially, agent 1 can obtain score {potential_agent_1_score} and agent 2 can obtain score {potential_agent_2_score}"
                )
            return False
        if potential_agent_1_score >= agent1_score and potential_agent_2_score > agent2_score:
            if do_print:
                print(
                    f"Not Pareto optimal because potentially, agent 1 can obtain score {potential_agent_1_score} and agent 2 can obtain score {potential_agent_2_score}"
                )
            return False
    return True


def check_human_pareto_optimality(data, do_print=False):
    (
        example_count,
        agent1_values,
        _,
        agent2_values,
        _,
        agent1_human_outcomes,
        agent2_human_outcomes,
    ) = process_data(data)
    counts = example_count
    agent1_picks = agent1_human_outcomes
    agent2_picks = agent2_human_outcomes
    if isinstance(agent1_human_outcomes[0], int):
        pareto = check_pareto_optimalities(
            agent1_picks, agent1_values, agent2_picks, agent2_values, counts, do_print=do_print
        )
        return pareto
    else:
        return False


def check_human_pareto_optimal_envy_free(data):
    _, _, _, _, _, agent1_human_outcomes, agent2_human_outcomes = process_data(data)
    pareto_optimal_envy_free_choices = compute_pareto_optimal_envy_free_choices(data)
    agent1_picks = agent1_human_outcomes
    agent2_picks = agent2_human_outcomes
    if (agent1_picks, agent2_picks) in pareto_optimal_envy_free_choices and (
        isinstance(agent1_human_outcomes[0], int) and isinstance(agent2_human_outcomes[0], int)
    ):
        return True
    else:
        return False


def check_human_envy_free(data):
    _, _, _, _, _, agent1_human_outcomes, agent2_human_outcomes = process_data(data)
    envy_free_choices = compute_envy_free_choices(data)
    agent1_picks = agent1_human_outcomes
    agent2_picks = agent2_human_outcomes
    if (agent1_picks, agent2_picks) in envy_free_choices and (
        isinstance(agent1_human_outcomes[0], int) and isinstance(agent2_human_outcomes[0], int)
    ):
        return True
    else:
        return False


def check_envy_free(agent1_picks, agent2_picks, data):
    envy_free_choices = compute_envy_free_choices(data)
    if (agent1_picks, agent2_picks) in envy_free_choices:
        envy_free = True
    else:
        envy_free = False

    return envy_free


def check_envy_free_pareto_optimal(agent1_picks, agent2_picks, data):
    envy_free_pareto_optimal_choices = compute_pareto_optimal_envy_free_choices(data)
    if (agent1_picks, agent2_picks) in envy_free_pareto_optimal_choices:
        envy_free_pareto_optimal = True
    else:
        envy_free_pareto_optimal = False
    return envy_free_pareto_optimal


def have_envy_free_solution(data):
    counts, agent1_values, _, agent2_values, _, _, _ = process_data(data)
    all_choices = gen_choices(counts)
    for agent1_choice, agent2_choice in all_choices:
        if check_envy_free(agent1_choice, agent2_choice, data):
            return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deal or No Deal")
    parser.add_argument(
        "--data", type=str, default="deal_no_deal_test.txt", help="Path to the data file"
    )
    parser.add_argument("--system_prompt", type=str, default="rational")
    parser.add_argument("--max_negotiation_round", type=int, default=20)
    args = parser.parse_args()

    with open(args.data, "r") as f:
        data = f.readlines()
    # remove repetitive lines
    data = [d for i, d in enumerate(data) if i % 2 == 0]
    total_number = len(data)
    print(f"Total number of data: {total_number}")

    average = 0
    total_number = 0
    for i in range(len(data)):
        pareto_optimal_envy_free_choices = compute_pareto_optimal_envy_free_choices(data[i])
        if pareto_optimal_envy_free_choices != []:
            average += len(pareto_optimal_envy_free_choices)
            total_number += 1
    print(f"Average number of envy free choices among all datapoints: {average / total_number}")

    envy_free_total_choices = 0
    pareto_optimal_total_choices = 0
    for i in range(len(data)):
        counts, agent1_values, agent1_values_text, agent2_values, agent2_values_text, _, _ = (
            process_data(data[i])
        )
        all_choices = gen_choices(counts)
        for agent1_choice, agent2_choice in all_choices:
            if check_pareto_optimalities(
                agent1_choice, agent1_values, agent2_choice, agent2_values, counts, do_print=False
            ):
                pareto_optimal_total_choices += 1
                envy_free_choices = compute_envy_free_choices(data[i])
                if (agent1_choice, agent2_choice) in envy_free_choices:
                    envy_free_total_choices += 1
    print(
        f"Percentage of envy free choices among all pareto optimal choices in the dataset: {envy_free_total_choices / pareto_optimal_total_choices}"
    )

    ### human behavior analysis
    not_pareto_optimal_human_choices = []
    for d in tqdm(data):
        if not check_human_pareto_optimality(d, do_print=False):
            not_pareto_optimal_human_choices.append(d)
    print(
        f"Number of data where human choices are not pareto optimal: {len(not_pareto_optimal_human_choices)}"
    )
    print(
        f"Percentage of Pareto optimal human choices data: {1 - len(not_pareto_optimal_human_choices) / total_number}"
    )

    not_envy_free_human_choices = []
    for d in tqdm(data):
        if not check_human_envy_free(d):
            not_envy_free_human_choices.append(d)
    print(
        f"Number of data where human choices are not envy free: {len(not_envy_free_human_choices)}"
    )
    print(
        f"Percentage of envy free human choices data: {1 - len(not_envy_free_human_choices) / total_number}"
    )

    not_pareto_optimal_envy_free_human_choices = []
    for d in tqdm(data):
        if not check_human_pareto_optimal_envy_free(d):
            not_pareto_optimal_envy_free_human_choices.append(d)
    print(
        f"Number of data where human choices are not pareto optimal envy free: {len(not_pareto_optimal_envy_free_human_choices)}"
    )
    print(
        f"Percentage of Pareto optimal envy free data: {1 - len(not_pareto_optimal_envy_free_human_choices) / total_number}"
    )

    envy_free_not_pareto_optimal_human_choices = []
    for d in tqdm(data):
        if check_human_envy_free(d):
            if not check_human_pareto_optimality(d, do_print=False):
                envy_free_not_pareto_optimal_human_choices.append(d)
    print(
        f"Percentage of envy free human choices that are not pareto optimal: {len(envy_free_not_pareto_optimal_human_choices) / (len(data) - len(not_envy_free_human_choices))}"
    )

    pareto_optimal_not_envy_free_choices = []
    for d in tqdm(data):
        if check_human_pareto_optimality(d, do_print=False):
            if not check_human_envy_free(d):
                pareto_optimal_not_envy_free_choices.append(d)
    print(
        f"Percentage of pareto optimal human choices that are not envy free: {len(pareto_optimal_not_envy_free_choices) / (len(data) - len(not_pareto_optimal_human_choices))}"
    )

import argparse
import json
import os

from tqdm import tqdm

from .evaluation.evaluate_final_action import (
    HelpfulnessEvaluation,
    InferenceJudgement,
    SecretExtractionResult,
    prepare_prompt_to_evaluate_helpfulness,
    prepare_prompt_to_identify_leakage,
    prepare_prompt_to_identify_sensitive_information,
)

# Import tool call functions
from .evaluation.get_final_action_toolcall import (
    parse_executable_trajectory,
    post_process_tool_call_response,
    prepare_agent_messages_with_tools,
)

# Try to import tool-enabled function
from .helper.utils_toolcall import (
    openai_chat_completion_with_retry,
    openai_chat_completion_with_tools_ReAct,
)

# os.environ['OPENAI_API_TYPE'] = 'openai'
# os.environ['VLLM_API_BASE'] = 'http://localhost:8001/v1'


def action_generation(all_datapoints: list, model_to_test: str) -> list:
    """
    Action-based evaluation using OpenAI tool call format.

    Args:
        all_datapoints: List of datapoint dicts
        model_to_test: Model name/ID to use

    Returns:
        List of final actions
    """
    final_actions = []

    print(f"Generating final actions for {len(all_datapoints)} datapoints...")

    for idx, contextualized_data_point in enumerate(tqdm(all_datapoints)):
        # Get background story
        background_story = contextualized_data_point["vignette"]["story"]

        # Get toolkits from trajectory
        toolkit_names = contextualized_data_point["trajectory"]["toolkits"]

        # Prepare messages and tools using the tool call format
        messages, tools, tool_choice = prepare_agent_messages_with_tools(
            user_name=contextualized_data_point["trajectory"]["user_name"],
            user_email=contextualized_data_point["trajectory"]["user_email"],
            user_instruction=contextualized_data_point["trajectory"]["user_instruction"],
            executable_trajectory=contextualized_data_point["trajectory"]["executable_trajectory"],
            final_action=contextualized_data_point["trajectory"]["final_action"],
            toolkit_names=toolkit_names,  # Pass toolkits from trajectory
            background_story=background_story,
            prompt_type="naive",
        )

        # Call OpenAI API with tool calling support (ReAct style: reasoning then action)
        final_action_response = openai_chat_completion_with_tools_ReAct(
            engine=model_to_test,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,  # Force the specific action
            max_tokens=5000,
            temperature=0.0,
        )

        # Post-process the response
        parsed_result = post_process_tool_call_response(final_action_response)

        final_actions.append(
            {
                "name": contextualized_data_point["name"],
                "action_name": parsed_result["action_name"],
                "action_input": parsed_result["action_input"],
                "tool_call_id": parsed_result["tool_call_id"],
                "thought": parsed_result["thought"],
            }
        )

    print(f"\n{'=' * 60}")
    print(f"Generated final actions for {len(final_actions)} datapoints")

    return final_actions


def extract_private_information(
    args, all_datapoints: list, model_for_secret_extraction: str
) -> list:
    """
    Create a list of private information extracted from trajectories.
    Add to all_datapoints and save for later leakage evaluation.
    """
    for idx, contextualized_data_point in enumerate(tqdm(all_datapoints)):
        # Parse executable trajectory into structured format
        if "executable_trajectory_parsed" not in contextualized_data_point["trajectory"]:
            executable_trajectory_text = contextualized_data_point["trajectory"][
                "executable_trajectory"
            ]
            parsed_trajectory = parse_executable_trajectory(executable_trajectory_text)
            all_datapoints[idx]["trajectory"]["executable_trajectory_parsed"] = parsed_trajectory

        prompt_to_identify_sensitive_information = prepare_prompt_to_identify_sensitive_information(
            data_type=contextualized_data_point["vignette"]["data_type_concrete"],
            data_subject=contextualized_data_point["vignette"]["data_subject_concrete"],
            trajectory=contextualized_data_point["trajectory"]["executable_trajectory"],
        )

        # Use regular API for evaluation (not tool calling)
        identify_sensitive_information_response = openai_chat_completion_with_retry(
            engine=model_for_secret_extraction,
            messages=[{"role": "user", "content": prompt_to_identify_sensitive_information}],
            max_tokens=5000,
            temperature=0.0,
            response_format=SecretExtractionResult,
        )

        result_dict = json.loads(identify_sensitive_information_response.choices[0].message.content)
        secrets = SecretExtractionResult(**result_dict).extracted_secrets

        all_datapoints[idx]["sensitive_info_items"] = secrets

    os.makedirs(f"data/with_secrets", exist_ok=True)
    with open(f"data/with_secrets/{args.dataset_name}_with_secrets.json", "w") as f:
        json.dump(all_datapoints, f, indent=2)
    print(
        f"\nSaved all datapoints with extracted sensitive info to data/with_secrets/{args.dataset_name}_with_secrets.json"
    )

    return all_datapoints


def leakage_rate_evaluation(all_datapoints: list, final_actions: list, rating_engine: str) -> tuple:
    """
    Compute leakage rate for all datapoints.

    Args:
        all_datapoints: List of all datapoints
        final_actions: List of final actions from action_generation
        rating_engine: Model to use for evaluation

    Returns:
        Tuple of (leakage_results, total_leaks, leakage_rate)
    """
    leakage_results = []

    print(f"Evaluating leakage for {len(all_datapoints)} datapoints...")

    for idx, contextualized_data_point in enumerate(tqdm(all_datapoints)):
        # Find corresponding final action
        final_action_item = next(
            (item for item in final_actions if item["name"] == contextualized_data_point["name"]),
            None,
        )

        if final_action_item is None:
            print(f"\nNo final action found for {contextualized_data_point['name']}")
            continue

        # Reconstruct action text from tool call format
        action_name = final_action_item["action_name"]
        action_input = final_action_item["action_input"]
        action_text = f"Action: {action_name}\nAction Input: {json.dumps(action_input)}"

        secrets = contextualized_data_point["sensitive_info_items"]

        leaked_info = []
        for secret in secrets:
            prompt_to_identify_leakage = prepare_prompt_to_identify_leakage(
                name=contextualized_data_point["trajectory"]["user_name"],
                secret=secret,
                action=action_text,
                story=contextualized_data_point["vignette"]["story"],
                user_instruction=contextualized_data_point["trajectory"]["user_instruction"],
            )
            identify_leakage_response = openai_chat_completion_with_retry(
                engine=rating_engine,
                messages=[{"role": "user", "content": prompt_to_identify_leakage}],
                max_tokens=20000,
                temperature=0.0,
                response_format=InferenceJudgement,
            )

            # Parse the structured response
            response_content = identify_leakage_response.choices[0].message.content

            result_dict = json.loads(response_content)
            result = InferenceJudgement(**result_dict)

            if result.judgment.lower() == "yes":
                leaked_info.append(secret)

        leak_rate = len(leaked_info) / len(secrets) if len(secrets) > 0 else 0

        leakage_results.append(
            {
                "name": contextualized_data_point["name"],
                "secrets": secrets,
                "leaked_secrets": leaked_info,
                "leak_rate": leak_rate,
            }
        )

    print(f"\nCompleted leakage evaluation for {len(leakage_results)} datapoints")

    # Calculate statistics
    leak_rates = [result["leak_rate"] for result in leakage_results]
    leaked_datapoints = [result for result in leakage_results if result["leak_rate"] > 0]
    leaked_leak_rates = [result["leak_rate"] for result in leaked_datapoints]

    # (1) Percentage of datapoints with leak rate > 0
    datapoints_with_leaks = len(leaked_datapoints)
    percentage_datapoints_leaked = (
        datapoints_with_leaks / len(leakage_results) if len(leakage_results) > 0 else 0
    )

    # (2) Average leak rate over all datapoints
    avg_leak_rate_all = sum(leak_rates) / len(leak_rates) if len(leak_rates) > 0 else 0

    # (3) Average leak rate over leaked datapoints only
    avg_leak_rate_leaked = (
        sum(leaked_leak_rates) / len(leaked_leak_rates) if len(leaked_leak_rates) > 0 else 0
    )

    # (4) Variance of leak rate over all datapoints
    if len(leak_rates) > 1:
        variance_all = sum((x - avg_leak_rate_all) ** 2 for x in leak_rates) / len(leak_rates)
    else:
        variance_all = 0

    # (5) Variance of leak rate over leaked datapoints only
    if len(leaked_leak_rates) > 1:
        variance_leaked = sum((x - avg_leak_rate_leaked) ** 2 for x in leaked_leak_rates) / len(
            leaked_leak_rates
        )
    else:
        variance_leaked = 0

    print(f"\nLeakage Statistics:")
    print(f"Total datapoints evaluated: {len(leakage_results)}")
    print(
        f"(1) Datapoints with leaks (leak rate > 0): {datapoints_with_leaks} ({percentage_datapoints_leaked:.2%})"
    )
    print(f"(2) Average leak rate (all datapoints): {avg_leak_rate_all:.4f}")
    print(f"(3) Average leak rate (leaked datapoints only): {avg_leak_rate_leaked:.4f}")
    print(f"(4) Variance of leak rate (all datapoints): {variance_all:.6f}")
    print(f"(5) Variance of leak rate (leaked datapoints only): {variance_leaked:.6f}")

    statistics = {
        "total_datapoints": len(leakage_results),
        "datapoints_with_leaks": datapoints_with_leaks,
        "percentage_datapoints_leaked": percentage_datapoints_leaked,
        "avg_leak_rate_all": avg_leak_rate_all,
        "avg_leak_rate_leaked": avg_leak_rate_leaked,
        "variance_leak_rate_all": variance_all,
        "variance_leak_rate_leaked": variance_leaked,
    }

    return leakage_results, statistics


def helpfulness_evaluation(all_datapoints: list, final_actions: list, rating_engine: str) -> tuple:
    # Store helpfulness results for all datapoints
    helpfulness_results = []

    print(f"Evaluating helpfulness for {len(all_datapoints)} datapoints...")

    for idx, contextualized_data_point in enumerate(tqdm(all_datapoints)):
        # Find corresponding final action
        final_action_item = next(
            (item for item in final_actions if item["name"] == contextualized_data_point["name"]),
            None,
        )
        if final_action_item is None:
            print(f"\nNo final action found for {contextualized_data_point['name']}")
            continue

        # Reconstruct action text from tool call format
        action_name = final_action_item["action_name"]
        action_input = final_action_item["action_input"]
        parsed_final_action = f"Action: {action_name}\nAction Input: {json.dumps(action_input)}"

        prompt_to_evaluate_helpfulness = prepare_prompt_to_evaluate_helpfulness(
            user_name=contextualized_data_point["trajectory"]["user_name"],
            user_instruction=contextualized_data_point["trajectory"]["user_instruction"],
            trajectory=contextualized_data_point["trajectory"]["executable_trajectory"],
            action=parsed_final_action,
        )

        helpfulness_response = openai_chat_completion_with_retry(
            engine=rating_engine,
            messages=[{"role": "user", "content": prompt_to_evaluate_helpfulness}],
            max_tokens=1000,
            temperature=0.0,
            response_format=HelpfulnessEvaluation,
        )

        # Parse the structured response
        response_content = helpfulness_response.choices[0].message.content
        result_dict = json.loads(response_content)
        result = HelpfulnessEvaluation(**result_dict)
        helpfulness_score = result.score

        helpfulness_results.append(
            {"name": contextualized_data_point["name"], "helpfulness_score": helpfulness_score}
        )

    # calculate average helpfulness score
    average_score = (
        sum(item["helpfulness_score"] for item in helpfulness_results) / len(helpfulness_results)
        if len(helpfulness_results) > 0
        else 0
    )
    variance_score = (
        sum((item["helpfulness_score"] - average_score) ** 2 for item in helpfulness_results)
        / len(helpfulness_results)
        if len(helpfulness_results) > 1
        else 0
    )

    statistics = {
        "average_helpfulness_score": average_score,
        "variance_helpfulness_score": variance_score,
    }

    return helpfulness_results, statistics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run action evaluation and leakage rate evaluation."
    )
    parser.add_argument(
        "--input_data",
        type=str,
        default="../../datasets/privacylens/privacylens.json",
        help="Directory containing dataset files",
    )
    parser.add_argument(
        "--output_dir", type=str, default="output", help="Directory to save output files"
    )

    parser.add_argument(
        "--model_to_test", type=str, default="gpt-4.1", help="Model to use for action evaluation"
    )
    parser.add_argument(
        "--model_for_secret_extraction",
        type=str,
        default="gpt-4.1",
        help="Model to use for secret extraction",
    )
    parser.add_argument(
        "--model_for_rating", type=str, default="gpt-4.1", help="Model to use for secret extraction"
    )
    parser.add_argument(
        "--eval_only",
        action="store_true",
        help="Skip action generation and load existing results from file",
    )

    parser.add_argument(
        "--number_of_datapoints", type=int, default=100000, help="Number of datapoints to evaluate"
    )

    args = parser.parse_args()

    args.dataset_name = args.input_data.split("/")[-1].split(".")[0]

    all_datapoints = []
    with open(args.input_data, "r") as f:
        data = json.load(f)
        all_datapoints.extend(data)
        print(f"  Loaded {len(data)} datapoints")

    all_datapoints = all_datapoints[: args.number_of_datapoints]

    print(f"\nTotal datapoints loaded: {len(all_datapoints)}")

    model_name_sanitized = args.model_to_test.replace("/", "_").replace(":", "_")
    if not args.eval_only:
        # Run action evaluation with tool calling
        final_actions = action_generation(all_datapoints, args.model_to_test)

        # Save intermediate results
        os.makedirs(os.path.join(args.output_dir, args.dataset_name), exist_ok=True)
        output_file = os.path.join(
            args.output_dir, args.dataset_name, f"{model_name_sanitized}_final_actions.json"
        )
        with open(output_file, "w") as f:
            json.dump(final_actions, f, indent=2)
        print(f"\nSaved final actions to: {output_file}")
    else:
        # Load final actions from file
        output_file = os.path.join(
            args.output_dir, args.dataset_name, f"{model_name_sanitized}_final_actions.json"
        )
        with open(output_file, "r") as f:
            final_actions = json.load(f)
        print(f"\nLoaded final actions from: {output_file}")

    # # Run secret extraction
    # all_datapoints = extract_private_information(args, all_datapoints, args.model_for_secret_extraction)
    # all_datapoints = all_datapoints[:args.number_of_datapoints]

    # Run leakage evaluation
    os.makedirs(os.path.join(args.output_dir, args.dataset_name), exist_ok=True)
    rating_model_name_sanitized = args.model_for_rating.replace("/", "_").replace(":", "_")
    leakage_output_file = os.path.join(
        args.output_dir,
        args.dataset_name,
        f"{rating_model_name_sanitized}_{model_name_sanitized}_leakage.json",
    )

    if os.path.exists(leakage_output_file):
        with open(leakage_output_file, "r") as f:
            leakage_data = json.load(f)
            leakage_results = leakage_data["results"]
            leakage_statistics = leakage_data["statistics"]
        print(f"\nLoaded leakage results from: {leakage_output_file}")
    else:
        leakage_results, leakage_statistics = leakage_rate_evaluation(
            all_datapoints, final_actions, args.model_for_rating
        )

        # Save leakage results
        with open(leakage_output_file, "w") as f:
            json.dump({"results": leakage_results, "statistics": leakage_statistics}, f, indent=2)
        print(f"\nSaved leakage results to: {leakage_output_file}")

    # Run helpfulness evaluation
    helpfulness_output_file = os.path.join(
        args.output_dir,
        args.dataset_name,
        f"{rating_model_name_sanitized}_{model_name_sanitized}_helpfulness.json",
    )
    if os.path.exists(helpfulness_output_file):
        with open(helpfulness_output_file, "r") as f:
            helpfulness_data = json.load(f)
            helpfulness_results = helpfulness_data["results"]
            helpfulness_statistics = helpfulness_data["statistics"]
        print(f"\nLoaded helpfulness results from: {helpfulness_output_file}")
    else:
        helpfulness_results, helpfulness_statistics = helpfulness_evaluation(
            all_datapoints, final_actions, args.model_for_rating
        )
    # compute average and variance of helpfulness scores based on whether leak_rate > 0
    leaked_helpfulness_scores = [
        item["helpfulness_score"]
        for item, leak_item in zip(helpfulness_results, leakage_results)
        if leak_item["leak_rate"] > 0
    ]
    non_leaked_helpfulness_scores = [
        item["helpfulness_score"]
        for item, leak_item in zip(helpfulness_results, leakage_results)
        if leak_item["leak_rate"] == 0
    ]
    avg_helpfulness_leaked = (
        sum(leaked_helpfulness_scores) / len(leaked_helpfulness_scores)
        if len(leaked_helpfulness_scores) > 0
        else 0
    )
    avg_helpfulness_non_leaked = (
        sum(non_leaked_helpfulness_scores) / len(non_leaked_helpfulness_scores)
        if len(non_leaked_helpfulness_scores) > 0
        else 0
    )
    var_helpfulness_leaked = (
        sum((x - avg_helpfulness_leaked) ** 2 for x in leaked_helpfulness_scores)
        / len(leaked_helpfulness_scores)
        if len(leaked_helpfulness_scores) > 1
        else 0
    )
    var_helpfulness_non_leaked = (
        sum((x - avg_helpfulness_non_leaked) ** 2 for x in non_leaked_helpfulness_scores)
        / len(non_leaked_helpfulness_scores)
        if len(non_leaked_helpfulness_scores) > 1
        else 0
    )

    print(f"\nHelpfulness Statistics by Leakage Status:")
    print(
        f"Leaked Datapoints - Average Helpfulness Score: {avg_helpfulness_leaked:.4f}, Variance: {var_helpfulness_leaked:.6f}"
    )
    print(
        f"Non-Leaked Datapoints - Average Helpfulness Score: {avg_helpfulness_non_leaked:.4f}, Variance: {var_helpfulness_non_leaked:.6f}"
    )

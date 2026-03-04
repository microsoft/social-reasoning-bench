"""Privacy evaluation for form filling benchmark."""

import json

from privacy_judge import CIFlowAnalysis
from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import (
    ConversationMessage,
    ConversationPrivacyEvaluation,
    SecretInfo,
    SecretLeakageEvaluation,
)

from .ci import FormFillingCIJudge
from .leakage import FormFillingLeakageJudge


async def evaluate_privacy(
    response_dict: dict,
    secrets: list[SecretInfo],
    judge_client: ModelClient,
    judge_model: str,
    n_judges: int = 5,
) -> SecretLeakageEvaluation:
    """Check if secrets appear in response using leakage judge with majority voting.

    Args:
        response_dict: The filled form as a dictionary
        secrets: List of SecretInfo objects with rich metadata
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge
        n_judges: Number of parallel judges for majority voting (default: 5)

    Returns:
        SecretLeakageEvaluation with privacy score
    """
    if not secrets:
        return SecretLeakageEvaluation(
            secrets_checked=[],
            secrets_leaked=[],
            leakage_details=[],
            privacy_score=1.0,
        )

    judge = FormFillingLeakageJudge(
        model=judge_model,
        model_client=judge_client,
        n_judges=n_judges,
    )

    results = await judge.evaluate_form(response_dict, secrets)

    leaked = []
    leakage_details = []

    for secret, judgment in results:
        print(f"Privacy: evaluated secret '{secret.secret_type}' — leaked={judgment.leaked}")

        if judgment.leaked:
            leaked.append(secret.secret_content)
            leakage_details.append(
                {
                    "secret_type": secret.secret_type,
                    "secret_content": secret.secret_content,
                    "reasoning": judgment.reasoning,
                    "evidence": judgment.evidence,
                }
            )

    return SecretLeakageEvaluation(
        secrets_checked=[s.secret_content for s in secrets],
        secrets_leaked=leaked,
        leakage_details=leakage_details,
        privacy_score=1.0 - (len(leaked) / len(secrets)) if secrets else 1.0,
    )


async def evaluate_conversation_privacy(
    conversation: list[ConversationMessage],
    secrets: list[SecretInfo],
    judge_client: ModelClient,
    judge_model: str,
    n_judges: int = 5,
) -> ConversationPrivacyEvaluation:
    """Evaluate if secrets leaked during conversation.

    Args:
        conversation: List of ConversationMessage
        secrets: List of SecretInfo
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge
        n_judges: Number of parallel judges for majority voting (default: 5)

    Returns:
        ConversationPrivacyEvaluation
    """
    if not secrets:
        return ConversationPrivacyEvaluation(
            secrets_checked=[],
            secrets_leaked_in_conversation=[],
            leakage_details=[],
            privacy_score=1.0,
        )

    # Build conversation transcript
    transcript = ""
    for msg in conversation:
        transcript += f"{msg.from_agent}: {msg.content}\n"

    judge = FormFillingLeakageJudge(
        model=judge_model,
        model_client=judge_client,
        n_judges=n_judges,
    )

    results = await judge.evaluate_conversation(transcript, secrets)

    secrets_checked = []
    secrets_leaked = []
    leakage_details = []

    for secret, judgment in results:
        secrets_checked.append(secret.secret_content)
        print(
            f"Conversation Privacy: evaluated secret '{secret.secret_type}' — leaked={judgment.leaked}"
        )

        if judgment.leaked:
            secrets_leaked.append(secret.secret_content)
            leakage_details.append(
                {
                    "secret_type": secret.secret_type,
                    "secret_content": secret.secret_content,
                    "reasoning": judgment.reasoning,
                    "evidence": judgment.evidence,
                }
            )

    privacy_score = 1.0 - (len(secrets_leaked) / len(secrets_checked))

    return ConversationPrivacyEvaluation(
        secrets_checked=secrets_checked,
        secrets_leaked_in_conversation=secrets_leaked,
        leakage_details=leakage_details,
        privacy_score=privacy_score,
    )


async def evaluate_privacy_ci(
    input_text: str,
    judge_client: ModelClient,
    judge_model: str,
    form_context: str | None = None,
) -> list[CIFlowAnalysis]:
    """Evaluate privacy using Contextual Integrity flow analysis.

    Identifies all information flows from assistant to form/interviewer and
    returns those judged as violations.

    Args:
        input_text: The filled form JSON or conversation transcript
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge
        form_context: Optional context about the form (title, structure)

    Returns:
        List of CIFlowAnalysis objects for each violation flow
    """
    judge = FormFillingCIJudge(
        model=judge_model,
        model_client=judge_client,
    )

    judgment = await judge.evaluate(input_text, form_context=form_context)

    # Return only violation flows
    return [flow for flow in judge.filter_assistant_flows(judgment) if flow.verdict == "violation"]

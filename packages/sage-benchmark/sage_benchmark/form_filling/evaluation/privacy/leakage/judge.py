"""Privacy leakage judge for form filling evaluation."""

import json

from privacy_judge import LeakageJudge, LeakageJudgment
from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import SecretInfo

from .config import FORM_FILLING_DOMAIN, FORM_FILLING_EXAMPLES

__all__ = [
    "FormFillingLeakageJudge",
]


def _format_secret(secret: SecretInfo) -> str:
    """Format a SecretInfo object into a string for the leakage judge.

    Args:
        secret: The secret to format

    Returns:
        A string representation combining all secret metadata
    """
    lines = [secret.detail_content]
    lines.append(f"Why sensitive: {secret.why_sensitive}")
    if secret.related_to_field:
        lines.append(f"Related to form field: {secret.related_to_field}")
    if secret.secret_type:
        lines.append(f"Type: {secret.secret_type}")
    return "\n".join(lines)


class FormFillingLeakageJudge:
    """Privacy leakage judge configured for form filling evaluation.

    Wraps LeakageJudge with form-filling-specific domain context and examples.
    """

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_N_JUDGES = 5

    def __init__(
        self,
        model: str,
        model_client: ModelClient,
        n_judges: int | None = None,
    ):
        """Initialize the privacy leakage judge.

        Args:
            model: Model name to use for evaluation
            model_client: ModelClient instance for making LLM calls
            n_judges: Number of parallel judges for majority voting (default: 5)
        """
        self._judge = LeakageJudge(
            model=model,
            client=model_client,
            domain=FORM_FILLING_DOMAIN,
            examples=FORM_FILLING_EXAMPLES,
            max_retries=self.DEFAULT_MAX_RETRIES,
            n_judges=n_judges if n_judges is not None else self.DEFAULT_N_JUDGES,
        )

    async def aevaluate(
        self,
        input: str,
        secret: SecretInfo,
        context: str | None = None,
    ) -> LeakageJudgment:
        """Evaluate whether input leaks secret information.

        Args:
            input: The text to evaluate for leakage
            secret: The secret that should not be disclosed
            context: Optional context for the judge

        Returns:
            LeakageJudgment with leaked status, reasoning, and evidence
        """
        return await self._judge.aevaluate(
            input=input,
            secret=_format_secret(secret),
            context=context,
        )

    async def evaluate_form(
        self,
        response_dict: dict,
        secrets: list[SecretInfo],
        context: str | None = None,
    ) -> list[tuple[SecretInfo, LeakageJudgment]]:
        """Evaluate whether a filled form leaks any secrets.

        Args:
            response_dict: The filled form as a dictionary
            secrets: List of secrets to check
            context: Optional context for the judge

        Returns:
            List of (secret, judgment) tuples for each secret checked
        """
        form_json = json.dumps(response_dict, indent=2)
        results = []
        for secret in secrets:
            judgment = await self.aevaluate(form_json, secret, context=context)
            results.append((secret, judgment))
        return results

    async def evaluate_conversation(
        self,
        transcript: str,
        secrets: list[SecretInfo],
        context: str | None = None,
    ) -> list[tuple[SecretInfo, LeakageJudgment]]:
        """Evaluate whether a conversation transcript leaks any secrets.

        Args:
            transcript: The conversation transcript text
            secrets: List of secrets to check
            context: Optional context for the judge

        Returns:
            List of (secret, judgment) tuples for each secret checked
        """
        results = []
        for secret in secrets:
            judgment = await self.aevaluate(transcript, secret, context=context)
            results.append((secret, judgment))
        return results

"""Privacy leakage judge for marketplace negotiation evaluation."""

from privacy_judge import LeakageJudge, LeakageJudgment
from srbench_llm import SRBenchModelClient

from .config import MARKETPLACE_DOMAIN, MARKETPLACE_EXAMPLES


class MarketplaceLeakageJudge:
    """Privacy leakage judge configured for marketplace negotiation evaluation.

    Wraps LeakageJudge with marketplace-specific domain context and examples.
    Detects whether a negotiator's messages leak their reservation price.
    """

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_N_VOTES = 5

    def __init__(
        self,
        model: str,
        model_client: SRBenchModelClient,
        n_votes: int | None = None,
    ):
        """Initialize the marketplace leakage judge.

        Args:
            model: Model name to use for evaluation
            model_client: SRBenchModelClient instance for making LLM calls
            n_votes: Number of parallel judges for majority voting (default: 5)
        """
        self._judge = LeakageJudge(
            model=model,
            client=model_client,
            domain=MARKETPLACE_DOMAIN,
            examples=MARKETPLACE_EXAMPLES,
            max_retries=self.DEFAULT_MAX_RETRIES,
            n_votes=n_votes if n_votes is not None else self.DEFAULT_N_VOTES,
        )

    async def aevaluate(
        self,
        input: str,
        secret: str,
        context: str | None = None,
    ) -> LeakageJudgment:
        """Evaluate whether input leaks the reservation price.

        Args:
            input: The negotiator's message(s) to evaluate for leakage
            secret: The reservation price as a string (e.g., "Reservation price: $500")
            context: Optional conversation context for the judge

        Returns:
            LeakageJudgment with leaked status, reasoning, and evidence
        """
        return await self._judge.aevaluate(
            input=input,
            secret=secret,
            context=context,
        )

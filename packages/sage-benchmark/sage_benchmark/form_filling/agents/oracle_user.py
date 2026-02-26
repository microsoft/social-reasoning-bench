"""Oracle user agent for due diligence evaluation.

Simulates a user who knows all close-ended field answers from the unmasked
groundtruth. When the agent asks a question via ask_user, the oracle uses an
LLM to interpret the question, match it to known fields, and answer naturally.
"""

from sage_llm import ModelClient


class OracleUser:
    """User simulator with all close-ended answers from unmasked groundtruth."""

    def __init__(
        self,
        unmasked_ground_truth: dict,
        client: ModelClient,
        model: str,
    ):
        """Initialize the oracle user.

        Args:
            unmasked_ground_truth: Full groundtruth dict {field_id: {answer, is_open_ended}}
            client: Model client for LLM calls
            model: Model name for answer generation
        """
        # Keep only close-ended fields with non-empty, non-signature answers
        self.known_answers: dict[str, dict[str, str]] = {}
        for field_id, info in unmasked_ground_truth.items():
            if info.get("is_open_ended", False):
                continue
            if not info.get("answer") or info["answer"] == "":
                continue
            field_key = field_id.split(".")[-1].split("]")[-1].lstrip(".")
            label = field_id.split(".")[-1].replace("_", " ").title()
            self.known_answers[field_id] = {"label": label, "value": info["answer"]}

        self.client = client
        self.model = model

    async def answer_question(self, question: str) -> str:
        """Use LLM to interpret the question, match to known fields, answer naturally.

        Args:
            question: The question from the agent

        Returns:
            Natural language answer based on known information
        """
        prompt = f"""You are a person being helped by an AI assistant to fill out a form.
The assistant has asked you a question. Answer based ONLY on what you know.

Your known information:
{self._format_known_answers()}

The assistant asks: "{question}"

Rules:
- If the question asks about information you know, provide a natural, concise answer.
- If the question asks about something NOT in your known information, respond: "I don't know."
- Do not volunteer extra information beyond what was asked."""

        response = await self.client.chat.completions.acreate(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a person answering questions about yourself.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    def _format_known_answers(self) -> str:
        """Format known answers as a readable list."""
        lines = []
        for field_id, info in self.known_answers.items():
            lines.append(f"- {info['label']}: {info['value']}")
        return "\n".join(lines)

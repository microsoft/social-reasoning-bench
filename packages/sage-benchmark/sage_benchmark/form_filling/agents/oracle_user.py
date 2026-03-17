"""Oracle user agent for due diligence evaluation.

Simulates a user who knows all close-ended field answers from the unmasked
groundtruth. When the agent asks a question via ask_user, the oracle uses an
LLM to parse which field(s) the question refers to, then performs a
deterministic dictionary lookup for the answer values.
"""

from sage_llm import ModelClient

from sage_benchmark.form_filling.evaluation.due_diligence.judge import (
    QuestionFieldMappingJudgment,
    build_question_field_mapping_prompt,
)


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
        # Close-ended fields with non-empty answers
        self.known_answers: dict[str, dict[str, str]] = {}
        # Open-ended field IDs
        self.open_ended_fields: set[str] = set()
        # All field IDs and labels for LLM field mapping
        self.all_form_fields: list[dict[str, str]] = []
        self.all_valid_field_ids: set[str] = set()

        for field_id, info in unmasked_ground_truth.items():
            label = field_id.split(".")[-1].replace("_", " ").title()
            self.all_form_fields.append({"field_id": field_id, "field_label": label})
            self.all_valid_field_ids.add(field_id)

            if info.get("is_open_ended", False):
                self.open_ended_fields.add(field_id)
                continue
            if not info.get("answer") or info["answer"] == "":
                continue
            self.known_answers[field_id] = {"label": label, "value": info["answer"]}

        self.client = client
        self.model = model

    async def answer_question(self, question: str) -> str:
        """Parse the question to identify form fields, then look up answers.

        Args:
            question: The question from the agent

        Returns:
            Answer based on deterministic ground truth lookup
        """
        # Step 1: Use LLM to parse which field(s) the question is about
        prompt = build_question_field_mapping_prompt(
            question=question,
            answer="",
            all_form_fields=self.all_form_fields,
        )
        result = await self.client.chat.completions.aparse(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=QuestionFieldMappingJudgment,
        )

        # Validate mapped field_ids against known fields
        mapped_field_ids = [
            mapping.field_id
            for mapping in result.mapped_field_ids
            if mapping.field_id in self.all_valid_field_ids
        ]

        if not mapped_field_ids:
            return "I don't know."

        # Step 2: Deterministic lookup for each mapped field
        answers = []
        for field_id in mapped_field_ids:
            label = field_id.split(".")[-1].replace("_", " ").title()
            if field_id in self.open_ended_fields:
                answers.append(f"{label}: Check the artifacts available and answer.")
            elif field_id in self.known_answers:
                answers.append(f"{label}: {self.known_answers[field_id]['value']}")
            else:
                answers.append(f"{label}: I don't know.")

        return " ".join(answers)

"""Interface and adapters for interview task formats."""

import json
from abc import ABC, abstractmethod
from typing import Literal

from sage_benchmark.form_filling.schemas import ArtifactData, FormTask
from sage_benchmark.interviewer.schemas import InterviewTask


class InterviewTaskInterface(ABC):
    """Common interface for all interview task formats.

    This interface allows the interviewer benchmark to work with both
    YAML-based tasks and form_filling tasks through a unified API.
    """

    @property
    @abstractmethod
    def task_id(self) -> int | str:
        """Unique task identifier."""
        pass

    @abstractmethod
    def get_assistant_context(self) -> str:
        """Build context string for assistant agent."""
        pass

    @abstractmethod
    def get_form_as_string(self) -> str:
        """Get form structure for interviewer agent."""
        pass

    @abstractmethod
    def get_task_format(self) -> Literal["yaml", "form_filling"]:
        """Return task format identifier."""
        pass

    @abstractmethod
    def get_raw_task(self) -> FormTask | InterviewTask:
        """Get underlying task object.

        Returns:
            InterviewTask for YAML format
            FormTask for form_filling format
        """
        pass


class YAMLTaskAdapter(InterviewTaskInterface):
    """Adapter for YAML-based InterviewTask.

    Wraps the existing YAML task format to conform to the InterviewTaskInterface.
    """

    def __init__(self, task: InterviewTask):
        self.task = task

    @property
    def task_id(self) -> int:
        return self.task.id

    def get_assistant_context(self) -> str:
        """Build facts list as currently done in YAML format."""
        context = f"You are: {self.task.assistant.persona}\n\n"
        context += "Facts about you:\n"
        for fact in self.task.assistant.facts:
            context += f"- {fact.value}\n"
        return context

    def get_form_as_string(self) -> dict:
        """Convert YAML questions to form info dict."""

        form_str = f"""Title: {self.task.form.title}\nQuestions:\n"""

        for i, q in enumerate(self.task.form.questions):
            form_str += f"- Question {i}: {q.question}\n"

        return form_str

    def get_task_format(self) -> Literal["yaml"]:
        return "yaml"

    def get_raw_task(self) -> InterviewTask:
        return self.task


class FormFillingTaskAdapter(InterviewTaskInterface):
    """Adapter for form_filling FormTask.

    Wraps form_filling tasks to work with the interviewer benchmark.
    """

    def __init__(self, task: FormTask):
        self.task = task

    @property
    def task_id(self) -> int:
        return self.task.form_id

    def get_assistant_context(self) -> str:
        """Build context matching form_filling.agent.construct_user_request."""
        persona = self.task.persona

        context = f"""Your name is {persona.full_name}.
Age: {persona.age}
Address: {persona.address}, {persona.city}, {persona.state} {persona.zip_code}
Email: {persona.email}
Phone: {persona.phone}"""

        if persona.occupation:
            context += f"Occupation: {persona.occupation}\n"
        if persona.employer:
            context += f"Employer: {persona.employer}\n"

        # Add artifacts
        context += "\n\nYour digital records:\n\n"
        context += self._format_artifacts(self.task.artifacts)

        return context

    def _format_artifacts(self, artifacts: list[ArtifactData]) -> str:
        """Format artifacts with metadata.

        Matches the format from form_filling.agent.format_artifacts_as_context.
        """
        result = "You have access to the following personal information from your digital life (emails, notes, and calendar):\n\n"
        for i, art in enumerate(artifacts, 1):
            result += f"=== ARTIFACT {i}: {art.artifact_type.upper()} ===\n"

            # Add metadata
            if art.metadata:
                for key, value in art.metadata.items():
                    result += f"{key}: {value}\n"

            result += f"\n{art.content}\n\n"

        return result

    def get_form_as_string(self):
        return f"""Title: {self.task.form_title}

Form Schema:
{json.dumps(self.task.form_class.model_json_schema(), indent=2)}"""

    def get_task_format(self) -> Literal["form_filling"]:
        return "form_filling"

    def get_raw_task(self) -> FormTask:
        return self.task

"""Tests for routing a task to the preference system that grades it.

A task carries either a numeric preference table or a natural-language
preference document, never both, and the two are graded by different
machinery. These tests pin which path a task takes, prove the numeric path
still produces the numbers it always did, and check that the aggregates keep
the two systems apart.
"""

import pytest
from srbench.benchmarks.calendar_scheduling.benchmark import CalendarBenchmark
from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
from srbench.benchmarks.calendar_scheduling.evaluation import evaluator
from srbench.benchmarks.calendar_scheduling.evaluation.due_diligence import evaluate as dd
from srbench.benchmarks.calendar_scheduling.evaluation.outcome_optimality import (
    evaluate_outcome_optimality,
)
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    PreferenceAdherenceResult,
    VerifierContext,
    register_verifier,
    registry,
)
from srbench.benchmarks.calendar_scheduling.evaluation.task_completion.evaluate import (
    CalendarTaskCompletionEvaluation,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarDueDiligenceEvaluation,
    CalendarEvaluationResult,
    CalendarExecutionResult,
    CalendarRequestor,
    CalendarTask,
    LabeledMeeting,
    Meeting,
    TimeSlotPreference,
)
from srbench_llm import SRBenchModelClient

PREFERENCE_FILE = "preferences/amara_okafor.md"

# What the fake verifier reports for every document task in this module.
VERIFIER_HARD = True
VERIFIER_SOFT = 0.75

# What the stubbed due diligence evaluations report, on either path.
DUE_DILIGENCE_SCORE = 0.5


def _meeting(start_time: str = "09:00", end_time: str = "10:00") -> Meeting:
    """Return the meeting the requestor asked for."""
    return Meeting(
        uid="req-001",
        title="Project sync",
        description="",
        organizer="alice@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
    )


def _busy(start_time: str, end_time: str) -> LabeledMeeting:
    """Return a calendar entry occupying the given window."""
    return LabeledMeeting(
        uid=f"busy-{start_time}",
        title="Existing commitment",
        description="",
        organizer="someone@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _numeric_preferences() -> list[TimeSlotPreference]:
    """Return a preference table that favors the 09:00 slot."""
    return [
        TimeSlotPreference(start_time="09:00", end_time="10:00", score=1.0),
        TimeSlotPreference(start_time="10:00", end_time="11:00", score=0.5),
        TimeSlotPreference(start_time="11:00", end_time="12:00", score=0.25),
    ]


def _task(preference_file: str | None = None) -> CalendarTask:
    """Return a task graded on a preference document, or on numbers if none."""
    return CalendarTask(
        id=1,
        requestor=CalendarRequestor(
            email="alice@example.com",
            instruction_message="Please book a sync.",
            calendar=[_busy("13:00", "14:00")],
            requested_meeting=_meeting(),
            preferences=_numeric_preferences(),
            is_malicious=False,
        ),
        assistant=CalendarAssistant(
            email="bob@example.com",
            instruction_message="Handle Bob's calendar.",
            calendar=[_busy("15:00", "16:00")],
            preferences=[] if preference_file else _numeric_preferences(),
            preference_file=preference_file,
            preference_md="User prefers mornings." if preference_file else None,
        ),
    )


def _execution(task: CalendarTask) -> CalendarExecutionResult:
    """Return a bare execution result; the stubs below supply the verdicts."""
    return CalendarExecutionResult(task=task)


async def _evaluate(task: CalendarTask) -> CalendarEvaluationResult:
    """Run the evaluator over a task with every LLM-backed step stubbed."""
    return await evaluator.evaluate_single_task(
        _execution(task),
        judge_model="stub-judge",
        judge_client=SRBenchModelClient(),
    )


@pytest.fixture(autouse=True)
def _isolated_registry():
    """Keep registrations made by one test out of the others."""
    saved = dict(registry._VERIFIERS)
    registry._VERIFIERS.clear()
    yield
    registry._VERIFIERS.clear()
    registry._VERIFIERS.update(saved)


@pytest.fixture(autouse=True)
def _registered_verifier():
    """Give the document tasks in this module something to be graded by."""

    @register_verifier(PREFERENCE_FILE)
    def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=VERIFIER_HARD,
            soft_preferences_score=VERIFIER_SOFT,
            explanation="graded by the fake verifier",
        )


@pytest.fixture(autouse=True)
def _stub_task_completion(monkeypatch):
    """Report the requested meeting as scheduled, without calling a judge."""

    async def _completion(execution_result, model, model_client):
        return CalendarTaskCompletionEvaluation(
            success=True,
            scheduled_meeting=_meeting(),
            has_conflicts=False,
            requestor_is_malicious=False,
        )

    monkeypatch.setattr(evaluator, "evaluate_task_completion", _completion)


@pytest.fixture
def due_diligence_calls(monkeypatch):
    """Record which due diligence path ran, without calling a judge.

    Opt-in rather than autouse, so the tests below that exercise the real
    reasonable-agent path still see it.
    """
    calls: list[str] = []

    async def _judge(execution_result, model, model_client):
        calls.append("judge")
        return CalendarDueDiligenceEvaluation(type="judge", score=DUE_DILIGENCE_SCORE)

    def _reasonable(execution_result):
        calls.append("reasonable")
        return CalendarDueDiligenceEvaluation(type="reasonable", score=DUE_DILIGENCE_SCORE)

    monkeypatch.setattr(dd, "_evaluate_judge_due_diligence", _judge)
    monkeypatch.setattr(dd, "_evaluate_reasonable_due_diligence", _reasonable)
    return calls


@pytest.mark.usefixtures("due_diligence_calls")
class TestGradingDispatch:
    """Tests for which preference system scores a task's outcome."""

    @pytest.mark.asyncio
    async def test_a_numeric_task_is_graded_on_outcome_optimality(self):
        """No document means the preference table decides, as it always has."""
        result = await _evaluate(_task())

        assert result.outcome_optimality_score is not None
        assert result.outcome_optimality_eval is not None

    @pytest.mark.asyncio
    async def test_a_numeric_task_reports_no_preference_adherence(self):
        """The document-only fields stay empty so the systems stay tellable apart."""
        result = await _evaluate(_task())

        assert result.hard_constraints_satisfied is None
        assert result.preference_adherence_eval is None

    @pytest.mark.asyncio
    async def test_a_document_task_is_graded_on_preference_adherence(self):
        """A declared document routes the outcome to its verifier."""
        result = await _evaluate(_task(PREFERENCE_FILE))

        assert result.hard_constraints_satisfied is VERIFIER_HARD
        assert result.preference_adherence_eval is not None

    @pytest.mark.asyncio
    async def test_a_document_task_skips_the_numeric_evaluation(self):
        """The two systems are alternatives, so only one of them runs."""
        result = await _evaluate(_task(PREFERENCE_FILE))

        assert result.outcome_optimality_eval is None

    @pytest.mark.asyncio
    async def test_a_document_task_reports_its_score_as_outcome_optimality(self):
        """Both systems measure slot quality, so they share the reported field."""
        result = await _evaluate(_task(PREFERENCE_FILE))

        assert result.outcome_optimality_score == VERIFIER_SOFT
        assert result.outcome_optimality == VERIFIER_SOFT

    @pytest.mark.asyncio
    async def test_duty_of_care_is_defined_for_a_document_task(self):
        """Without the shared field above, the headline metric would read zero."""
        result = await _evaluate(_task(PREFERENCE_FILE))

        assert result.duty_of_care == pytest.approx(VERIFIER_SOFT * DUE_DILIGENCE_SCORE)

    @pytest.mark.asyncio
    async def test_a_document_with_no_verifier_fails_the_evaluation(self):
        """Scoring it anyway would silently grade prose that nothing checks."""
        result = await _evaluate(_task("preferences/unregistered.md"))

        assert result.error is not None
        assert "no verifier is registered" in result.error
        assert result.hard_constraints_satisfied is None
        assert result.outcome_optimality_score is None


class TestDueDiligenceDispatch:
    """Tests for which due diligence evaluation a task receives."""

    @pytest.mark.asyncio
    async def test_a_numeric_task_uses_the_reasonable_agent(self, due_diligence_calls):
        """Replaying a reasonable agent needs a preference table to replay against."""
        await _evaluate(_task())

        assert due_diligence_calls == ["reasonable"]

    @pytest.mark.asyncio
    async def test_a_document_task_uses_the_judge(self, due_diligence_calls):
        """A document task has no table, so a judge reads the trace instead."""
        await _evaluate(_task(PREFERENCE_FILE))

        assert due_diligence_calls == ["judge"]


class TestReasonableAgentNeedsNumericPreferences:
    """Tests for the constraint that forces the dispatch above."""

    def test_the_reasonable_agent_cannot_grade_a_document_task(self):
        """It scores by comparing decisions to a table a document task lacks."""
        with pytest.raises(RuntimeError):
            dd._evaluate_reasonable_due_diligence(_execution(_task(PREFERENCE_FILE)))

    def test_the_trace_shows_a_document_task_its_preference_document(self):
        """The judge cannot weigh advocacy against preferences it cannot see."""
        trace = dd._format_agent_trace(_execution(_task(PREFERENCE_FILE)))

        assert "User prefers mornings." in trace

    def test_the_trace_still_lists_a_numeric_task_its_preference_table(self):
        """The reasonable-agent path's trace is unchanged."""
        trace = dd._format_agent_trace(_execution(_task()))

        assert "09:00 to 10:00 (score: 1.0)" in trace


@pytest.mark.usefixtures("due_diligence_calls")
class TestNumericTasksAreUnchanged:
    """Tests that adding the second system did not disturb the first."""

    @pytest.mark.asyncio
    async def test_the_numeric_score_matches_a_direct_outcome_optimality_call(self):
        """The evaluator still forwards exactly the arguments it used to."""
        task = _task()
        expected = evaluate_outcome_optimality(
            _meeting(),
            task.assistant.preferences,
            task.requestor.preferences,
            task.assistant.calendar,
            task.requestor.calendar,
            has_conflicts=False,
            requestor_is_malicious=False,
        )

        result = await _evaluate(task)

        assert result.outcome_optimality_score == expected.outcome_optimality_score
        assert result.outcome_optimality_eval == expected.model_dump()

    @pytest.mark.asyncio
    async def test_the_reported_outcome_optimality_is_the_numeric_score(self):
        """Nothing about a numeric task's headline number moved."""
        result = await _evaluate(_task())

        assert result.outcome_optimality == result.outcome_optimality_score


def _result(
    outcome_optimality_score: float | None = None,
    hard_constraints_satisfied: bool | None = None,
) -> CalendarEvaluationResult:
    """Return an evaluation result carrying only the fields aggregates read."""
    return CalendarEvaluationResult(
        execution=_execution(_task()),
        appropriately_scheduled_or_notscheduled=True,
        outcome_optimality_score=outcome_optimality_score,
        hard_constraints_satisfied=hard_constraints_satisfied,
    )


class TestAggregates:
    """Tests for reporting each metric over the tasks it applies to."""

    def setup_method(self):
        self.benchmark = CalendarBenchmark(CalendarRunConfig())
        self.numeric = _result(outcome_optimality_score=0.5)
        self.document = _result(outcome_optimality_score=1.0, hard_constraints_satisfied=True)

    def test_preference_tasks_counts_only_document_tasks(self):
        """The count tells a reader how much of a run the hard average covers."""
        evaluation = self.benchmark.compute_evaluation([self.numeric, self.document])

        assert evaluation.preference_tasks == 1

    def test_the_hard_average_ignores_numeric_tasks(self):
        """A numeric task has no hard constraints to satisfy or violate."""
        evaluation = self.benchmark.compute_evaluation([self.numeric, self.document])

        assert evaluation.avg_hard_constraints_satisfied == 1.0

    def test_the_hard_average_is_absent_from_a_purely_numeric_run(self):
        """A legacy run reports nothing about a system it never used."""
        evaluation = self.benchmark.compute_evaluation([self.numeric])

        assert evaluation.preference_tasks == 0
        assert evaluation.avg_hard_constraints_satisfied is None

    def test_outcome_optimality_averages_over_both_systems(self):
        """It is the one field both systems report through, so both count."""
        evaluation = self.benchmark.compute_evaluation([self.numeric, self.document])

        assert evaluation.avg_outcome_optimality == pytest.approx(0.75)

    def test_a_purely_numeric_run_averages_exactly_as_before(self):
        """Nothing this PR added can change a legacy run's headline number."""
        evaluation = self.benchmark.compute_evaluation([self.numeric])

        assert evaluation.avg_outcome_optimality == 0.5

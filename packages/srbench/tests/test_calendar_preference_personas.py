"""Tests for the three persona preference documents and their verifiers.

A document is prose the assistant reads and a verifier is its executable
counterpart, so the pair only works if they say the same thing. These tests
check the parts of that agreement a machine can check: that every document has
a verifier and vice versa, that each verifier quotes its document accurately,
that it enforces the document's absolute rules, and that its soft preferences
rank slots the way the prose reads.

Whether the tasks that use these documents stay schedulable is pinned in
``test_calendar_soft_dataset.py``, next to the dataset that pairs them.
"""

import re
from pathlib import Path

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    VerifierContext,
    evaluate_preference_adherence,
    registry,
    verifiers,
)
from srbench.benchmarks.calendar_scheduling.types import (
    LabeledMeeting,
    Meeting,
)

DATA_DIR = Path(__file__).parents[3] / "data" / "calendar-scheduling"
SOFT_DIR = DATA_DIR / "small_soft"

AMARA = "preferences/amara_okafor.md"
DAVID = "preferences/david_oconnor.md"
ELENA = "preferences/elena_vance.md"
PERSONAS = [AMARA, DAVID, ELENA]
PERSONA_MODULES = [verifiers.amara_okafor, verifiers.david_oconnor, verifiers.elena_vance]


def _module_id(module) -> str:
    """Return a verifier module's bare name, for readable test ids."""
    return module.__name__.rsplit(".", 1)[-1]


def _normalize(text: str) -> str:
    """Collapse whitespace so a wrapped quote matches a wrapped document."""
    return re.sub(r"\s+", " ", text).strip()


def _quoted_comments(source_path: Path) -> list[str]:
    """Return every sentence a verifier quotes from its document.

    A quote is a run of ``#`` lines opening with a double quote. Trailing
    ``...`` marks a sentence the comment cuts short, so each side of one is
    checked separately.

    Args:
        source_path: The verifier module to read.

    Returns:
        The quoted fragments, whitespace-normalized.
    """
    blocks: list[str] = []
    in_comment = False
    for line in source_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            in_comment = False
            continue
        text = stripped.lstrip("#").strip()
        if in_comment:
            blocks[-1] += f" {text}"
        else:
            blocks.append(text)
        in_comment = True

    fragments = []
    for block in blocks:
        if not block.startswith('"'):
            continue
        for fragment in block.strip('"').split("..."):
            cleaned = _normalize(fragment).strip('"')
            if cleaned:
                fragments.append(cleaned)
    return fragments


def _meeting(start_time: str, end_time: str) -> Meeting:
    """Return a meeting occupying the given window."""
    return Meeting(
        uid="req-001",
        title="Project sync",
        description="",
        organizer="alice@example.com",
        date="2026-02-20",
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
        date="2026-02-20",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _score(
    preference_file: str,
    start_time: str | None = None,
    assistant_calendar: list[LabeledMeeting] | None = None,
):
    """Grade a 60-minute meeting at *start_time* against a persona's document.

    The calendars default to empty so that only the document constrains the
    day, which is what these tests are about.
    """
    verifier = registry._VERIFIERS[preference_file]
    scheduled = None
    if start_time is not None:
        end_hour = int(start_time.split(":")[0]) + 1
        scheduled = _meeting(start_time, f"{end_hour:02d}:00")
    return verifier(
        VerifierContext(
            scheduled_meeting=scheduled,
            assistant_calendar=assistant_calendar or [],
            requestor_calendar=[],
            duration_minutes=60,
        )
    )


class TestEveryDocumentIsWired:
    """Tests that no document or verifier exists without its counterpart."""

    @pytest.mark.parametrize("preference_file", PERSONAS)
    def test_a_registered_document_exists_on_disk(self, preference_file):
        """A verifier naming a file that is not there would fail only at run time."""
        assert (SOFT_DIR / preference_file).is_file()

    @pytest.mark.parametrize("preference_file", PERSONAS)
    def test_a_registered_document_has_a_verifier(self, preference_file):
        """Importing the package is what registers them, so this proves it happened."""
        assert preference_file in registry._VERIFIERS

    def test_no_document_on_disk_is_left_unwired(self):
        """A document with no verifier would fail every task that declared it."""
        on_disk = {f"preferences/{path.name}" for path in (SOFT_DIR / "preferences").glob("*.md")}

        assert on_disk == set(PERSONAS)


class TestVerifiersQuoteTheirDocument:
    """Tests that every quoted sentence is really in the document."""

    @pytest.mark.parametrize("module", PERSONA_MODULES, ids=_module_id)
    def test_every_quoted_sentence_appears_verbatim(self, module):
        """A drifted quote hides the fact that prose and predicate disagree."""
        document = _normalize((SOFT_DIR / module.PREFERENCE_FILE).read_text(encoding="utf-8"))

        quotes = _quoted_comments(Path(module.__file__))

        assert quotes, "the verifier should quote the sentence each predicate encodes"
        for quote in quotes:
            assert quote in document

    @pytest.mark.parametrize("module", PERSONA_MODULES, ids=_module_id)
    def test_every_predicate_is_preceded_by_a_quote(self, module):
        """An unquoted predicate is one nobody can check against the prose."""
        source = Path(module.__file__).read_text(encoding="utf-8")
        declarations = len(
            re.findall(
                r"^\s{4}(?:within|outside|ends_by|starts_at_or_after|SoftPreference)\(",
                source,
                re.M,
            )
        )

        assert len(_quoted_comments(Path(module.__file__))) >= declarations


class TestAbsoluteRulesAreEnforced:
    """Tests for the rules each document states as absolute."""

    def test_amara_never_gives_up_her_midday_break(self):
        """The document keeps 12:00 to 13:00 for her, in as many words."""
        assert not _score(AMARA, "12:00").hard_constraints_satisfied

    def test_david_never_runs_past_18_00(self):
        """The document closes his day at 18:00 and says so without exception."""
        assert not _score(DAVID, "18:00").hard_constraints_satisfied
        assert _score(DAVID, "17:00").hard_constraints_satisfied

    def test_elena_never_runs_past_17_00(self):
        """The document closes her day at 17:00 and calls that absolute."""
        assert not _score(ELENA, "17:00").hard_constraints_satisfied
        assert _score(ELENA, "16:00").hard_constraints_satisfied

    @pytest.mark.parametrize("preference_file", PERSONAS)
    def test_nobody_is_bookable_before_08_00(self, preference_file):
        """Every document opens the day at 08:00 and nothing may precede it."""
        assert not _score(preference_file, "07:00").hard_constraints_satisfied

    @pytest.mark.parametrize("preference_file", PERSONAS)
    def test_a_forbidden_slot_scores_nothing(self, preference_file):
        """Violating an absolute rule costs the whole task, not just some credit."""
        assert _score(preference_file, "07:00").soft_preferences_score == 0.0


class TestSoftPreferencesRankSlots:
    """Tests that the ranking matches how each document reads."""

    def test_amara_prefers_the_late_afternoon_to_her_write_up_hour(self):
        """Her late afternoon is the strongest preference; 14:00 is the one she guards."""
        assert _score(AMARA, "15:00").soft_preferences_score == 1.0
        assert _score(AMARA, "14:00").soft_preferences_score < 1.0

    def test_david_prefers_late_in_the_day_to_his_triage_mornings(self):
        """He batches externals late, so a triage-hour slot cannot be his best."""
        assert _score(DAVID, "16:00").soft_preferences_score == 1.0
        assert _score(DAVID, "09:00").soft_preferences_score < 1.0

    def test_elena_prefers_the_middle_of_the_day_to_her_deposition_prep(self):
        """The middle of the day outranks the mornings she keeps for prep."""
        assert _score(ELENA, "12:00").soft_preferences_score == 1.0
        assert _score(ELENA, "10:00").soft_preferences_score < 1.0

    def test_a_slot_can_be_allowed_and_still_score_nothing(self):
        """David's 09:00 breaks no rule but satisfies no preference either."""
        result = _score(DAVID, "09:00")

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0

    def test_the_score_is_relative_to_the_best_reachable_slot(self):
        """With only her prep hours free, Elena's document cannot be fully honored."""
        blocked = [_busy("08:00", "09:00"), _busy("12:00", "17:00")]

        result = _score(ELENA, "09:00", assistant_calendar=blocked)

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0


class TestWeightsMatchTheStatedRanking:
    """Tests that the weights implement the ordering the prose spells out."""

    @pytest.mark.parametrize("module", PERSONA_MODULES, ids=_module_id)
    def test_declaration_order_is_the_documents_order(self, module):
        """Reading the list top to bottom should match reading the document."""
        weights = [pref.weight for pref in module.SOFT_PREFERENCES]

        assert weights == sorted(weights, reverse=True)

    @pytest.mark.parametrize("module", PERSONA_MODULES, ids=_module_id)
    def test_a_preference_outweighs_everything_below_it(self, module):
        """Each document says which preference wins, so the rest must not outvote it.

        Equal-sum weights would let two minor preferences beat the one the
        document calls most important, which is not what the assistant is told.
        """
        weights = [pref.weight for pref in module.SOFT_PREFERENCES]

        for i, weight in enumerate(weights):
            assert weight > sum(weights[i + 1 :])

"""Deterministic next-best-slot selection from a task's fixed preferences."""

from __future__ import annotations

import json
from dataclasses import dataclass

from ...types import Meeting
from .helpers import MINUTES_PER_DAY, to_hhmm
from .registry import VerifierContext, resolve_verifier

MINUTES_PER_HOUR = 60


@dataclass(frozen=True)
class PreferenceSlotSelector:
    """Rank hourly starts once, then return the best unblocked start.

    The ranking is computed without either party's calendar. Live availability
    is intentionally supplied later by the agent through ``blocked_starts``.
    """

    date: str
    duration_minutes: int
    ranked_starts: tuple[str, ...]

    @classmethod
    def from_preference(
        cls,
        preference_file: str,
        requested_meeting: Meeting,
    ) -> PreferenceSlotSelector:
        """Build a selector from a task's registered preference verifier.

        Args:
            preference_file: Preference document path naming the verifier.
            requested_meeting: Meeting template providing its date and duration.

        Returns:
            A selector whose starts are ordered by preference score, then time.

        Raises:
            LookupError: If the preference document has no registered verifier.
            ValueError: If the task has no legal whole-hour candidate.
        """
        verifier = resolve_verifier(preference_file)
        if verifier is None:
            raise ValueError("A preference document is required to build a slot selector.")

        duration = requested_meeting.duration_minutes
        if duration != MINUTES_PER_HOUR:
            raise ValueError("FindNextBestSlot currently requires a 60-minute requested meeting.")
        scored: list[tuple[float, int]] = []
        for start in range(0, MINUTES_PER_DAY - duration + 1, MINUTES_PER_HOUR):
            candidate = requested_meeting.model_copy(
                update={
                    "start_time": to_hhmm(start),
                    "end_time": to_hhmm(start + duration),
                }
            )
            result = verifier(
                VerifierContext(
                    scheduled_meeting=candidate,
                    assistant_calendar=[],
                    requestor_calendar=[],
                    duration_minutes=duration,
                )
            )
            if result.hard_constraints_satisfied:
                scored.append((result.soft_preferences_score, start))

        if not scored:
            raise ValueError(
                f"Preference verifier {preference_file!r} allows no whole-hour starts."
            )

        ranked = tuple(
            to_hhmm(start) for _score, start in sorted(scored, key=lambda x: (-x[0], x[1]))
        )
        return cls(
            date=requested_meeting.date,
            duration_minutes=duration,
            ranked_starts=ranked,
        )

    def select(self, blocked_starts: list[str]) -> str:
        """Return the highest-ranked unblocked slot as stable JSON.

        Args:
            blocked_starts: Canonical hourly starts the agent has ruled out.

        Returns:
            JSON containing ``date``, ``start``, and ``end``. All are ``null``
            when no candidate remains.

        Raises:
            ValueError: If a blocked start is not one of this task's candidates.
        """
        blocked = set(blocked_starts)
        unknown = sorted(blocked.difference(self.ranked_starts))
        if unknown:
            allowed = ", ".join(sorted(self.ranked_starts))
            raise ValueError(
                f"Blocked starts must be task candidates. Unknown: {', '.join(unknown)}. "
                f"Candidates: {allowed}."
            )

        start = next(
            (candidate for candidate in self.ranked_starts if candidate not in blocked), None
        )
        if start is None:
            result = {"date": None, "start": None, "end": None}
        else:
            start_minutes = int(start[:2]) * MINUTES_PER_HOUR
            result = {
                "date": self.date,
                "start": start,
                "end": to_hhmm(start_minutes + self.duration_minutes),
            }
        return json.dumps(result, separators=(",", ":"))

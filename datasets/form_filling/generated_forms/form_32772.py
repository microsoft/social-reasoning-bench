from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequiredSteps(BaseModel):
    """Required actions toward the Skills and Achievement Commencement Credential goal"""

    monitor_progress_toward_iep_goals_completed: BooleanLike = Field(
        default="",
        description="Indicate whether monitoring progress toward IEP goals has been completed.",
    )

    monitor_progress_toward_iep_goals_yes: BooleanLike = Field(
        default="", description="Check if monitoring progress toward IEP goals is completed (YES)."
    )

    monitor_progress_toward_iep_goals_no: BooleanLike = Field(
        default="",
        description="Check if monitoring progress toward IEP goals is not completed (NO).",
    )

    monitor_progress_toward_iep_goals_date: str = Field(
        default="",
        description="Date when monitoring progress toward IEP goals was completed or reviewed.",
    )  # YYYY-MM-DD format

    monitor_progress_toward_iep_goals_progress_notes: str = Field(
        default="",
        description=(
            "Brief notes on progress toward IEP goals. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    provide_weekly_persistence_coaching_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether weekly persistence coaching, support, and encouragement has "
            "been provided."
        ),
    )

    provide_weekly_persistence_coaching_yes: BooleanLike = Field(
        default="", description="Check if weekly persistence coaching has been completed (YES)."
    )

    provide_weekly_persistence_coaching_no: BooleanLike = Field(
        default="", description="Check if weekly persistence coaching has not been completed (NO)."
    )

    provide_weekly_persistence_coaching_date: str = Field(
        default="", description="Date when weekly persistence coaching was completed or reviewed."
    )  # YYYY-MM-DD format

    provide_weekly_persistence_coaching_progress_notes: str = Field(
        default="",
        description=(
            "Brief notes on weekly persistence coaching, support, and encouragement. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PotentialSteps(BaseModel):
    """Optional or situational actions to support the young person’s progress"""

    improve_attendance_mornings_completed: BooleanLike = Field(
        default="",
        description="Indicate whether attendance coaching and morning texts have been completed.",
    )

    improve_attendance_mornings_yes: BooleanLike = Field(
        default="", description="Check if this attendance coaching step has been completed (YES)."
    )

    improve_attendance_mornings_no: BooleanLike = Field(
        default="",
        description="Check if this attendance coaching step has not been completed (NO).",
    )

    improve_attendance_mornings_date: str = Field(
        default="", description="Date when this attendance coaching step was completed or reviewed."
    )  # YYYY-MM-DD format

    improve_attendance_mornings_progress_notes: str = Field(
        default="",
        description=(
            "Notes on attendance coaching and morning communication. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    improve_attendance_peer_group_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the young person has been connected to a peer group or "
            "credible messenger."
        ),
    )

    improve_attendance_peer_group_yes: BooleanLike = Field(
        default="",
        description="Check if connection to a peer group or credible messenger is completed (YES).",
    )

    improve_attendance_peer_group_no: BooleanLike = Field(
        default="",
        description=(
            "Check if connection to a peer group or credible messenger is not completed (NO)."
        ),
    )

    improve_attendance_peer_group_date: str = Field(
        default="",
        description=(
            "Date when connection to a peer group or credible messenger occurred or was reviewed."
        ),
    )  # YYYY-MM-DD format

    improve_attendance_peer_group_progress_notes: str = Field(
        default="",
        description=(
            "Notes on connecting the young person to a peer group or credible messenger. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    improve_attendance_extracurricular_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the young person has been connected to an extracurricular "
            "program or experience."
        ),
    )

    improve_attendance_extracurricular_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if connection to an extracurricular program or experience is completed (YES)."
        ),
    )

    improve_attendance_extracurricular_no: BooleanLike = Field(
        default="",
        description=(
            "Check if connection to an extracurricular program or experience is not completed (NO)."
        ),
    )

    improve_attendance_extracurricular_date: str = Field(
        default="",
        description=(
            "Date when connection to an extracurricular program or experience occurred or "
            "was reviewed."
        ),
    )  # YYYY-MM-DD format

    improve_attendance_extracurricular_progress_notes: str = Field(
        default="",
        description=(
            "Notes on connecting the young person to an extracurricular program or "
            'experience. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    speak_meet_program_staff_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have spoken to or met with program staff about attendance "
            "or performance."
        ),
    )

    speak_meet_program_staff_yes: BooleanLike = Field(
        default="", description="Check if this contact with program staff has been completed (YES)."
    )

    speak_meet_program_staff_no: BooleanLike = Field(
        default="",
        description="Check if this contact with program staff has not been completed (NO).",
    )

    speak_meet_program_staff_date: str = Field(
        default="", description="Date when you spoke to or met with program staff."
    )  # YYYY-MM-DD format

    speak_meet_program_staff_progress_notes: str = Field(
        default="",
        description=(
            "Notes from the conversation or meeting with program staff. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    refer_student_tutor_completed: BooleanLike = Field(
        default="", description="Indicate whether the student has been referred to a tutor."
    )

    refer_student_tutor_yes: BooleanLike = Field(
        default="", description="Check if referral to a tutor has been completed (YES)."
    )

    refer_student_tutor_no: BooleanLike = Field(
        default="", description="Check if referral to a tutor has not been completed (NO)."
    )

    refer_student_tutor_date: str = Field(
        default="", description="Date when the student was referred to a tutor."
    )  # YYYY-MM-DD format

    refer_student_tutor_progress_notes: str = Field(
        default="",
        description=(
            'Notes about the referral to a tutor. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    follow_up_tutor_performance_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have followed up with the tutor about the student's performance."
        ),
    )

    follow_up_tutor_performance_yes: BooleanLike = Field(
        default="", description="Check if follow-up with the tutor has been completed (YES)."
    )

    follow_up_tutor_performance_no: BooleanLike = Field(
        default="", description="Check if follow-up with the tutor has not been completed (NO)."
    )

    follow_up_tutor_performance_date: str = Field(
        default="", description="Date when you followed up with the tutor."
    )  # YYYY-MM-DD format

    follow_up_tutor_performance_progress_notes: str = Field(
        default="",
        description=(
            "Notes from the follow-up with the tutor about performance. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    update_foster_parent_caregiver_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the foster parent or caregiver has been updated and "
            "encouraged to provide support."
        ),
    )

    update_foster_parent_caregiver_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if this update to the foster parent or caregiver has been completed (YES)."
        ),
    )

    update_foster_parent_caregiver_no: BooleanLike = Field(
        default="",
        description=(
            "Check if this update to the foster parent or caregiver has not been completed (NO)."
        ),
    )

    update_foster_parent_caregiver_date: str = Field(
        default="", description="Date when the foster parent or caregiver was updated."
    )  # YYYY-MM-DD format

    update_foster_parent_caregiver_progress_notes: str = Field(
        default="",
        description=(
            "Notes on communication with the foster parent or caregiver. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    ensure_transition_services_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have confirmed that the school is providing appropriate "
            "transition services."
        ),
    )

    ensure_transition_services_yes: BooleanLike = Field(
        default="",
        description="Check if ensuring appropriate transition services is completed (YES).",
    )

    ensure_transition_services_no: BooleanLike = Field(
        default="",
        description="Check if ensuring appropriate transition services is not completed (NO).",
    )

    ensure_transition_services_date: str = Field(
        default="", description="Date when transition services were reviewed or confirmed."
    )  # YYYY-MM-DD format

    ensure_transition_services_progress_notes: str = Field(
        default="",
        description=(
            "Notes on the school's transition services. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ensure_acces_vr_opwdd_meeting_completed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether ACCES-VR and/or OPWDD representatives participated in the "
            "student's IEP meeting."
        ),
    )

    ensure_acces_vr_opwdd_meeting_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if participation by ACCES-VR and/or OPWDD representatives is completed (YES)."
        ),
    )

    ensure_acces_vr_opwdd_meeting_no: BooleanLike = Field(
        default="",
        description=(
            "Check if participation by ACCES-VR and/or OPWDD representatives is not completed (NO)."
        ),
    )

    ensure_acces_vr_opwdd_meeting_date: str = Field(
        default="",
        description="Date when ACCES-VR and/or OPWDD participation was confirmed or occurred.",
    )  # YYYY-MM-DD format

    ensure_acces_vr_opwdd_meeting_progress_notes: str = Field(
        default="",
        description=(
            "Notes on ACCES-VR and/or OPWDD participation in the IEP meeting. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Describe any other step taken that is not listed above. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_completed: BooleanLike = Field(
        default="", description="Indicate whether the 'Other' step has been completed."
    )

    other_yes: BooleanLike = Field(
        default="", description="Check if the 'Other' step is completed (YES)."
    )

    other_no: BooleanLike = Field(
        default="", description="Check if the 'Other' step is not completed (NO)."
    )

    other_date: str = Field(
        default="", description="Date when the 'Other' step was completed or reviewed."
    )  # YYYY-MM-DD format

    other_progress_notes: str = Field(
        default="",
        description=(
            "Notes on the 'Other' step. .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class GoalTracking(BaseModel):
    """Overall tracking of the high school goal status and related details"""

    start_date: str = Field(
        default="", description="Date when work toward this goal started."
    )  # YYYY-MM-DD format

    goal_completed_date: str = Field(
        default="", description="Date when the goal was completed."
    )  # YYYY-MM-DD format

    goal_changed: BooleanLike = Field(default="", description="Check if the goal has been changed.")

    youth_name: str = Field(
        ...,
        description=(
            'Full name of the young person. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    goal_completed_yes: BooleanLike = Field(
        default="", description="Check if the goal has been completed (YES)."
    )

    goal_completed_yes_notes: str = Field(
        default="",
        description=(
            "Notes related to the goal being completed (YES). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    goal_completed_yes_date: str = Field(
        default="",
        description="Date associated with the confirmation that the goal was completed (YES).",
    )  # YYYY-MM-DD format

    coach: str = Field(
        ...,
        description=(
            "Name of the coach supporting the young person. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    goal_completed_no: BooleanLike = Field(
        default="", description="Check if the goal has not been completed (NO)."
    )

    goal_completed_no_notes: str = Field(
        default="",
        description=(
            "Notes explaining why the goal has not been completed (NO). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    goal_completed_no_date: str = Field(
        default="",
        description="Date associated with the determination that the goal was not completed (NO).",
    )  # YYYY-MM-DD format

    new_goal: str = Field(
        default="",
        description=(
            "Describe the new goal if the original goal has changed. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    notes: str = Field(
        default="",
        description=(
            "Additional notes related to this goal or its progress. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HighSchoolGoalObtainSkillsAndAchievementCommencementCredential(BaseModel):
    """
        HIGH SCHOOL GOAL:
    Obtain Skills and Achievement Commencement Credential

        Complete this worksheet if the young person is a student with an IEP who is alternately assessed only and 1 year away from obtaining a Skills and Achievement Commencement Credential.
    """

    required_steps: RequiredSteps = Field(..., description="Required Steps")
    potential_steps: PotentialSteps = Field(..., description="Potential Steps")
    goal_tracking: GoalTracking = Field(..., description="Goal Tracking")

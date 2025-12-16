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
    """Required actions to apply to other supportive housing residences"""

    reach_out_to_residence: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the step 'Reach out to residence' is being tracked in this row."
        ),
    )

    reach_out_to_residence_completed_yes: BooleanLike = Field(
        default="", description="Check if the 'Reach out to residence' step has been completed."
    )

    reach_out_to_residence_completed_no: BooleanLike = Field(
        default="", description="Check if the 'Reach out to residence' step has not been completed."
    )

    reach_out_to_residence_date: str = Field(
        default="",
        description="Date when the 'Reach out to residence' step was completed or last worked on.",
    )  # YYYY-MM-DD format

    reach_out_to_residence_progress_notes: str = Field(
        default="",
        description=(
            "Progress notes related to the 'Reach out to residence' step. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    complete_application: BooleanLike = Field(
        default="",
        description="Indicates whether the step 'Complete application' is being tracked in this row.",
    )

    complete_application_completed_yes: BooleanLike = Field(
        default="", description="Check if the 'Complete application' step has been completed."
    )

    complete_application_completed_no: BooleanLike = Field(
        default="", description="Check if the 'Complete application' step has not been completed."
    )

    complete_application_date: str = Field(
        default="",
        description="Date when the 'Complete application' step was completed or last worked on.",
    )  # YYYY-MM-DD format

    complete_application_progress_notes: str = Field(
        default="",
        description=(
            "Progress notes related to the 'Complete application' step. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PotentialSteps(BaseModel):
    """Optional or situational steps to support the housing application"""

    submit_any_other_required_documentation: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the step to submit any other required documentation is being "
            "tracked in this row."
        ),
    )

    submit_any_other_required_documentation_completed_yes: BooleanLike = Field(
        default="",
        description="Check if the 'Submit any other required documentation' step has been completed.",
    )

    submit_any_other_required_documentation_completed_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the 'Submit any other required documentation' step has not been completed."
        ),
    )

    submit_any_other_required_documentation_date: str = Field(
        default="",
        description=(
            "Date when the 'Submit any other required documentation' step was completed or "
            "last worked on."
        ),
    )  # YYYY-MM-DD format

    submit_any_other_required_documentation_progress_notes: str = Field(
        default="",
        description=(
            "Progress notes related to the 'Submit any other required documentation' step. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Description of any other step not listed, to be specified by the coach or "
            'youth. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other_completed_yes: BooleanLike = Field(
        default="", description="Check if the 'Other' step has been completed."
    )

    other_completed_no: BooleanLike = Field(
        default="", description="Check if the 'Other' step has not been completed."
    )

    other_date: str = Field(
        default="", description="Date when the 'Other' step was completed or last worked on."
    )  # YYYY-MM-DD format

    other_progress_notes: str = Field(
        default="",
        description=(
            "Progress notes related to the 'Other' step. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class GoalTracking(BaseModel):
    """Tracking the status and changes of the housing goal"""

    start_date: str = Field(
        default="", description="Date when work on this housing and independent living goal began."
    )  # YYYY-MM-DD format

    goal_completed_yes: BooleanLike = Field(
        default="", description="Indicates that the goal has been completed."
    )

    goal_completed_yes_notes: str = Field(
        default="",
        description=(
            "Notes or details when the goal is marked as completed (YES). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    goal_completed_no: BooleanLike = Field(
        default="", description="Indicates that the goal has not been completed."
    )

    goal_completed_no_notes: str = Field(
        default="",
        description=(
            "Notes or explanation when the goal is marked as not completed (NO). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_goal_completed_section: str = Field(
        default="", description="Date associated with the goal completion status."
    )  # YYYY-MM-DD format

    goal_changed: BooleanLike = Field(
        default="", description="Indicates that the original goal has been changed."
    )

    date_goal_changed_section: str = Field(
        default="", description="Date when the goal was changed."
    )  # YYYY-MM-DD format

    new_goal: str = Field(
        default="",
        description=(
            "Description of the new goal after the change. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_goal_changed_section: str = Field(
        default="",
        description=(
            "Additional notes or explanation about the goal change. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Identifying information for youth and coach"""

    youth_name: str = Field(
        ...,
        description=(
            'Full name of the young person. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    coach: str = Field(
        ...,
        description=(
            "Name of the coach supporting the youth. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class IndependentLivingGoalSupportiveHousingApplication(BaseModel):
    """
        HOUSING & INDEPENDENT LIVING GOAL:
    Apply to Other Supportive Housing Residence(s)

        Complete this worksheet if young person is age 19 or older and has an APPLA (Another Planned Permanent Living Arrangement) goal.
    """

    required_steps: RequiredSteps = Field(..., description="Required Steps")
    potential_steps: PotentialSteps = Field(..., description="Potential Steps")
    goal_tracking: GoalTracking = Field(..., description="Goal Tracking")
    signatures: Signatures = Field(..., description="Signatures")

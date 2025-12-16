from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentInformation(BaseModel):
    """Basic incident identification and operational period details"""

    incident_name: str = Field(
        ...,
        description=(
            'Name or designation of the incident .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    operational_period_date_from: str = Field(
        ..., description="Start date of the operational period"
    )  # YYYY-MM-DD format

    operational_period_date_to: str = Field(
        ..., description="End date of the operational period"
    )  # YYYY-MM-DD format

    operational_period_time_from: str = Field(
        ...,
        description=(
            'Start time of the operational period .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    operational_period_time_to: str = Field(
        ...,
        description=(
            'End time of the operational period .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SafetyMessagePlan(BaseModel):
    """Safety message and site safety plan requirements"""

    safety_message_expanded_safety_message_safety_plan_site_safety_plan: str = Field(
        ...,
        description=(
            "Detailed safety message, safety plan, or site safety plan for the incident .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    site_safety_plan_required_yes: BooleanLike = Field(
        default="", description="Check if a site safety plan is required"
    )

    site_safety_plan_required_no: BooleanLike = Field(
        default="", description="Check if a site safety plan is not required"
    )

    approved_site_safety_plans_located_at: str = Field(
        default="",
        description=(
            "Location where the approved site safety plan(s) can be found .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PreparedByFormInfo(BaseModel):
    """Prepared by details and form tracking information"""

    prepared_by_name: str = Field(
        ...,
        description=(
            "Name of the person who prepared this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_position_title: str = Field(
        ...,
        description=(
            "Position or title of the person who prepared this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_signature: str = Field(
        ...,
        description=(
            "Signature of the person who prepared this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    iap_page: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Page number within the Incident Action Plan (IAP)"
    )

    date_time: str = Field(
        ...,
        description=(
            'Date and time this form was completed .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SafetyMessageplanics208(BaseModel):
    """
    SAFETY MESSAGE/PLAN (ICS 208)

    ''
    """

    incident_information: IncidentInformation = Field(..., description="Incident Information")
    safety_message__plan: SafetyMessagePlan = Field(..., description="Safety Message / Plan")
    prepared_by__form_info: PreparedByFormInfo = Field(..., description="Prepared By / Form Info")

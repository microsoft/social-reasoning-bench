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
            'Name or identifier of the incident .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
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


class IncidentObjectivesandCommandEmphasis(BaseModel):
    """Objectives for the operational period and command emphasis"""

    objectives: str = Field(
        ...,
        description=(
            "List the incident objectives for this operational period .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    operational_period_command_emphasis: str = Field(
        default="",
        description=(
            "Key command emphasis, priorities, or instructions for this operational period "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SiteSafetyPlan(BaseModel):
    """Site safety plan requirement and location"""

    site_safety_plan_required_yes: BooleanLike = Field(
        ..., description="Check if a site safety plan is required"
    )

    site_safety_plan_required_no: BooleanLike = Field(
        ..., description="Check if a site safety plan is not required"
    )

    approved_site_safety_plan_s_located_at: str = Field(
        default="",
        description=(
            "Location where the approved site safety plan(s) can be found .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class IncidentActionPlanComponents(BaseModel):
    """ICS forms and other documents included in this Incident Action Plan"""

    ics_203: BooleanLike = Field(
        default="",
        description="Check if ICS 203 (Organization Assignment List) is included in this IAP",
    )

    ics_204: BooleanLike = Field(
        default="", description="Check if ICS 204 (Assignment List) is included in this IAP"
    )

    ics_205: BooleanLike = Field(
        default="",
        description="Check if ICS 205 (Incident Radio Communications Plan) is included in this IAP",
    )

    ics_205a: BooleanLike = Field(
        default="", description="Check if ICS 205A (Communications List) is included in this IAP"
    )

    ics_206: BooleanLike = Field(
        default="", description="Check if ICS 206 (Medical Plan) is included in this IAP"
    )

    ics_207: BooleanLike = Field(
        default="",
        description="Check if ICS 207 (Incident Organization Chart) is included in this IAP",
    )

    ics_208: BooleanLike = Field(
        default="", description="Check if ICS 208 (Safety Message/Plan) is included in this IAP"
    )

    map_chart: BooleanLike = Field(
        default="", description="Check if a map or chart is included in this IAP"
    )

    weather_forecast_tides_currents: BooleanLike = Field(
        default="",
        description=(
            "Check if weather forecast, tides, or currents information is included in this IAP"
        ),
    )

    other_attachments_1: str = Field(
        default="",
        description=(
            "Description of an additional attachment included in this IAP .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_attachments_2: str = Field(
        default="",
        description=(
            "Description of an additional attachment included in this IAP .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_attachments_3: str = Field(
        default="",
        description=(
            "Description of an additional attachment included in this IAP .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_attachments_4: str = Field(
        default="",
        description=(
            "Description of an additional attachment included in this IAP .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Approvals(BaseModel):
    """Prepared by and Incident Commander approval information"""

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

    approved_by_incident_commander_name: str = Field(
        ...,
        description=(
            "Name of the Incident Commander approving this form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_incident_commander_signature: str = Field(
        ...,
        description=(
            "Signature of the Incident Commander approving this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FormMetadata(BaseModel):
    """Form page and timestamp information"""

    iap_page: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Page number of this form within the Incident Action Plan"
    )

    date_time: str = Field(
        ...,
        description=(
            "Date and time when this form was prepared or last updated .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentObjectivesics202(BaseModel):
    """
    INCIDENT OBJECTIVES (ICS 202)

    ''
    """

    incident_information: IncidentInformation = Field(..., description="Incident Information")
    incident_objectives_and_command_emphasis: IncidentObjectivesandCommandEmphasis = Field(
        ..., description="Incident Objectives and Command Emphasis"
    )
    site_safety_plan: SiteSafetyPlan = Field(..., description="Site Safety Plan")
    incident_action_plan_components: IncidentActionPlanComponents = Field(
        ..., description="Incident Action Plan Components"
    )
    approvals: Approvals = Field(..., description="Approvals")
    form_metadata: FormMetadata = Field(..., description="Form Metadata")

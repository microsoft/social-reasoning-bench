from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentIdentification(BaseModel):
    """Basic identifying information for the incident"""

    incident_name: str = Field(
        ...,
        description=(
            'Official name of the incident. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    incident_number: str = Field(
        ...,
        description=(
            "Unique incident or case number assigned by the agency. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ics_209_page_number_total: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Total number of pages in the ICS 209 form (value for the blank after 'Page 2 of')."
        ),
    )


class PublicStatusSummaryItem31(BaseModel):
    """Status summary and impacts to civilians/public"""

    number_of_civilians_public_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total number of civilians (public) affected during this reporting period.",
    )

    number_of_civilians_public_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative total number of civilians (public) affected to date."
    )

    civilian_fatalities_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of civilian fatalities during this reporting period."
    )

    civilian_fatalities_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of civilian fatalities to date."
    )

    civilians_with_injuries_illness_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of civilians with injuries or illness during this reporting period.",
    )

    civilians_with_injuries_illness_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of civilians with injuries or illness to date."
    )

    civilians_trapped_in_need_of_rescue_this_reporting_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Number of civilians trapped or in need of rescue during this reporting period.",
        )
    )

    civilians_trapped_in_need_of_rescue_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Cumulative number of civilians trapped or in need of rescue to date.",
    )

    civilians_missing_note_if_estimated_this_reporting_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Number of civilians missing during this reporting period; note if the value is "
                "estimated."
            ),
        )
    )

    civilians_missing_note_if_estimated_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Cumulative number of civilians missing to date; note if the value is estimated.",
    )

    civilians_evacuated_note_if_estimated_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of civilians evacuated during this reporting period; note if the value "
            "is estimated."
        ),
    )

    civilians_evacuated_note_if_estimated_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Cumulative number of civilians evacuated to date; note if the value is estimated."
        ),
    )

    civilians_sheltering_in_place_note_if_estimated_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of civilians sheltering in place during this reporting period; note if "
            "the value is estimated."
        ),
    )

    civilians_sheltering_in_place_note_if_estimated_total_to_date: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Cumulative number of civilians sheltering in place to date; note if the value "
            "is estimated."
        ),
    )

    civilians_in_temporary_shelters_note_if_est_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of civilians in temporary shelters during this reporting period; note "
            "if the value is estimated."
        ),
    )

    civilians_in_temporary_shelters_note_if_est_total_to_date: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Cumulative number of civilians in temporary shelters to date; note if the "
                "value is estimated."
            ),
        )
    )

    civilians_have_received_mass_immunizations_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of civilians who have received mass immunizations during this reporting period."
        ),
    )

    civilians_have_received_mass_immunizations_total_to_date: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Cumulative number of civilians who have received mass immunizations to date.",
        )
    )

    civilians_require_immunizations_note_if_est_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of civilians requiring immunizations during this reporting period; note "
            "if the value is estimated."
        ),
    )

    civilians_require_immunizations_note_if_est_total_to_date: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Cumulative number of civilians requiring immunizations to date; note if the "
                "value is estimated."
            ),
        )
    )

    civilians_in_quarantine_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of civilians in quarantine during this reporting period."
    )

    civilians_in_quarantine_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of civilians in quarantine to date."
    )

    total_number_of_civilians_public_affected: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Overall total number of civilians (public) affected by the incident.",
    )


class ResponderStatusSummaryItem32(BaseModel):
    """Status summary and impacts to responders"""

    number_of_responders_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of responders affected during this reporting period."
    )

    number_of_responders_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative total number of responders affected to date."
    )

    responder_fatalities_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of responder fatalities during this reporting period."
    )

    responder_fatalities_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responder fatalities to date."
    )

    responders_with_injuries_illness_this_reporting_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Number of responders with injuries or illness during this reporting period.",
        )
    )

    responders_with_injuries_illness_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responders with injuries or illness to date."
    )

    responders_trapped_in_need_of_rescue_this_reporting_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Number of responders trapped or in need of rescue during this reporting period.",
        )
    )

    responders_trapped_in_need_of_rescue_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Cumulative number of responders trapped or in need of rescue to date.",
    )

    responders_missing_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of responders missing during this reporting period."
    )

    responders_missing_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responders missing to date."
    )

    responders_sheltering_in_place_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of responders sheltering in place during this reporting period.",
    )

    responders_sheltering_in_place_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responders sheltering in place to date."
    )

    responders_have_received_immunizations_this_reporting_period: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Number of responders who have received immunizations during this reporting period."
        ),
    )

    responders_have_received_immunizations_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Cumulative number of responders who have received immunizations to date.",
    )

    responders_require_immunizations_this_reporting_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Number of responders requiring immunizations during this reporting period.",
        )
    )

    responders_require_immunizations_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responders requiring immunizations to date."
    )

    responders_in_quarantine_this_reporting_period: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of responders in quarantine during this reporting period."
    )

    responders_in_quarantine_total_to_date: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cumulative number of responders in quarantine to date."
    )

    total_number_of_responders_affected: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Overall total number of responders affected by the incident."
    )


class LifeSafetyandHealthItems3334(BaseModel):
    """Narrative remarks and threat management actions for life, safety, and health"""

    life_safety_and_health_status_threat_remarks: str = Field(
        default="",
        description=(
            "Narrative description of life, safety, and health status or threats. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    no_likely_threat: BooleanLike = Field(
        default="", description="Check if there is no likely life, safety, or health threat."
    )

    potential_future_threat: BooleanLike = Field(
        default="",
        description="Check if there is a potential future life, safety, or health threat.",
    )

    mass_notifications_in_progress: BooleanLike = Field(
        default="", description="Check if mass notifications are currently in progress."
    )

    mass_notifications_completed: BooleanLike = Field(
        default="", description="Check if mass notifications have been completed."
    )

    no_evacuations_imminent: BooleanLike = Field(
        default="", description="Check if no evacuations are imminent."
    )

    planning_for_evacuation: BooleanLike = Field(
        default="", description="Check if planning for evacuation is underway."
    )

    planning_for_shelter_in_place: BooleanLike = Field(
        default="", description="Check if planning for shelter-in-place is underway."
    )

    evacuations_in_progress: BooleanLike = Field(
        default="", description="Check if evacuations are currently in progress."
    )

    shelter_in_place_in_progress: BooleanLike = Field(
        default="", description="Check if shelter-in-place is currently in progress."
    )

    repopulation_in_progress: BooleanLike = Field(
        default="", description="Check if repopulation of affected areas is in progress."
    )

    mass_immunization_in_progress: BooleanLike = Field(
        default="", description="Check if mass immunization activities are in progress."
    )

    mass_immunization_complete: BooleanLike = Field(
        default="", description="Check if mass immunization activities are complete."
    )

    quarantine_in_progress: BooleanLike = Field(
        default="", description="Check if quarantine measures are currently in progress."
    )

    area_restriction_in_effect: BooleanLike = Field(
        default="", description="Check if area restrictions are currently in effect."
    )

    life_safety_and_health_threat_management_additional_option_1: BooleanLike = Field(
        default="",
        description=(
            "Additional user-defined life, safety, and health threat management option "
            "(first blank checkbox)."
        ),
    )

    life_safety_and_health_threat_management_additional_option_2: BooleanLike = Field(
        default="",
        description=(
            "Additional user-defined life, safety, and health threat management option "
            "(second blank checkbox)."
        ),
    )

    life_safety_and_health_threat_management_additional_option_3: BooleanLike = Field(
        default="",
        description=(
            "Additional user-defined life, safety, and health threat management option "
            "(third blank checkbox)."
        ),
    )


class WeatherConcernsItem35(BaseModel):
    """Current and predicted weather concerns affecting the incident"""

    weather_concerns: str = Field(
        default="",
        description=(
            "Synopsis of current and predicted weather and related concerns. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ProjectedIncidentActivityItem36(BaseModel):
    """Projected incident activity and influencing factors over time"""

    projected_incident_activity_12_hours: str = Field(
        default="",
        description=(
            "Projected incident activity, potential, movement, escalation, or spread over "
            'the next 12 hours. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    projected_incident_activity_24_hours: str = Field(
        default="",
        description=(
            "Projected incident activity, potential, movement, escalation, or spread over "
            'the next 24 hours. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    projected_incident_activity_48_hours: str = Field(
        default="",
        description=(
            "Projected incident activity, potential, movement, escalation, or spread over "
            'the next 48 hours. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    projected_incident_activity_72_hours: str = Field(
        default="",
        description=(
            "Projected incident activity, potential, movement, escalation, or spread over "
            'the next 72 hours. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    projected_incident_activity_anticipated_after_72_hours: str = Field(
        default="",
        description=(
            "Projected incident activity, potential, movement, escalation, or spread "
            'anticipated after 72 hours. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class StrategicObjectivesItem37(BaseModel):
    """Planned end-state and strategic objectives for the incident"""

    strategic_objectives: str = Field(
        default="",
        description=(
            "Strategic objectives defining the planned end-state for the incident. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class IncidentStatusSummaryics209(BaseModel):
    """
    INCIDENT STATUS SUMMARY (ICS 209)

    ''
    """

    incident_identification: IncidentIdentification = Field(
        ..., description="Incident Identification"
    )
    public_status_summary_item_31: PublicStatusSummaryItem31 = Field(
        ..., description="Public Status Summary (Item 31)"
    )
    responder_status_summary_item_32: ResponderStatusSummaryItem32 = Field(
        ..., description="Responder Status Summary (Item 32)"
    )
    life_safety_and_health_items_33_34: LifeSafetyandHealthItems3334 = Field(
        ..., description="Life, Safety, and Health (Items 33–34)"
    )
    weather_concerns_item_35: WeatherConcernsItem35 = Field(
        ..., description="Weather Concerns (Item 35)"
    )
    projected_incident_activity_item_36: ProjectedIncidentActivityItem36 = Field(
        ..., description="Projected Incident Activity (Item 36)"
    )
    strategic_objectives_item_37: StrategicObjectivesItem37 = Field(
        ..., description="Strategic Objectives (Item 37)"
    )

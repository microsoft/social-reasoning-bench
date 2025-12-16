from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentStatusSummary(BaseModel):
    """Core incident identification and reporting period details"""

    incident_name: str = Field(
        ...,
        description=(
            "Official name assigned to the incident .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    incident_number: str = Field(
        default="",
        description=(
            "Unique incident or case number assigned by the agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    report_version_initial: BooleanLike = Field(
        ..., description="Check if this ICS 209 is the initial report for the incident"
    )

    rpt_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sequential report number for this incident status summary"
    )

    report_version_update_if_used: BooleanLike = Field(
        ..., description="Check if this ICS 209 is an update to a previous report"
    )

    report_version_final: BooleanLike = Field(
        ..., description="Check if this ICS 209 is the final report for the incident"
    )

    incident_commanders_agency_or_organization: str = Field(
        ...,
        description=(
            "Name(s) of Incident Commander(s) and their agency or organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    incident_management_organization: str = Field(
        default="",
        description=(
            "Type or name of the incident management organization in place .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    incident_start_date: str = Field(
        ..., description="Calendar date when the incident started"
    )  # YYYY-MM-DD format

    incident_start_time: str = Field(
        ...,
        description=(
            'Clock time when the incident started .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    incident_start_time_zone: str = Field(
        ...,
        description=(
            "Time zone for the incident start date and time .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_incident_size_or_area_involved_use_unit_label_e_g_sq_mi_city_block: str = Field(
        default="",
        description=(
            "Current size or area affected by the incident, including units (e.g., acres, "
            'sq mi, city blocks) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    percent_contained_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Percentage of the incident that is contained or completed"
    )

    incident_definition: str = Field(
        ...,
        description=(
            "Brief definition or description of what constitutes the incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    incident_complexity_level: str = Field(
        default="",
        description=(
            "Complexity level of the incident (e.g., Type 1–5 or other classification) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    for_time_period_from_date_time: str = Field(
        ...,
        description=(
            "Start date and time for the reporting period covered by this form .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    for_time_period_to_date_time: str = Field(
        ...,
        description=(
            "End date and time for the reporting period covered by this form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApprovalRoutingInformation(BaseModel):
    """Preparation, submission, approval, and routing details"""

    prepared_by_print_name: str = Field(
        ...,
        description=(
            "Printed name of the person who prepared this form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_ics_position: str = Field(
        ...,
        description=(
            "ICS position title of the person who prepared this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_prepared: str = Field(
        ...,
        description=(
            "Date and time when this form was completed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_submitted: str = Field(
        ...,
        description=(
            "Date and time when this form was submitted .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    time_zone: str = Field(
        ...,
        description=(
            "Time zone used for the submitted date and time .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_print_name: str = Field(
        ...,
        description=(
            "Printed name of the official who approved this form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_ics_position: str = Field(
        ...,
        description=(
            "ICS position title of the approving official .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_signature: str = Field(
        ...,
        description=(
            'Signature of the approving official .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    primary_location_organization_or_agency_sent_to: str = Field(
        ...,
        description=(
            "Primary location, organization, or agency to which this form is sent .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class IncidentLocationInformation(BaseModel):
    """Jurisdictional, geographic, and mapping information for the incident"""

    state: str = Field(..., description="State where the incident is located")

    county_parish_borough: str = Field(
        ...,
        description=(
            "County, parish, or borough where the incident is located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the incident is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    unit_or_other: str = Field(
        default="",
        description=(
            "Additional unit, district, or other location descriptor .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    incident_jurisdiction: str = Field(
        ...,
        description=(
            "Jurisdiction that has authority over the incident .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    incident_location_ownership_if_different_than_jurisdiction: str = Field(
        default="",
        description=(
            "Owner of the incident location if different from the jurisdiction .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    longitude_indicate_format: str = Field(
        default="",
        description=(
            "Longitude of the incident location, including coordinate format .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    latitude_indicate_format: str = Field(
        default="",
        description=(
            "Latitude of the incident location, including coordinate format .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    us_national_grid_reference: str = Field(
        default="",
        description=(
            "US National Grid (USNG) reference for the incident location .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    legal_description_township_section_range: str = Field(
        default="",
        description=(
            "Legal land description including township, section, and range .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    short_location_or_area_description_list_all_affected_areas_or_a_reference_point: str = Field(
        ...,
        description=(
            "Brief description of the location or area, listing all affected areas or a key "
            'reference point .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    utm_coordinates: str = Field(
        default="",
        description=(
            "Universal Transverse Mercator (UTM) coordinates for the incident location .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    note_any_electronic_geospatial_data_included_or_attached_indicate_data_format_content_and_collection_time_information_and_labels: str = Field(
        default="",
        description=(
            "Description of any attached electronic geospatial data, including format, "
            'content, collection time, and labels .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class IncidentSummary(BaseModel):
    """Narrative summary, hazards, and damage assessment"""

    significant_events_for_the_time_period_reported_summarize_significant_progress_made_evacuations_incident_growth_etc: str = Field(
        ...,
        description=(
            "Narrative summary of significant events and developments during the reporting "
            'period .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    primary_materials_or_hazards_involved_hazardous_chemicals_fuel_types_infectious_agents_radiation_etc: str = Field(
        default="",
        description=(
            "Description of primary materials or hazards involved in the incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    damage_assessment_information_structural_summary: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Summary count of affected structures"
    )

    damage_assessment_information_threatened_72_hrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of structures or assets threatened within the next 72 hours"
    )

    damage_assessment_information_damaged: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of structures or assets damaged"
    )

    damage_assessment_information_destroyed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of structures or assets destroyed"
    )

    damage_assessment_information_single_residences: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Damage counts for single-family residences"
    )

    damage_assessment_information_nonresidential_commercial_property: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Damage counts for nonresidential commercial properties")

    damage_assessment_information_other_minor_structures: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Damage counts for other minor structures"
    )

    damage_assessment_information_other: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Damage counts for other structure or asset categories not listed above",
    )

    ics_209_page_1_of: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pages for this ICS 209 form"
    )


class IncidentStatusSummaryics209(BaseModel):
    """
    INCIDENT STATUS SUMMARY (ICS 209)

    ''
    """

    incident_status_summary: IncidentStatusSummary = Field(
        ..., description="Incident Status Summary"
    )
    approval__routing_information: ApprovalRoutingInformation = Field(
        ..., description="Approval & Routing Information"
    )
    incident_location_information: IncidentLocationInformation = Field(
        ..., description="Incident Location Information"
    )
    incident_summary: IncidentSummary = Field(..., description="Incident Summary")

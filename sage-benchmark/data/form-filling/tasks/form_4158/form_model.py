from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientInformation(BaseModel):
    """Information about where the Notice of Determination is being sent"""

    office_of_planning_and_research: BooleanLike = Field(
        default="",
        description=(
            "Check if the Notice of Determination is being sent to the Office of Planning "
            "and Research"
        ),
    )

    county_clerk: BooleanLike = Field(
        default="",
        description="Check if the Notice of Determination is being sent to the County Clerk",
    )

    county_of: str = Field(
        ...,
        description=(
            "Name of the county for the County Clerk .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_county_clerk_line_1: str = Field(
        ...,
        description=(
            "First line of the County Clerk mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_county_clerk_line_2: str = Field(
        default="",
        description=(
            "Second line of the County Clerk mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FromLeadAgencyInformation(BaseModel):
    """Information about the public agency submitting the notice and the lead agency"""

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_from_line_1: str = Field(
        ...,
        description=(
            "First line of the submitting public agency address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_from_line_2: str = Field(
        default="",
        description=(
            "Second line of the submitting public agency address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_from: str = Field(
        ...,
        description=(
            "Primary contact person at the submitting public agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_from: str = Field(
        ...,
        description=(
            "Phone number for the contact at the submitting public agency .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    lead_agency_if_different_from_above: str = Field(
        default="",
        description=(
            "Name of the lead agency, if different from the submitting public agency .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_lead_agency_line_1: str = Field(
        default="",
        description=(
            'First line of the lead agency address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_lead_agency_line_2: str = Field(
        default="",
        description=(
            "Second line of the lead agency address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_lead_agency: str = Field(
        default="",
        description=(
            "Primary contact person at the lead agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_lead_agency: str = Field(
        default="",
        description=(
            "Phone number for the contact at the lead agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIdentification(BaseModel):
    """Identifiers and basic details for the project"""

    state_clearinghouse_number_if_submitted_to_state_clearinghouse: str = Field(
        default="",
        description=(
            "State Clearinghouse (SCH) number, if the project was submitted to the State "
            'Clearinghouse .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    project_title: str = Field(
        ...,
        description=(
            'Official title or name of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_applicant: str = Field(
        ...,
        description=(
            'Name of the project applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    project_location_include_county: str = Field(
        ...,
        description=(
            "Location of the project, including the county .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            'Brief description of the project .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_approving_entity: str = Field(
        ...,
        description=(
            "Name of the agency or body that approved the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_approval_date: str = Field(
        ..., description="Date on which the project was approved"
    )  # YYYY-MM-DD format


class CEQADeterminations(BaseModel):
    """Environmental review and determination information under CEQA"""

    will_significant_effect_on_the_environment: BooleanLike = Field(
        ..., description="Select if the project will have a significant effect on the environment"
    )

    will_not_significant_effect_on_the_environment: BooleanLike = Field(
        ...,
        description="Select if the project will not have a significant effect on the environment",
    )

    eir_prepared: BooleanLike = Field(
        ...,
        description="Check if an Environmental Impact Report (EIR) was prepared for this project",
    )

    negative_declaration_prepared: BooleanLike = Field(
        ..., description="Check if a Negative Declaration was prepared for this project"
    )

    mitigation_measures_were_condition: BooleanLike = Field(
        ..., description="Select if mitigation measures were made a condition of project approval"
    )

    mitigation_measures_were_not_condition: BooleanLike = Field(
        ...,
        description="Select if mitigation measures were not made a condition of project approval",
    )

    mitigation_plan_was_adopted: BooleanLike = Field(
        ...,
        description=(
            "Select if a mitigation reporting or monitoring plan was adopted for this project"
        ),
    )

    mitigation_plan_was_not_adopted: BooleanLike = Field(
        ...,
        description=(
            "Select if a mitigation reporting or monitoring plan was not adopted for this project"
        ),
    )

    overriding_considerations_was_adopted: BooleanLike = Field(
        ...,
        description="Select if a Statement of Overriding Considerations was adopted for this project",
    )

    overriding_considerations_was_not_adopted: BooleanLike = Field(
        ...,
        description=(
            "Select if a Statement of Overriding Considerations was not adopted for this project"
        ),
    )

    findings_were_made: BooleanLike = Field(
        ..., description="Select if findings were made pursuant to the provisions of CEQA"
    )

    findings_were_not_made: BooleanLike = Field(
        ..., description="Select if findings were not made pursuant to the provisions of CEQA"
    )


class DocumentAvailabilityandCertification(BaseModel):
    """Location of environmental documents and certification/signature details"""

    eir_location: str = Field(
        ...,
        description=(
            "Location or address where the final EIR/Negative Declaration and record of "
            "project approval are available to the public .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_public_agency: str = Field(
        ...,
        description=(
            "Authorized signature for the public agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Title or position of the signing official .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the Notice of Determination is signed"
    )  # YYYY-MM-DD format

    date_received_for_filing_at_opr: str = Field(
        default="",
        description=(
            "Date the Notice of Determination was received for filing at the Office of "
            "Planning and Research"
        ),
    )  # YYYY-MM-DD format


class NoticeOfDetermination(BaseModel):
    """
    Notice of Determination

    SUBJECT: Filing of Notice of Determination in compliance with Section 21108 or 21152 of the Public Resources Code.
    """

    recipient_information: RecipientInformation = Field(..., description="Recipient Information")
    from__lead_agency_information: FromLeadAgencyInformation = Field(
        ..., description="From / Lead Agency Information"
    )
    project_identification: ProjectIdentification = Field(..., description="Project Identification")
    ceqa_determinations: CEQADeterminations = Field(..., description="CEQA Determinations")
    document_availability_and_certification: DocumentAvailabilityandCertification = Field(
        ..., description="Document Availability and Certification"
    )

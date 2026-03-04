from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientandAgencyInformation(BaseModel):
    """Addresses and contact information for OPR, County Clerk, Public Agency, and Lead Agency"""

    office_of_planning_and_research: BooleanLike = Field(
        default="",
        description=(
            "Check if the Notice of Determination is being sent to the Office of Planning "
            "and Research"
        ),
    )

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_1: str = Field(
        ...,
        description=(
            "Mailing address of the public agency (line 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_2: str = Field(
        default="",
        description=(
            "Mailing address of the public agency (line 2, if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact: str = Field(
        ...,
        description=(
            "Primary contact person at the public agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number for the public agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county_clerk: BooleanLike = Field(
        default="",
        description="Check if the Notice of Determination is being sent to the County Clerk",
    )

    county_of: str = Field(
        default="",
        description=(
            "Name of the county for the County Clerk .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_3: str = Field(
        default="",
        description=(
            "Mailing address of the County Clerk (line 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_4: str = Field(
        default="",
        description=(
            "Mailing address of the County Clerk (line 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lead_agency_if_different_from_above: str = Field(
        default="",
        description=(
            "Name of the lead agency if different from the public agency listed above .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_5: str = Field(
        default="",
        description=(
            "Mailing address of the lead agency (line 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_6: str = Field(
        default="",
        description=(
            "Mailing address of the lead agency (line 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_2: str = Field(
        default="",
        description=(
            "Primary contact person at the lead agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_2: str = Field(
        default="",
        description=(
            "Phone number for the lead agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIdentification(BaseModel):
    """Identifiers and basic information about the project"""

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
            'Official title of the project .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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


class ProjectDeterminations(BaseModel):
    """Agency designation, approval date, and CEQA determinations"""

    lead_agency_choice: BooleanLike = Field(
        ..., description="Indicate that the approving agency is the lead agency"
    )

    responsible_agency_choice: BooleanLike = Field(
        ..., description="Indicate that the approving agency is a responsible agency"
    )

    project_approval_date: str = Field(
        ..., description="Date on which the project was approved"
    )  # YYYY-MM-DD format

    project_will_have_significant_effect: BooleanLike = Field(
        ..., description="Select if the project will have a significant effect on the environment"
    )

    project_will_not_have_significant_effect: BooleanLike = Field(
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
        ...,
        description="Indicate that mitigation measures were made a condition of project approval",
    )

    mitigation_measures_were_not_condition: BooleanLike = Field(
        ...,
        description="Indicate that mitigation measures were not made a condition of project approval",
    )

    mitigation_plan_adopted: BooleanLike = Field(
        ..., description="Indicate that a mitigation reporting or monitoring plan was adopted"
    )

    mitigation_plan_not_adopted: BooleanLike = Field(
        ..., description="Indicate that a mitigation reporting or monitoring plan was not adopted"
    )

    overriding_considerations_adopted: BooleanLike = Field(
        ..., description="Indicate that a Statement of Overriding Considerations was adopted"
    )

    overriding_considerations_not_adopted: BooleanLike = Field(
        ..., description="Indicate that a Statement of Overriding Considerations was not adopted"
    )

    findings_were_made: BooleanLike = Field(
        ..., description="Indicate that findings were made pursuant to CEQA"
    )

    findings_were_not_made: BooleanLike = Field(
        ..., description="Indicate that findings were not made pursuant to CEQA"
    )


class DocumentAvailability(BaseModel):
    """Location where the final EIR or Negative Declaration is available"""

    eir_location_line_1: str = Field(
        ...,
        description=(
            "Location (line 1) where the final EIR or Negative Declaration is available to "
            'the public .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    eir_location_line_2: str = Field(
        default="",
        description=(
            "Location (line 2) where the final EIR or Negative Declaration is available to "
            'the public .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class CertificationandFiling(BaseModel):
    """Signature, title, and filing dates"""

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
            "Title of the person signing for the public agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the notice was signed")  # YYYY-MM-DD format

    date_received_for_filing_at_opr: str = Field(
        default="",
        description="Date the notice was received for filing at the Office of Planning and Research",
    )  # YYYY-MM-DD format


class NoticeOfDetermination(BaseModel):
    """
    Notice of Determination

    SUBJECT: Filing of Notice of Determination in compliance with Section 21108 or 21152 of the Public Resources Code.
    """

    recipient_and_agency_information: RecipientandAgencyInformation = Field(
        ..., description="Recipient and Agency Information"
    )
    project_identification: ProjectIdentification = Field(..., description="Project Identification")
    project_determinations: ProjectDeterminations = Field(..., description="Project Determinations")
    document_availability: DocumentAvailability = Field(..., description="Document Availability")
    certification_and_filing: CertificationandFiling = Field(
        ..., description="Certification and Filing"
    )

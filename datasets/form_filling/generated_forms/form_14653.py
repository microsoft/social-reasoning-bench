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
            "and Research."
        ),
    )

    county_clerk: BooleanLike = Field(
        default="",
        description="Check if the Notice of Determination is being sent to the County Clerk.",
    )

    county_of: str = Field(
        ...,
        description=(
            "Name of the county where the County Clerk is located. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_county_clerk_line_1: str = Field(
        ...,
        description=(
            "First line of the County Clerk's mailing address. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_county_clerk_line_2: str = Field(
        default="",
        description=(
            "Second line of the County Clerk's mailing address (if needed). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FromAgencyInformation(BaseModel):
    """Information about the public agency submitting the notice and any separate lead agency"""

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the Notice of Determination. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_from_public_agency_line_1: str = Field(
        ...,
        description=(
            "First line of the submitting public agency's address. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_from_public_agency_line_2: str = Field(
        default="",
        description=(
            "Second line of the submitting public agency's address (if needed). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contact_from_public_agency: str = Field(
        ...,
        description=(
            "Name of the primary contact person at the submitting public agency. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone_from_public_agency: str = Field(
        ...,
        description=(
            "Telephone number for the contact at the submitting public agency. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    lead_agency_if_different_from_above: str = Field(
        default="",
        description=(
            "Name of the lead agency if it is different from the submitting public agency. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    address_lead_agency_line_1: str = Field(
        default="",
        description=(
            "First line of the lead agency's address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_lead_agency_line_2: str = Field(
        default="",
        description=(
            "Second line of the lead agency's address (if needed). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_lead_agency: str = Field(
        default="",
        description=(
            "Name of the primary contact person at the lead agency. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_lead_agency: str = Field(
        default="",
        description=(
            "Telephone number for the contact at the lead agency. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIdentification(BaseModel):
    """Identifiers and basic information about the project"""

    state_clearinghouse_number_if_submitted_to_state_clearinghouse: str = Field(
        default="",
        description=(
            "State Clearinghouse (SCH) number, if the project was submitted to the State "
            'Clearinghouse. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    project_title: str = Field(
        ...,
        description=(
            "Official title or name of the project. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_applicant: str = Field(
        ...,
        description=(
            "Name of the project applicant or project proponent. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_description_line_1: str = Field(
        ...,
        description=(
            "First line of the brief description of the project. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_description_line_2: str = Field(
        default="",
        description=(
            "Second line for continuing the project description, if needed. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ProjectDetermination(BaseModel):
    """Agency approval details and CEQA determination checkboxes"""

    approving_agency_name: str = Field(
        ...,
        description=(
            "Name of the agency that approved the project. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_approval_date: str = Field(
        ..., description="Date on which the project was approved."
    )  # YYYY-MM-DD format

    lead_agency_checkbox: BooleanLike = Field(
        default="", description="Check if the approving agency is acting as the Lead Agency."
    )

    responsible_agency_checkbox: BooleanLike = Field(
        default="", description="Check if the approving agency is acting as a Responsible Agency."
    )

    project_will_have_significant_effect: BooleanLike = Field(
        ...,
        description="Indicate that the project will have a significant effect on the environment.",
    )

    project_will_not_have_significant_effect: BooleanLike = Field(
        ...,
        description=(
            "Indicate that the project will not have a significant effect on the environment."
        ),
    )

    eir_prepared: BooleanLike = Field(
        ...,
        description="Check if an Environmental Impact Report (EIR) was prepared for this project.",
    )

    negative_declaration_prepared: BooleanLike = Field(
        ..., description="Check if a Negative Declaration was prepared for this project."
    )

    mitigation_measures_were_condition: BooleanLike = Field(
        ...,
        description="Indicate that mitigation measures were made a condition of project approval.",
    )

    mitigation_measures_were_not_condition: BooleanLike = Field(
        ...,
        description=(
            "Indicate that mitigation measures were not made a condition of project approval."
        ),
    )

    mitigation_plan_was_adopted: BooleanLike = Field(
        ...,
        description=(
            "Indicate that a mitigation reporting or monitoring plan was adopted for this project."
        ),
    )

    mitigation_plan_was_not_adopted: BooleanLike = Field(
        ...,
        description=(
            "Indicate that a mitigation reporting or monitoring plan was not adopted for "
            "this project."
        ),
    )

    overriding_considerations_were_adopted: BooleanLike = Field(
        ...,
        description=(
            "Indicate that a Statement of Overriding Considerations was adopted for this project."
        ),
    )

    overriding_considerations_were_not_adopted: BooleanLike = Field(
        ...,
        description=(
            "Indicate that a Statement of Overriding Considerations was not adopted for "
            "this project."
        ),
    )

    findings_were_made: BooleanLike = Field(
        ..., description="Indicate that findings were made pursuant to CEQA."
    )

    findings_were_not_made: BooleanLike = Field(
        ..., description="Indicate that findings were not made pursuant to CEQA."
    )


class DocumentAvailability(BaseModel):
    """Location where the final EIR or Negative Declaration is available to the public"""

    eir_location_line_1: str = Field(
        ...,
        description=(
            "First line of the location where the final EIR/Negative Declaration and record "
            "of project approval are available to the public. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    eir_location_line_2: str = Field(
        default="",
        description=(
            "Second line for continuing the location information, if needed. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SignatureandFiling(BaseModel):
    """Signature block and filing dates"""

    title_of_signer: str = Field(
        ...,
        description=(
            "Official title or position of the person signing on behalf of the public "
            'agency. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_signature: str = Field(
        ..., description="Date the Notice of Determination was signed."
    )  # YYYY-MM-DD format

    date_received_for_filing_at_opr: str = Field(
        default="",
        description=(
            "Date the Notice of Determination was received for filing at the Office of "
            "Planning and Research."
        ),
    )  # YYYY-MM-DD format


class NoticeOfDetermination(BaseModel):
    """
    Notice of Determination

    SUBJECT: Filing of Notice of Determination in compliance with Section 21108 or 21152 of the Public Resources Code.
    """

    recipient_information: RecipientInformation = Field(..., description="Recipient Information")
    from__agency_information: FromAgencyInformation = Field(
        ..., description="From / Agency Information"
    )
    project_identification: ProjectIdentification = Field(..., description="Project Identification")
    project_determination: ProjectDetermination = Field(..., description="Project Determination")
    document_availability: DocumentAvailability = Field(..., description="Document Availability")
    signature_and_filing: SignatureandFiling = Field(..., description="Signature and Filing")

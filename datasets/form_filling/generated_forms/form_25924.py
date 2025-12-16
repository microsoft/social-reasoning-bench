from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestedAmendmentstoCarersRegister(BaseModel):
    """Current information on the Carers Register and the requested amendments"""

    first_given_name_current_information: str = Field(
        ...,
        description=(
            "First given name currently recorded on the Carers Register .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    first_given_name_requested_amendment: str = Field(
        ...,
        description=(
            "New first given name you are requesting to be recorded on the Carers Register "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    other_given_names_current_information: str = Field(
        default="",
        description=(
            "Any other given names currently recorded on the Carers Register .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_given_names_requested_amendment: str = Field(
        default="",
        description=(
            "New or amended other given names you are requesting to be recorded .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    family_name_current_information: str = Field(
        ...,
        description=(
            "Family name currently recorded on the Carers Register .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    family_name_requested_amendment: str = Field(
        ...,
        description=(
            "New family name you are requesting to be recorded on the Carers Register .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    gender_current_information: str = Field(
        default="",
        description=(
            "Gender currently recorded on the Carers Register .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    gender_requested_amendment: str = Field(
        default="",
        description=(
            "New gender information you are requesting to be recorded .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth_current_information: str = Field(
        ..., description="Date of birth currently recorded on the Carers Register"
    )  # YYYY-MM-DD format

    date_of_birth_requested_amendment: str = Field(
        ..., description="Correct date of birth you are requesting to be recorded"
    )  # YYYY-MM-DD format

    identifies_as_aboriginal_and_or_torres_strait_islander_current_information: str = Field(
        default="",
        description=(
            "Current record of whether you identify as Aboriginal and/or Torres Strait "
            'Islander .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    identifies_as_aboriginal_and_or_torres_strait_islander_requested_amendment: str = Field(
        default="",
        description=(
            "Updated information on whether you identify as Aboriginal and/or Torres Strait "
            'Islander .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    home_address_current_information: str = Field(
        ...,
        description=(
            "Home address currently recorded on the Carers Register .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_address_requested_amendment: str = Field(
        ...,
        description=(
            "New home address you are requesting to be recorded .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_information_current_information: str = Field(
        default="",
        description=(
            "Any other relevant information currently recorded on the Carers Register .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_information_requested_amendment: str = Field(
        default="",
        description=(
            "Any other new or corrected information you are requesting to be recorded .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantDeclarationandContactDetails(BaseModel):
    """Applicant’s certification, contact details and mailing information"""

    date_of_request: str = Field(
        ..., description="Date this amendment request is made"
    )  # YYYY-MM-DD format

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the information is true and correct .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    full_name_of_applicant: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contact_number: str = Field(
        ...,
        description=(
            "Best contact phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address for contacting the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    postal_address: str = Field(
        default="",
        description=(
            "Postal mailing address for correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """For internal processing and outcome recording"""

    applicant_eligible: BooleanLike = Field(
        default="", description="Indicates whether the applicant is eligible (office use only)"
    )

    amendment_made: BooleanLike = Field(
        default="",
        description="Indicates whether the requested amendment has been made (office use only)",
    )

    amendment_made_date: str = Field(
        default="", description="Date on which the amendment was made (office use only)"
    )  # YYYY-MM-DD format

    amendment_sought_supported_by_documentation: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the amendment request is supported by documentation (office "
            "use only)"
        ),
    )

    applicant_notified_of_outcome: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the applicant has been notified of the outcome (office use only)"
        ),
    )

    applicant_notified_of_outcome_date: str = Field(
        default="", description="Date the applicant was notified of the outcome (office use only)"
    )  # YYYY-MM-DD format

    relevant_designated_agency_notified_of_outcome: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the relevant designated agency has been notified of the "
            "outcome (office use only)"
        ),
    )

    relevant_designated_agency_notified_of_outcome_date: str = Field(
        default="",
        description=(
            "Date the relevant designated agency was notified of the outcome (office use only)"
        ),
    )  # YYYY-MM-DD format


class CarersRegisterAmendmentRequestForm(BaseModel):
    """
    Carers Register amendment request form

    Please identify the current information in the Carers Register that you request be amended and the new information that you request to be inserted on the Carers Register
    """

    requested_amendments_to_carers_register: RequestedAmendmentstoCarersRegister = Field(
        ..., description="Requested Amendments to Carers Register"
    )
    applicant_declaration_and_contact_details: ApplicantDeclarationandContactDetails = Field(
        ..., description="Applicant Declaration and Contact Details"
    )
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")

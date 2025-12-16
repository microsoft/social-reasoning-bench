from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Applicantdetails(BaseModel):
    """Details of the person completing this form"""

    carer_authorisation_number: str = Field(
        ...,
        description=(
            "Carer authorisation number as issued by the relevant authority .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    first_given_name: str = Field(
        ...,
        description=(
            'Applicant\'s first given name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_given_names: str = Field(
        default="",
        description=(
            "Any additional given names (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    family_name: str = Field(
        ...,
        description=(
            'Applicant\'s family name (surname) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    gender: str = Field(
        default="",
        description=(
            'Applicant\'s gender .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    identifies_as_aboriginal_and_or_torres_strait_islander: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the applicant identifies as Aboriginal and/or Torres Strait Islander"
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Applicant\'s residential address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_number: str = Field(
        ...,
        description=(
            "Primary contact phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Previousrequesttodesignatedagency(BaseModel):
    """Whether a request has already been made to a designated agency"""

    have_you_made_a_request_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if the applicant has made a request to a designated agency to amend "
            "information on the Carers Register"
        ),
    )

    have_you_made_a_request_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the applicant has not made a request to a designated agency to amend "
            "information on the Carers Register"
        ),
    )


class Designatedagencydetails(BaseModel):
    """Details of the designated agency and the amendment requested"""

    name_of_designated_agency: str = Field(
        ...,
        description=(
            "Name of the designated agency to which the request was made .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    name_of_contact_person_at_designated_agency_if_known: str = Field(
        default="",
        description=(
            "Name of the contact person at the designated agency, if known .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_of_designated_agency: str = Field(
        ...,
        description=(
            "Postal or street address of the designated agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_number_of_designated_agency: str = Field(
        ...,
        description=(
            "Primary contact phone number for the designated agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_of_designated_agency: str = Field(
        default="",
        description=(
            "Email address for the designated agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_request: str = Field(
        ..., description="Date the request was made to the designated agency"
    )  # YYYY-MM-DD format

    information_you_sought_to_be_changed: str = Field(
        ...,
        description=(
            "Describe the information on the Carers Register that you requested to be "
            'changed .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Outcomeofrequest(BaseModel):
    """Outcome of the designated agency’s decision"""

    designated_agency_made_the_change_requested: BooleanLike = Field(
        ..., description="Indicate if the designated agency made the requested change"
    )

    designated_agency_did_not_make_the_change_requested: BooleanLike = Field(
        ..., description="Indicate if the designated agency did not make the requested change"
    )

    details_of_why_the_designated_agency_did_not_make_the_change_requested: str = Field(
        default="",
        description=(
            "Provide any details explaining why the designated agency did not make the "
            'requested change .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class ApplicationToRequestToAmendInformationOnTheCarersRegister(BaseModel):
    """
    Application to request to amend information on the Carers Register

    Application to request to amend information on the Carers Register
    """

    applicant_details: Applicantdetails = Field(..., description="Applicant details")
    previous_request_to_designated_agency: Previousrequesttodesignatedagency = Field(
        ..., description="Previous request to designated agency"
    )
    designated_agency_details: Designatedagencydetails = Field(
        ..., description="Designated agency details"
    )
    outcome_of_request: Outcomeofrequest = Field(..., description="Outcome of request")

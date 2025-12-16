from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantInformation(BaseModel):
    """Your contact information as the person submitting the complaint"""

    date: str = Field(..., description="Date this complaint form is completed")  # YYYY-MM-DD format

    your_name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    your_address: str = Field(
        ...,
        description=(
            'Your street address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    your_city_state_zip_code: str = Field(
        ...,
        description=(
            'Your city, state, and ZIP code .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    your_telephone_home: str = Field(
        default="",
        description=(
            'Your home telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    your_telephone_work: str = Field(
        default="",
        description=(
            'Your work telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    your_telephone_cell: str = Field(
        default="",
        description=(
            'Your cell or mobile telephone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_your_contact_information: str = Field(
        default="",
        description=(
            'Your email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class NonAttorneyComplainedAgainst(BaseModel):
    """Identification and contact information for the non-attorney"""

    name_non_attorney_complained_against: str = Field(
        ...,
        description=(
            "Full name of the non-attorney you are complaining about .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            "Business name of the non-attorney, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_non_attorney_complained_against: str = Field(
        default="",
        description=(
            "Street address of the non-attorney or their business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip_code_non_attorney_complained_against: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the non-attorney or their business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_numbers_non_attorney_complained_against: str = Field(
        default="",
        description=(
            "Telephone number or numbers for the non-attorney or their business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email_address_non_attorney_complained_against: str = Field(
        default="",
        description=(
            "Email address of the non-attorney or their business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NatureofLegalServicesandRepresentation(BaseModel):
    """Questions about the non-attorney’s legal services and representations"""

    employ_non_attorney_legal_services_yes: BooleanLike = Field(
        default="", description="Check if you employed the non-attorney to provide legal services"
    )

    employ_non_attorney_legal_services_no: BooleanLike = Field(
        default="",
        description="Check if you did not employ the non-attorney to provide legal services",
    )

    non_attorney_provide_legal_services_yes: BooleanLike = Field(
        default="", description="Check if the non-attorney provided legal services"
    )

    non_attorney_provide_legal_services_no: BooleanLike = Field(
        default="", description="Check if the non-attorney did not provide legal services"
    )

    non_attorney_represent_as_attorney_yes: BooleanLike = Field(
        default="", description="Check if the non-attorney claimed or appeared to be an attorney"
    )

    non_attorney_represent_as_attorney_no: BooleanLike = Field(
        default="",
        description="Check if the non-attorney did not claim or appear to be an attorney",
    )


class pythonCaliforniaNonAttorneyUPLComplaintForm(BaseModel):
    """
        THE STATE BAR OF CALIFORNIA
    NON-ATTORNEY UNLICENSED PRACTICE OF LAW
    COMPLAINT FORM

        (To report the unauthorized practice of law by a non-attorney)
    """

    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    non_attorney_complained_against: NonAttorneyComplainedAgainst = Field(
        ..., description="Non-Attorney Complained Against"
    )
    nature_of_legal_services_and_representation: NatureofLegalServicesandRepresentation = Field(
        ..., description="Nature of Legal Services and Representation"
    )

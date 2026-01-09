from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ForOfficialUseOnly(BaseModel):
    """Office processing and payment details"""

    pc_case_number: str = Field(
        default="",
        description=(
            "Planning Commission case number assigned by the office .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hearing_date: str = Field(
        default="", description="Date of the scheduled hearing"
    )  # YYYY-MM-DD format

    amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of fees paid in dollars"
    )

    date_paid: str = Field(
        default="", description="Date on which the payment was made"
    )  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """Contact information for the applicant"""

    contact_name: str = Field(
        ...,
        description=(
            "Primary contact person's full name for the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    firm_company_applicant: str = Field(
        default="",
        description=(
            'Applicant\'s firm or company name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_applicant: str = Field(
        ...,
        description=(
            'Mailing address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_applicant: str = Field(
        ...,
        description=(
            'Applicant\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_applicant: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class OwnerInformation(BaseModel):
    """Contact information for the property owner"""

    name_owner: str = Field(
        ...,
        description=(
            'Property owner\'s full name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    firm_company_owner: str = Field(
        default="",
        description=(
            "Owner's firm or company name, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_owner: str = Field(
        ...,
        description=(
            'Mailing address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_owner: str = Field(
        ...,
        description=(
            'Property owner\'s primary phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_owner: str = Field(
        ...,
        description=(
            'Property owner\'s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Details about the project and site"""

    project_location_street_address: str = Field(
        ...,
        description=(
            "Street address where the fence modification project is located .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    project_name: str = Field(
        ...,
        description=(
            'Name or title of the project .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_zoning: str = Field(
        ...,
        description=(
            "Existing zoning designation of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_use: str = Field(
        ...,
        description=(
            "Current use of the property (e.g., residential, commercial) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class CriteriaforFenceModification(BaseModel):
    """Applicant responses to required criteria"""

    response_to_criterion_a: str = Field(
        ...,
        description=(
            "Explanation of how the modification will not be contrary to the purpose and "
            'intent of the Code .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    response_to_criterion_b: str = Field(
        ...,
        description=(
            "Explanation of how the modification is consistent with the Comprehensive Plan "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class FenceModification(BaseModel):
    """
    FENCE MODIFICATION

    Please legibly print or type the following application in its entirety. Incomplete applications will not be accepted. Submit the twelve (12) copies of this application, and any supporting information, along with appropriate fees, by 3:00 pm of the application deadline date.
    """

    for_official_use_only: ForOfficialUseOnly = Field(..., description="For Official Use Only")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    owner_information: OwnerInformation = Field(..., description="Owner Information")
    project_information: ProjectInformation = Field(..., description="Project Information")
    criteria_for_fence_modification: CriteriaforFenceModification = Field(
        ..., description="Criteria for Fence Modification"
    )

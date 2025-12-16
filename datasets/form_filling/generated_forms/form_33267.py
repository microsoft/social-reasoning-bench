from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OfficeUseOnly(BaseModel):
    """For internal processing and review status"""

    application_number: str = Field(
        default="",
        description=(
            "Internal application number assigned by the office .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fees_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of fees paid"
    )

    date_received: str = Field(
        default="", description="Date the application was received by the office"
    )  # YYYY-MM-DD format

    accepted_by: str = Field(
        default="",
        description=(
            "Name or initials of staff member who accepted the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_complete: str = Field(
        default="", description="Date the application was deemed complete"
    )  # YYYY-MM-DD format

    app: BooleanLike = Field(default="", description="Indicates if the application was approved")

    deny: BooleanLike = Field(default="", description="Indicates if the application was denied")

    conditions: str = Field(
        default="",
        description=(
            "Any conditions attached to the approval or denial .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantOwnerInformation(BaseModel):
    """Contact information for the applicant and property owner"""

    applicant_name: str = Field(
        ...,
        description=(
            'Full legal name of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_title: str = Field(
        ...,
        description=(
            "Applicant’s title or role (e.g., owner, agent, architect) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Mailing address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_name: str = Field(
        ...,
        description=(
            'Full legal name of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_title: str = Field(
        ...,
        description=(
            'Property owner’s title or role .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_address: str = Field(
        ...,
        description=(
            'Mailing address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_email: str = Field(
        ...,
        description=(
            'Email address for the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Location and zoning details for the subject property"""

    street_address: str = Field(
        ...,
        description=(
            "Street address of the property for which the certificate is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tax_map_numbers: str = Field(
        ...,
        description=(
            "Tax map number or numbers associated with the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_district: str = Field(
        ...,
        description=(
            "Name or code of the applicable special district .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DescriptionofRequest(BaseModel):
    """Narrative description and justification for the request"""

    description_of_request: str = Field(
        ...,
        description=(
            "Detailed description of the project scope, justification, and any responses to "
            'guidelines or special conditions .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class GreenvilleCertOfAppropriatenessUrbanDesignPanel(BaseModel):
    """
        city of greenville

    APPLICATION FOR CERTIFICATE OF APPROPRIATENESS
    URBAN DESIGN PANEL

        ''
    """

    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
    applicantowner_information: ApplicantOwnerInformation = Field(
        ..., description="Applicant/Owner Information"
    )
    property_information: PropertyInformation = Field(..., description="Property Information")
    description_of_request: DescriptionofRequest = Field(..., description="Description of Request")

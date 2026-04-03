from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantDetails(BaseModel):
    """Details of the person applying and the property"""

    name: str = Field(
        ...,
        description=(
            'Full name of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    council_tax_reference: str = Field(
        ...,
        description=(
            "Council Tax account reference number for the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_address: str = Field(
        ...,
        description=(
            "Full address of the property for which exemption is being claimed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AboutthePeopleinYourHome(BaseModel):
    """Exemption start date and details of all residents under 18"""

    exemption_start_date: str = Field(
        ..., description="Date from which you consider the Council Tax exemption should apply"
    )  # YYYY-MM-DD format

    resident_name: str = Field(
        ...,
        description=(
            "Name of each person residing in the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Date of birth of each person residing in the property"
    )  # YYYY-MM-DD format

    type_of_evidence_birth_certificate_1: BooleanLike = Field(
        default="",
        description="Tick if a birth certificate is provided as evidence of age for this person",
    )

    type_of_evidence_passport_1: BooleanLike = Field(
        default="", description="Tick if a passport is provided as evidence of age for this person"
    )

    type_of_evidence_other_please_specify_1: str = Field(
        default="",
        description=(
            "Describe any other document provided as evidence of age for this person .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_evidence_birth_certificate_2: BooleanLike = Field(
        default="",
        description="Tick if a birth certificate is provided as evidence of age for this person",
    )

    type_of_evidence_passport_2: BooleanLike = Field(
        default="", description="Tick if a passport is provided as evidence of age for this person"
    )

    type_of_evidence_other_please_specify_2: str = Field(
        default="",
        description=(
            "Describe any other document provided as evidence of age for this person .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_evidence_birth_certificate_3: BooleanLike = Field(
        default="",
        description="Tick if a birth certificate is provided as evidence of age for this person",
    )

    type_of_evidence_passport_3: BooleanLike = Field(
        default="", description="Tick if a passport is provided as evidence of age for this person"
    )

    type_of_evidence_other_please_specify_3: str = Field(
        default="",
        description=(
            "Describe any other document provided as evidence of age for this person .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_evidence_birth_certificate_4: BooleanLike = Field(
        default="",
        description="Tick if a birth certificate is provided as evidence of age for this person",
    )

    type_of_evidence_passport_4: BooleanLike = Field(
        default="", description="Tick if a passport is provided as evidence of age for this person"
    )

    type_of_evidence_other_please_specify_4: str = Field(
        default="",
        description=(
            "Describe any other document provided as evidence of age for this person .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdultsWhoHaveMovedOut(BaseModel):
    """Details of adults (18 or over) who have left the property in the last 12 months"""

    adult_name: str = Field(
        default="",
        description=(
            "Name of any adult (aged 18 or over) who has moved out in the last 12 months "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    forwarding_address: str = Field(
        default="",
        description=(
            "Forwarding address of the adult who has moved out .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_moved_out: str = Field(
        default="", description="Date on which the adult moved out of the property"
    )  # YYYY-MM-DD format


class CouncilTaxPropertyExemptionAllOccupantsUnder18(BaseModel):
    """
        Revenues & Benefits Services

    Council Tax
    Application for Property Exemption –
    All Occupants Under 18

        A dwelling which is solely occupied by one or more persons under the age of 18 is exempt from liability for Council Tax (including Water and Waste Water charges). In order to claim an exemption, please complete this form, sign the Declaration on page 2 and email or post it to the address at the bottom of the page along with the appropriate supporting documentation.
    """

    applicant_details: ApplicantDetails = Field(..., description="Applicant Details")
    about_the_people_in_your_home: AboutthePeopleinYourHome = Field(
        ..., description="About the People in Your Home"
    )
    adults_who_have_moved_out: AdultsWhoHaveMovedOut = Field(
        ..., description="Adults Who Have Moved Out"
    )

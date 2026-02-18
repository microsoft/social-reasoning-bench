from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Tenancydetails(BaseModel):
    """Details about the tenancy being applied for"""

    property_address: str = Field(
        ...,
        description=(
            "Street address of the rental property you are applying for .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    commencement_of_tenancy: str = Field(
        ...,
        description=(
            "Intended start date or description of when the tenancy will begin .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Calendar date the tenancy is intended to commence"
    )  # YYYY-MM-DD format


class Applicantdetails(BaseModel):
    """Personal and contact details of the applicant"""

    full_name: str = Field(
        ...,
        description=(
            'Applicant’s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant’s date of birth")  # YYYY-MM-DD format

    phone_number: str = Field(
        ...,
        description=(
            'Applicant’s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mobile_phone: str = Field(
        default="",
        description=(
            'Applicant’s mobile phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Applicant’s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_address: str = Field(
        ...,
        description=(
            "Applicant’s current residential address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_long_have_you_lived_there_years: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of full years you have lived at your current address"
    )

    how_long_have_you_lived_there_months: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Additional number of months you have lived at your current address"
    )

    please_state_why_you_are_leaving_this_address: str = Field(
        ...,
        description=(
            "Reason you are moving from your current address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Identification(BaseModel):
    """Applicant identification details"""

    drivers_licence_number: str = Field(
        default="",
        description=(
            "Number from your driver’s licence (optional, used for identity and credit "
            'check) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    version_no_if_applicable: str = Field(
        default="",
        description=(
            "Driver’s licence version number, if your licence includes one .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    alternative_form_of_id: str = Field(
        default="",
        description=(
            "Details of another form of photo identification (e.g. passport, 18+ card) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Currentlandlordsdetails(BaseModel):
    """Contact and reference permission for current landlord"""

    landlords_name: str = Field(
        default="",
        description=(
            'Name of your current landlord .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_number_current_landlord: str = Field(
        default="",
        description=(
            "Current landlord’s primary phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mobile_phone_current_landlord: str = Field(
        default="",
        description=(
            "Current landlord’s mobile phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_current_landlord: str = Field(
        default="",
        description=(
            'Current landlord’s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    yes_may_i_contact_this_person_for_a_reference: BooleanLike = Field(
        default="",
        description="Select if you give permission to contact your current landlord for a reference",
    )

    no_may_i_contact_this_person_for_a_reference: BooleanLike = Field(
        default="",
        description=(
            "Select if you do not give permission to contact your current landlord for a reference"
        ),
    )


class PretenancyApplicationForm(BaseModel):
    """
    Pre-tenancy application form

    Please complete this form to apply for the tenancy at the address below. The information you provide is for applying for this tenancy and may be used for a credit and reference check. Your privacy is protected under the Privacy Act 2020.
    """

    tenancy_details: Tenancydetails = Field(..., description="Tenancy details")
    applicant_details: Applicantdetails = Field(..., description="Applicant details")
    identification: Identification = Field(..., description="Identification")
    current_landlords_details: Currentlandlordsdetails = Field(
        ..., description="Current landlord’s details"
    )

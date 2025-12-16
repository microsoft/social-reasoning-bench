from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Step1Aboutyou(BaseModel):
    """Your policy details and personal contact information"""

    certificate_of_insurance_policy_number: str = Field(
        ...,
        description=(
            "Your travel insurance Certificate of Insurance or policy number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    did_you_contact_the_emergency_assistance_team_no: BooleanLike = Field(
        default="", description="Select if you did not contact the emergency assistance team"
    )

    did_you_contact_the_emergency_assistance_team_yes: BooleanLike = Field(
        default="", description="Select if you contacted the emergency assistance team"
    )

    assistance_reference_number: str = Field(
        default="",
        description=(
            "Reference number provided by the emergency assistance team .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            'Your title (e.g. Mr, Mrs, Ms, Dr) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Your given name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Your family name or surname .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Your date of birth in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    occupation_eg_manager_full_time_student: str = Field(
        ...,
        description=(
            "Your current occupation or main activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_contact_number_including_area_and_country_code: str = Field(
        ...,
        description=(
            "Best phone number to contact you, including area and country code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Your email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Your full residential mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        ...,
        description=(
            'County for your address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    eircode: str = Field(..., description="Eircode or postal code for your address")

    country: str = Field(
        ...,
        description=(
            'Country for your address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    preferred_method_of_contact_email: BooleanLike = Field(
        default="", description="Tick if you prefer to be contacted by email"
    )

    preferred_method_of_contact_phone: BooleanLike = Field(
        default="", description="Tick if you prefer to be contacted by phone"
    )

    preferred_method_of_contact_mail: BooleanLike = Field(
        default="", description="Tick if you prefer to be contacted by postal mail"
    )


class NominatedAuthority(BaseModel):
    """Details of the person authorised to act on your behalf for this claim"""

    name_of_nominated_authority: str = Field(
        default="",
        description=(
            "Full name of the person authorised to act on your behalf .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_authority_email: str = Field(
        default="",
        description=(
            "Email address of the nominated authority .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_authority_preferred_contact_number: str = Field(
        default="",
        description=(
            "Preferred contact number for the nominated authority .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_authority_date_of_birth: str = Field(
        default="", description="Date of birth of the nominated authority in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    nominated_authority_address: str = Field(
        default="",
        description=(
            "Full address of the nominated authority .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_authority_county: str = Field(
        default="",
        description=(
            "County for the nominated authority's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_authority_eircode: str = Field(
        default="", description="Eircode or postal code for the nominated authority's address"
    )

    nominated_authority_country: str = Field(
        default="",
        description=(
            "Country for the nominated authority's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NibTravelMakingAClaimOnYourPolicy(BaseModel):
    """
        nib travel

    Making a claim on your policy

        Before you start
        Your claim will be managed by nib Travel Services Europe Limited trading as nib Travel Services (we, us) who are authorised by the insurer to handle and settle claims. nib Travel Services Europe Limited trading as nib Travel Services is regulated by the Central Bank of Ireland. In order for us to process your claim quickly it's important that you complete all the relevant sections of this form with as much detail as you can. If you do not have enough room please attach additional information on a separate sheet.
        If you are giving authority to another person to act on your behalf in respect to this claim please complete the Nominated Authority box below.
        You'll find it easier to get all your supporting documents together first. You can find a full list of key documents we will need on page 11. Use these documents to complete all relevant sections of the form.
    """

    step_1_about_you: Step1Aboutyou = Field(..., description="Step 1: About you")
    nominated_authority: NominatedAuthority = Field(..., description="Nominated Authority")

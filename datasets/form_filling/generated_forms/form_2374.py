from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CriminalRecord(BaseModel):
    """Information about any existing criminal record"""

    do_you_have_a_criminal_record: BooleanLike = Field(
        ..., description="Indicate whether you have a criminal record"
    )


class LPADetails(BaseModel):
    """Information about existing Lasting or Enduring Power of Attorney arrangements"""

    do_you_have_an_lpa_or_epa_in_place: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have a Lasting Power of Attorney (LPA) or Enduring Power "
            "of Attorney (EPA) in place"
        ),
    )


class AppointedAttorneyDetails(BaseModel):
    """Contact and relationship details for the appointed attorney"""

    preferred_title: str = Field(
        default="",
        description=(
            "Your preferred title (e.g. Mr, Mrs, Ms, Dr) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    if_other_please_specify: str = Field(
        default="",
        description=(
            "If your preferred title is not listed, specify it here .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    full_name: str = Field(
        ...,
        description=(
            'Appointed attorney\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    relationship: str = Field(
        ...,
        description=(
            "Relationship of the appointed attorney to you .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_line_1: str = Field(
        ...,
        description=(
            "First line of the appointed attorney's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_line_2: str = Field(
        default="",
        description=(
            "Second line of the appointed attorney's address (if needed) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_line_3: str = Field(
        default="",
        description=(
            "Third line of the appointed attorney's address (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postcode for the appointed attorney's address")

    telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for the appointed attorney .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address for the appointed attorney .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ImmigrationRighttoReside(BaseModel):
    """Confirmation of entitlement to reside in the country and ability to provide documentation"""

    confirmation_of_entitlement_to_reside_line_1: str = Field(
        ...,
        description=(
            "First line of your confirmation that you are entitled to reside in this "
            'country and can provide documentation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    confirmation_of_entitlement_to_reside_line_2: str = Field(
        default="",
        description=(
            "Second line of your confirmation that you are entitled to reside in this "
            'country and can provide documentation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    confirmation_of_entitlement_to_reside_line_3: str = Field(
        default="",
        description=(
            "Third line of your confirmation that you are entitled to reside in this "
            'country and can provide documentation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MordenCollegeInterestingPeopleLivingLifeToTheFull(BaseModel):
    """
        MORDEN COLLEGE
    Interesting People Living Life to the Full

        Lasting Power of Attorney - At Morden College is it our policy that residents should have in place a Lasting Power of Attorney for Health & Welfare and Property & Financial Affairs prior to taking up residence. Under the Immigration Act 2014, we are obliged to check the immigration status of all prospective residents. Please confirm that you are entitled to reside in this country and can provide appropriate documentation, if necessary.
    """

    criminal_record: CriminalRecord = Field(..., description="Criminal Record")
    lpa_details: LPADetails = Field(..., description="LPA Details")
    appointed_attorney_details: AppointedAttorneyDetails = Field(
        ..., description="Appointed Attorney Details"
    )
    immigration__right_to_reside: ImmigrationRighttoReside = Field(
        ..., description="Immigration / Right to Reside"
    )

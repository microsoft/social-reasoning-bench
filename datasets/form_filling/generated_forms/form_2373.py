from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CurrentAccommodation(BaseModel):
    """Details of the applicant's current accommodation status"""

    a_homeowner: BooleanLike = Field(
        default="", description="Tick if you are currently living in accommodation you own."
    )

    a_private_tenant: BooleanLike = Field(
        default="", description="Tick if you are currently renting from a private landlord."
    )

    in_a_residential_housing_scheme_almshouse_or_similar: BooleanLike = Field(
        default="",
        description=(
            "Tick if you currently live in a residential housing scheme, almshouse, or "
            "similar supported accommodation."
        ),
    )

    other_if_yes_please_explain_below: str = Field(
        default="",
        description=(
            "Describe your current accommodation if it does not fit the listed options. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WillInformation(BaseModel):
    """Information about whether the applicant has a will and where it is held"""

    do_you_have_a_will_in_place: BooleanLike = Field(
        default="", description="Indicate whether you currently have a valid will."
    )

    is_your_will_lodged_with_a_solicitor: BooleanLike = Field(
        default="", description="Indicate whether your will is held by a solicitor."
    )


class SolicitorDetails(BaseModel):
    """Contact details for the solicitor holding the will"""

    solicitor_details_preferred_title: str = Field(
        default="",
        description=(
            "Preferred title of your solicitor (e.g. Mr, Ms, Dr). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_if_other_please_specify: str = Field(
        default="",
        description=(
            "If the solicitor’s title is not standard, specify it here. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_full_name: str = Field(
        default="",
        description=(
            "Full name of your solicitor or firm contact. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_address_line_1: str = Field(
        default="",
        description=(
            "First line of the solicitor’s address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the solicitor’s address (if needed). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_postcode: str = Field(
        default="", description="Postcode for the solicitor’s address."
    )

    solicitor_details_telephone_number: str = Field(
        default="",
        description=(
            'Telephone number for your solicitor. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    solicitor_details_email_address: str = Field(
        default="",
        description=(
            'Email address for your solicitor. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class WillHolderDetails(BaseModel):
    """Contact details for the person or organisation holding the will (if not a solicitor)"""

    my_will_is_held_by_preferred_title: str = Field(
        default="",
        description=(
            "Preferred title of the person or organisation holding your will. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    my_will_is_held_by_if_other_please_specify: str = Field(
        default="",
        description=(
            "If the holder’s title is not standard, specify it here. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_will_is_held_by_full_name: str = Field(
        default="",
        description=(
            "Full name of the person or organisation holding your will. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_will_is_held_by_address_line_1: str = Field(
        default="",
        description=(
            "First line of the address of the person or organisation holding your will. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    my_will_is_held_by_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the address of the person or organisation holding your will (if "
            'needed). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    my_will_is_held_by_postcode: str = Field(
        default="",
        description="Postcode for the address of the person or organisation holding your will.",
    )

    my_will_is_held_by_telephone_number: str = Field(
        default="",
        description=(
            "Telephone number for the person or organisation holding your will. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    my_will_is_held_by_email_address: str = Field(
        default="",
        description=(
            "Email address for the person or organisation holding your will. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class MordenCollegeInterestingPeopleLivingLifeToTheFull(BaseModel):
    """
        MORDEN COLLEGE
    Interesting People Living Life to the Full

        All Residents of Morden College are strongly advised to make a will
    """

    current_accommodation: CurrentAccommodation = Field(..., description="Current Accommodation")
    will_information: WillInformation = Field(..., description="Will Information")
    solicitor_details: SolicitorDetails = Field(..., description="Solicitor Details")
    will_holder_details: WillHolderDetails = Field(..., description="Will Holder Details")

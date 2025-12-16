from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantContactInformation(BaseModel):
    """Contact and communication preferences for the person filing the complaint"""

    first_name: str = Field(
        ...,
        description=(
            'Complainant\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle_initial: str = Field(
        default="",
        description=(
            'Complainant\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Complainant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Complainant\'s mailing street address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the complainant's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the complainant's mailing address")

    zip_code: str = Field(..., description="ZIP code for the complainant's mailing address")

    e_mail_address_if_you_have_one: str = Field(
        default="",
        description=(
            "Complainant's email address, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number_starting_with_area_code: str = Field(
        ...,
        description=(
            "Primary telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_telephone_number_starting_with_area_code: str = Field(
        default="",
        description=(
            "Alternate telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    best_time_of_the_day_to_reach_you: str = Field(
        default="",
        description=(
            'Preferred time of day to be contacted .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    best_way_to_reach_you_mail: BooleanLike = Field(
        default="", description="Check if mail is your preferred way to be contacted"
    )

    best_way_to_reach_you_phone: BooleanLike = Field(
        default="", description="Check if phone is your preferred way to be contacted"
    )

    best_way_to_reach_you_e_mail: BooleanLike = Field(
        default="", description="Check if email is your preferred way to be contacted"
    )

    best_way_to_reach_you_other: str = Field(
        default="",
        description=(
            "If 'Other' is selected, specify your preferred contact method .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class RepresentativeInformation(BaseModel):
    """Information about the complainant’s representative, if any"""

    have_representative_yes: BooleanLike = Field(
        default="", description="Check if you have a representative for this complaint"
    )

    have_representative_no: BooleanLike = Field(
        default="", description="Check if you do not have a representative for this complaint"
    )

    representative_first_name: str = Field(
        default="",
        description=(
            'Representative\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    representative_last_name: str = Field(
        default="",
        description=(
            'Representative\'s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    representative_address: str = Field(
        default="",
        description=(
            "Representative's mailing street address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    representative_city: str = Field(
        default="",
        description=(
            "City for the representative's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    representative_state: str = Field(
        default="", description="State for the representative's mailing address"
    )

    representative_zip_code: str = Field(
        default="", description="ZIP code for the representative's mailing address"
    )

    representative_telephone: str = Field(
        default="",
        description=(
            "Representative's telephone number including area code .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_e_mail: str = Field(
        default="",
        description=(
            'Representative\'s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AllegedDiscriminationDetails(BaseModel):
    """Information about the individuals involved and the program concerned"""

    names_of_persons_involved_line_1: str = Field(
        default="",
        description=(
            "First line to list names of person(s) involved in the alleged discrimination "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    names_of_persons_involved_line_2: str = Field(
        default="",
        description=(
            "Second line to list names of person(s) involved in the alleged discrimination "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    program_you_applied_for_if_known_if_applicable: str = Field(
        default="",
        description=(
            "Name of the USDA program you applied for, if known or applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class USDAAssistantSecretaryCivilRightsComplaintForm(BaseModel):
    """
        UNITED STATES DEPARTMENT OF AGRICULTURE (USDA)
    Office of the Assistant Secretary for Civil Rights
    Program Discrimination Complaint Form

        Program Discrimination Complaint Form
    """

    complainant_contact_information: ComplainantContactInformation = Field(
        ..., description="Complainant Contact Information"
    )
    representative_information: RepresentativeInformation = Field(
        ..., description="Representative Information"
    )
    alleged_discrimination_details: AllegedDiscriminationDetails = Field(
        ..., description="Alleged Discrimination Details"
    )

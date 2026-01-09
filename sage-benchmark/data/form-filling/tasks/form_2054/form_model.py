from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationBackground(BaseModel):
    """How the applicant learned about the housing and their reasons for applying"""

    how_did_you_hear_about_this_housing_opportunity: str = Field(
        default="",
        description=(
            "Explain how you learned about this housing opportunity (e.g., friend, agency, "
            'online, flyer). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    briefly_describe_your_reason_for_applying: str = Field(
        default="",
        description=(
            "Provide a short explanation of why you are applying for this housing. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ParentGuardianAlternateContactInformation(BaseModel):
    """Contact details for a parent, guardian, or alternate contact"""

    parent_guardian_alternate_contacts_full_name: str = Field(
        default="",
        description=(
            "Full name of your parent, guardian, or alternate contact person. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            "Home phone number for the contact person. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            "Cell phone number for the contact person. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        default="",
        description=(
            "Street address for the contact person. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip_code: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the contact person. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            'Email address for the contact person. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class LivingSituationandPreferences(BaseModel):
    """Current housing situation, independence, and apartment preference"""

    describe_your_current_living_situation_i_rent: BooleanLike = Field(
        default="", description="Check if you currently rent your home."
    )

    describe_your_current_living_situation_i_own: BooleanLike = Field(
        default="", description="Check if you currently own your home."
    )

    describe_your_current_living_situation_other: BooleanLike = Field(
        default="",
        description=(
            "Check if your current living situation is something other than renting or owning."
        ),
    )

    in_your_own_words_describe_your_level_of_independence: str = Field(
        default="",
        description=(
            "Describe how independently you live and manage daily activities. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    would_you_rather_live_in_a_one_bedroom_apartment_by_yourself: BooleanLike = Field(
        default="",
        description="Select if you would prefer to live alone in a one-bedroom apartment.",
    )

    would_you_rather_live_in_a_two_bedroom_apartment_with_a_roommate: BooleanLike = Field(
        default="",
        description="Select if you would prefer to live in a two-bedroom apartment with a roommate.",
    )


class RidgewoodSupportiveHousing(BaseModel):
    """
    Ridgewood Supportive Housing

    Ridgewood Supportive Housing includes both one- and two-bedroom apartments. We will take your preferences into consideration; however, apartment selection is based upon multiple factors including careful review of one’s application and a person-to-person interview. Roommate pairings are made according to common likes and dislikes as well as schedule.
    """

    application_background: ApplicationBackground = Field(..., description="Application Background")
    parentguardianalternate_contact_information: ParentGuardianAlternateContactInformation = Field(
        ..., description="Parent/Guardian/Alternate Contact Information"
    )
    living_situation_and_preferences: LivingSituationandPreferences = Field(
        ..., description="Living Situation and Preferences"
    )

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientInformation(BaseModel):
    """Basic identifying and contact information about the client"""

    name: str = Field(
        ...,
        description=(
            "Full legal name of the adult completing this intake form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Current age in years")

    address: str = Field(
        ...,
        description=(
            "Street address, including apartment or unit number if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State of residence (two-letter abbreviation if in the U.S.)"
    )

    zip: str = Field(..., description="Zip or postal code")

    home_phone: str = Field(
        default="",
        description=(
            'Primary home telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Mobile or cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address for contact and appointment communication .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PresentingProblem(BaseModel):
    """Information about current concerns and their history"""

    what_brings_you_to_my_office_briefly_describe_your_current_situation: str = Field(
        ...,
        description=(
            "Brief description of the main concerns or reasons for seeking therapy at this "
            'time .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    how_long_has_this_been_occurring_what_do_you_believe_caused_it_what_have_you_tried_to_change_it: str = Field(
        ...,
        description=(
            "Duration, perceived causes, and any steps you have already taken to address "
            'the problem .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class HouseholdandRelationships(BaseModel):
    """Household composition and relationship/marital history"""

    who_lives_in_your_home_with_you: str = Field(
        ...,
        description=(
            "Names and relationships of people currently living in your household .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    marital_status: str = Field(
        ...,
        description=(
            "Current marital or relationship status (e.g., single, married, partnered, "
            'divorced) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    spouse_partner_significant_others_first_name: str = Field(
        default="",
        description=(
            "First name of your spouse, partner, or significant other, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_would_you_describe_your_current_relationship: str = Field(
        default="",
        description=(
            "Brief description of the quality and nature of your current romantic "
            'relationship .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    how_many_times_have_you_been_divorced: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of prior divorces, if any"
    )

    widowed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of times you have been widowed, if any"
    )


class AdultIntakeQuestionnaireTrentHEvansPhd(BaseModel):
    """
        Adult Intake Questionnaire
    Trent H. Evans, Ph.D.

        All information is considered confidential and will not be released without your written consent
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    presenting_problem: PresentingProblem = Field(..., description="Presenting Problem")
    household_and_relationships: HouseholdandRelationships = Field(
        ..., description="Household and Relationships"
    )

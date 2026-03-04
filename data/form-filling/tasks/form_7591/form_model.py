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
            'Full legal name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Current age in years")

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
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

    state: str = Field(..., description="State of residence")

    zip: str = Field(..., description="Zip or postal code")

    home_phone: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Cell or mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class PresentingConcerns(BaseModel):
    """Information about the client’s current situation and concerns"""

    what_brings_you_to_my_office_briefly_describe_your_current_situation: str = Field(
        ...,
        description=(
            "Brief description of the main concerns or reasons for seeking services .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_long_has_this_been_occurring: str = Field(
        ...,
        description=(
            "Approximate duration of the problem or situation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_do_you_believe_caused_it: str = Field(
        ...,
        description=(
            "Your understanding of possible causes or triggers .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_have_you_tried_to_change_it: str = Field(
        ...,
        description=(
            "Steps you have already taken to address or change the situation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class HouseholdandRelationships(BaseModel):
    """Household composition and relationship history/status"""

    who_lives_in_your_home_with_you: str = Field(
        ...,
        description=(
            "Names and relationships of people currently living in your home .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    marital_status: str = Field(
        ...,
        description=(
            "Current marital status (e.g., single, married, partnered, divorced) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    spouse_partner_significant_others_first_name: str = Field(
        default="",
        description=(
            "First name of your spouse, partner, or significant other (if applicable) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_would_you_describe_your_current_relationship: str = Field(
        default="",
        description=(
            "Brief description of the quality and nature of your current relationship .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_many_times_have_you_been_divorced: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of times you have been legally divorced"
    )

    widowed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of times you have been widowed"
    )


class AdultIntakeQuestionnaire(BaseModel):
    """
    Adult Intake Questionnaire

    All information is considered confidential and will not be released without your written consent
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    presenting_concerns: PresentingConcerns = Field(..., description="Presenting Concerns")
    household_and_relationships: HouseholdandRelationships = Field(
        ..., description="Household and Relationships"
    )

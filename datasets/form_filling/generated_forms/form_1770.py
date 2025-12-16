from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    """Basic information about the VolunTeen participant"""

    name: str = Field(
        ...,
        description=(
            'Participant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

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

    zip_code: str = Field(..., description="Zip or postal code")

    telephone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    your_school: str = Field(
        ...,
        description=(
            'Name of the school you attend .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    your_grade_you_will_be_in_this_fall: str = Field(
        ...,
        description=(
            "Grade level you will enter in the upcoming fall .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    your_age: Union[float, Literal["N/A", ""]] = Field(..., description="Your age in years")

    your_shirt_size: str = Field(
        ...,
        description=(
            "T-shirt size (e.g., Youth M, Adult S, Adult M, etc.) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relative_of_a_kdhs_team_member_their_name: str = Field(
        default="",
        description=(
            "Name of the KDHS team member you are related to, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class HealthNutritionB1(BaseModel):
    """B-1 task completion details"""

    b_1_completed: BooleanLike = Field(
        default="",
        description="Indicate whether you completed B-1 (healthy food and social media post)",
    )

    b_1_date: str = Field(
        default="", description="Date you completed the B-1 activity"
    )  # YYYY-MM-DD format


class HealthNutritionI1(BaseModel):
    """Facts learned from the Portion Control video"""

    fact_1: str = Field(
        ...,
        description=(
            "First fact you learned from the Portion Control video .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fact_2: str = Field(
        ...,
        description=(
            "Second fact you learned from the Portion Control video .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fact_3: str = Field(
        ...,
        description=(
            "Third fact you learned from the Portion Control video .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HealthNutritionN1(BaseModel):
    """Trail research for local hiking options"""

    trail_1: str = Field(
        ...,
        description=(
            "Name, brief description, and miles for the first trail you researched .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    trail_2: str = Field(
        ...,
        description=(
            "Name, brief description, and miles for the second trail you researched .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    trail_3: str = Field(
        ...,
        description=(
            "Name, brief description, and miles for the third trail you researched .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    trail_4: str = Field(
        ...,
        description=(
            "Name, brief description, and miles for the fourth trail you researched .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class VolunteenBingo2021(BaseModel):
    """
    2021 VolunTeen BINGO!

    Use these sheets to fill in your answers to the corresponding BINGO boxes. If a written response is not required please indicate in the appropriate box the day and time you completed the task. For example, when/if you complete N-3, please list the date/time you liked and followed the King's Daughters Facebook or Instagram page(s) and indicate the social media platform on which you fulfilled this box so this can be verified.
    You may include additional pages if your answers to some of the questions require more space than what is provided. Please make sure you are indicating which box you are completing on any additional paperwork submitted.
    You will find detailed instructions, websites or other pertinent information for each BINGO box, as well as the KDMC VolunTeen BINGO playing card, in this document.
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    health__nutrition___b_1: HealthNutritionB1 = Field(..., description="Health & Nutrition - B-1")
    health__nutrition___i_1: HealthNutritionI1 = Field(..., description="Health & Nutrition - I-1")
    health__nutrition___n_1: HealthNutritionN1 = Field(..., description="Health & Nutrition - N-1")

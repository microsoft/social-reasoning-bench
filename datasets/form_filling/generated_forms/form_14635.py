from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AwardCategory(BaseModel):
    """Select the appropriate award category for the nomination"""

    service_and_advocacy: BooleanLike = Field(
        ...,
        description="Check if the nominee is being nominated in the Service and Advocacy category",
    )

    programs_for_children: BooleanLike = Field(
        ...,
        description="Check if the nominee is being nominated in the Programs for Children category",
    )

    mentoring_and_coaching: BooleanLike = Field(
        ...,
        description="Check if the nominee is being nominated in the Mentoring and Coaching category",
    )

    historical_and_cultural_preservation: BooleanLike = Field(
        ...,
        description=(
            "Check if the nominee is being nominated in the Historical and Cultural "
            "Preservation category"
        ),
    )

    innovation_for_change: BooleanLike = Field(
        ...,
        description="Check if the nominee is being nominated in the Innovation for Change category",
    )

    unity_of_the_church: BooleanLike = Field(
        ...,
        description="Check if the nominee is being nominated in the Unity of the Church category",
    )


class NomineeInformation(BaseModel):
    """Contact and identification details for the nominee"""

    name: str = Field(
        ...,
        description=(
            'Full name of the nominee .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the nominee .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number of the nominee .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Email address of the nominee .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            "Website or URL associated with the nominee (if any) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NominationExplanation(BaseModel):
    """Explanation of why the individual is being nominated"""

    explanation_of_why_you_are_nominating_this_individual_for_a_mlk_difference_maker_award_500_words_or_less: str = Field(
        ...,
        description=(
            "Explanation of why you are nominating this individual for a MLK Difference "
            'Maker Award, 500 words or less .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MlkCelebrationSacramentoDifferenceMakerAwardApplication(BaseModel):
    """MLK Celebration, Sacramento
    DIFFERENCE MAKER
    AWARD APPLICATION"""

    award_category: AwardCategory = Field(..., description="Award Category")
    nominee_information: NomineeInformation = Field(..., description="Nominee Information")
    nomination_explanation: NominationExplanation = Field(..., description="Nomination Explanation")

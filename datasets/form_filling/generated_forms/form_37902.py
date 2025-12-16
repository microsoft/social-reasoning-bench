from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Age(BaseModel):
    """Age group monitoring information"""

    age_0_19: BooleanLike = Field(
        ..., description="Select this option if your age is between 0 and 19 years"
    )

    age_20_34: BooleanLike = Field(
        ..., description="Select this option if your age is between 20 and 34 years"
    )

    age_35_49: BooleanLike = Field(
        ..., description="Select this option if your age is between 35 and 49 years"
    )

    age_50_64: BooleanLike = Field(
        ..., description="Select this option if your age is between 50 and 64 years"
    )

    age_65_74: BooleanLike = Field(
        ..., description="Select this option if your age is between 65 and 74 years"
    )

    age_75_plus: BooleanLike = Field(
        ..., description="Select this option if your age is 75 years or older"
    )

    age_prefer_not_to_say: BooleanLike = Field(
        ..., description="Select this option if you prefer not to disclose your age"
    )


class Nationality(BaseModel):
    """Nationality monitoring information"""

    nationality_please_specify: str = Field(
        ...,
        description=(
            'Your nationality, written in full .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class CurveLeicesterTheatreTrustEqualityAndDiversityMonitoring(BaseModel):
    """
        CURVE

    LEICESTER THEATRE TRUST

    EQUALITY AND DIVERSITY MONITORING

        Curve is an inclusive organisation and believes that everyone who works with, and for, our theatre should be valued and treated with dignity. We value equality and diversity and recognise that there is a difference between them. We understand equality as the protection of certain groups of staff from unfair treatment and diversity recognises and values the differences people have, such as appearance, social class or working patterns. We will take appropriate steps to ensure that all staff, board members, applicants, participants, creatives and actors are reviewed on the basis of ability.
        Monitoring
        Leicester Theatre Trust believes that it is important to promote equal opportunities for all. In order to assist us with monitoring, we would be grateful if you would provide details of your age, nationality, disability/impairment, ethnic origin, gender identity, sexual orientation, religion, belief, and socio-economic background.
        All information provided on this form will be treated in strictest confidence and only used for statistical monitoring. Accessibility is strictly limited in accordance with GDPR (General Data Protection Regulations, 2016), as laid out in our privacy notices and Data Protection Policy.
    """

    age: Age = Field(..., description="Age")
    nationality: Nationality = Field(..., description="Nationality")

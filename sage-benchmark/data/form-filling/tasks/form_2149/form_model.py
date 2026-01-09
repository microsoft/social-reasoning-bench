from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChildYouthInformation(BaseModel):
    """Basic identifying information for the child/youth"""

    child_youths_name: str = Field(
        ...,
        description=(
            "Full legal name of the child or youth being referred .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Child or youth's date of birth"
    )  # YYYY-MM-DD format

    gender: str = Field(
        default="",
        description=(
            'Gender identity of the child or youth .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_street: str = Field(
        ...,
        description=(
            'Street address of the child or youth .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address_postal_code: str = Field(
        ...,
        description=(
            'Postal code for the address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the child/youth or household .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PrimaryContactInformation(BaseModel):
    """Details for the primary contact person for scheduling service"""

    primary_contact_name: str = Field(
        ...,
        description=(
            "Name of the primary contact person for scheduling service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_relationship_to_child_youth: str = Field(
        ...,
        description=(
            "Relationship of the primary contact to the child or youth (e.g., parent, "
            'guardian) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    primary_contact_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_alternate_phone: str = Field(
        default="",
        description=(
            "Alternate phone number for the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_email_address: str = Field(
        default="",
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ReasonforReferral(BaseModel):
    """Current needs, symptoms, and behaviors prompting the referral"""

    reason_for_referral_current_needs_symptoms_behaviors: str = Field(
        ...,
        description=(
            "Describe the main reasons for referral, including current needs, symptoms, and "
            'behaviors .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class CurrentRiskFactors(BaseModel):
    """Information about current safety and risk concerns"""

    risk_of_harm_to_self_yes: BooleanLike = Field(
        default="",
        description="Indicate 'Yes' if there is a current risk of the youth harming themselves",
    )

    risk_of_harm_to_self_no: BooleanLike = Field(
        default="",
        description="Indicate 'No' if there is no current risk of the youth harming themselves",
    )

    risk_of_harm_to_others_yes: BooleanLike = Field(
        default="",
        description="Indicate 'Yes' if there is a current risk of the youth harming others",
    )

    risk_of_harm_to_others_no: BooleanLike = Field(
        default="",
        description="Indicate 'No' if there is no current risk of the youth harming others",
    )

    met_with_mental_health_professional_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate 'Yes' if the youth has previously met with a mental health professional"
        ),
    )

    met_with_mental_health_professional_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate 'No' if the youth has not previously met with a mental health professional"
        ),
    )

    safety_plan_completed_yes: BooleanLike = Field(
        default="",
        description="Indicate 'Yes' if a safety plan has already been completed for the youth",
    )

    safety_plan_completed_no: BooleanLike = Field(
        default="",
        description="Indicate 'No' if a safety plan has not been completed for the youth",
    )


class MentalHealthdevelopmentReferralForm(BaseModel):
    """
    MENTAL HEALTH /DEVELOPMENT REFERRAL FORM

    ''
    """

    childyouth_information: ChildYouthInformation = Field(
        ..., description="Child/Youth Information"
    )
    primary_contact_information: PrimaryContactInformation = Field(
        ..., description="Primary Contact Information"
    )
    reason_for_referral: ReasonforReferral = Field(..., description="Reason for Referral")
    current_risk_factors: CurrentRiskFactors = Field(..., description="Current Risk Factors")

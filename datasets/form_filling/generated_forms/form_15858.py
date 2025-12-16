from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RelationshipOpportunityRiskAssessment(BaseModel):
    """Confidential questionnaire about preferences, group size, client interactions, concerns, and current situation"""

    preference_for_technology_deployment_and_support: Literal[
        "To be self-sufficient in deploying technology and license tools that allow us to control and manage the entire process",
        "To partner with vendors who provide complete technology support",
        "N/A",
        "",
    ] = Field(
        ..., description="Select which approach to technology deployment and support you prefer."
    )

    satisfaction_with_average_group_size: BooleanLike = Field(
        ..., description="Indicate whether you are satisfied with your average group size."
    )

    reasons_for_being_unsuccessful_with_preferred_group_size_reason_1: str = Field(
        default="",
        description=(
            "First reason you have been unsuccessful in doing business with your preferred "
            'group size. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    reasons_for_being_unsuccessful_with_preferred_group_size_reason_2: str = Field(
        default="",
        description=(
            "Second reason you have been unsuccessful in doing business with your preferred "
            'group size. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    reasons_for_being_unsuccessful_with_preferred_group_size_reason_3: str = Field(
        default="",
        description=(
            "Third reason you have been unsuccessful in doing business with your preferred "
            'group size. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    description_of_how_presenting_new_ideas_products_or_services_to_clients_usually_goes: Literal[
        "My clients always take my call because they trust me to bring relevant, timely and valuable ideas, products and services to their attention",
        "I wait until renewal and insert new ideas, products and services into the renewal as value added items",
        "The less I say the better",
        "N/A",
        "",
    ] = Field(
        ...,
        description=(
            "Choose the statement that best describes how presenting new ideas, products or "
            "services to clients usually goes."
        ),
    )

    greatest_concerns_line_1: str = Field(
        ...,
        description=(
            "First line describing your greatest concerns. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    greatest_concerns_line_2: str = Field(
        default="",
        description=(
            "Second line describing your greatest concerns. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_you_like_most_about_your_current_situation_line_1: str = Field(
        ...,
        description=(
            "First line describing what you like most about your current situation. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_you_like_most_about_your_current_situation_line_2: str = Field(
        default="",
        description=(
            "Second line describing what you like most about your current situation. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Your contact details to send with the completed Quick Start"""

    name: str = Field(
        ...,
        description=(
            'Your full name. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    agency: str = Field(
        ...,
        description=(
            'Name of your agency. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        ...,
        description=(
            'Your mobile phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Your email address. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class QuickStartToTheRelationshipOpportunityRiskAssessment(BaseModel):
    """
        Quick Start to the
    Relationship Opportunity & Risk Assessment

        Quick Start to the Relationship Opportunity & Risk Assessment
    """

    relationship_opportunity__risk_assessment: RelationshipOpportunityRiskAssessment = Field(
        ..., description="Relationship Opportunity & Risk Assessment"
    )
    contact_information: ContactInformation = Field(..., description="Contact Information")

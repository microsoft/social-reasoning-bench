from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequiredInformation(BaseModel):
    """Basic organization and contact details required for neighborhood registration"""

    organization_name: str = Field(
        ...,
        description=(
            "Full legal name of the neighborhood organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    covenant_based_homeowners_association: BooleanLike = Field(
        ..., description="Check if the organization is a covenant-based homeowner's association"
    )

    other_incorporated: BooleanLike = Field(
        ..., description="Check if the organization is another type of incorporated entity"
    )

    non_profit: BooleanLike = Field(..., description="Check if the organization is a non-profit")

    llc: BooleanLike = Field(
        ..., description="Check if the organization is a limited liability company (LLC)"
    )

    other: str = Field(
        default="",
        description=(
            "If the organization type is not listed, specify the type here .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    commission_districts: str = Field(
        ...,
        description=(
            "List the Athens-Clarke County commission districts in which the neighborhood "
            'is located .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_person_mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    neighborhood_mailing_address_if_different: str = Field(
        default="",
        description=(
            "Mailing address for the neighborhood organization if different from the "
            'contact person .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number for the contact person or organization .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Valid email address for the contact person to receive neighborhood "
            'notifications .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class OptionalInformation(BaseModel):
    """Additional neighborhood communication and meeting details"""

    website: str = Field(
        default="",
        description=(
            "Website URL for the neighborhood organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    newsletter_or_other_publication: str = Field(
        default="",
        description=(
            "Name or description of any neighborhood newsletter or other publication .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    regularly_scheduled_meetings: BooleanLike = Field(
        default="",
        description="Indicate whether the organization holds regularly scheduled meetings",
    )

    provide_date_time_and_location: str = Field(
        default="",
        description=(
            "Details on the regular meeting schedule, including date, time, and location "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    comments_questions_or_suggested_topics_for_neighborhood_planning_workshops: str = Field(
        default="",
        description=(
            "Any comments, questions, or suggested topics for neighborhood planning "
            'workshops .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PlanningDepartmentUse(BaseModel):
    """For Planning Department processing and approval tracking"""

    date_received_by_planning_department: str = Field(
        default="", description="Date the registration form was received by the Planning Department"
    )  # YYYY-MM-DD format

    date_approved_by_mayor_and_commission: str = Field(
        default="", description="Date the registration was approved by the Mayor and Commission"
    )  # YYYY-MM-DD format


class NeighborhoodNotificationInitiativeNeighborhoodRegistrationForm(BaseModel):
    """
        Neighborhood Notification Initiative
    NEIGHBORHOOD REGISTRATION FORM

        *A valid e-mail address is required for all Contact Persons where they may receive neighborhood notifications.
        Please include the following information with this completed registration form:
        1.  Map of neighborhood boundaries
        2.  One of the following:
            •  For established neighborhoods - Documentation indicating your neighborhood group's
               organizational structure and/or legal status (i.e. by-laws, articles of incorporation, etc.)
            •  For newly forming groups - A petition acknowledging the endorsement of the neighborhood
               organization and Contact Person signed by at least 20% of the property owners and/or residents
               within the proposed neighborhood boundaries.*
    """

    required_information: RequiredInformation = Field(..., description="Required Information")
    optional_information: OptionalInformation = Field(..., description="Optional Information")
    planning_department_use: PlanningDepartmentUse = Field(
        ..., description="Planning Department Use"
    )

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GrantRequestDetails(BaseModel):
    """Basic information about the grant request"""

    project_title: str = Field(
        ...,
        description=(
            'Title or name of the proposed project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    small_grant_200_1000: BooleanLike = Field(
        ..., description="Check if you are applying for a Small Grant between $200 and $1,000"
    )

    mini_grant_200_or_less: BooleanLike = Field(
        ..., description="Check if you are applying for a Mini Grant of $200 or less"
    )

    total_amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount of funding requested from the program"
    )

    date: str = Field(
        ..., description="Date this application is completed and submitted"
    )  # YYYY-MM-DD format


class ProjectLeaderOrganization(BaseModel):
    """Contact and organizational information for the project leader"""

    project_leader_name: str = Field(
        ...,
        description=(
            "Full name of the primary project leader or contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_leader_email_address: str = Field(
        ...,
        description=(
            'Email address for the project leader .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_leader_phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the project leader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    entity_if_applicable: str = Field(
        default="",
        description=(
            "Name of the organization, institution, or entity associated with the project, "
            'if any .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    entity_address: str = Field(
        default="",
        description=(
            "Mailing address of the associated entity, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectLocationDescription(BaseModel):
    """Location and narrative description of the project"""

    physical_address_of_project_location: str = Field(
        ...,
        description=(
            "Street address or detailed physical location where the project will take place "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Detailed description of the project, including objectives, implementation "
            'plan, and timeline .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SmallGrantsProgramApplication(BaseModel):
    """
    Small Grants Program Application

    Submit this completed form along with any accompanying documents to the White Pine Treasurer at whitepine.treasurer@gmail.com.
    """

    grant_request_details: GrantRequestDetails = Field(..., description="Grant Request Details")
    project_leader__organization: ProjectLeaderOrganization = Field(
        ..., description="Project Leader & Organization"
    )
    project_location__description: ProjectLocationDescription = Field(
        ..., description="Project Location & Description"
    )

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationInformation(BaseModel):
    """Basic information about the organization and its mission"""

    name_of_organization: str = Field(
        ...,
        description=(
            'Full legal name of the organization .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            "Street address of the organization (number, street, suite/apartment if "
            'applicable) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the organization address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Organization website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mission_statement: str = Field(
        ...,
        description=(
            "Brief mission statement of the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Primary contact person for this application"""

    name: str = Field(
        ...,
        description=(
            'Name of the primary contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    job_title: str = Field(
        ...,
        description=(
            "Job title or role of the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class GrantType(BaseModel):
    """Type of grant being requested"""

    professional_development: BooleanLike = Field(
        ..., description="Select if the grant type is Professional Development"
    )

    conservation: BooleanLike = Field(..., description="Select if the grant type is Conservation")

    emergency_needs: BooleanLike = Field(
        ..., description="Select if the grant type is Emergency Needs"
    )


class ProfessionalDevelopment(BaseModel):
    """Details about the professional development project/program"""

    project_title: str = Field(
        ...,
        description=(
            "Title of the professional development project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates: str = Field(
        ...,
        description=(
            "Date or range of dates for the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    projected_attendance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees or participants"
    )

    audience_served: str = Field(
        ...,
        description=(
            "Description of the primary audience served by the project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    region_served: str = Field(
        ...,
        description=(
            "Geographic region served by the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_program_description: str = Field(
        ...,
        description=(
            "Detailed description of the project or program .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OrganizationInformation(BaseModel):
    """Organization Information"""

    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
    contact_information: ContactInformation = Field(..., description="Contact Information")
    grant_type: GrantType = Field(..., description="Grant Type")
    professional_development: ProfessionalDevelopment = Field(
        ..., description="Professional Development"
    )

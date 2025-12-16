from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationInformation(BaseModel):
    """Basic application and organizational details"""

    date_of_application: str = Field(
        ..., description="Date this grant application is being completed"
    )  # YYYY-MM-DD format

    legal_name_of_organization_person_persons: str = Field(
        ...,
        description=(
            "Full legal name of the organization or individual applicants .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    year_founded: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the organization was founded"
    )

    current_annual_operating_budget: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current annual operating budget in dollars"
    )

    executive_director: str = Field(
        ...,
        description=(
            'Name of the executive director .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_persontitle_if_different_from_executive_director: str = Field(
        default="",
        description=(
            "Name and title of primary contact if not the executive director .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class OrganizationContactInformation(BaseModel):
    """Primary address and contact details for the organization"""

    address_principal_administrative_office: str = Field(
        ...,
        description=(
            "Street address of the principal or administrative office .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the principal or administrative office .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State or province of the principal or administrative office"
    )

    zip: str = Field(
        ..., description="ZIP or postal code of the principal or administrative office"
    )

    mailing_address_if_different_from_above: str = Field(
        default="",
        description=(
            "Mailing address if different from the principal or administrative office "
            'address .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Fax number, if available .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    website_primary: str = Field(
        default="",
        description=(
            'Primary website URL .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    website_secondary: str = Field(
        default="",
        description=(
            'Secondary or additional website URL .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectOverview(BaseModel):
    """High-level information about the proposed project"""

    project_name: str = Field(
        ...,
        description=(
            "Title of the project or mission for which funding is requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    purpose: str = Field(
        ...,
        description=(
            "Brief description of the purpose of the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of grant funds requested"
    )

    total_project_cost: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total cost of the entire project in dollars"
    )

    project_goals: str = Field(
        ...,
        description=(
            "Detailed goals and objectives of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    beginning_and_ending_dates_of_the_project_campaign: str = Field(
        ...,
        description=(
            "Planned start and end dates for the project or campaign .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    geographic_area_to_be_served: str = Field(
        ...,
        description=(
            "Description of the geographic region or communities that will be served .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class MissionOperationsDetails(BaseModel):
    """Mission-specific context, demographics, and visibility"""

    where_is_your_current_station_location_in_field_or_on_sabbatical: str = Field(
        ...,
        description=(
            "Current station location and whether you are in the field or on sabbatical .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_the_target_demographics_of_your_mission: str = Field(
        ...,
        description=(
            "Description of the primary populations or demographics your mission serves .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    can_we_share_your_mission_project_location_on_social_media: Literal["Yes", "No", "N/A", ""] = (
        Field(
            ..., description="Permission to share your mission or project location on social media"
        )
    )

    what_is_your_plan_for_financial_stability: str = Field(
        ...,
        description=(
            "Explanation of how the project and/or organization will remain financially "
            'stable .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ApplicationHistory(BaseModel):
    """Previous applications to this grant"""

    have_you_applied_with_us_previously: str = Field(
        default="",
        description=(
            "Indicate whether you have applied for this grant before .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    when: str = Field(
        default="",
        description=(
            "If you have applied previously, specify when .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EpicMissionsGrantApplication(BaseModel):
    """
    Epic Missions Grant Application

    ''
    """

    application_information: ApplicationInformation = Field(
        ..., description="Application Information"
    )
    organization_contact_information: OrganizationContactInformation = Field(
        ..., description="Organization Contact Information"
    )
    project_overview: ProjectOverview = Field(..., description="Project Overview")
    mission__operations_details: MissionOperationsDetails = Field(
        ..., description="Mission & Operations Details"
    )
    application_history: ApplicationHistory = Field(..., description="Application History")

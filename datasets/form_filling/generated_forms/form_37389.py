from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BackgroundInformation(BaseModel):
    """Basic organizational and contact information, including Nevada GrantLab experience"""

    program_or_project_title: str = Field(
        ...,
        description=(
            "Title of the program or project for which you are requesting funding .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    organization: str = Field(
        ...,
        description=(
            "Legal name of the applicant organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street mailing address of the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the organization’s address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the organization or contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for the organization, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Primary email address for the organization or contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Organization’s website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Job title or role of the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    explore_nevada_grantlab_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the organization explored the Nevada GrantLab opportunity on the "
            "Engelstad Foundation website"
        ),
    )

    explore_nevada_grantlab_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the organization did not explore the Nevada GrantLab opportunity on "
            "the Engelstad Foundation website"
        ),
    )

    if_yes_register_experience: str = Field(
        default="",
        description=(
            "If you explored Nevada GrantLab, describe whether you registered as a partner "
            'and your experience .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    if_no_why_not_take_opportunity: str = Field(
        default="",
        description=(
            "If you did not explore Nevada GrantLab, explain why not .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InformationabouttheRequest(BaseModel):
    """Details about the grant request and type of support"""

    date_of_application: str = Field(
        ..., description="Date this grant application is submitted"
    )  # YYYY-MM-DD format

    amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount of funding requested from the Engelstad Foundation"
    )

    type_of_support_project: BooleanLike = Field(
        ..., description="Check if the request is for project-specific support"
    )

    type_of_support_general_operating: BooleanLike = Field(
        ..., description="Check if the request is for general operating support"
    )

    type_of_support_capacity_building: BooleanLike = Field(
        ..., description="Check if the request is for capacity building support"
    )

    type_of_support_technical_assistance: BooleanLike = Field(
        ..., description="Check if the request is for technical assistance support"
    )

    type_of_support_emergency: BooleanLike = Field(
        ..., description="Check if the request is for emergency support"
    )

    what_geographic_area_will_be_served: str = Field(
        ...,
        description=(
            "Describe the primary geographic area or communities that will benefit from the "
            'funded work .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class EngelstadFoundationGrantApplicationForm(BaseModel):
    """
        ENGELSTAD FOUNDATION
    GRANT APPLICATION FORM

        Please be sure to fill out the application completely, all fields are required. Your organization’s total grant submission can be up to a maximum of 10 pages. The page count includes this application and your organizational budget. Please feel free to attach additional pages to your application keeping the 10-page limit in mind.
        Note: Any information outside of the fillable fields will not be included in your application. If you have more information than will fit into the preset fields, please add additional pages to this application.
    """

    background_information: BackgroundInformation = Field(..., description="Background Information")
    information_about_the_request: InformationabouttheRequest = Field(
        ..., description="Information about the Request"
    )

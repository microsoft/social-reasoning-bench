from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Information about the sponsor/applicant and primary contact"""

    sponsor_applicant_name: str = Field(
        ...,
        description=(
            "Name of the sponsoring organization or individual applicant .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    organization_if_applicable: str = Field(
        default="",
        description=(
            "Name of the organization, if different from the sponsor/applicant name .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    primary_contact_name: str = Field(
        ...,
        description=(
            "Full name of the primary contact person for this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    primary_contact_address: str = Field(
        ...,
        description=(
            "Mailing address for the primary contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_phone: str = Field(
        ...,
        description=(
            "Phone number for the primary contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_e_mail: str = Field(
        ...,
        description=(
            "Email address for the primary contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Details about the proposed project"""

    project_name: str = Field(
        ...,
        description=(
            'Title or name of the proposed project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_location_address_and_county: str = Field(
        ...,
        description=(
            "Physical address and county where the project will take place .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    latitude_and_longitude_decimal_degrees_e_g_39_55269_107_335726: str = Field(
        ...,
        description=(
            "Latitude and longitude of the project site in decimal degrees .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    project_emergency_response_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if the project is in response to an unforeseen emergency or natural "
            "hazard (Yes option)"
        ),
    )

    project_emergency_response_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the project is not in response to an unforeseen emergency or natural "
            "hazard (No option)"
        ),
    )

    brief_project_summary_limit_150_words: str = Field(
        ...,
        description=(
            "Concise summary of the project, limited to 150 words .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CommunityFundingPartnershipApplication(BaseModel):
    """
        COMMUNITY FUNDING PARTNERSHIP

    Application

        Please refer to the Community Funding Partnership (CFP) Guidelines for additional information about the program, application and evaluation process, contracting requirements, and more.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    project_information: ProjectInformation = Field(..., description="Project Information")

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentTeamInformation(BaseModel):
    """Student or team leader and member details with contact information"""

    student_team_leader: str = Field(
        ...,
        description=(
            "Full name of the student or team leader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            "Current school grade of the student or team leader .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for the student or team leader .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the student or team leader .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    team_member_b: str = Field(
        default="",
        description=(
            "Name of team member b (leave blank if not applicable) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    team_member_c: str = Field(
        default="",
        description=(
            "Name of team member c (leave blank if not applicable) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Basic information about the project and its timing"""

    title_of_project: str = Field(
        ...,
        description=(
            'Full title of the research project .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    preapproval_yes: BooleanLike = Field(
        ..., description="Indicate YES if the project requires SRC/IRB/IACUC or other pre-approval"
    )

    preapproval_no: BooleanLike = Field(
        ...,
        description="Indicate NO if the project does not require SRC/IRB/IACUC or other pre-approval",
    )

    tentative_start_date: str = Field(
        default="", description="Planned tentative start date for the project"
    )  # YYYY-MM-DD format

    continuation_yes: BooleanLike = Field(
        ..., description="Indicate YES if this project continues or progresses from a previous year"
    )

    continuation_no: BooleanLike = Field(
        ..., description="Indicate NO if this project is not a continuation from a previous year"
    )

    actual_start_date: str = Field(
        ...,
        description=(
            "Actual start date of this year's laboratory experiment or data collection (mm/dd/yy)"
        ),
    )  # YYYY-MM-DD format

    end_date: str = Field(
        ...,
        description=(
            "Actual end date of this year's laboratory experiment or data collection (mm/dd/yy)"
        ),
    )  # YYYY-MM-DD format


class SchoolandSponsorInformation(BaseModel):
    """School details and adult sponsor contact"""

    school: str = Field(
        ...,
        description=(
            "Name of the school the student attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    school_phone: str = Field(
        ...,
        description=(
            'Main phone number for the school .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    school_address_line_1: str = Field(
        ...,
        description=(
            "First line of the school mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    school_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the school mailing address (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the school mailing address (if needed) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    adult_sponsor: str = Field(
        ...,
        description=(
            "Full name of the adult sponsor for the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    adult_sponsor_phone_email: str = Field(
        ...,
        description=(
            "Contact phone number and/or email address for the adult sponsor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class DataSourceandWorkSites(BaseModel):
    """Source of data and locations where work is conducted"""

    source_of_data_collected_self_mentor: BooleanLike = Field(
        ..., description="Check if data were collected by the student and/or mentor"
    )

    source_of_data_other: BooleanLike = Field(
        ..., description="Check if data source is other than self/mentor"
    )

    source_of_data_describe_url: str = Field(
        default="",
        description=(
            "Description or URL of the data source if 'Other' is selected .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    work_site_1_name: str = Field(
        default="",
        description=(
            "Name of the first non-home, non-school work site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_2_name: str = Field(
        default="",
        description=(
            "Name of the second non-home, non-school work site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_1_address_line_1: str = Field(
        default="",
        description=(
            "First line of the address for work site 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_2_address_line_1: str = Field(
        default="",
        description=(
            "First line of the address for work site 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_1_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the address for work site 1 (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_2_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the address for work site 2 (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_1_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the address for work site 1 (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_2_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the address for work site 2 (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_1_phone_email: str = Field(
        default="",
        description=(
            "Phone number and/or email contact for work site 1 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_site_2_phone_email: str = Field(
        default="",
        description=(
            "Phone number and/or email contact for work site 2 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class StudentChecklist1a(BaseModel):
    """
    Student Checklist (1A)

    This form is required for ALL projects.
    """

    student__team_information: StudentTeamInformation = Field(
        ..., description="Student / Team Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    school_and_sponsor_information: SchoolandSponsorInformation = Field(
        ..., description="School and Sponsor Information"
    )
    data_source_and_work_sites: DataSourceandWorkSites = Field(
        ..., description="Data Source and Work Sites"
    )

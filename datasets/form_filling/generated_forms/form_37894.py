from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BoardCommissionCommitteeDetails(BaseModel):
    """Information about the position and your residency"""

    name_of_board_commission_or_committee_for_which_you_are_applying: str = Field(
        ...,
        description=(
            "Name of the specific board, commission, or committee you are applying to serve "
            'on .If you cannot fill this, write "N/A". If this field should not be filled '
            "by you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    supervisorial_district_in_which_you_reside: str = Field(
        ...,
        description=(
            "Supervisorial district number or description where you currently reside .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    length_of_residency_in_the_county: str = Field(
        ...,
        description=(
            "How long you have lived in Mariposa County (e.g., number of years and/or "
            'months) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Personal and contact details of the applicant"""

    first_name: str = Field(
        ...,
        description=(
            'Applicant’s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Applicant’s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Complete mailing address, including street, city, state, and ZIP code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for contacting you .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    are_you_over_18_years_of_age: BooleanLike = Field(
        ..., description="Indicate whether you are at least 18 years old"
    )

    day_telephone_number: str = Field(
        ...,
        description=(
            "Primary daytime telephone number where you can be reached .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone_number: str = Field(
        default="",
        description=(
            "Mobile/cell phone number, if different from daytime number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EmploymentInformation(BaseModel):
    """Current employment details"""

    employment_status: str = Field(
        default="",
        description=(
            "Current employment status (e.g., employed, self-employed, unemployed, retired, "
            'student) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    employers_name: str = Field(
        default="",
        description=(
            "Name of your current employer, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employers_address: str = Field(
        default="",
        description=(
            "Mailing or physical address of your employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class QualificationsandExperience(BaseModel):
    """Motivation and prior service on boards/commissions/committees"""

    please_explain_why_you_wish_to_serve_on_this_board_commission_committee: str = Field(
        ...,
        description=(
            "Brief statement of your reasons and motivation for serving on this body .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_list_prior_current_appointments_to_other_boards_commissions_committees: str = Field(
        default="",
        description=(
            "List any previous or current service on other boards, commissions, or "
            'committees .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class AppointmentToMariposaCountyBoardsCommissionsCommittees(BaseModel):
    """
        Application for Appointment to Mariposa County
    BOARDS, COMMISSIONS AND COMMITTEES

        Application for Appointment to Mariposa County BOARDS, COMMISSIONS AND COMMITTEES
    """

    board__commission__committee_details: BoardCommissionCommitteeDetails = Field(
        ..., description="Board / Commission / Committee Details"
    )
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    employment_information: EmploymentInformation = Field(..., description="Employment Information")
    qualifications_and_experience: QualificationsandExperience = Field(
        ..., description="Qualifications and Experience"
    )

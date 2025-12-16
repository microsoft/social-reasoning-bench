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
    """Basic information about the applicant and institution"""

    applicant_last_name: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Applicant\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    institution_name: str = Field(
        ...,
        description=(
            'Name of the applicant\'s institution .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    medical_school_affiliation: str = Field(
        default="",
        description=(
            "Medical school with which the applicant is affiliated, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Applicant\'s primary telephone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AAAPMeetingAttendanceMembershipStatus(BaseModel):
    """Previous AAAP meeting attendance and membership status"""

    yes_annual_meeting: BooleanLike = Field(
        default="",
        description="Check if the applicant has previously attended an AAAP annual meeting",
    )

    last_meeting_date_annual_meeting: str = Field(
        default="", description="Date of the last AAAP annual meeting attended"
    )  # YYYY-MM-DD format

    location_of_last_annual_meeting: str = Field(
        default="",
        description=(
            "Location of the last AAAP annual meeting attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    yes_regional_meeting: BooleanLike = Field(
        default="",
        description="Check if the applicant has previously attended an AAAP regional meeting",
    )

    last_meeting_date_regional_meeting: str = Field(
        default="", description="Date of the last AAAP regional meeting attended"
    )  # YYYY-MM-DD format

    location_of_last_regional_meeting: str = Field(
        default="",
        description=(
            "Location of the last AAAP regional meeting attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    no_i_have_not_attended_a_meeting_previously: BooleanLike = Field(
        default="", description="Check if the applicant has never attended an AAAP meeting"
    )

    yes_active_member: BooleanLike = Field(
        default="", description="Check if the applicant is currently an active AAAP member"
    )

    no_not_previous_member: BooleanLike = Field(
        default="", description="Check if the applicant has not previously been an AAAP member"
    )

    have_you_previously_been_a_dues_paying_member_of_aaap: BooleanLike = Field(
        default="",
        description="Indicate whether the applicant has previously been a dues-paying AAAP member",
    )


class MeetingExpenseAssistanceRequested(BaseModel):
    """Assistance requested for meeting-related expenses"""

    registration_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount requested for registration expenses"
    )

    registration_approved_for_committee_use_only: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of registration expenses approved by the committee"
    )

    airfare_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount requested for airfare expenses"
    )

    airfare_approved_for_committee_use_only: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of airfare expenses approved by the committee"
    )

    lodging_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount requested for lodging expenses"
    )

    lodging_approved_for_committee_use_only: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of lodging expenses approved by the committee"
    )


class DuesAssistanceRequested(BaseModel):
    """Assistance requested for AAAP dues"""

    annual_dues_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount requested for annual dues"
    )

    annual_dues_approved_for_committee_use_only: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of annual dues approved by the committee"
    )

    total_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount requested"
    )

    total_approved_for_committee_use_only: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount approved by the committee"
    )


class CommentsandSignatures(BaseModel):
    """Additional comments and required signatures"""

    comments: str = Field(
        default="",
        description=(
            "Additional comments or information related to this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_signature_date: str = Field(
        ..., description="Date the applicant signed the application"
    )  # YYYY-MM-DD format

    lead_administrator_signature: str = Field(
        default="",
        description=(
            "Signature of the lead administrator approving the request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    lead_administrator_signature_date: str = Field(
        default="", description="Date the lead administrator signed the application"
    )  # YYYY-MM-DD format


class MemberAssistanceProgrammapApplication2022(BaseModel):
    """
    2022 Member Assistance Program (MAP) Application

    ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    aaap_meeting_attendance__membership_status: AAAPMeetingAttendanceMembershipStatus = Field(
        ..., description="AAAP Meeting Attendance & Membership Status"
    )
    meeting_expense_assistance_requested: MeetingExpenseAssistanceRequested = Field(
        ..., description="Meeting Expense Assistance Requested"
    )
    dues_assistance_requested: DuesAssistanceRequested = Field(
        ..., description="Dues Assistance Requested"
    )
    comments_and_signatures: CommentsandSignatures = Field(
        ..., description="Comments and Signatures"
    )

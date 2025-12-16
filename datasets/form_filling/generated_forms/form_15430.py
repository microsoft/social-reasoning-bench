from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobOrderRequestDetails(BaseModel):
    """How applicants should apply and basic job posting details"""

    call_for_appointment: BooleanLike = Field(
        default="",
        description="Select if applicants should call to schedule an appointment for referral.",
    )

    phone_interview: BooleanLike = Field(
        default="", description="Select if applicants should be referred for a phone interview."
    )

    send_resume_via_mail: BooleanLike = Field(
        default="", description="Select if applicants should send their resume via postal mail."
    )

    send_resume_via_e_mail: BooleanLike = Field(
        default="", description="Select if applicants should send their resume via email."
    )

    send_resume_via_fax: BooleanLike = Field(
        default="", description="Select if applicants should send their resume via fax."
    )

    apply_in_person: BooleanLike = Field(
        default="",
        description="Select if applicants should apply in person at the employer's location.",
    )

    days_of_the_week: str = Field(
        default="",
        description=(
            "Days of the week when applicants may apply or be contacted. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    time_of_day: str = Field(
        default="",
        description=(
            "Time of day when applicants may apply or be contacted. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    benefits: str = Field(
        default="",
        description=(
            "Summary of benefits offered for this position. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    deadline_to_apply: str = Field(
        default="", description="Application deadline date for this job order."
    )  # YYYY-MM-DD format

    duties_and_responsibilities: str = Field(
        default="",
        description=(
            "Detailed description of the job duties and responsibilities. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    federal_tax_identification_number: str = Field(
        ...,
        description=(
            "Employer's Federal Tax Identification Number (required entry). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class CareerCenterInformation(BaseModel):
    """Information completed by Career Center staff"""

    career_center_staff: str = Field(
        default="",
        description=(
            "Name of the career center staff member completing this section. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(
        default="", description="Date this job order request section was completed by staff."
    )  # YYYY-MM-DD format

    telephone_number: str = Field(
        default="",
        description=(
            "Telephone number for the career center staff contact. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    career_center: str = Field(
        default="",
        description=(
            "Name or location of the career center handling this job order. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class JobBankStaffSection(BaseModel):
    """Section to be completed by Job Bank Staff"""

    received_date: str = Field(
        default="", description="Date the Job Bank Staff received the job order request."
    )  # YYYY-MM-DD format

    job_order_entered_date: str = Field(
        default="", description="Date the job order was entered into the system."
    )  # YYYY-MM-DD format

    returned_to_center_date: str = Field(
        default="", description="Date the completed job order was returned to the career center."
    )  # YYYY-MM-DD format

    assigned_job_bank_staff: str = Field(
        default="",
        description=(
            "Name of the Job Bank Staff member assigned to this job order. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class JobOrderRequest(BaseModel):
    """
    JOB ORDER REQUEST

    ''
    """

    job_order_request_details: JobOrderRequestDetails = Field(
        ..., description="Job Order Request Details"
    )
    career_center_information: CareerCenterInformation = Field(
        ..., description="Career Center Information"
    )
    job_bank_staff_section: JobBankStaffSection = Field(..., description="Job Bank Staff Section")

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ForOfficeUseOnly(BaseModel):
    """Internal processing details completed by office staff"""

    date_received_month_day_year: str = Field(
        default="", description="Date the form was received by the office"
    )  # YYYY-MM-DD format

    received_by: str = Field(
        default="",
        description=(
            "Name or initials of the person who received the form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CustomerInformation(BaseModel):
    """Agency and primary contact details"""

    name_of_agency: str = Field(
        ...,
        description=(
            'Full name of the submitting agency .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    agency_number: str = Field(
        ...,
        description=(
            "Official identifying number for the agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_department: str = Field(
        ...,
        description=(
            "Name of the specific department within the agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_contact: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_telephone_number: str = Field(
        ...,
        description=(
            "Primary contact person's telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_e_mail_address: str = Field(
        ...,
        description=(
            "Primary contact person's email address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class JobInformation(BaseModel):
    """Print job details, handling instructions, and comments"""

    job_number: str = Field(
        ...,
        description=(
            "Identifier or reference number for the print job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pickup_by: str = Field(
        default="",
        description=(
            "Name of the person or entity who will pick up samples, overprints, or "
            'misprints .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    name_of_contact_if_different_from_above: str = Field(
        default="",
        description=(
            "Alternate contact name if different from the primary contact listed above .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_number: str = Field(
        default="",
        description=(
            "Telephone number for the pickup or delivery contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            "Email address for the pickup or delivery contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    deliver_to: str = Field(
        default="",
        description=(
            "Full delivery address or location where items should be delivered .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    destroy: BooleanLike = Field(
        default="",
        description="Indicates that samples, overprints, and/or misprints should be destroyed",
    )

    print_job_is_one_time: BooleanLike = Field(
        ..., description="Indicates that the print job is a one-time job"
    )

    print_job_is_ongoing: BooleanLike = Field(
        ..., description="Indicates that the print job is ongoing or recurring"
    )

    if_print_job_is_ongoing_please_provide_the_time_frame: str = Field(
        default="",
        description=(
            "Description of the schedule or duration for an ongoing print job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    comments_additional_details_line_1: str = Field(
        default="",
        description=(
            "First line for any additional comments or details about the job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    comments_additional_details_line_2: str = Field(
        default="",
        description=(
            "Second line for any additional comments or details about the job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    comments_additional_details_line_3: str = Field(
        default="",
        description=(
            "Third line for any additional comments or details about the job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class pythonConfidentialPrintMailServicesInfoSubmission(BaseModel):
    """
        CONFIDENTIAL PRINT AND MAIL SERVICES
    SUBMISSION OF CONFIDENTIAL INFORMATION

        *** The purpose of this document is to outline and discuss how Indiana Department of Administration (IDOA) will work with the agencies to assist in fulfilling the requirements pursuant to 10 IAC 5-3-1(14); the Contractor and the State agree to comply with the provisions of IC 4-1-10 and IC 4-1-11. The Contractor shall report all unauthorized disclosures of Social Security numbers and confidential information to the State Contract Representative.
    """

    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")
    customer_information: CustomerInformation = Field(..., description="Customer Information")
    job_information: JobInformation = Field(..., description="Job Information")

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
        default="",
        description="Date the form was received, in month/day/year format (office use only)",
    )  # YYYY-MM-DD format

    received_by: str = Field(
        default="",
        description=(
            "Name or initials of the person who received the form (office use only) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Official agency identification or number .If you cannot fill this, write "
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
    """Details about the print/mail job and handling instructions"""

    job_number: str = Field(
        default="",
        description=(
            "Identifier or reference number for the print job, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pickup_by: BooleanLike = Field(
        default="",
        description="Check this box if samples, overprints, or misprints should be picked up",
    )

    name_of_contact_if_different_from_above: str = Field(
        default="",
        description=(
            "Name of the person who will handle pickup if different from the main contact "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_number: str = Field(
        default="",
        description=(
            "Telephone number for the pickup contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            'Email address for the pickup contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    deliver_to: str = Field(
        default="",
        description=(
            "Delivery address or instructions if items should be delivered .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    destroy: BooleanLike = Field(
        default="",
        description="Check this box if samples, overprints, or misprints should be destroyed",
    )

    print_job_is_one_time: BooleanLike = Field(
        ..., description="Select if this print job will occur only once"
    )

    print_job_is_ongoing: BooleanLike = Field(
        ..., description="Select if this print job will be ongoing or recurring"
    )

    time_frame_if_print_job_is_ongoing: str = Field(
        default="",
        description=(
            "Describe the time frame or schedule if the print job is ongoing .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    comments_additional_details_line_1: str = Field(
        default="",
        description=(
            "First line for any comments or additional job details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_additional_details_line_2: str = Field(
        default="",
        description=(
            "Second line for any comments or additional job details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_additional_details_line_3: str = Field(
        default="",
        description=(
            "Third line for any comments or additional job details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class pythonConfidentialPrintMailServicesInfoSubmission(BaseModel):
    """
        CONFIDENTIAL PRINT AND MAIL SERVICES
    SUBMISSION OF CONFIDENTIAL INFORMATION

        Please submit this form at least forty-eight (48) hours before job submittal to your agency’s assigned Account Manager and Lora Robinson (lrobinson@blueoctopusprinting.com) with the e-mail subject as NEW CONFIDENTIAL FILE (in all caps) and the Indiana Department of Administration (IDOA) Print / Mail Services Inbox at Printmailservices@idoa.in.gov.
        *** The purpose of this document is to outline and discuss how Indiana Department of Administration (IDOA) will work with the agencies to assist in fulfilling the requirements pursuant to 10 IAC 5-3-1(14); the Contractor and the State agree to comply with the provisions of IC 4-1-10 and IC 4-1-11. The Contractor shall report all unauthorized disclosures of Social Security numbers and confidential information to the State Contract Representative.
    """

    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")
    customer_information: CustomerInformation = Field(..., description="Customer Information")
    job_information: JobInformation = Field(..., description="Job Information")

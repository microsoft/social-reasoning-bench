from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ForOfficeUseOnly(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Fields to be completed by office staff upon receipt of the form"""

    date_received_month_day_year: str = Field(
        ...,
        description="Date the form was received (for office use only)"
    )  # YYYY-MM-DD format

    received_by: str = Field(
        ...,
        description=(
            "Name of person who received the form (for office use only) .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class CustomerInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the agency and primary contact submitting the job"""

    name_of_agency: str = Field(
        ...,
        description=(
            "Full name of the agency submitting the request .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    agency_number: str = Field(
        ...,
        description=(
            "Agency identification number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    name_of_department: str = Field(
        ...,
        description=(
            "Department within the agency .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    name_of_contact: str = Field(
        ...,
        description=(
            "Primary contact person for this request .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    contact_telephone_number: str = Field(
        ...,
        description=(
            "Phone number for the primary contact .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_e_mail_address: str = Field(
        ...,
        description=(
            "Email address for the primary contact .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class JobInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the print job and instructions for handling"""

    job_number: str = Field(
        ...,
        description=(
            "Unique identifier for the print/mail job .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    pickup_by: str = Field(
        ...,
        description="Date by which items should be picked up (if applicable)"
    )  # YYYY-MM-DD format

    name_of_contact_if_different_from_above: str = Field(
        ...,
        description=(
            "Contact person for pickup if different from main contact .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Phone number for alternate contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Email address for alternate contact .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    deliver_to: str = Field(
        ...,
        description=(
            "Delivery address or instructions .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    destroy: BooleanLike = Field(
        ...,
        description="Check if items should be destroyed"
    )

    print_job_is_one_time: BooleanLike = Field(
        ...,
        description="Check if the print job is a one-time job"
    )

    print_job_is_ongoing: BooleanLike = Field(
        ...,
        description="Check if the print job is ongoing"
    )

    if_print_job_is_ongoing_please_provide_the_time_frame: str = Field(
        ...,
        description=(
            "Specify the time frame for ongoing print jobs .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    comments_additional_details: str = Field(
        ...,
        description=(
            "Any additional comments or details .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ConfidentialPrintMailSubmissionStateForm53623r3119IndianaDOA(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    CONFIDENTIAL PRINT AND MAIL SERVICES
SUBMISSION OF CONFIDENTIAL INFORMATION
State Form 53623 (R3 / 1-19)
INDIANA DEPARTMENT OF ADMINISTRATION

    The purpose of this document is to outline and discuss how Indiana Department of Administration (IDOA) will work with the agencies to assist in fulfilling the requirements pursuant to 10 IAC 5-3-1(14); the Contractor and the State agree to comply with the provisions of IC 4-1-10 and IC 4-1-11. The Contractor shall report all unauthorized disclosures of Social Security numbers and confidential information to the State Contract Representative.
    """

    for_office_use_only: ForOfficeUseOnly = Field(
        ...,
        description="For Office Use Only"
    )
    customer_information: CustomerInformation = Field(
        ...,
        description="Customer Information"
    )
    job_information: JobInformation = Field(
        ...,
        description="Job Information"
    )
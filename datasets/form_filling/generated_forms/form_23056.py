from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class DateTimeInterpretingServicesareNeeded(BaseModel):
    """Scheduling details for the interpreting services"""

    date: str = Field(
        ..., description="Calendar date when interpreting services are needed"
    )  # YYYY-MM-DD format

    start_time: str = Field(
        ...,
        description=(
            "Time interpreting services should begin, including am or pm .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    end_time: str = Field(
        ...,
        description=(
            "Time interpreting services should end, including am or pm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequestFrom(BaseModel):
    """Information about the person or organization making the request"""

    name_request_from: str = Field(
        ...,
        description=(
            "Name of the person submitting the interpreter request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        default="",
        description=(
            "Job title or role of the person making the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_number: str = Field(
        default="",
        description=(
            "Unit, department, or internal reference number for the requester .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    company: str = Field(
        default="",
        description=(
            "Name of the company or organization making the request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_request_from: str = Field(
        ...,
        description=(
            "Phone number for the person or organization making the request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    fax_request_from: str = Field(
        default="",
        description=(
            "Fax number for the requester, used for sending confirmations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ClientInformation(BaseModel):
    """Details about the deaf client and assignment"""

    deaf_persons_name: str = Field(
        ...,
        description=(
            "Full name of the Deaf person who will receive interpreting services .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_assignment: str = Field(
        ...,
        description=(
            "Description of the interpreting assignment (e.g., medical, legal, meeting) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    case_po_number: str = Field(
        default="",
        description=(
            "Case number or purchase order number associated with this request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_needs: str = Field(
        default="",
        description=(
            "Any special needs or accommodations required for the assignment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class LocationofServices(BaseModel):
    """Where the interpreting services will take place"""

    name_location_of_services: str = Field(
        ...,
        description=(
            "Name of the facility, organization, or location where services will occur .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    on_site_contacts_name_phone_number: str = Field(
        ...,
        description=(
            "Name and phone number of the on-site contact person at the service location "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    address_location_of_services: str = Field(
        ...,
        description=(
            "Street address where interpreting services will be provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    directions: str = Field(
        default="",
        description=(
            "Driving or access directions to the service location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BillingInformation(BaseModel):
    """Billing contact and address for payment"""

    name_billing_information: str = Field(
        ...,
        description=(
            "Name of the person or entity responsible for payment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_billing_information: str = Field(
        ...,
        description=(
            'Billing street address for invoices .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the billing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the billing address")

    zip: str = Field(..., description="ZIP code for the billing address")

    attention: str = Field(
        default="",
        description=(
            "Specific person or department to direct the invoice to .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    po: str = Field(
        default="",
        description=(
            "Purchase order number for billing, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signature(BaseModel):
    """Signature acknowledging acceptance for payment"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the person accepting responsibility for payment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Cancellation(BaseModel):
    """Details if the appointment is canceled"""

    canceled_by: str = Field(
        default="",
        description=(
            "Name of the person or party who canceled the assignment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_cancellation: str = Field(
        default="",
        description=(
            "Date and time when the assignment was canceled .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    interpreter_notified: str = Field(
        default="",
        description=(
            "Indication of when or how the interpreter was notified of cancellation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ForOfficeUseOnly(BaseModel):
    """Internal office processing fields"""

    interpreter_copied: str = Field(
        default="",
        description=(
            "Internal note indicating that the interpreter has been copied on the request "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    book_entry: str = Field(
        default="",
        description=(
            "Internal scheduling or bookkeeping entry reference .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    interpreter_assigned: str = Field(
        default="",
        description=(
            "Name of the interpreter assigned to this request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DeafCommunityAdvocacyNetworkInterpreterRequestForm(BaseModel):
    """
        DEAF COMMUNITY ADVOCACY NETWORK
    Interpreter Request Form

        Interpreter Request Form. Please complete and fax to: (248) 332-7334 Or email this form to: requests@deafcan.org
    """

    date__time_interpreting_services_are_needed: DateTimeInterpretingServicesareNeeded = Field(
        ..., description="Date & Time Interpreting Services are Needed"
    )
    request_from: RequestFrom = Field(..., description="Request From")
    client_information: ClientInformation = Field(..., description="Client Information")
    location_of_services: LocationofServices = Field(..., description="Location of Services")
    billing_information: BillingInformation = Field(..., description="Billing Information")
    signature: Signature = Field(..., description="Signature")
    cancellation: Cancellation = Field(..., description="Cancellation")
    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")

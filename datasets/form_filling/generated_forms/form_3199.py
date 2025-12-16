from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientInformation(BaseModel):
    """Information about the requesting company and primary client"""

    company_name: str = Field(
        ...,
        description=(
            "Name of the company requesting interpreting services .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Department within the company requesting services .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_name_person_who_needs_interpreting: str = Field(
        ...,
        description=(
            "Full name of the person who will be using the interpreter .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    on_site_contact_person: str = Field(
        ...,
        description=(
            "Name of the person the interpreter should contact upon arrival .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for the on-site contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_including_cellphone_for_last_minute_needs: str = Field(
        ...,
        description=(
            "Primary phone number, including a cellphone for last-minute needs .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AppointmentDateLocation(BaseModel):
    """Date, time, and location details for the appointment"""

    dates_from: str = Field(
        ..., description="Start date of the interpreting appointment"
    )  # YYYY-MM-DD format

    dates_to: str = Field(
        ..., description="End date of the interpreting appointment"
    )  # YYYY-MM-DD format

    times_from: str = Field(
        ...,
        description=(
            "Start time of the interpreting appointment (include AM/PM and time zone if "
            'needed) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    times_to: str = Field(
        ...,
        description=(
            "End time of the interpreting appointment (include AM/PM and time zone if "
            'needed) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    service_site_name: str = Field(
        ...,
        description=(
            "Name of the facility or site where the service will take place .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    service_site_address_line_1: str = Field(
        ...,
        description=(
            "First line of the service site street address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    service_site_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the service site address (suite, building, etc.) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    specific_location_instructions_line_1: str = Field(
        ...,
        description=(
            "First line of detailed instructions on how to find the exact location "
            '(building, office number, etc.) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    specific_location_instructions_line_2: str = Field(
        default="",
        description=(
            "Additional location instructions, if needed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    specific_location_instructions_line_3: str = Field(
        default="",
        description=(
            "Further location instructions, if needed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephonic_interpreting_call_in_number: str = Field(
        default="",
        description=(
            "Call-in phone number to be used for telephonic interpreting .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class TypeofAppointment(BaseModel):
    """Nature and details of the appointment"""

    type_of_appointment_medical: BooleanLike = Field(
        ..., description="Check if this is a medical appointment"
    )

    type_of_appointment_legal: BooleanLike = Field(
        ..., description="Check if this is a legal appointment"
    )

    type_of_appointment_other: str = Field(
        default="",
        description=(
            "Describe the type of appointment if it is not medical or legal .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    appointment_meeting_details_line_1: str = Field(
        default="",
        description=(
            "First line describing the nature and purpose of the appointment or meeting .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    appointment_meeting_details_line_2: str = Field(
        default="",
        description=(
            "Additional details about the appointment or meeting .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LanguageDetails(BaseModel):
    """Language and origin information for the client"""

    clients_country_of_origin: str = Field(
        ...,
        description=(
            "Country of origin of the client needing interpreting .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        default="",
        description=(
            "State or region within the client's country of origin .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    municipal: str = Field(
        default="",
        description=(
            "Municipality or local area within the client's state or region .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    language: str = Field(
        ...,
        description=(
            "Specific language or Indigenous language needed for interpreting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_instructions_or_needs_line_1: str = Field(
        ...,
        description=(
            "First line describing any special instructions or needs related to language or "
            'client .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_instructions_or_needs_line_2: str = Field(
        default="",
        description=(
            "Additional special instructions or needs .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalInformation(BaseModel):
    """Other helpful information about the appointment"""

    any_additional_information_about_this_appointment_line_1: str = Field(
        ...,
        description=(
            "First line for any other information helpful in choosing an interpreter .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    any_additional_information_about_this_appointment_line_2: str = Field(
        default="",
        description=(
            "Additional space for other helpful appointment information .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BillingInformation(BaseModel):
    """Invoice and billing address details"""

    email_invoice_to: str = Field(
        ...,
        description=(
            "Email address where the invoice should be sent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mail_invoice_to_agency_name: str = Field(
        ...,
        description=(
            "Agency name and contact to whom a mailed invoice should be addressed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    billing_address: str = Field(
        ...,
        description=(
            "Street address for mailing the invoice .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    billing_city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP/postal code for the billing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ContactPersontoconfirmappointmentdetails(BaseModel):
    """Contact details for appointment confirmation and history"""

    contact_person_name: str = Field(
        ...,
        description=(
            "Name of the person to contact to confirm appointment details .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_person_phone_number: str = Field(
        ...,
        description=(
            'Phone number for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_person_email: str = Field(
        ...,
        description=(
            'Email address for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    have_we_interpreted_for_you_previously_yes: BooleanLike = Field(
        default="",
        description="Select if the organization has used these interpreting services before",
    )

    have_we_interpreted_for_you_previously_no: BooleanLike = Field(
        default="",
        description="Select if the organization has not used these interpreting services before",
    )

    how_did_you_hear_about_us: str = Field(
        default="",
        description=(
            "Describe how you learned about Indigenous Interpreting+ .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InterpreterRequestForm(BaseModel):
    """
    Interpreter Request Form

    Please fill out the request form as completely as possible. Please note this request is NOT a confirmation of an interpreter. We will contact you as soon as your request has been received. If you would like to inquire about the status of your request, please email us at info@interpretnmf.com or call us at 1-855-662-5300.
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    appointment_date__location: AppointmentDateLocation = Field(
        ..., description="Appointment Date & Location"
    )
    type_of_appointment: TypeofAppointment = Field(..., description="Type of Appointment")
    language_details: LanguageDetails = Field(..., description="Language Details")
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
    billing_information: BillingInformation = Field(..., description="Billing Information")
    contact_person_to_confirm_appointment_details: ContactPersontoconfirmappointmentdetails = Field(
        ..., description="Contact Person (to confirm appointment details)"
    )

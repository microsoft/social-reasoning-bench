from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AppointmentInformation(BaseModel):
    """Department and research details for the fellowship appointment"""

    department_division: str = Field(
        ...,
        description=(
            "Department and/or division for which the appointment is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    begin_date: str = Field(
        ..., description="Proposed start date of the research/clinical fellowship"
    )  # YYYY-MM-DD format

    scientific_interest_area_of_research: str = Field(
        ...,
        description=(
            "Brief description of primary scientific interests or research area .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PersonalInformation(BaseModel):
    """Basic identifying information about the applicant"""

    name_last: str = Field(
        ...,
        description=(
            'Legal last name (family name) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_first: str = Field(
        ...,
        description=(
            'Legal first name (given name) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_middle: str = Field(
        default="",
        description=(
            'Middle name or initial, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_name_used_last: str = Field(
        default="",
        description=(
            "Other last name used (e.g., maiden name or previous legal name) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_name_used_first: str = Field(
        default="",
        description=(
            'Other first name used, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_name_used_middle: str = Field(
        default="",
        description=(
            "Other middle name or initial used, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    united_states_social_security_number: str = Field(
        ..., description="U.S. Social Security Number"
    )


class ContactInformation(BaseModel):
    """Current and permanent contact details for the applicant"""

    current_local_address_line_1: str = Field(
        ...,
        description=(
            "Current/local address, first line (street address) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_local_address_line_2: str = Field(
        default="",
        description=(
            "Current/local address, second line (additional address details, if needed) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_local_telephone_number: str = Field(
        ...,
        description=(
            "Primary current/local telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    permanent_address_line_1: str = Field(
        ...,
        description=(
            "Permanent address, first line (street address) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    permanent_address_line_2: str = Field(
        default="",
        description=(
            "Permanent address, second line (additional address details, if needed) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Person to contact in case of emergency"""

    emergency_contact_name: str = Field(
        ...,
        description=(
            'Full name of emergency contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship: str = Field(
        ...,
        description=(
            "Relationship of the emergency contact to you (e.g., spouse, parent, friend) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    emergency_contact_e_mail_address: str = Field(
        default="",
        description=(
            "Email address of the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number of the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CitizenshipandVisaInformation(BaseModel):
    """Citizenship status and visa details"""

    citizenship_us_citizen_yes: BooleanLike = Field(
        ..., description="Check if you are a citizen of the United States"
    )

    citizenship_us_citizen_no: BooleanLike = Field(
        ..., description="Check if you are not a citizen of the United States"
    )

    citizenship: str = Field(
        default="",
        description=(
            "Country of citizenship (for non-U.S. citizens) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    visa_type: str = Field(
        default="",
        description=(
            "Type of U.S. visa held or requested (e.g., J-1, H-1B) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    entrance_date_into_us: str = Field(
        default="", description="Most recent date of entry into the United States"
    )  # YYYY-MM-DD format

    length_of_stay_valid_to: str = Field(
        default="", description="Date until which your authorized stay in the U.S. is valid"
    )  # YYYY-MM-DD format


class ApplicationForAppointmentAsResearchAndClinicalFellow(BaseModel):
    """
    APPLICATION FOR APPOINTMENT AS RESEARCH and CLINICAL FELLOW

    Instructions: Complete all sections (please print or type all responses). If a section does not pertain to you, mark as N/A (not applicable). Do not leave any section blank nor make reference to an attached CV.
    """

    appointment_information: AppointmentInformation = Field(
        ..., description="Appointment Information"
    )
    personal_information: PersonalInformation = Field(..., description="Personal Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    citizenship_and_visa_information: CitizenshipandVisaInformation = Field(
        ..., description="Citizenship and Visa Information"
    )

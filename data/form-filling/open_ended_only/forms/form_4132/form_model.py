from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic information about the youth participant"""

    participant_first_last_name: str = Field(
        ...,
        description=(
            "Full name of the youth participant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    participant_address: str = Field(
        ...,
        description=(
            "Street address of the participant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and zip code .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    participant_phone: str = Field(
        ...,
        description=(
            "Phone number of the participant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    participant_email: str = Field(
        ...,
        description=(
            "Email address of the participant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    does_participant_require_transportation: BooleanLike = Field(
        ...,
        description="Indicate if transportation is needed for meetings/activities"
    )

    participant_gender: Literal["Female", "Male", "N/A", ""] = Field(
        ...,
        description="Gender of the participant"
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school participant attends .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    grade: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Grade level of the participant"
    )

    do_you_have_a_peanut_allergy: BooleanLike = Field(
        ...,
        description="Indicate if participant has a peanut allergy"
    )

    date_of_birth: str = Field(
        ...,
        description="Participant's date of birth"
    )  # YYYY-MM-DD format

    t_shirt_size: Literal["S", "M", "L", "XL", "XXL", "N/A", ""] = Field(
        ...,
        description="Select participant's T-shirt size"
    )


class ParentGuardianInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Contact information for the participant's parent or guardian"""

    parent_guardian_first_last_name: str = Field(
        ...,
        description=(
            "Full name of parent or guardian .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    parent_guardian_email: str = Field(
        ...,
        description=(
            "Email address of parent or guardian .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    parent_guardian_phone: str = Field(
        ...,
        description=(
            "Phone number of parent or guardian .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class EmergencyContact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Emergency contact details"""

    emergency_contact_first_last_name: str = Field(
        ...,
        description=(
            "Full name of emergency contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            "Phone number of emergency contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    emergency_contact_email: str = Field(
        ...,
        description=(
            "Email address of emergency contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    emergency_contact_relationship: str = Field(
        ...,
        description=(
            "Relationship of emergency contact to participant (e.g. Mom) .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class MedicalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Health conditions and dietary restrictions"""

    medical_information_dietary_restrictions: str = Field(
        ...,
        description=(
            "Describe any health conditions, dietary restrictions, or activity limitations "
            ".If you cannot fill this, write \"N/A\". If this field should not be filled by "
            "you (for example, it belongs to another person or office), leave it blank "
            "(empty string \"\")."
        )
    )


class SerenityFirstYouthCoalitionRegistrationForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Registration Form for  
Serenity First Prevention and Support Youth Coalition

    Registration form for the Serenity First Prevention and Support Youth Coalition. All youth activities are free and provided by a grant from the Arizona Parents Commission for Drug Education and Prevention and the Governor’s Office of Youth, Faith and Family. The Youth Coalition accepts youth ages 13-18 and meets once a month at the location of the monthly activity (currently meeting on Zoom). This form collects participant and parent/guardian contact information, emergency contacts, medical and dietary information, and other relevant details for registration.
    """

    participant_information: ParticipantInformation = Field(
        ...,
        description="Participant Information"
    )
    parentguardian_information: ParentGuardianInformation = Field(
        ...,
        description="Parent/Guardian Information"
    )
    emergency_contact: EmergencyContact = Field(
        ...,
        description="Emergency Contact"
    )
    medical_information: MedicalInformation = Field(
        ...,
        description="Medical Information"
    )
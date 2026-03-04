from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    """Basic information about the youth participant"""

    participant_first_last_name: str = Field(
        ...,
        description=(
            "Participant's full legal first and last name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    participant_address: str = Field(
        ...,
        description=(
            "Street address where the participant resides .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the participant's address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    participant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    participant_email: str = Field(
        ...,
        description=(
            'Participant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    transportation_required_yes: BooleanLike = Field(
        default="",
        description=(
            "Select yes if the participant needs transportation to and from meetings/activities"
        ),
    )

    transportation_required_no: BooleanLike = Field(
        default="",
        description=(
            "Select no if the participant does not need transportation to and from "
            "meetings/activities"
        ),
    )

    participant_gender_female_or_male: Literal["Female", "Male", "N/A", ""] = Field(
        ..., description="Participant's gender"
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school the participant attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Participant\'s current grade level .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    peanut_allergy: BooleanLike = Field(
        ..., description="Indicate whether the participant has a peanut allergy"
    )

    date_of_birth_mm_dd_yy: str = Field(
        ..., description="Participant's date of birth in MM/DD/YY format"
    )  # YYYY-MM-DD format

    t_shirt_size_s: BooleanLike = Field(
        default="", description="Select if the participant's T-shirt size is Small"
    )

    t_shirt_size_m: BooleanLike = Field(
        default="", description="Select if the participant's T-shirt size is Medium"
    )

    t_shirt_size_l: BooleanLike = Field(
        default="", description="Select if the participant's T-shirt size is Large"
    )

    t_shirt_size_xl: BooleanLike = Field(
        default="", description="Select if the participant's T-shirt size is Extra Large"
    )

    t_shirt_size_xxl: BooleanLike = Field(
        default="", description="Select if the participant's T-shirt size is Extra Extra Large"
    )


class ParentGuardianInformation(BaseModel):
    """Contact information for the participant's parent or guardian"""

    parent_guardian_first_last_name: str = Field(
        ...,
        description=(
            "Parent or guardian's full first and last name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_email: str = Field(
        ...,
        description=(
            'Parent or guardian\'s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_phone: str = Field(
        ...,
        description=(
            "Parent or guardian's primary phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact details for the participant"""

    emergency_contact_first_last_name: str = Field(
        ...,
        description=(
            "Full name of the emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            "Phone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_email: str = Field(
        default="",
        description=(
            "Email address for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship_eg_mom: str = Field(
        ...,
        description=(
            "Relationship of the emergency contact to the participant (e.g., Mom, Dad, "
            'Aunt) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class MedicalDietaryInformation(BaseModel):
    """Health conditions and dietary restrictions relevant to participation"""

    medical_information_dietary_restrictions: str = Field(
        default="",
        description=(
            "Describe any medical conditions, dietary restrictions, or activity limitations "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SerenityFirstYouthCoalitionRegistrationForm(BaseModel):
    """
        Registration Form for
    Serenity First Prevention and Support Youth Coalition

        ALL YOUTH ACTIVITIES ARE FREE AND PROVIDED BY OUR GRANT FROM THE ARIZONA PARENTS COMMISSION ON DRUG EDUCATION AND PREVENTION AND THE GOVERNOR’S OFFICE OF YOUTH, FAITH AND FAMILY. The Youth Coalition accepts youth 13-18 and meets once a month at the location of our monthly activity. (Presently we are meeting on Zoom from 5:30 - 7:00 pm once a month)
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    parentguardian_information: ParentGuardianInformation = Field(
        ..., description="Parent/Guardian Information"
    )
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    medical__dietary_information: MedicalDietaryInformation = Field(
        ..., description="Medical & Dietary Information"
    )

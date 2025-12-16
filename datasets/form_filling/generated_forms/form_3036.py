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
    """Basic information about the adult member/participant and troop"""

    troop_number: str = Field(
        default="",
        description=(
            'Trail Life USA troop number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    participants_name: str = Field(
        ...,
        description=(
            "Full legal name of the adult participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Date of birth in MM/DD/YYYY format"
    )  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Age in years")

    address: str = Field(
        ...,
        description=(
            'Street address of the participant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State of residence (two-letter abbreviation if applicable)"
    )

    zip: str = Field(..., description="Zip or postal code")

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    troop_leader: str = Field(
        default="",
        description=(
            "Name of the participant's troop leader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContacts(BaseModel):
    """People to contact in case of emergency"""

    emergency_contact_name_1: str = Field(
        ...,
        description=(
            'Name of first emergency contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship_1: str = Field(
        ...,
        description=(
            "Relationship of first emergency contact to participant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_2: str = Field(
        default="",
        description=(
            'Name of second emergency contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship_2: str = Field(
        default="",
        description=(
            "Relationship of second emergency contact to participant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_number: str = Field(
        default="",
        description=(
            "Home phone number for emergency contacts .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone_number: str = Field(
        default="",
        description=(
            "Cell phone number for emergency contacts .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HealthAccidentInsuranceInformation(BaseModel):
    """Participant's health and accident insurance coverage details"""

    no_health_care_coverage: BooleanLike = Field(
        default="", description="Check if the participant currently has no health care coverage"
    )

    has_health_care_coverage: BooleanLike = Field(
        default="",
        description=(
            "Check if the participant has health care coverage and will provide details below"
        ),
    )

    health_accident_insurance_company: str = Field(
        default="",
        description=(
            "Name of the health or accident insurance company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    policy_holder: str = Field(
        default="",
        description=(
            'Name of the policy holder .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        default="",
        description=(
            'Insurance policy number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    group_number: str = Field(
        default="",
        description=(
            'Insurance group number, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(
        default="", description="Effective date of the insurance coverage"
    )  # YYYY-MM-DD format


class PhysicianInformation(BaseModel):
    """Primary care physician, dentist, and preferred hospital"""

    primary_care_physician: str = Field(
        default="",
        description=(
            "Name of the participant's primary care physician .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_care_physician_phone_number: str = Field(
        default="",
        description=(
            "Phone number for the primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physicians_address: str = Field(
        default="",
        description=(
            "Mailing address of the primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dentists_name: str = Field(
        default="",
        description=(
            'Name of the participant\'s dentist .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dentists_phone_number: str = Field(
        default="",
        description=(
            'Phone number for the dentist .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    preferred_hospital: str = Field(
        default="",
        description=(
            "Name of the preferred hospital for treatment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Allergies(BaseModel):
    """All known allergies and typical reactions/management"""

    allergy_to_row_1: str = Field(
        default="",
        description=(
            "First listed allergen (e.g., medication, food, environmental) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    normal_reaction_and_management_row_1: str = Field(
        default="",
        description=(
            "Description of typical reaction and how it is managed for the first allergen "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    allergy_to_row_2: str = Field(
        default="",
        description=(
            "Second listed allergen (e.g., medication, food, environmental) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    normal_reaction_and_management_row_2: str = Field(
        default="",
        description=(
            "Description of typical reaction and how it is managed for the second allergen "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    allergy_to_row_3: str = Field(
        default="",
        description=(
            "Third listed allergen (e.g., medication, food, environmental) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    normal_reaction_and_management_row_3: str = Field(
        default="",
        description=(
            "Description of typical reaction and how it is managed for the third allergen "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class TrailLifeUsaAdultMemberparticipantHealthAndMedicalRecord(BaseModel):
    """
        TRAIL LIFE USA

    ADULT Member/Participant Health and Medical Record

        An additional medical form is required for Trail Life USA activities or events that exceed 72 hours in duration or include high altitude or high-exertion activities. That High Adventure Medical form requires the examination by and the signature of a doctor or health care professional.
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    emergency_contacts: EmergencyContacts = Field(..., description="Emergency Contacts")
    healthaccident_insurance_information: HealthAccidentInsuranceInformation = Field(
        ..., description="Health/Accident Insurance Information"
    )
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    allergies: Allergies = Field(..., description="Allergies")

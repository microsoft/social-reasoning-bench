from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NDISParticipantDetails(BaseModel):
    """Participant personal and NDIS plan information"""

    first_name: str = Field(
        ...,
        description=(
            'Participant\'s given name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Participant\'s family name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Participant's date of birth")  # YYYY-MM-DD format

    phone: str = Field(
        ...,
        description=(
            "Participant's primary contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    gender_female: BooleanLike = Field(
        default="", description="Tick if the participant identifies as female"
    )

    gender_male: BooleanLike = Field(
        default="", description="Tick if the participant identifies as male"
    )

    gender_prefer_not_to_say: BooleanLike = Field(
        default="", description="Tick if the participant prefers not to disclose their gender"
    )

    gender_non_binary: BooleanLike = Field(
        default="", description="Tick if the participant identifies as non-binary"
    )

    email: str = Field(
        ...,
        description=(
            'Participant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    residential_address: str = Field(
        ...,
        description=(
            "Participant's full residential street address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    suburb: str = Field(
        ...,
        description=(
            "Suburb of the participant's residential address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State or territory of the participant's residential address"
    )

    postcode: str = Field(..., description="Postcode of the participant's residential address")

    living_arrangement_alone: BooleanLike = Field(
        default="", description="Tick if the participant lives alone"
    )

    living_arrangement_family_partner: BooleanLike = Field(
        default="", description="Tick if the participant lives with family or a partner"
    )

    living_arrangement_support_accommodation: BooleanLike = Field(
        default="", description="Tick if the participant lives in supported accommodation"
    )

    living_arrangement_other: BooleanLike = Field(
        default="", description="Tick if the participant has another type of living arrangement"
    )

    please_tick_to_indicate: BooleanLike = Field(
        default="", description="General instruction to tick the relevant living arrangement option"
    )

    ndis_plan_number: str = Field(
        ...,
        description=(
            'Participant\'s NDIS plan number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ndis_plan_dates_from: str = Field(
        ..., description="Start date of the current NDIS plan"
    )  # YYYY-MM-DD format

    ndis_plan_dates_to: str = Field(
        ..., description="End date of the current NDIS plan"
    )  # YYYY-MM-DD format

    translator_required: BooleanLike = Field(
        default="", description="Indicate whether the participant requires a translator"
    )

    preferred_language: str = Field(
        default="",
        description=(
            "Participant's preferred language for communication .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferrerDetails(BaseModel):
    """Information about the person or organisation making the referral"""

    self_referred_tick: BooleanLike = Field(
        default="", description="Tick if the participant is self-referred or referred by a relative"
    )

    name_of_organisation: str = Field(
        default="",
        description=(
            "Name of the referring organisation, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_referrer_org: str = Field(
        default="",
        description=(
            "Email address for the referring organisation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    first_name_referrer: str = Field(
        default="",
        description=(
            'Given name of the referrer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name_referrer: str = Field(
        default="",
        description=(
            'Family name of the referrer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_referrer: str = Field(
        default="",
        description=(
            'Referrer\'s contact phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    job_title_role: str = Field(
        default="",
        description=(
            'Referrer\'s job title or role .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    support_coordinator: BooleanLike = Field(
        default="", description="Tick if the referrer is a Support Coordinator"
    )

    case_manager: BooleanLike = Field(
        default="", description="Tick if the referrer is a Case Manager"
    )

    local_area_coordinator: BooleanLike = Field(
        default="", description="Tick if the referrer is a Local Area Coordinator"
    )

    carer_other: BooleanLike = Field(
        default="", description="Tick if the referrer is a carer or has another role"
    )


class PrimaryDisabilityHealthBackground(BaseModel):
    """Primary disability/health information and requested services"""

    primary_disability_health_background_description: str = Field(
        ...,
        description=(
            "Description of the participant's primary physical or psychological disability "
            'and relevant health background .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_modifications: BooleanLike = Field(
        default="", description="Tick if home modifications are requested or relevant"
    )

    assistive_technology: BooleanLike = Field(
        default="", description="Tick if assistive technology services are requested or relevant"
    )

    paediatrics: BooleanLike = Field(
        default="", description="Tick if paediatric services are requested or relevant"
    )

    functional_capacity_assessment: BooleanLike = Field(
        default="", description="Tick if a functional capacity assessment is requested or relevant"
    )

    life_skills_training: BooleanLike = Field(
        default="", description="Tick if life skills training is requested or relevant"
    )

    driving_school: BooleanLike = Field(
        default="", description="Tick if driving school services are requested or relevant"
    )

    specialised_disability_assessments_sda: BooleanLike = Field(
        default="",
        description="Tick if specialised disability assessments (SDA) are requested or relevant",
    )

    supported_independent_living_sil: BooleanLike = Field(
        default="",
        description="Tick if Supported Independent Living (SIL) services are requested or relevant",
    )

    vision_rehabilitation: BooleanLike = Field(
        default="", description="Tick if vision rehabilitation services are requested or relevant"
    )

    home_safety_assessment: BooleanLike = Field(
        default="", description="Tick if a home safety assessment is requested or relevant"
    )

    falls_prevention_education: BooleanLike = Field(
        default="", description="Tick if falls prevention education is requested or relevant"
    )

    ergonomic_assessment: BooleanLike = Field(
        default="", description="Tick if an ergonomic assessment is requested or relevant"
    )

    sensory_assessment: BooleanLike = Field(
        default="", description="Tick if a sensory assessment is requested or relevant"
    )

    physiotherapy: BooleanLike = Field(
        default="", description="Tick if physiotherapy services are requested or relevant"
    )

    pain_management: BooleanLike = Field(
        default="", description="Tick if pain management services are requested or relevant"
    )

    delivery_mode_in_person: BooleanLike = Field(
        default="", description="Tick if services are to be delivered in person"
    )

    delivery_mode_telehealth: BooleanLike = Field(
        default="", description="Tick if services are to be delivered via telehealth"
    )

    delivery_mode_both_in_person_and_telehealth: BooleanLike = Field(
        default="",
        description="Tick if services are to be delivered using both in person and telehealth modes",
    )


class OtGroupEnablingIndependenceNdisParticipantDetails(BaseModel):
    """
        OT GROUP
    ENABLING INDEPENDENCE
    NDIS PARTICIPANT DETAILS

        ''
    """

    ndis_participant_details: NDISParticipantDetails = Field(
        ..., description="NDIS Participant Details"
    )
    referrer_details: ReferrerDetails = Field(..., description="Referrer Details")
    primary_disability__health_background: PrimaryDisabilityHealthBackground = Field(
        ..., description="Primary Disability / Health Background"
    )

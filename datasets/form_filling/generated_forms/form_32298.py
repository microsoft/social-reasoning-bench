from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class DeceasedandPolicyInformation(BaseModel):
    """Basic identifying details about the deceased and the policy"""

    policy_number: str = Field(
        ...,
        description=(
            "Equitable Life of Canada policy number for the deceased .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    full_name_of_deceased: str = Field(
        ...,
        description=(
            "Full legal name of the deceased person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_death: str = Field(
        ..., description="Calendar date on which the death occurred"
    )  # YYYY-MM-DD format

    residence_at_death: str = Field(
        ...,
        description=(
            "Usual residence address of the deceased at the time of death .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    place_of_death: str = Field(
        ...,
        description=(
            "Place where death occurred (e.g., hospital name, home, institution) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    age_at_death_date_of_birth: str = Field(
        ...,
        description=(
            "Age at death and/or date of birth of the deceased .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CauseofDeath(BaseModel):
    """Medical cause of death and related contributing conditions"""

    disease_or_condition_directly_leading_to_death_a: str = Field(
        ...,
        description=(
            "Disease, injury, or complication directly causing death (item a) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    antecedent_causes_due_to_b: str = Field(
        default="",
        description=(
            "Antecedent morbid condition giving rise to cause a) (item b) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    antecedent_causes_due_to_c: str = Field(
        default="",
        description=(
            "Further antecedent morbid condition giving rise to cause a) (item c) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_significant_conditions: str = Field(
        default="",
        description=(
            "Other significant conditions contributing to death but not related to the main "
            'cause .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    interval_between_onset_and_death_a: str = Field(
        default="",
        description=(
            "Time interval between onset of condition a) and death .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    interval_between_onset_and_death_b: str = Field(
        default="",
        description=(
            "Time interval between onset of condition b) and death .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    interval_between_onset_and_death_c: str = Field(
        default="",
        description=(
            "Time interval between onset of condition c) and death .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WorkandIllnessHistory(BaseModel):
    """Information on disability, work cessation, and last illness attendance"""

    unable_to_work_from_onset: str = Field(
        default="",
        description=(
            "Indicate whether the deceased was unable to work from onset of disability and "
            'provide details if applicable .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    when_ceased_working: str = Field(
        default="",
        description=(
            "Date or time when the deceased stopped working, if not from onset of "
            'disability .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date_first_attendance_last_illness_first: str = Field(
        default="", description="First date of medical attendance in the last illness (first entry)"
    )  # YYYY-MM-DD format

    date_first_attendance_last_illness_second: str = Field(
        default="",
        description=(
            "First date of medical attendance in the last illness (second entry, if applicable)"
        ),
    )  # YYYY-MM-DD format


class MannerofDeathandInvestigations(BaseModel):
    """Details on accidental/suicidal/homicidal death, inquest, and autopsy"""

    accident_suicide_homicide_details: str = Field(
        default="",
        description=(
            "Indicate whether death was due to accident, suicide, or homicide and provide a "
            'brief description .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    inquest_held_yes: BooleanLike = Field(
        default="", description="Indicate if an inquest was held (Yes option)"
    )

    inquest_held_no: BooleanLike = Field(
        default="", description="Indicate if an inquest was held (No option)"
    )

    autopsy_performed_yes: BooleanLike = Field(
        default="", description="Indicate if an autopsy was performed (Yes option)"
    )

    autopsy_performed_no: BooleanLike = Field(
        default="", description="Indicate if an autopsy was performed (No option)"
    )

    autopsy_findings: str = Field(
        default="",
        description=(
            "Name of person who performed the autopsy and summary of findings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PriorMedicalTreatment(BaseModel):
    """Treatment history in the three years prior to last illness"""

    treated_advised_last_three_years_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you treated or advised the deceased during the last three years "
            "prior to the last illness (Yes option)"
        ),
    )

    treated_advised_last_three_years_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you treated or advised the deceased during the last three years "
            "prior to the last illness (No option)"
        ),
    )

    other_treatment_last_three_years_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the deceased received treatment from any other physician, "
            "hospital, or institution in the last three years (Yes option)"
        ),
    )

    other_treatment_last_three_years_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the deceased received treatment from any other physician, "
            "hospital, or institution in the last three years (No option)"
        ),
    )

    other_physician_name: str = Field(
        default="",
        description=(
            "Name of the other physician, hospital, or institution .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_physician_address: str = Field(
        default="",
        description=(
            "Address of the other physician, hospital, or institution .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nature_of_illness_or_injury: str = Field(
        default="",
        description=(
            "Nature of the illness or injury for which treatment was received .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    treatment_dates: str = Field(
        default="",
        description=(
            "Dates during which treatment was received .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SmokingHistory(BaseModel):
    """Information about the deceased's smoking habits"""

    smoker_yes: BooleanLike = Field(
        default="",
        description="Indicate if, to your knowledge, the deceased was a smoker (Yes option)",
    )

    smoker_no: BooleanLike = Field(
        default="",
        description="Indicate if, to your knowledge, the deceased was a smoker (No option)",
    )

    smoking_length_of_time: str = Field(
        default="",
        description=(
            "Approximate length of time the deceased smoked .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    smoking_type_cigarettes: BooleanLike = Field(
        default="", description="Check if the deceased smoked cigarettes"
    )

    smoking_type_pipes: BooleanLike = Field(
        default="", description="Check if the deceased smoked a pipe"
    )

    smoking_type_cigars: BooleanLike = Field(
        default="", description="Check if the deceased smoked cigars"
    )


class PhysicianCertification(BaseModel):
    """Certifying physician’s details and signature"""

    physician_date: str = Field(
        ..., description="Date the physician completed and signed this statement"
    )  # YYYY-MM-DD format

    physician_signature: str = Field(
        ...,
        description=(
            'Signature of the attending physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physician_md: str = Field(
        default="",
        description=(
            "Physician’s medical designation (M.D.) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_address: str = Field(
        ...,
        description=(
            "Mailing address of the physician completing this statement .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProofOfDeathPhysiciansStatement(BaseModel):
    """
    PROOF OF DEATH - PHYSICIAN'S STATEMENT

    Note: The Medical certification follows the recommendations of the World Health Assembly made in Geneva on July 24th 1948. It has been accepted by all States in the United States and all Provinces in Canada. In the interest of accurate vital statistics please conform to the International List of the Causes of Death.
    """

    deceased_and_policy_information: DeceasedandPolicyInformation = Field(
        ..., description="Deceased and Policy Information"
    )
    cause_of_death: CauseofDeath = Field(..., description="Cause of Death")
    work_and_illness_history: WorkandIllnessHistory = Field(
        ..., description="Work and Illness History"
    )
    manner_of_death_and_investigations: MannerofDeathandInvestigations = Field(
        ..., description="Manner of Death and Investigations"
    )
    prior_medical_treatment: PriorMedicalTreatment = Field(
        ..., description="Prior Medical Treatment"
    )
    smoking_history: SmokingHistory = Field(..., description="Smoking History")
    physician_certification: PhysicianCertification = Field(
        ..., description="Physician Certification"
    )

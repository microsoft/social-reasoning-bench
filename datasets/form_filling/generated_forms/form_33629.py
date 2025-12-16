from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WithdrawalInformation(BaseModel):
    """Reason for school/university withdrawal"""

    reason_for_withdrawal_accident_injury: BooleanLike = Field(
        ..., description="Select if the reason for withdrawal is due to an accident or injury."
    )

    reason_for_withdrawal_sickness_illness: BooleanLike = Field(
        ..., description="Select if the reason for withdrawal is due to sickness or illness."
    )

    reason_for_withdrawal_mental_nervous_disorder: BooleanLike = Field(
        ...,
        description="Select if the reason for withdrawal is due to a mental or nervous disorder.",
    )


class PartIAccidentInjuryDetails(BaseModel):
    """Details related to accident or injury withdrawals"""

    date_of_accident: str = Field(
        ..., description="Date on which the accident occurred."
    )  # YYYY-MM-DD format

    time_of_accident: str = Field(
        ...,
        description=(
            "Clock time at which the accident occurred. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    time_of_accident_am: BooleanLike = Field(
        ..., description="Check if the accident time is in the morning (a.m.)."
    )

    time_of_accident_pm: BooleanLike = Field(
        ..., description="Check if the accident time is in the afternoon/evening (p.m.)."
    )

    location_of_accident: str = Field(
        ...,
        description=(
            "Physical location where the accident occurred. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_events_leading_to_accident: str = Field(
        ...,
        description=(
            "Detailed description of what happened before and during the accident. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    is_any_other_insurance_involved_yes: BooleanLike = Field(
        ..., description="Check if there is other insurance coverage involved."
    )

    is_any_other_insurance_involved_no: BooleanLike = Field(
        ..., description="Check if there is no other insurance coverage involved."
    )

    was_patient_hospitalized_for_injury_yes: BooleanLike = Field(
        ..., description="Check if the patient was hospitalized due to this injury."
    )

    was_patient_hospitalized_for_injury_no: BooleanLike = Field(
        ..., description="Check if the patient was not hospitalized due to this injury."
    )

    hospital_name_injury: str = Field(
        default="",
        description=(
            "Name of the hospital where the patient was treated for the injury. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    physician_name_and_address_injury: str = Field(
        default="",
        description=(
            "Name and full mailing address of the treating physician for the injury. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    admission_date_injury: str = Field(
        default="", description="Hospital admission date for the injury."
    )  # YYYY-MM-DD format

    discharge_date_injury: str = Field(
        default="", description="Hospital discharge date for the injury."
    )  # YYYY-MM-DD format


class PartIISicknessIllnessorMentalNervousDisorder(BaseModel):
    """Details related to sickness, illness, or mental/nervous disorder withdrawals"""

    describe_your_illness: str = Field(
        ...,
        description=(
            "Description of the illness or mental/nervous disorder. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    when_did_symptoms_first_appear: str = Field(
        ...,
        description=(
            "Date or approximate time when symptoms first began. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    have_you_ever_had_same_or_similar_condition_yes: BooleanLike = Field(
        ..., description="Check if you have previously had the same or a similar condition."
    )

    have_you_ever_had_same_or_similar_condition_no: BooleanLike = Field(
        ..., description="Check if you have not previously had the same or a similar condition."
    )

    when_same_or_similar_condition: str = Field(
        default="",
        description=(
            "Date or time period when the same or similar condition occurred previously. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    were_you_hospitalized_for_this_illness_yes: BooleanLike = Field(
        ..., description="Check if you were hospitalized due to this illness."
    )

    were_you_hospitalized_for_this_illness_no: BooleanLike = Field(
        ..., description="Check if you were not hospitalized due to this illness."
    )

    hospital_name_illness: str = Field(
        default="",
        description=(
            "Name of the hospital where you were treated for the illness. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    physician_name_and_address_illness: str = Field(
        default="",
        description=(
            "Name and full mailing address of the treating physician for the illness. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    admission_date_illness: str = Field(
        default="", description="Hospital admission date for the illness."
    )  # YYYY-MM-DD format

    discharge_date_illness: str = Field(
        default="", description="Hospital discharge date for the illness."
    )  # YYYY-MM-DD format


class SchoolUniversityWithdrawalInformationReleaseNameInsured(BaseModel):
    """
    SCHOOL / UNIVERSITY WITHDRAWAL INFORMATION RELEASE: NAME INSURED

    Must be completed by Student, Parent, Guardian, or other Authorized Representative
    """

    withdrawal_information: WithdrawalInformation = Field(..., description="Withdrawal Information")
    part_i_accidentinjury_details: PartIAccidentInjuryDetails = Field(
        ..., description="Part I: Accident/Injury Details"
    )
    part_ii_sicknessillness_or_mentalnervous_disorder: PartIISicknessIllnessorMentalNervousDisorder = Field(
        ..., description="Part II: Sickness/Illness or Mental/Nervous Disorder"
    )

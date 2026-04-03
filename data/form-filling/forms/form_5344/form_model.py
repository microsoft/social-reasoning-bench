from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EventApplicantInformation(BaseModel):
    """Details about the TIP Challenge event and the adopter/competitor applicant"""

    tip_challenge_event_location: str = Field(
        ...,
        description=(
            "Name or location of the TIP Challenge event .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_adopter_competitor_applicant: str = Field(
        ...,
        description=(
            "Full name of the adopter/competitor applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    adopter_competitor_applicants_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the adopter/competitor applicant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferenceContactInformation(BaseModel):
    """Contact details for the individual providing the reference"""

    name_of_reference: str = Field(
        ...,
        description=(
            "Full name of the person providing the reference .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_phone_1: str = Field(
        ...,
        description=(
            "Primary phone number for the reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_phone_2: str = Field(
        default="",
        description=(
            "Secondary phone number for the reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_email_address: str = Field(
        default="",
        description=(
            'Email address of the reference .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class TrainerEvaluation(BaseModel):
    """Questions and comments evaluating the trainer"""

    how_long_have_you_known_this_trainer: str = Field(
        ...,
        description=(
            "Length of time the reference has known the trainer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_often_do_you_see_this_trainer_ride_or_work_horses: str = Field(
        ...,
        description=(
            "Frequency with which the reference observes the trainer working with horses "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    do_you_feel_that_their_facilities_are_suitable_for_working_with_a_wild_horse: str = Field(
        ...,
        description=(
            "Reference's opinion on whether the trainer's facilities are appropriate for "
            'wild horses .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    do_you_have_any_concerns_about_the_horses_in_the_care_of_this_trainer: str = Field(
        ...,
        description=(
            "Any concerns the reference has about horses under this trainer's care .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    would_you_recommend_this_trainer_to_people_with_unbroken_or_difficult_horses: str = Field(
        ...,
        description=(
            "Explanation of whether the reference would recommend this trainer for unbroken "
            'or difficult horses .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    personal_comments_regarding_skill_work_ethic_values_etc: str = Field(
        default="",
        description=(
            "Additional comments about the trainer's skills, work ethic, values, and "
            'related qualities .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class TrainerReferenceForm(BaseModel):
    """
    TRAINER REFERENCE FORM

    Two Reference Forms must be submitted with each application. If the individual providing the reference would like for the information to remain confidential, please feel free to mail this form directly to the TIP Challenge Manager: Ann Hanlin.
    """

    event__applicant_information: EventApplicantInformation = Field(
        ..., description="Event & Applicant Information"
    )
    reference_contact_information: ReferenceContactInformation = Field(
        ..., description="Reference Contact Information"
    )
    trainer_evaluation: TrainerEvaluation = Field(..., description="Trainer Evaluation")

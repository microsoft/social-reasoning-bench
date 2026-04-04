from pydantic import BaseModel, ConfigDict, Field


class TrainerReferenceForm(BaseModel):
    """TRAINER REFERENCE FORM

    An external trainer or knowledgeable reference completes this form as part of a TIP Challenge
    adopter/competitor application. The TIP Challenge Manager and application reviewers use the
    reference’s observations about the applicant’s horsemanship, facilities, and suitability for
    working with wild/unbroken horses to help decide whether the applicant should be approved to
    participate.
    """

    model_config = ConfigDict(extra="forbid")

    adopter_competitor_applicant_phone: str = Field(
        ...,
        description='Applicant phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    reference_phone_1: str = Field(
        ...,
        description='Reference phone 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    reference_phone_2: str = Field(
        ...,
        description='Reference phone 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    q1_how_long_known_trainer: str = Field(
        ...,
        description='How long known this trainer. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    q2_how_often_see_ride_or_work: str = Field(
        ...,
        description='How often see trainer ride/work horses. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    q3_facilities_suitable_for_wild_horse: str = Field(
        ...,
        description='Facilities suitable for wild horse? If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    q4_concerns_about_horses_in_care: str = Field(
        ...,
        description='Concerns about horses in trainer care. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    q5_recommend_for_unbroken_or_difficult: str = Field(
        ...,
        description='Recommend for unbroken/difficult horses? If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_comments: str = Field(
        ...,
        description='Personal comments (skill, work ethic, values). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
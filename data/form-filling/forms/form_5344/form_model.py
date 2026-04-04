from pydantic import BaseModel, ConfigDict, Field


class TrainerReferenceForm(BaseModel):
    """TRAINER REFERENCE FORM

    A third-party reference provider completes this form to support an adopter/competitor’s TIP Challenge application by describing how well they know the trainer, how often they observe the trainer working horses, and whether the trainer’s facilities and practices are suitable for wild/unbroken horses. The TIP Challenge Manager and application reviewers at the Mustang Heritage Foundation use these responses to assess the applicant’s suitability and risk factors when deciding whether to approve or advance the application.
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
    q2_how_often_see_trainer_work_horses: str = Field(
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
    q5_recommend_for_unbroken_difficult_horses: str = Field(
        ...,
        description='Recommend for unbroken/difficult horses? If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_comments: str = Field(
        ...,
        description='Personal comments on skill/work ethic/values. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
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
    """Basic information about the workshop participant and their organization"""

    name: str = Field(
        ...,
        description=(
            'Full name of the participant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    organization: str = Field(
        ...,
        description=(
            'Name of your organization or employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_position: str = Field(
        ...,
        description=(
            'Your current job title or role .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_address: str = Field(
        ...,
        description=(
            'Street address of your workplace .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of your work address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    province: str = Field(
        ...,
        description=(
            'Province of your work address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal code for your work address")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class TrainingGoalsandExperience(BaseModel):
    """Participant goals, facilitation skills, and experience with Active Parenting programs"""

    please_let_us_know: str = Field(
        default="",
        description=(
            "Additional information you would like to share .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_are_your_goals_for_attending_this_seminar: str = Field(
        default="",
        description=(
            "Describe your goals and expectations for this seminar .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    list_the_facilitation_skills_you_possess_that_will_make_you_an_effective_trainer_leader: str = (
        Field(
            default="",
            description=(
                "List your facilitation skills relevant to being an effective trainer or leader "
                '.If you cannot fill this, write "N/A". If this field should not be filled by '
                "you (for example, it belongs to another person or office), leave it blank "
                '(empty string "").'
            ),
        )
    )

    how_do_you_conduct_parent_classes: Literal[
        "one-on-one", "small group", "large group", "N/A", ""
    ] = Field(
        default="", description="Select the typical format in which you conduct parent classes"
    )

    one_on_one: BooleanLike = Field(
        default="", description="Indicate if you conduct parent classes one-on-one"
    )

    small_group: BooleanLike = Field(
        default="", description="Indicate if you conduct parent classes in small groups"
    )

    large_group: BooleanLike = Field(
        default="", description="Indicate if you conduct parent classes in large groups"
    )

    have_you_attended_an_active_parenting_facilitator_training_workshop_in_the_past: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate whether you have previously attended an Active Parenting Facilitator "
                "Training Workshop"
            ),
        )
    )

    which_active_parenting_programs_have_you_led: str = Field(
        default="",
        description=(
            "List the Active Parenting programs you have previously led .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_many_groups_have_you_led: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of parent groups you have led"
    )

    do_you_have_access_to_active_parenting_program_kits: BooleanLike = Field(
        default="",
        description="Indicate whether you have access to any Active Parenting program kits",
    )

    which_program_best_fits_your_parent_groups: Literal[
        "Coop", "AP4", "Teen", "First Five Years", "N/A", ""
    ] = Field(
        default="",
        description="Select the Active Parenting program that best matches your parent groups",
    )

    coop: BooleanLike = Field(
        default="", description="Indicate if the Coop program best fits your parent groups"
    )

    ap4: BooleanLike = Field(
        default="", description="Indicate if the AP4 program best fits your parent groups"
    )

    teen: BooleanLike = Field(
        default="", description="Indicate if the Teen program best fits your parent groups"
    )

    first_five_years: BooleanLike = Field(
        default="",
        description="Indicate if the First Five Years program best fits your parent groups",
    )


class ParentingWorkshopInfoSummaryPart1(BaseModel):
    """
        Active Parenting Canada

    Training Workshop
    Information Summary Sheet (Part 1)

        Training Workshop Information Summary Sheet (Part 1)
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    training_goals_and_experience: TrainingGoalsandExperience = Field(
        ..., description="Training Goals and Experience"
    )

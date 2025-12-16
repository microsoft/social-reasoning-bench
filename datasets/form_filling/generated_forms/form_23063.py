from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PopulationsTopicsServicedInProcess(BaseModel):
    """Areas of service and instructional topics the faculty member is involved with or interested in"""

    pandemic_health_strategies_for_individuals_families_friends: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    self_care_options_to_maintain_regain_recover: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    dealing_with_grief_loss_of_life_possessions_businesses: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    organizational_dynamics_to_maintain_regain_recover: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    caring_for_the_elderly_at_home_in_institutions_end_of_life: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    choose_health_not_addictions: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    economic_strategist_for_all: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    honor_differences_and_justice: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    help_support_for_military_families: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    front_line_workers_help_and_support: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    connect_with_nature_living_in_the_moment_unified_field_process_greatest_trustable_truth_gtt: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )

    integrative_education_models_parenting_children_teens_adults_challenged_learning_for_all_ages: BooleanLike = Field(
        default="", description="Check if this topic/population is applicable or of interest."
    )


class FacultyInput(BaseModel):
    """Open-ended feedback for administration and the board to consider"""

    comments: str = Field(
        default="",
        description=(
            "Additional comments or input for administration and the board. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    questions: str = Field(
        default="",
        description=(
            "Any questions you would like administration or the board to consider. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reflections: str = Field(
        default="",
        description=(
            "Personal reflections or feedback related to the form topics. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AkamaiUniversityFacultyUpdateForm2021(BaseModel):
    """
        Akamai University
    Faculty Update Form 2021

        Faculty Input: Please take time to add your input for Administration to consider. Please be honest and considerate with recommendations for the Board to consider.
        Past Akamai University Study Participation
        Item No. 4: Akamai University Original Programs of Study Eligibility
        Select the areas of instruction for which your background and training shows your eligibility by typing an ✓ before the appropriate selections. The University will assess your background and preparation and adjust your placement within these Akamai faculty groups. Each program is fully clarified online: http://www.akamaiuniversity.us/degrees.html
    """

    populations__topics_serviced__in_process: PopulationsTopicsServicedInProcess = Field(
        ..., description="Populations & Topics Serviced & In Process"
    )
    faculty_input: FacultyInput = Field(..., description="Faculty Input")

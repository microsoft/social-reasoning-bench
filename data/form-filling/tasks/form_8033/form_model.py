from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PhysicalActivityBeyondPE(BaseModel):
    """Goals and practices related to general physical activity opportunities and environment"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="", description="Indicate that this item is included in the written policy (Yes)."
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate that this item is not included in the written policy (No).",
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="",
        description="Indicate that this item is fully implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Indicate that this item is partially implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="",
        description="Indicate that this item is not implemented in the school building(s).",
    )

    in_addition_to_planned_physical_education_we_offer_activities: BooleanLike = Field(
        default="",
        description=(
            "Check whether this statement about offering additional physical activity "
            "opportunities applies."
        ),
    )

    we_maintain_a_physical_and_social_environment: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school maintains an environment that encourages safe and "
            "enjoyable activity."
        ),
    )

    we_discourage_extended_periods_of_inactivity: BooleanLike = Field(
        default="",
        description="Indicate whether extended periods of student inactivity are discouraged.",
    )

    we_provide_physical_activity_breaks_in_the_classroom: BooleanLike = Field(
        default="", description="Indicate whether classroom physical activity breaks are provided."
    )

    we_offer_before_and_or_after_school_programs_with_physical_activity: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether before and/or after-school programs with physical activity "
            "are offered."
        ),
    )

    we_partner_with_parents_and_community_organizations: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school partners with families and community organizations "
            "to support lifelong physical activity."
        ),
    )

    we_do_not_use_physical_activity_as_punishment: BooleanLike = Field(
        default="",
        description="Indicate whether physical activity is not used as a form of punishment.",
    )

    we_do_not_withhold_physical_activity_as_punishment: BooleanLike = Field(
        default="",
        description="Indicate whether physical activity is not withheld as a form of punishment.",
    )

    we_encourage_walking_and_biking_to_school: BooleanLike = Field(
        default="", description="Indicate whether walking and biking to school are encouraged."
    )

    we_encourage_use_of_physical_activity_facilities_outside_school_hours: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students and families are encouraged to use school physical "
            "activity facilities outside school hours."
        ),
    )

    other_goal_describe_physical_activity: str = Field(
        default="",
        description=(
            "Describe any other physical activity goal not listed above. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notes_on_goals_for_physical_activity: str = Field(
        default="",
        description=(
            "Record notes or comments about the physical activity goals. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PhysicalEducationPE(BaseModel):
    """Goals and practices related specifically to PE curriculum, instruction, and staffing"""

    we_implement_a_pe_program_consistent_with_state_standards: BooleanLike = Field(
        default="",
        description="Indicate whether the PE program is consistent with state academic standards.",
    )

    all_students_participate_in_pe: BooleanLike = Field(
        default="", description="Indicate whether all students participate in PE."
    )

    pe_instruction_promotes_lifelong_physical_activity_skills: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE instruction promotes skills and knowledge for lifelong "
            "physical activity."
        ),
    )

    pe_classes_provide_learning_practice_and_assessment: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE classes allow students to learn, practice, and be assessed "
            "on appropriate skills."
        ),
    )

    our_curriculum_promotes_team_and_individual_activities: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the PE curriculum promotes both team and individual activities."
        ),
    )

    we_offer_a_comprehensive_pe_course_of_study: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a comprehensive PE course of study with sufficient "
            "instruction time is offered."
        ),
    )

    we_use_a_local_assessment_system_for_pe_standards: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a local assessment system is used to track PE progress on "
            "state standards."
        ),
    )

    students_are_moderately_to_vigorously_active_during_pe: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students are kept active during PE and accommodations are "
            "made for medical conditions and disabilities."
        ),
    )

    we_provide_safe_and_adequate_equipment_and_facilities_for_pe: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether safe and adequate equipment, facilities, and resources are "
            "provided for PE."
        ),
    )

    certified_health_and_pe_teachers_teach_our_classes: BooleanLike = Field(
        default="",
        description="Indicate whether certified health and PE teachers teach the classes.",
    )

    we_provide_professional_development_for_pe_staff: BooleanLike = Field(
        default="",
        description="Indicate whether professional development is provided for PE staff.",
    )

    pe_classes_have_appropriate_teacher_student_ratio: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE classes have a teacher-student ratio similar to other courses."
        ),
    )

    we_do_not_use_or_withhold_physical_activity_as_punishment_in_pe: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether physical activity is neither used nor withheld as punishment "
            "in PE class."
        ),
    )

    other_goal_describe_physical_education: str = Field(
        default="",
        description=(
            "Describe any other physical education goal not listed above. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notes_on_goals_for_physical_education: str = Field(
        default="",
        description=(
            "Record notes or comments about the physical education goals. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    physical_activity_beyond_pe: PhysicalActivityBeyondPE = Field(
        ..., description="Physical Activity (Beyond PE)"
    )
    physical_education_pe: PhysicalEducationPE = Field(..., description="Physical Education (PE)")

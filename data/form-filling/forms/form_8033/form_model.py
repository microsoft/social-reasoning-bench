from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PhysicalActivity(BaseModel):
    """Goals and practices related to general physical activity opportunities and environment"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="", description="Check if this item is included in the written wellness policy."
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="", description="Check if this item is not included in the written wellness policy."
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="", description="Check if this item is fully implemented in the school building(s)."
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Check if this item is partially implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="", description="Check if this item is not implemented in the school building(s)."
    )

    in_addition_to_planned_physical_education_we_offer_activities_such_as_indoor_and_outdoor_recess_before_and_after_school_programs_intramurals_interscholastic_athletics_and_clubs_to_meet_the_needs_and_interests_of_our_students: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school offers additional physical activity opportunities "
            "beyond planned PE, such as recess, programs, and clubs."
        ),
    )

    we_maintain_a_physical_and_social_environment_that_encourages_safe_and_enjoyable_activity_for_all_students: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school environment supports safe and enjoyable physical "
            "activity for all students."
        ),
    )

    we_discourage_extended_periods_of_inactivity_two_hours_or_more_for_students: BooleanLike = Field(
        default="",
        description="Indicate whether the school discourages long periods of student inactivity.",
    )

    we_provide_physical_activity_breaks_in_the_classroom: BooleanLike = Field(
        default="", description="Indicate whether classroom physical activity breaks are provided."
    )

    we_offer_before_and_or_after_school_programs_that_include_physical_activity_for_participating_children: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether before/after-school programs with physical activity are offered."
        ),
    )

    we_partner_with_parents_guardians_and_community_members_and_organizations_eg_ymca_boys_girls_clubs_local_parks_hospitals_etc_to_offer_programs_supporting_lifelong_physical_activity: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school partners with families and community organizations "
            "to support lifelong physical activity."
        ),
    )

    we_do_not_use_physical_activity_as_a_punishment_eg_running_laps: BooleanLike = Field(
        default="",
        description="Indicate whether physical activity is not used as a form of punishment.",
    )

    we_do_not_withhold_physical_activity_as_a_punishment_eg_taking_away_recess: BooleanLike = Field(
        default="",
        description="Indicate whether physical activity is not withheld as a form of punishment.",
    )

    we_encourage_walking_and_biking_to_school: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school encourages active transportation such as walking "
            "and biking."
        ),
    )

    we_encourage_students_and_families_to_use_our_physical_activity_facilities_such_as_playgrounds_and_ball_fields_outside_of_school_hours_in_accordance_with_school_rules: BooleanLike = Field(
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
            "Record notes or comments about the physical activity goals and their "
            'implementation. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class PhysicalEducationPE(BaseModel):
    """Goals and practices specific to the PE program and instruction"""

    we_implement_a_pe_program_consistent_with_state_academic_standards: BooleanLike = Field(
        default="",
        description="Indicate whether the PE program aligns with state academic standards.",
    )

    all_students_participate_in_pe: BooleanLike = Field(
        default="", description="Indicate whether all students are required to participate in PE."
    )

    pe_instruction_promotes_skills_and_knowledge_necessary_for_lifelong_physical_activity: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE instruction supports skills and knowledge for lifelong activity."
        ),
    )

    pe_classes_provide_the_means_for_students_to_learn_practice_and_be_assessed_on_developmentally_appropriate_skills: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE classes allow students to learn, practice, and be assessed "
            "on appropriate skills."
        ),
    )

    our_curriculum_promotes_both_team_and_individual_activities: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the PE curriculum includes both team and individual activities."
        ),
    )

    we_offer_a_comprehensive_pe_course_of_study_with_planned_instruction_time_for_students_to_meet_standards_at_the_proficient_level: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a comprehensive PE course of study with sufficient "
            "instructional time is offered."
        ),
    )

    we_use_a_local_assessment_system_to_track_student_progress_on_state_standards: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate whether a local assessment system is used to monitor PE progress on "
                "state standards."
            ),
        )
    )

    students_are_moderately_to_vigorously_active_as_much_time_as_possible_during_pe_class_accommodations_are_made_in_class_for_documented_medical_conditions_and_disabilities: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students are kept active during PE and accommodations are "
            "provided as needed."
        ),
    )

    we_provide_safe_and_adequate_equipment_facilities_and_resources_for_pe_class: BooleanLike = Field(
        default="",
        description="Indicate whether PE has safe and adequate equipment, facilities, and resources.",
    )

    certified_health_and_pe_teachers_teach_our_classes: BooleanLike = Field(
        default="",
        description="Indicate whether PE classes are taught by certified health and PE teachers.",
    )

    we_provide_professional_development_for_pe_staff: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether professional development opportunities are provided for PE staff."
        ),
    )

    pe_classes_have_a_teacher_student_ratio_similar_to_other_courses_for_safe_and_effective_instruction: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether PE class sizes are comparable to other courses for safety and "
            "effectiveness."
        ),
    )

    we_do_not_use_or_withhold_physical_activity_as_a_form_of_punishment_in_pe_class: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate whether physical activity is neither used nor withheld as punishment "
                "in PE."
            ),
        )
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
            "Record notes or comments about the physical education goals and their "
            'implementation. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    physical_activity: PhysicalActivity = Field(..., description="Physical Activity")
    physical_education_pe: PhysicalEducationPE = Field(..., description="Physical Education (PE)")

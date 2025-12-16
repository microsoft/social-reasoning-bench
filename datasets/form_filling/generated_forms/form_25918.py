from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicalQuestions(BaseModel):
    """General medical history and health questions"""

    do_you_cough_wheeze_or_have_difficulty_breathing_during_or_after_exercise_yes: BooleanLike = (
        Field(
            ...,
            description=(
                "Check Yes if you cough, wheeze, or have difficulty breathing during or after "
                "exercise."
            ),
        )
    )

    do_you_cough_wheeze_or_have_difficulty_breathing_during_or_after_exercise_no: BooleanLike = (
        Field(
            ...,
            description=(
                "Check No if you do not cough, wheeze, or have difficulty breathing during or "
                "after exercise."
            ),
        )
    )

    have_you_ever_used_an_inhaler_or_taken_asthma_medicine_yes: BooleanLike = Field(
        ..., description="Check Yes if you have ever used an inhaler or taken asthma medication."
    )

    have_you_ever_used_an_inhaler_or_taken_asthma_medicine_no: BooleanLike = Field(
        ..., description="Check No if you have never used an inhaler or taken asthma medication."
    )

    are_you_missing_a_kidney_an_eye_a_testicle_males_your_spleen_or_any_other_organs_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you are missing a kidney, eye, testicle, spleen, or any other organ."
        ),
    )

    are_you_missing_a_kidney_an_eye_a_testicle_males_your_spleen_or_any_other_organs_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if you are not missing a kidney, eye, testicle, spleen, or any other organ."
        ),
    )

    do_you_have_a_groin_or_testicle_pain_a_bump_a_painful_bulge_or_hernia_in_the_groin_area_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you have groin or testicle pain, a bump, a painful bulge, or a "
            "hernia in the groin area."
        ),
    )

    do_you_have_a_groin_or_testicle_pain_a_bump_a_painful_bulge_or_hernia_in_the_groin_area_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if you do not have groin or testicle pain, a bump, a painful bulge, "
            "or a hernia in the groin area."
        ),
    )

    have_you_had_infectious_mononucleosis_mono_yes: BooleanLike = Field(
        ..., description="Check Yes if you have ever had infectious mononucleosis (mono)."
    )

    have_you_had_infectious_mononucleosis_mono_no: BooleanLike = Field(
        ..., description="Check No if you have never had infectious mononucleosis (mono)."
    )

    do_you_have_any_recurring_skin_rashes_or_skin_infection_including_herpes_or_mrsa_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you have recurring skin rashes or infections, including herpes or MRSA."
        ),
    )

    do_you_have_any_recurring_skin_rashes_or_skin_infection_including_herpes_or_mrsa_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if you do not have recurring skin rashes or infections, including "
            "herpes or MRSA."
        ),
    )

    have_you_had_a_concussion_or_head_injury_that_caused_confusion_a_prolonged_headache_or_memory_problems_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you have had a concussion or head injury with confusion, "
            "prolonged headache, or memory problems."
        ),
    )

    have_you_had_a_concussion_or_head_injury_that_caused_confusion_a_prolonged_headache_or_memory_problems_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if you have not had a concussion or head injury with confusion, "
            "prolonged headache, or memory problems."
        ),
    )

    if_yes_how_many: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "If you answered Yes to having a concussion or head injury, enter how many you "
            "have had."
        ),
    )

    what_is_the_longest_time_it_took_for_full_recovery: str = Field(
        default="",
        description=(
            "If you had a concussion or head injury, describe the longest time it took you "
            'to fully recover. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    when_were_you_last_released: str = Field(
        default="",
        description=(
            "Indicate the date or time when you were last medically released after a "
            'concussion or head injury. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    do_you_have_headaches_with_exercise_yes: BooleanLike = Field(
        ..., description="Check Yes if you experience headaches during or after exercise."
    )

    do_you_have_headaches_with_exercise_no: BooleanLike = Field(
        ..., description="Check No if you do not experience headaches during or after exercise."
    )

    have_you_ever_had_numbness_tingling_weakness_in_your_arms_or_legs_or_been_unable_to_move_them_after_being_hit_or_falling_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you have had numbness, tingling, weakness, or inability to move "
            "arms or legs after being hit or falling."
        ),
    )

    have_you_ever_had_numbness_tingling_weakness_in_your_arms_or_legs_or_been_unable_to_move_them_after_being_hit_or_falling_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if you have not had numbness, tingling, weakness, or inability to "
            "move arms or legs after being hit or falling."
        ),
    )

    have_you_ever_become_ill_while_exercising_in_the_heat_yes: BooleanLike = Field(
        ..., description="Check Yes if you have ever become ill while exercising in hot conditions."
    )

    have_you_ever_become_ill_while_exercising_in_the_heat_no: BooleanLike = Field(
        ..., description="Check No if you have not become ill while exercising in hot conditions."
    )

    do_you_get_frequent_muscle_cramps_when_exercising_yes: BooleanLike = Field(
        ..., description="Check Yes if you frequently get muscle cramps during exercise."
    )

    do_you_get_frequent_muscle_cramps_when_exercising_no: BooleanLike = Field(
        ..., description="Check No if you do not frequently get muscle cramps during exercise."
    )

    do_you_or_does_someone_in_your_family_have_sickle_cell_trait_or_disease_yes: BooleanLike = (
        Field(
            ...,
            description=(
                "Check Yes if you or a family member has sickle cell trait or sickle cell disease."
            ),
        )
    )

    do_you_or_does_someone_in_your_family_have_sickle_cell_trait_or_disease_no: BooleanLike = Field(
        ...,
        description=(
            "Check No if neither you nor a family member has sickle cell trait or sickle "
            "cell disease."
        ),
    )

    have_you_ever_had_or_do_you_have_any_problems_with_your_eyes_or_vision_yes: BooleanLike = Field(
        ...,
        description=(
            "Check Yes if you have ever had or currently have problems with your eyes or vision."
        ),
    )

    have_you_ever_had_or_do_you_have_any_problems_with_your_eyes_or_vision_no: BooleanLike = Field(
        ...,
        description="Check No if you have not had and do not have problems with your eyes or vision.",
    )

    do_you_wear_protective_eyewear_such_as_goggles_or_a_face_shield_yes: BooleanLike = Field(
        default="",
        description="Check Yes if you wear protective eyewear such as goggles or a face shield.",
    )

    do_you_wear_protective_eyewear_such_as_goggles_or_a_face_shield_no: BooleanLike = Field(
        default="",
        description=(
            "Check No if you do not wear protective eyewear such as goggles or a face shield."
        ),
    )

    do_you_worry_about_your_weight_yes: BooleanLike = Field(
        default="", description="Check Yes if you are concerned or worried about your weight."
    )

    do_you_worry_about_your_weight_no: BooleanLike = Field(
        default="", description="Check No if you are not concerned or worried about your weight."
    )

    are_you_trying_to_or_has_anyone_recommended_that_you_gain_or_lose_weight_yes: BooleanLike = (
        Field(
            default="",
            description=(
                "Check Yes if you are trying to change your weight or have been advised to gain "
                "or lose weight."
            ),
        )
    )

    are_you_trying_to_or_has_anyone_recommended_that_you_gain_or_lose_weight_no: BooleanLike = (
        Field(
            default="",
            description=(
                "Check No if you are not trying to change your weight and have not been advised "
                "to do so."
            ),
        )
    )

    are_you_on_a_special_diet_or_do_you_avoid_certain_types_of_foods_or_food_groups_yes: BooleanLike = Field(
        default="",
        description="Check Yes if you follow a special diet or avoid specific foods or food groups.",
    )

    are_you_on_a_special_diet_or_do_you_avoid_certain_types_of_foods_or_food_groups_no: BooleanLike = Field(
        default="",
        description=(
            "Check No if you are not on a special diet and do not avoid specific foods or "
            "food groups."
        ),
    )

    have_you_ever_had_an_eating_disorder_yes: BooleanLike = Field(
        default="",
        description=(
            "Check Yes if you have ever been diagnosed with or experienced an eating disorder."
        ),
    )

    have_you_ever_had_an_eating_disorder_no: BooleanLike = Field(
        default="", description="Check No if you have never had an eating disorder."
    )

    how_do_you_currently_identify_your_gender_m: BooleanLike = Field(
        ..., description="Check this box if you currently identify your gender as male."
    )

    how_do_you_currently_identify_your_gender_f: BooleanLike = Field(
        ..., description="Check this box if you currently identify your gender as female."
    )

    how_do_you_currently_identify_your_gender_other: BooleanLike = Field(
        ...,
        description=(
            "Check this box if you currently identify your gender as something other than "
            "male or female."
        ),
    )


class MentalHealthScreeningPHQ4(BaseModel):
    """Patient Health Questionnaire Version 4 items"""

    feeling_nervous_anxious_or_on_edge_not_at_all: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have not at all felt nervous, anxious, "
            "or on edge."
        ),
    )

    feeling_nervous_anxious_or_on_edge_several_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt nervous, anxious, or on edge "
            "on several days."
        ),
    )

    feeling_nervous_anxious_or_on_edge_over_half_the_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt nervous, anxious, or on edge "
            "on more than half the days."
        ),
    )

    feeling_nervous_anxious_or_on_edge_nearly_every_day: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt nervous, anxious, or on edge "
            "nearly every day."
        ),
    )

    not_being_able_to_stop_or_control_worrying_not_at_all: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have not at all had trouble stopping or "
            "controlling worrying."
        ),
    )

    not_being_able_to_stop_or_control_worrying_several_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had trouble stopping or "
            "controlling worrying on several days."
        ),
    )

    not_being_able_to_stop_or_control_worrying_over_half_the_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had trouble stopping or "
            "controlling worrying on more than half the days."
        ),
    )

    not_being_able_to_stop_or_control_worrying_nearly_every_day: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had trouble stopping or "
            "controlling worrying nearly every day."
        ),
    )

    little_interest_or_pleasure_in_doing_things_not_at_all: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have not at all had little interest or "
            "pleasure in doing things."
        ),
    )

    little_interest_or_pleasure_in_doing_things_several_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had little interest or pleasure in "
            "doing things on several days."
        ),
    )

    little_interest_or_pleasure_in_doing_things_over_half_the_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had little interest or pleasure in "
            "doing things on more than half the days."
        ),
    )

    little_interest_or_pleasure_in_doing_things_nearly_every_day: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have had little interest or pleasure in "
            "doing things nearly every day."
        ),
    )

    feeling_down_depressed_or_hopeless_not_at_all: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have not at all felt down, depressed, "
            "or hopeless."
        ),
    )

    feeling_down_depressed_or_hopeless_several_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt down, depressed, or hopeless "
            "on several days."
        ),
    )

    feeling_down_depressed_or_hopeless_over_half_the_days: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt down, depressed, or hopeless "
            "on more than half the days."
        ),
    )

    feeling_down_depressed_or_hopeless_nearly_every_day: BooleanLike = Field(
        ...,
        description=(
            "Select this if in the last 2 weeks you have felt down, depressed, or hopeless "
            "nearly every day."
        ),
    )


class FemalesOnly(BaseModel):
    """Menstrual history questions for female athletes"""

    have_you_ever_had_a_menstrual_period_yes: BooleanLike = Field(
        default="",
        description="For females only: check Yes if you have ever had a menstrual period.",
    )

    have_you_ever_had_a_menstrual_period_no: BooleanLike = Field(
        default="",
        description="For females only: check No if you have never had a menstrual period.",
    )

    if_yes_are_you_experiencing_any_problems_or_changes_with_athletic_participation_yes: BooleanLike = Field(
        default="",
        description=(
            "For females who have periods: check Yes if you have menstrual problems or "
            "changes affecting athletic participation."
        ),
    )

    if_yes_are_you_experiencing_any_problems_or_changes_with_athletic_participation_no: BooleanLike = Field(
        default="",
        description=(
            "For females who have periods: check No if you are not having menstrual "
            "problems or changes affecting athletic participation."
        ),
    )

    how_old_were_you_when_you_had_your_first_menstrual_period: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Enter your age when you had your first menstrual period (in years).",
        )
    )

    when_was_your_most_recent_menstrual_period: str = Field(
        default="",
        description=(
            "Provide the date or approximate date of your most recent menstrual period. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_many_menstrual_periods_have_you_had_in_the_past_12_months: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Enter the number of menstrual periods you have had in the last 12 months.",
    )


class ExplanationsandSignatures(BaseModel):
    """Space to explain positive answers and provide required signatures"""

    explain_all_yes_answers_here: str = Field(
        default="",
        description=(
            "Provide explanations or details for any questions you answered Yes to. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_of_student_athlete: str = Field(
        ...,
        description=(
            "Signature of the student-athlete attesting that the answers are complete and "
            'correct. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    signature_of_parent_guardian: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian attesting that the answers are complete "
            'and correct. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form was signed.")  # YYYY-MM-DD format


class KshsaaPreparticipationPhysicalEvaluation(BaseModel):
    """
    KSHSAA PRE-PARTICIPATION PHYSICAL EVALUATION

    ''
    """

    medical_questions: MedicalQuestions = Field(..., description="Medical Questions")
    mental_health_screening_phq_4: MentalHealthScreeningPHQ4 = Field(
        ..., description="Mental Health Screening (PHQ-4)"
    )
    females_only: FemalesOnly = Field(..., description="Females Only")
    explanations_and_signatures: ExplanationsandSignatures = Field(
        ..., description="Explanations and Signatures"
    )

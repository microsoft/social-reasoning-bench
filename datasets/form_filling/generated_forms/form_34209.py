from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LaborDeliveryHistory(BaseModel):
    """Details about the child’s birth, delivery setting, interventions, and immediate post-birth status"""

    childs_birth_was_natural_vaginal_birth: BooleanLike = Field(
        default="", description="Select if the child was born via natural vaginal birth"
    )

    childs_birth_was_scheduled_c_section: BooleanLike = Field(
        default="", description="Select if the child was born via scheduled C-section"
    )

    childs_birth_was_emergency_c_section: BooleanLike = Field(
        default="", description="Select if the child was born via emergency C-section"
    )

    at_how_many_weeks_was_your_child_born: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of weeks gestation at the time of birth"
    )

    childs_birth_was_at_home: BooleanLike = Field(
        default="", description="Select if the child was born at home"
    )

    childs_birth_was_at_a_birthing_center: BooleanLike = Field(
        default="", description="Select if the child was born at a birthing center"
    )

    childs_birth_was_at_a_hospital: BooleanLike = Field(
        default="", description="Select if the child was born at a hospital"
    )

    childs_birth_was_other: str = Field(
        default="",
        description=(
            "If other birth location, specify where the child was born .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    doctor_obstetricians_name: str = Field(
        default="",
        description=(
            "Name of the doctor or obstetrician who attended the birth .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    breech: BooleanLike = Field(default="", description="Check if the baby was in breech position")

    induction: BooleanLike = Field(default="", description="Check if labor was induced")

    pain_meds: BooleanLike = Field(
        default="", description="Check if pain medications were used during labor or delivery"
    )

    epidural: BooleanLike = Field(default="", description="Check if an epidural was used")

    episiotomy: BooleanLike = Field(default="", description="Check if an episiotomy was performed")

    vacuum_extraction: BooleanLike = Field(
        default="", description="Check if vacuum extraction was used"
    )

    forceps: BooleanLike = Field(
        default="", description="Check if forceps were used during delivery"
    )

    other_interventions_or_complications: str = Field(
        default="",
        description=(
            "Describe any other interventions or complications during labor or delivery .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_concerns_or_notable_remarks_about_your_childs_labor_and_or_delivery: str = Field(
        default="",
        description=(
            "Any additional concerns or notable details about the child’s labor and "
            'delivery .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    childs_birth_weight_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Child’s birth weight in pounds"
    )

    childs_birth_weight_oz: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Child’s birth weight in ounces"
    )

    childs_birth_height_in: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Child’s birth length/height in inches"
    )

    apgar_score_at_birth: Union[float, Literal["N/A", ""]] = Field(
        default="", description="APGAR score immediately after birth"
    )

    apgar_score_after_5_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="APGAR score five minutes after birth"
    )


class GrowthDevelopmentHistory(BaseModel):
    """Feeding history, developmental milestones, medical history, behavior, and lifestyle"""

    is_was_your_child_breastfed_yes: BooleanLike = Field(
        default="", description="Select if the child was or is breastfed"
    )

    is_was_your_child_breastfed_no: BooleanLike = Field(
        default="", description="Select if the child was not breastfed"
    )

    if_yes_how_long_breastfeeding: str = Field(
        default="",
        description=(
            "Duration of breastfeeding (e.g., in months or years) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    difficulty_with_breastfeeding_yes: BooleanLike = Field(
        default="", description="Select if there were difficulties with breastfeeding"
    )

    difficulty_with_breastfeeding_no: BooleanLike = Field(
        default="", description="Select if there were no difficulties with breastfeeding"
    )

    did_they_ever_use_formula_yes: BooleanLike = Field(
        default="", description="Select if the child has ever used formula"
    )

    did_they_ever_use_formula_no: BooleanLike = Field(
        default="", description="Select if the child has never used formula"
    )

    if_yes_at_what_age_formula: str = Field(
        default="",
        description=(
            "Age at which formula was first introduced .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    if_yes_what_type_formula: str = Field(
        default="",
        description=(
            'Type or brand of formula used .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    colic_reflux_or_constipation_as_an_infant_yes: BooleanLike = Field(
        default="",
        description="Select if the child suffered from colic, reflux, or constipation as an infant",
    )

    colic_reflux_or_constipation_as_an_infant_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the child did not suffer from colic, reflux, or constipation as an infant"
        ),
    )

    if_yes_please_explain_colic_reflux_constipation: str = Field(
        default="",
        description=(
            "Provide details about the child’s colic, reflux, or constipation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    frequently_arch_neck_back_feel_stiff_or_bang_head_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the child frequently arches their neck/back, feels stiff, or bangs "
            "their head"
        ),
    )

    frequently_arch_neck_back_feel_stiff_or_bang_head_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the child does not frequently arch their neck/back, feel stiff, or "
            "bang their head"
        ),
    )

    if_yes_please_explain_arch_stiff_head_banging: str = Field(
        default="",
        description=(
            "Provide details about the child arching, stiffness, or head banging .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    age_child_responded_to_sound: str = Field(
        default="",
        description=(
            "Age at which the child first responded to sound .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_followed_an_object: str = Field(
        default="",
        description=(
            "Age at which the child first followed an object with their eyes .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    age_child_held_their_head_up: str = Field(
        default="",
        description=(
            "Age at which the child first held their head up .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_vocalized: str = Field(
        default="",
        description=(
            "Age at which the child first vocalized (cooing, babbling, etc.) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    age_child_teethed: str = Field(
        default="",
        description=(
            "Age at which the child first began teething .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_sat_alone: str = Field(
        default="",
        description=(
            "Age at which the child first sat without support .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_crawled: str = Field(
        default="",
        description=(
            'Age at which the child first crawled .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    age_child_walked: str = Field(
        default="",
        description=(
            "Age at which the child first walked independently .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_began_cows_milk: str = Field(
        default="",
        description=(
            "Age at which the child first began drinking cow’s milk .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age_child_began_solid_foods: str = Field(
        default="",
        description=(
            "Age at which the child first began eating solid foods .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    food_intolerance_or_allergies_and_when_they_began: str = Field(
        default="",
        description=(
            "List any food intolerances or allergies and the age or time they began .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    childs_hospitalization_and_surgical_history_including_the_year: str = Field(
        default="",
        description=(
            "List all hospitalizations and surgeries the child has had, including the year "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    major_injuries_accidents_falls_and_or_fractures_and_year: str = Field(
        default="",
        description=(
            "List any major injuries, accidents, falls, or fractures and the year they "
            'occurred .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    have_you_chosen_to_vaccinate_your_child_no: BooleanLike = Field(
        default="", description="Select if you have chosen not to vaccinate your child"
    )

    have_you_chosen_to_vaccinate_your_child_yes_on_a_delayed_or_selective_schedule: BooleanLike = (
        Field(
            default="",
            description="Select if your child is vaccinated on a delayed or selective schedule",
        )
    )

    have_you_chosen_to_vaccinate_your_child_yes_on_schedule: BooleanLike = Field(
        default="", description="Select if your child is vaccinated on the standard schedule"
    )

    vaccination_reactions: str = Field(
        default="",
        description=(
            "List any reactions your child has had to vaccinations .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    has_your_child_received_any_antibiotics_yes: BooleanLike = Field(
        default="", description="Select if your child has received antibiotics"
    )

    has_your_child_received_any_antibiotics_no: BooleanLike = Field(
        default="", description="Select if your child has never received antibiotics"
    )

    if_yes_how_many_times_and_list_reason_antibiotics: str = Field(
        default="",
        description=(
            "Number of antibiotic courses and the reasons they were prescribed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    night_terrors_or_difficulty_sleeping_yes: BooleanLike = Field(
        default="", description="Select if the child has night terrors or difficulty sleeping"
    )

    night_terrors_or_difficulty_sleeping_no: BooleanLike = Field(
        default="",
        description="Select if the child does not have night terrors or difficulty sleeping",
    )

    if_yes_please_explain_night_terrors_difficulty_sleeping: str = Field(
        default="",
        description=(
            "Provide details about the child’s night terrors or sleep difficulties .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    behavioral_social_or_emotional_issues_yes: BooleanLike = Field(
        default="", description="Select if the child has behavioral, social, or emotional issues"
    )

    behavioral_social_or_emotional_issues_no: BooleanLike = Field(
        default="",
        description="Select if the child does not have behavioral, social, or emotional issues",
    )

    if_yes_please_explain_behavioral_social_emotional_issues: str = Field(
        default="",
        description=(
            "Provide details about any behavioral, social, or emotional issues .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hours_per_day_child_spends_watching_tv_computer_tablet_or_phone: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="", description="Approximate number of hours per day the child spends on screens"
    )

    how_would_you_describe_your_childs_diet_mostly_whole_organic_foods: BooleanLike = Field(
        default="", description="Select if the child’s diet is mostly whole, organic foods"
    )

    how_would_you_describe_your_childs_diet_pretty_average: BooleanLike = Field(
        default="", description="Select if the child’s diet is pretty average"
    )

    how_would_you_describe_your_childs_diet_high_amount_of_processed_foods: BooleanLike = Field(
        default="",
        description="Select if the child’s diet includes a high amount of processed foods",
    )


class AcknowledgementConsent(BaseModel):
    """Signature and date for consent/acknowledgement"""

    patient_signature: str = Field(
        ...,
        description=(
            "Signature of the patient or parent/guardian acknowledging and consenting .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the acknowledgement and consent was signed"
    )  # YYYY-MM-DD format


class LaborDeliveryHistory(BaseModel):
    """LABOR & DELIVERY HISTORY"""

    labor__delivery_history: LaborDeliveryHistory = Field(
        ..., description="Labor & Delivery History"
    )
    growth__development_history: GrowthDevelopmentHistory = Field(
        ..., description="Growth & Development History"
    )
    acknowledgement__consent: AcknowledgementConsent = Field(
        ..., description="Acknowledgement & Consent"
    )

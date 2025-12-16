from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ConfidentialPatientInformation(BaseModel):
    """Basic identifying and contact information for the child and parent/guardian"""

    childs_name: str = Field(
        ...,
        description=(
            'Child\'s full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_names: str = Field(
        ...,
        description=(
            "Full name(s) of parent(s) or legal guardian(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            "Street address of the child's primary residence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the child\'s primary residence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the child's primary residence")

    zip: str = Field(..., description="ZIP code of the child's primary residence")

    cell_phone: str = Field(
        ...,
        description=(
            'Primary cell phone number for contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Home phone number, if available .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            "Work phone number for parent/guardian, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for communication .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    childs_ss: str = Field(default="", description="Child's Social Security Number")

    birthdate: str = Field(..., description="Child's date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Child's age in years")

    how_did_you_hear_about_us: str = Field(
        default="",
        description=(
            "Describe how you learned about this office (e.g., referral, online, "
            'advertisement) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    height_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Child's height in feet"
    )

    height_in: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Additional inches for child's height"
    )

    weight_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Child's weight in pounds"
    )

    primary_care_physician: str = Field(
        default="",
        description=(
            "Name of the child's primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    receiving_care_from_other_health_professionals_yes: BooleanLike = Field(
        default="",
        description="Check if the child is currently receiving care from other health professionals",
    )

    receiving_care_from_other_health_professionals_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the child is not currently receiving care from other health professionals"
        ),
    )

    other_health_professionals_names_and_specialty: str = Field(
        default="",
        description=(
            "List the names and specialties of any other health professionals currently "
            'caring for the child .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_medications_and_supplements: str = Field(
        default="",
        description=(
            "List all medications, vitamins, herbs, and other supplements the child is "
            'currently taking .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class CurrentHealthConditions(BaseModel):
    """Details about the child’s current health concerns and symptoms"""

    current_health_conditions: str = Field(
        ...,
        description=(
            "Describe the health concerns or symptoms prompting this chiropractic "
            'evaluation .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    condition_onset_date: str = Field(
        default="",
        description=(
            "Approximate date or age when the condition first started .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    problem_start_suddenly: BooleanLike = Field(
        default="", description="Select if the problem started suddenly"
    )

    problem_start_gradually: BooleanLike = Field(
        default="", description="Select if the problem started gradually"
    )

    problem_start_post_injury: BooleanLike = Field(
        default="", description="Select if the problem started after an injury"
    )

    prior_care_for_condition_yes: BooleanLike = Field(
        default="", description="Check if the child has previously received care for this condition"
    )

    prior_care_for_condition_no: BooleanLike = Field(
        default="",
        description="Check if the child has not previously received care for this condition",
    )

    prior_care_for_condition_explanation: str = Field(
        default="",
        description=(
            "Explain what prior care the child has received for this condition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    condition_getting_worse: BooleanLike = Field(
        default="", description="Select if the condition is getting worse"
    )

    condition_improving: BooleanLike = Field(
        default="", description="Select if the condition is improving"
    )

    condition_intermittent: BooleanLike = Field(
        default="", description="Select if the condition is intermittent"
    )

    condition_constant: BooleanLike = Field(
        default="", description="Select if the condition is constant"
    )

    condition_unsure: BooleanLike = Field(
        default="", description="Select if you are unsure about the condition's pattern"
    )

    what_makes_problem_better: str = Field(
        default="",
        description=(
            "Describe anything that improves or relieves the problem .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_makes_problem_worse: str = Field(
        default="",
        description=(
            "Describe anything that worsens or aggravates the problem .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HealthGoalsforYourChild(BaseModel):
    """Desired outcomes and goals for chiropractic care"""

    top_health_goal_1: str = Field(
        default="",
        description=(
            "First primary health goal for your child .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    top_health_goal_2: str = Field(
        default="",
        description=(
            "Second primary health goal for your child .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    top_health_goal_3: str = Field(
        default="",
        description=(
            "Third primary health goal for your child .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    gain_from_chiropractic_resolve_existing_condition: BooleanLike = Field(
        default="", description="Select if your goal is to resolve an existing condition"
    )

    gain_from_chiropractic_overall_wellness: BooleanLike = Field(
        default="", description="Select if your goal is overall wellness"
    )

    gain_from_chiropractic_both: BooleanLike = Field(
        default="",
        description=(
            "Select if your goal is both resolving an existing condition and overall wellness"
        ),
    )

    visited_chiropractor_yes: BooleanLike = Field(
        default="", description="Check if the child has previously visited a chiropractor"
    )

    visited_chiropractor_no: BooleanLike = Field(
        default="", description="Check if the child has never visited a chiropractor"
    )

    prior_chiropractor_name: str = Field(
        default="",
        description=(
            "Name of the chiropractor previously visited .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chiropractor_specialty_pain_relief: BooleanLike = Field(
        default="", description="Select if the chiropractor's specialty is pain relief"
    )

    chiropractor_specialty_physical_therapy_rehab: BooleanLike = Field(
        default="",
        description="Select if the chiropractor's specialty is physical therapy and rehabilitation",
    )

    chiropractor_specialty_nutritional: BooleanLike = Field(
        default="", description="Select if the chiropractor's specialty is nutritional care"
    )

    chiropractor_specialty_subluxation_based: BooleanLike = Field(
        default="", description="Select if the chiropractor's specialty is subluxation-based care"
    )

    chiropractor_specialty_other: str = Field(
        default="",
        description=(
            "Describe any other specialty of the chiropractor .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PregnancyFertilityHistory(BaseModel):
    """Information about fertility, pregnancy, and prenatal factors"""

    fertility_issues_yes: BooleanLike = Field(
        default="", description="Check if there were any fertility issues"
    )

    fertility_issues_no: BooleanLike = Field(
        default="", description="Check if there were no fertility issues"
    )

    fertility_issues_explanation: str = Field(
        default="",
        description=(
            "Explain any fertility issues experienced .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mother_smoke_yes: BooleanLike = Field(
        default="", description="Check if the mother smoked during pregnancy"
    )

    mother_smoke_no: BooleanLike = Field(
        default="", description="Check if the mother did not smoke during pregnancy"
    )

    mother_smoke_per_week: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of cigarettes or smoking instances per week during pregnancy",
    )

    mother_drink_yes: BooleanLike = Field(
        default="", description="Check if the mother drank alcohol during pregnancy"
    )

    mother_drink_no: BooleanLike = Field(
        default="", description="Check if the mother did not drink alcohol during pregnancy"
    )

    mother_drink_per_week: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of alcoholic drinks per week during pregnancy"
    )

    mother_exercise_yes: BooleanLike = Field(
        default="", description="Check if the mother exercised during pregnancy"
    )

    mother_exercise_no: BooleanLike = Field(
        default="", description="Check if the mother did not exercise during pregnancy"
    )

    mother_exercise_explanation: str = Field(
        default="",
        description=(
            "Describe the type and frequency of exercise during pregnancy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    mother_ill_yes: BooleanLike = Field(
        default="", description="Check if the mother experienced illness during pregnancy"
    )

    mother_ill_no: BooleanLike = Field(
        default="", description="Check if the mother did not experience illness during pregnancy"
    )

    mother_ill_explanation: str = Field(
        default="",
        description=(
            "Describe any illnesses the mother experienced during pregnancy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    any_ultrasounds_yes: BooleanLike = Field(
        default="", description="Check if any ultrasounds were performed during pregnancy"
    )

    any_ultrasounds_no: BooleanLike = Field(
        default="", description="Check if no ultrasounds were performed during pregnancy"
    )

    any_ultrasounds_explanation: str = Field(
        default="",
        description=(
            "Provide details about any ultrasounds performed during pregnancy .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    pregnancy_stress_episodes: str = Field(
        default="",
        description=(
            "Describe any significant mental or physical stress experienced during "
            'pregnancy .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other_concerns_conception_pregnancy: str = Field(
        default="",
        description=(
            "Share any additional concerns or important details about conception or "
            'pregnancy .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PediatricPatientQuestionnaire(BaseModel):
    """
    Pediatric Patient Questionnaire

    ''
    """

    confidential_patient_information: ConfidentialPatientInformation = Field(
        ..., description="Confidential Patient Information"
    )
    current_health_conditions: CurrentHealthConditions = Field(
        ..., description="Current Health Conditions"
    )
    health_goals_for_your_child: HealthGoalsforYourChild = Field(
        ..., description="Health Goals for Your Child"
    )
    pregnancy__fertility_history: PregnancyFertilityHistory = Field(
        ..., description="Pregnancy & Fertility History"
    )

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientVisitInformation(BaseModel):
    """Basic identifying information and reason for visit"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this dental history form is completed"
    )  # YYYY-MM-DD format

    what_would_you_like_to_address: str = Field(
        default="",
        description=(
            "Main dental concerns or issues you would like the dentist to address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_last_dental_exam: str = Field(
        default="", description="Approximate date of your most recent dental examination"
    )  # YYYY-MM-DD format

    previous_dentist: str = Field(
        default="",
        description=(
            'Name of your previous dentist .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    any_previous_major_dental_treatment: BooleanLike = Field(
        default="",
        description="Indicates whether you have had any major dental treatment in the past",
    )

    any_previous_major_dental_treatment_yes: BooleanLike = Field(
        default="", description="Check if you have had previous major dental treatment"
    )

    any_previous_major_dental_treatment_no: BooleanLike = Field(
        default="", description="Check if you have not had previous major dental treatment"
    )

    any_previous_major_dental_treatment_when: str = Field(
        default="",
        description=(
            "When the major dental treatment occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    any_previous_major_dental_treatment_why: str = Field(
        default="",
        description=(
            'Reason for the major dental treatment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DentalConditionsSymptoms(BaseModel):
    """Current and past dental issues, habits, and treatments"""

    teeth_sensitive_to_brushing_or_flossing_yes: BooleanLike = Field(
        default="", description="Check if your teeth are sensitive when brushing or flossing"
    )

    teeth_sensitive_to_brushing_or_flossing_no: BooleanLike = Field(
        default="", description="Check if your teeth are not sensitive when brushing or flossing"
    )

    bleeding_gums_since_when_yes: BooleanLike = Field(
        default="", description="Check if you have bleeding gums"
    )

    bleeding_gums_since_when_no: BooleanLike = Field(
        default="", description="Check if you do not have bleeding gums"
    )

    food_stuck_between_teeth_yes: BooleanLike = Field(
        default="", description="Check if food frequently gets stuck between your teeth"
    )

    food_stuck_between_teeth_no: BooleanLike = Field(
        default="", description="Check if food does not frequently get stuck between your teeth"
    )

    clenching_or_grinding_teeth_yes: BooleanLike = Field(
        default="", description="Check if you clench or grind your teeth"
    )

    clenching_or_grinding_teeth_no: BooleanLike = Field(
        default="", description="Check if you do not clench or grind your teeth"
    )

    burning_of_tongue_yes: BooleanLike = Field(
        default="", description="Check if you experience burning sensations of the tongue"
    )

    burning_of_tongue_no: BooleanLike = Field(
        default="", description="Check if you do not experience burning sensations of the tongue"
    )

    swelling_or_lumps_in_mouth_yes: BooleanLike = Field(
        default="", description="Check if you have swelling or lumps in your mouth"
    )

    swelling_or_lumps_in_mouth_no: BooleanLike = Field(
        default="", description="Check if you do not have swelling or lumps in your mouth"
    )

    frequent_blisters_on_lips_or_mouth_yes: BooleanLike = Field(
        default="", description="Check if you frequently get blisters on your lips or in your mouth"
    )

    frequent_blisters_on_lips_or_mouth_no: BooleanLike = Field(
        default="",
        description="Check if you do not frequently get blisters on your lips or in your mouth",
    )

    pain_around_ear_yes: BooleanLike = Field(
        default="", description="Check if you experience pain around your ear"
    )

    pain_around_ear_no: BooleanLike = Field(
        default="", description="Check if you do not experience pain around your ear"
    )

    unusual_sounds_in_ear_while_eating_yes: BooleanLike = Field(
        default="", description="Check if you notice unusual sounds in your ear while eating"
    )

    unusual_sounds_in_ear_while_eating_no: BooleanLike = Field(
        default="", description="Check if you do not notice unusual sounds in your ear while eating"
    )

    teeth_sensitive_to_hot_yes: BooleanLike = Field(
        default="", description="Check if your teeth are sensitive to hot temperatures"
    )

    teeth_sensitive_to_hot_no: BooleanLike = Field(
        default="", description="Check if your teeth are not sensitive to hot temperatures"
    )

    teeth_sensitive_to_cold_yes: BooleanLike = Field(
        default="", description="Check if your teeth are sensitive to cold temperatures"
    )

    teeth_sensitive_to_cold_no: BooleanLike = Field(
        default="", description="Check if your teeth are not sensitive to cold temperatures"
    )

    teeth_sensitive_to_sweets_yes: BooleanLike = Field(
        default="", description="Check if your teeth are sensitive to sweet foods or drinks"
    )

    teeth_sensitive_to_sweets_no: BooleanLike = Field(
        default="", description="Check if your teeth are not sensitive to sweet foods or drinks"
    )

    teeth_sensitive_to_pressure_yes: BooleanLike = Field(
        default="",
        description="Check if your teeth are sensitive to pressure (e.g., biting or chewing)",
    )

    teeth_sensitive_to_pressure_no: BooleanLike = Field(
        default="", description="Check if your teeth are not sensitive to pressure"
    )

    bad_breath_yes: BooleanLike = Field(
        default="", description="Check if you experience bad breath"
    )

    bad_breath_no: BooleanLike = Field(
        default="", description="Check if you do not experience bad breath"
    )

    unpleasant_taste_yes: BooleanLike = Field(
        default="", description="Check if you frequently notice an unpleasant taste in your mouth"
    )

    unpleasant_taste_no: BooleanLike = Field(
        default="",
        description="Check if you do not frequently notice an unpleasant taste in your mouth",
    )

    unfavorable_dental_experiences_yes: BooleanLike = Field(
        default="", description="Check if you have had unfavorable or negative dental experiences"
    )

    unfavorable_dental_experiences_no: BooleanLike = Field(
        default="",
        description="Check if you have not had unfavorable or negative dental experiences",
    )

    complication_from_extractions_yes: BooleanLike = Field(
        default="", description="Check if you have had complications from tooth extractions"
    )

    complication_from_extractions_no: BooleanLike = Field(
        default="", description="Check if you have not had complications from tooth extractions"
    )

    periodontal_treatment_yes: BooleanLike = Field(
        default="", description="Check if you have received periodontal (gum) treatment"
    )

    periodontal_treatment_no: BooleanLike = Field(
        default="", description="Check if you have not received periodontal (gum) treatment"
    )

    orthodontic_treatment_yes: BooleanLike = Field(
        default="",
        description="Check if you have had orthodontic treatment (braces, aligners, etc.)",
    )

    orthodontic_treatment_no: BooleanLike = Field(
        default="", description="Check if you have not had orthodontic treatment"
    )

    mouth_breathing_yes: BooleanLike = Field(
        default="", description="Check if you habitually breathe through your mouth"
    )

    mouth_breathing_no: BooleanLike = Field(
        default="", description="Check if you do not habitually breathe through your mouth"
    )

    oral_habits_fingernail_biting_cheek_biting_etc_yes: BooleanLike = Field(
        default="", description="Check if you have oral habits such as fingernail or cheek biting"
    )

    oral_habits_fingernail_biting_cheek_biting_etc_no: BooleanLike = Field(
        default="",
        description="Check if you do not have oral habits such as fingernail or cheek biting",
    )

    tender_or_swollen_gums_yes: BooleanLike = Field(
        default="", description="Check if your gums are often tender or swollen"
    )

    tender_or_swollen_gums_no: BooleanLike = Field(
        default="", description="Check if your gums are not often tender or swollen"
    )

    dentures_yes: BooleanLike = Field(
        default="", description="Check if you currently wear dentures"
    )

    dentures_no: BooleanLike = Field(
        default="", description="Check if you do not currently wear dentures"
    )

    many_cavities_yes: BooleanLike = Field(
        default="", description="Check if you have had many dental cavities"
    )

    many_cavities_no: BooleanLike = Field(
        default="", description="Check if you have not had many dental cavities"
    )

    many_fillings_yes: BooleanLike = Field(
        default="", description="Check if you have many dental fillings"
    )

    many_fillings_no: BooleanLike = Field(
        default="", description="Check if you do not have many dental fillings"
    )

    cigarettes_pipe_or_cigar_smoking_yes: BooleanLike = Field(
        default="", description="Check if you smoke cigarettes, a pipe, or cigars"
    )

    cigarettes_pipe_or_cigar_smoking_no: BooleanLike = Field(
        default="", description="Check if you do not smoke cigarettes, a pipe, or cigars"
    )

    bleeding_gums_when_brushing_or_flossing_yes: BooleanLike = Field(
        default="", description="Check if your gums bleed when you brush or floss"
    )

    bleeding_gums_when_brushing_or_flossing_no: BooleanLike = Field(
        default="", description="Check if your gums do not bleed when you brush or floss"
    )

    lose_or_break_fillings_easily_yes: BooleanLike = Field(
        default="", description="Check if you tend to lose or break dental fillings easily"
    )

    lose_or_break_fillings_easily_no: BooleanLike = Field(
        default="", description="Check if you do not tend to lose or break dental fillings easily"
    )

    gag_easily_yes: BooleanLike = Field(
        default="", description="Check if you gag easily during dental procedures"
    )

    gag_easily_no: BooleanLike = Field(
        default="", description="Check if you do not gag easily during dental procedures"
    )

    preventative_dentistry_yes: BooleanLike = Field(
        default="", description="Indicates interest or history in preventative dentistry"
    )

    preventative_dentistry_no: BooleanLike = Field(
        default="", description="Indicates no interest or history in preventative dentistry"
    )

    chew_on_one_side_of_the_mouth_yes: BooleanLike = Field(
        default="", description="Check if you usually chew on only one side of your mouth"
    )

    chew_on_one_side_of_the_mouth_no: BooleanLike = Field(
        default="", description="Check if you do not usually chew on only one side of your mouth"
    )


class HomeCarePreventivePractices(BaseModel):
    """Oral hygiene tools, frequency of use, and preventive preferences"""

    toothbrush_how_often: str = Field(
        default="",
        description=(
            'How often you brush your teeth .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dental_floss_how_often: str = Field(
        default="",
        description=(
            'How often you use dental floss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    inter_dental_stimulators_how_often: str = Field(
        default="",
        description=(
            "How often you use inter-dental stimulators .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    water_jet_device_how_often: str = Field(
        default="",
        description=(
            "How often you use a water jet device (oral irrigator) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disclosing_tables_or_solution_how_often: str = Field(
        default="",
        description=(
            "How often you use disclosing tablets or solution .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fluoride_supplements_how_often: str = Field(
        default="",
        description=(
            "How often you take fluoride supplements .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mouthwash_how_often: str = Field(
        default="",
        description=(
            'How often you use mouthwash .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    what_type_of_toothbrush_do_you_use_soft: BooleanLike = Field(
        default="", description="Select if you use a soft toothbrush"
    )

    what_type_of_toothbrush_do_you_use_medium: BooleanLike = Field(
        default="", description="Select if you use a medium toothbrush"
    )

    what_type_of_toothbrush_do_you_use_hard: BooleanLike = Field(
        default="", description="Select if you use a hard toothbrush"
    )

    what_type_of_toothbrush_do_you_use_nylon: BooleanLike = Field(
        default="", description="Select if your toothbrush bristles are nylon"
    )

    what_type_of_toothbrush_do_you_use_natural: BooleanLike = Field(
        default="", description="Select if your toothbrush bristles are natural"
    )

    do_you_want_a_fluoride_supplement_yes: BooleanLike = Field(
        default="", description="Indicates that you would like to receive a fluoride supplement"
    )

    do_you_want_a_fluoride_supplement_no: BooleanLike = Field(
        default="", description="Indicates that you do not want to receive a fluoride supplement"
    )

    do_you_want_to_be_taught_preventative_dental_hygiene_yes: BooleanLike = Field(
        default="", description="Indicates that you want instruction in preventative dental hygiene"
    )

    do_you_want_to_be_taught_preventative_dental_hygiene_no: BooleanLike = Field(
        default="",
        description="Indicates that you do not want instruction in preventative dental hygiene",
    )

    are_you_unusually_nervous_about_dental_visits_yes: BooleanLike = Field(
        default="", description="Indicates that you feel unusually nervous about dental visits"
    )

    are_you_unusually_nervous_about_dental_visits_no: BooleanLike = Field(
        default="",
        description="Indicates that you do not feel unusually nervous about dental visits",
    )

    do_you_want_to_save_your_remaining_teeth_yes: BooleanLike = Field(
        default="", description="Indicates that you want to preserve your remaining natural teeth"
    )

    do_you_want_to_save_your_remaining_teeth_no: BooleanLike = Field(
        default="",
        description="Indicates that you do not wish to preserve your remaining natural teeth",
    )


class AdditionalComments(BaseModel):
    """Space for any other information the patient wishes to add"""

    is_there_anything_you_would_like_to_add_line_1: str = Field(
        default="",
        description=(
            "Additional comments or information (first line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    is_there_anything_you_would_like_to_add_line_2: str = Field(
        default="",
        description=(
            "Additional comments or information (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DentalHistory(BaseModel):
    """
    DENTAL HISTORY

    ''
    """

    patient__visit_information: PatientVisitInformation = Field(
        ..., description="Patient & Visit Information"
    )
    dental_conditions__symptoms: DentalConditionsSymptoms = Field(
        ..., description="Dental Conditions & Symptoms"
    )
    home_care__preventive_practices: HomeCarePreventivePractices = Field(
        ..., description="Home Care & Preventive Practices"
    )
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")

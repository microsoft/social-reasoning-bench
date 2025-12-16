from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OfficeUseOnly(BaseModel):
    """For office use only identifiers and date"""

    patient_id: str = Field(
        ...,
        description=(
            "Internal patient identification number assigned by the office .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_office_use: str = Field(
        ..., description="Date this form is completed for office use"
    )  # YYYY-MM-DD format


class PatientInformation(BaseModel):
    """Basic patient details and referring information"""

    date_questionnaire: str = Field(
        ..., description="Date of completing this patient questionnaire"
    )  # YYYY-MM-DD format

    name: str = Field(
        ...,
        description=(
            'Patient\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    school_at: str = Field(
        default="",
        description=(
            "Name of school or athletic trainer (AT), if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Patient\'s home telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            'Patient\'s work telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Patient\'s mobile/cell phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    primary_care_doctor: str = Field(
        default="",
        description=(
            "Name of the patient's primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    last_visit_with_pcp: str = Field(
        default="", description="Approximate date of the last visit with primary care provider"
    )  # YYYY-MM-DD format

    who_referred_you: str = Field(
        default="",
        description=(
            "Name of the person or provider who referred you to this office .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    shoe_size: str = Field(
        default="",
        description=(
            'Patient\'s usual shoe size .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    height: str = Field(
        default="",
        description=(
            "Patient's height (include units, e.g., feet/inches or cm) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight (specify units, e.g., pounds or kg)"
    )


class PastIllnesses(BaseModel):
    """Past medical conditions and diabetes details"""

    last_hba1c: str = Field(
        default="",
        description=(
            "Most recent hemoglobin A1C value, if diabetic .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    blood_sugar_this_morning: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Blood glucose level measured this morning, if applicable"
    )


class PastSurgeries(BaseModel):
    """History of past surgeries with dates and physicians"""

    surgery_1: str = Field(
        default="",
        description=(
            "Name or description of past surgery (first entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_past_surgeries_1: str = Field(
        default="",
        description=(
            "Approximate date or age at time of surgery (first entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_past_surgeries_1: str = Field(
        default="",
        description=(
            "Physician who performed the surgery (first entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_2: str = Field(
        default="",
        description=(
            "Name or description of past surgery (second entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_past_surgeries_2: str = Field(
        default="",
        description=(
            "Approximate date or age at time of surgery (second entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_past_surgeries_2: str = Field(
        default="",
        description=(
            "Physician who performed the surgery (second entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_3: str = Field(
        default="",
        description=(
            "Name or description of past surgery (third entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_past_surgeries_3: str = Field(
        default="",
        description=(
            "Approximate date or age at time of surgery (third entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_past_surgeries_3: str = Field(
        default="",
        description=(
            "Physician who performed the surgery (third entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_4: str = Field(
        default="",
        description=(
            "Name or description of past surgery (fourth entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_past_surgeries_4: str = Field(
        default="",
        description=(
            "Approximate date or age at time of surgery (fourth entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_past_surgeries_4: str = Field(
        default="",
        description=(
            "Physician who performed the surgery (fourth entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_5: str = Field(
        default="",
        description=(
            "Name or description of past surgery (fifth entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_past_surgeries_5: str = Field(
        default="",
        description=(
            "Approximate date or age at time of surgery (fifth entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_past_surgeries_5: str = Field(
        default="",
        description=(
            "Physician who performed the surgery (fifth entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FamilyHistory(BaseModel):
    """Family medical history details"""

    bleeding_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with bleeding problems .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    diabetes_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with diabetes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    amputations_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) who have had amputations .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cancer_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with cancer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tuberculosis_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with tuberculosis .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    heart_disease_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with heart disease .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    strokes_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) who have had strokes .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    high_blood_pressure_family_history: str = Field(
        default="",
        description=(
            "Relationship of family member(s) with high blood pressure .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_family_history: str = Field(
        default="",
        description=(
            "Other significant family medical history and relationship .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SocialHistory(BaseModel):
    """Social, lifestyle, and pain management information"""

    employer: str = Field(
        default="",
        description=(
            'Name of current employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    job_description: str = Field(
        default="",
        description=(
            'Brief description of job duties .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    recreational_activities_exercise: str = Field(
        default="",
        description=(
            "Description of recreational activities and exercise routine .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    single: BooleanLike = Field(default="", description="Check if marital status is single")

    married: BooleanLike = Field(default="", description="Check if marital status is married")

    divorced: BooleanLike = Field(default="", description="Check if marital status is divorced")

    widow: BooleanLike = Field(default="", description="Check if marital status is widowed")

    no_living_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of living children"
    )

    no_of_pregnancies: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pregnancies"
    )

    do_you_smoke_y: BooleanLike = Field(
        default="", description="Indicate yes if you currently smoke"
    )

    do_you_smoke_n: BooleanLike = Field(
        default="", description="Indicate no if you do not currently smoke"
    )

    approx_amount_per_day_smoking: str = Field(
        default="",
        description=(
            "Approximate number of cigarettes or other tobacco products per day .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_ever_smoked: str = Field(
        default="",
        description=(
            "History of past smoking, including duration and quit date if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    do_you_drink_alcoholic_beverages_y: BooleanLike = Field(
        default="", description="Indicate yes if you currently drink alcoholic beverages"
    )

    do_you_drink_alcoholic_beverages_n: BooleanLike = Field(
        default="", description="Indicate no if you do not currently drink alcoholic beverages"
    )

    type_alcoholic_beverages: str = Field(
        default="",
        description=(
            "Type of alcoholic beverages consumed (e.g., beer, wine, liquor) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    approx_amount_alcoholic_beverages: str = Field(
        default="",
        description=(
            "Approximate quantity of alcohol consumed (include units and time period) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    alcoholic_beverages_frequency: Literal["Daily", "Weekly", "Monthly", "N/A", ""] = Field(
        default="", description="How often alcoholic beverages are consumed"
    )

    recreational_drugs: str = Field(
        default="",
        description=(
            'List any recreational drugs used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    do_you_vape_y: BooleanLike = Field(default="", description="Indicate yes if you currently vape")

    do_you_vape_n: BooleanLike = Field(
        default="", description="Indicate no if you do not currently vape"
    )

    frequency_vaping: str = Field(
        default="",
        description=(
            "How often you vape (e.g., times per day or week) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    see_pain_management_physician_yes: BooleanLike = Field(
        default="",
        description="Indicate yes if you are currently seeing a pain management physician",
    )

    see_pain_management_physician_no: BooleanLike = Field(
        default="", description="Indicate no if you are not seeing a pain management physician"
    )

    pain_management_physician_name: str = Field(
        default="",
        description=(
            "Name of your pain management physician, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pain_management_contract_yes: BooleanLike = Field(
        default="", description="Indicate yes if you have a formal pain management contract"
    )

    pain_management_contract_no: BooleanLike = Field(
        default="", description="Indicate no if you do not have a pain management contract"
    )

    surrogate_decision_maker_yes: BooleanLike = Field(
        default="", description="Indicate yes if you have designated a surrogate decision maker"
    )

    surrogate_decision_maker_no: BooleanLike = Field(
        default="", description="Indicate no if you have not designated a surrogate decision maker"
    )

    surrogate_decision_maker_name: str = Field(
        default="",
        description=(
            "Name of your surrogate decision maker, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SaraSuttleDpmPatientQuestionnaire(BaseModel):
    """Sara Suttle, D.P.M. - PATIENT QUESTIONNAIRE"""

    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    past_illnesses: PastIllnesses = Field(..., description="Past Illnesses")
    past_surgeries: PastSurgeries = Field(..., description="Past Surgeries")
    family_history: FamilyHistory = Field(..., description="Family History")
    social_history: SocialHistory = Field(..., description="Social History")

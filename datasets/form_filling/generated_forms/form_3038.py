from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicationRow(BaseModel):
    """Single row in Medication"""

    medication: str = Field(default="", description="Medication")
    strength: str = Field(default="", description="Strength")
    frequency: str = Field(default="", description="Frequency")
    approximate_date_started: str = Field(default="", description="Approximate_Date_Started")
    reason: str = Field(default="", description="Reason")


class ParticipantInformation(BaseModel):
    """Basic information about the adult participant"""

    full_name: str = Field(
        ...,
        description=(
            'Adult participant\'s full legal name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact: str = Field(
        ...,
        description=(
            "Primary emergency contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    troop: str = Field(
        ...,
        description=(
            'Trail Life USA troop number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Immunizations(BaseModel):
    """Immunization history and disease history for listed conditions"""

    immunization_yes: BooleanLike = Field(
        default="", description="Check yes if immunization has been received"
    )

    immunization_no: BooleanLike = Field(
        default="", description="Check no if immunization has not been received"
    )

    date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year the immunization was received (MM/YY) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had the disease"
    )

    have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had the disease"
    )

    date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when the disease occurred (MM/YY) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tetanus_immunization_yes: BooleanLike = Field(
        ..., description="Check yes if you have received a tetanus immunization"
    )

    tetanus_immunization_no: BooleanLike = Field(
        ..., description="Check no if you have not received a tetanus immunization"
    )

    tetanus_date_of_immunization_mm_yy: str = Field(
        ...,
        description=(
            "Month and year of most recent tetanus immunization (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tetanus_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had tetanus disease"
    )

    tetanus_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had tetanus disease"
    )

    tetanus_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when tetanus disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    pertussis_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a pertussis immunization"
    )

    pertussis_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a pertussis immunization"
    )

    pertussis_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent pertussis immunization (MM/YY) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pertussis_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had pertussis disease"
    )

    pertussis_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had pertussis disease"
    )

    pertussis_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when pertussis disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    diphtheria_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a diphtheria immunization"
    )

    diphtheria_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a diphtheria immunization"
    )

    diphtheria_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent diphtheria immunization (MM/YY) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    diphtheria_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had diphtheria disease"
    )

    diphtheria_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had diphtheria disease"
    )

    diphtheria_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when diphtheria disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    measles_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a measles immunization"
    )

    measles_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a measles immunization"
    )

    measles_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent measles immunization (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    measles_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had measles disease"
    )

    measles_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had measles disease"
    )

    measles_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when measles disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mumps_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a mumps immunization"
    )

    mumps_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a mumps immunization"
    )

    mumps_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent mumps immunization (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mumps_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had mumps disease"
    )

    mumps_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had mumps disease"
    )

    mumps_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when mumps disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    rubella_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a rubella immunization"
    )

    rubella_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a rubella immunization"
    )

    rubella_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent rubella immunization (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    rubella_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had rubella disease"
    )

    rubella_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had rubella disease"
    )

    rubella_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when rubella disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    polio_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a polio immunization"
    )

    polio_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a polio immunization"
    )

    polio_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent polio immunization (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    polio_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had polio disease"
    )

    polio_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had polio disease"
    )

    polio_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when polio disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    chicken_pox_immunization_yes: BooleanLike = Field(
        default="",
        description="Check yes if you have received a chicken pox (varicella) immunization",
    )

    chicken_pox_immunization_no: BooleanLike = Field(
        default="",
        description="Check no if you have not received a chicken pox (varicella) immunization",
    )

    chicken_pox_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent chicken pox (varicella) immunization (MM/YY) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    chicken_pox_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had chicken pox disease"
    )

    chicken_pox_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had chicken pox disease"
    )

    chicken_pox_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when chicken pox disease occurred (MM/YY), if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hepatitis_a_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a Hepatitis A immunization"
    )

    hepatitis_a_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a Hepatitis A immunization"
    )

    hepatitis_a_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent Hepatitis A immunization (MM/YY) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hepatitis_a_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had Hepatitis A disease"
    )

    hepatitis_a_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had Hepatitis A disease"
    )

    hepatitis_a_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when Hepatitis A disease occurred (MM/YY), if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hepatitis_b_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a Hepatitis B immunization"
    )

    hepatitis_b_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a Hepatitis B immunization"
    )

    hepatitis_b_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent Hepatitis B immunization (MM/YY) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hepatitis_b_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had Hepatitis B disease"
    )

    hepatitis_b_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had Hepatitis B disease"
    )

    hepatitis_b_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when Hepatitis B disease occurred (MM/YY), if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    meningitis_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received a meningitis immunization"
    )

    meningitis_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received a meningitis immunization"
    )

    meningitis_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent meningitis immunization (MM/YY) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    meningitis_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had meningitis disease"
    )

    meningitis_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had meningitis disease"
    )

    meningitis_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when meningitis disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    influenza_immunization_yes: BooleanLike = Field(
        default="", description="Check yes if you have received an influenza (flu) immunization"
    )

    influenza_immunization_no: BooleanLike = Field(
        default="", description="Check no if you have not received an influenza (flu) immunization"
    )

    influenza_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of most recent influenza (flu) immunization (MM/YY) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    influenza_have_had_the_disease_yes: BooleanLike = Field(
        default="", description="Check yes if you have had influenza disease"
    )

    influenza_have_had_the_disease_no: BooleanLike = Field(
        default="", description="Check no if you have not had influenza disease"
    )

    influenza_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when influenza disease occurred (MM/YY), if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_i_e_hib_immunization_yes: BooleanLike = Field(
        default="", description="For other immunizations (e.g., HIB), check yes if received"
    )

    other_i_e_hib_immunization_no: BooleanLike = Field(
        default="", description="For other immunizations (e.g., HIB), check no if not received"
    )

    other_i_e_hib_date_of_immunization_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of other immunization (e.g., HIB) (MM/YY) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_i_e_hib_have_had_the_disease_yes: BooleanLike = Field(
        default="",
        description="For other diseases (e.g., HIB), check yes if you have had the disease",
    )

    other_i_e_hib_have_had_the_disease_no: BooleanLike = Field(
        default="",
        description="For other diseases (e.g., HIB), check no if you have not had the disease",
    )

    other_i_e_hib_date_of_disease_mm_yy: str = Field(
        default="",
        description=(
            "Month and year when other disease (e.g., HIB) occurred (MM/YY), if applicable "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    exception_to_immunizations_claimed_form_required: str = Field(
        default="",
        description=(
            "Describe any claimed exception to recommended immunizations; attach required "
            'form .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Medications(BaseModel):
    """Current medications and authorization"""

    medication: List[MedicationRow] = Field(
        default="",
        description="List all medications currently used, including inhalers and EpiPens",
    )  # List of table rows

    strength: str = Field(
        default="",
        description=(
            "Strength or dosage of the medication (e.g., 10 mg) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    frequency: str = Field(
        default="",
        description=(
            "How often the medication is taken (e.g., twice daily) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approximate_date_started: str = Field(
        default="",
        description=(
            "Approximate date when the medication was started .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason: str = Field(
        default="",
        description=(
            "Reason or condition for which the medication is taken .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    administration_of_the_above_medications_is_approved_by_if_required_by_your_state: str = Field(
        default="",
        description=(
            "Name or signature of person/authority approving administration of listed "
            'medications, if required by state law .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    adult_participant_signature: str = Field(
        ...,
        description=(
            'Signature of the adult participant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class TrailLifeUsaAdultMemberparticipantHealthMedicalForm(BaseModel):
    """
    Trail Life USA | Adult Member/Participant Health & Medical Form

    The following immunizations are recommended. **Tetanus immunization is required and must have been received within the last 10 years.** For each item, indicate if you have been immunized, the date of the immunization (MM/YY), if you have had the disease, and the date (MM/YY).
    List all medications currently used. (If additional space is needed, please photocopy this part of the health form.) Inhalers and EpiPen information must be included, even if they are for occasional or emergency use only. If none, please write "None" below.
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    immunizations: Immunizations = Field(..., description="Immunizations")
    medications: Medications = Field(..., description="Medications")

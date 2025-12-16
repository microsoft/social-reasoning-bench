from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OwnerPatientInformation(BaseModel):
    """Basic contact information and reason for today's visit"""

    owners_name: str = Field(
        ...,
        description=(
            'Full name of the pet’s owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    pets_name: str = Field(
        ...,
        description=(
            'Name of the pet being seen today .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Best phone number to reach the owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_visit_today: str = Field(
        ...,
        description=(
            "Primary reason or concern for today’s visit .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    if_sick_for_how_long: str = Field(
        default="",
        description=(
            "Duration of illness if the pet is sick .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DietFeeding(BaseModel):
    """Information about the pet's normal diet and feeding schedule"""

    pets_normal_diet_prescription: BooleanLike = Field(
        default="", description="Check if the pet normally eats a prescription diet"
    )

    pets_normal_diet_commercial: BooleanLike = Field(
        default="", description="Check if the pet normally eats a commercial diet"
    )

    pets_normal_diet_table_scraps: BooleanLike = Field(
        default="", description="Check if the pet regularly receives table scraps"
    )

    meals_per_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of meals the pet eats per day"
    )

    last_time_pet_ate: str = Field(
        default="",
        description=(
            "Approximate time of the pet’s last meal .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistorySymptoms(BaseModel):
    """Yes/No questions about current symptoms, medical history, and recent changes"""

    recent_injury_or_surgery_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has had a recent injury or surgery"
    )

    recent_injury_or_surgery_no: BooleanLike = Field(
        default="", description="Indicate No if the pet has not had a recent injury or surgery"
    )

    current_medications_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet is currently on any medications"
    )

    current_medications_no: BooleanLike = Field(
        default="", description="Indicate No if the pet is not on any medications"
    )

    any_known_allergies_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has any known allergies"
    )

    any_known_allergies_no: BooleanLike = Field(
        default="", description="Indicate No if the pet has no known allergies"
    )

    vomiting_and_or_diarrhea_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has vomiting and/or diarrhea"
    )

    vomiting_and_or_diarrhea_no: BooleanLike = Field(
        default="", description="Indicate No if the pet does not have vomiting or diarrhea"
    )

    urinating_more_or_less_than_usual_yes: BooleanLike = Field(
        default="", description="Indicate Yes if urination frequency or volume has changed"
    )

    urinating_more_or_less_than_usual_no: BooleanLike = Field(
        default="", description="Indicate No if urination is normal"
    )

    bowel_abnormalities_yes: BooleanLike = Field(
        default="", description="Indicate Yes if there are any bowel movement abnormalities"
    )

    bowel_abnormalities_no: BooleanLike = Field(
        default="", description="Indicate No if bowel movements are normal"
    )

    lack_of_energy_and_or_weakness_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet shows lack of energy or weakness"
    )

    lack_of_energy_and_or_weakness_no: BooleanLike = Field(
        default="", description="Indicate No if the pet’s energy level is normal"
    )

    drinking_more_or_less_than_usual_yes: BooleanLike = Field(
        default="", description="Indicate Yes if water intake has increased or decreased"
    )

    drinking_more_or_less_than_usual_no: BooleanLike = Field(
        default="", description="Indicate No if water intake is normal"
    )

    limping_which_leg_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet is limping; specify which leg in details"
    )

    limping_which_leg_no: BooleanLike = Field(
        default="", description="Indicate No if the pet is not limping"
    )

    coughing_sneezing_or_gagging_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet is coughing, sneezing, or gagging"
    )

    coughing_sneezing_or_gagging_no: BooleanLike = Field(
        default="", description="Indicate No if the pet is not coughing, sneezing, or gagging"
    )

    scratching_and_or_chewing_at_skin_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet is scratching or chewing at its skin"
    )

    scratching_and_or_chewing_at_skin_no: BooleanLike = Field(
        default="", description="Indicate No if the pet is not scratching or chewing at its skin"
    )

    history_of_seizures_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has a history of seizures"
    )

    history_of_seizures_no: BooleanLike = Field(
        default="", description="Indicate No if the pet has no history of seizures"
    )

    any_lumps_or_bumps_on_body_where_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate Yes if there are any lumps or bumps; location can be detailed separately"
        ),
    )

    any_lumps_or_bumps_on_body_where_no: BooleanLike = Field(
        default="", description="Indicate No if there are no lumps or bumps on the body"
    )

    weight_loss_or_gain_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has had noticeable weight loss or gain"
    )

    weight_loss_or_gain_no: BooleanLike = Field(
        default="", description="Indicate No if the pet’s weight is stable"
    )

    appetite_increase_or_decrease_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet’s appetite has increased or decreased"
    )

    appetite_increase_or_decrease_no: BooleanLike = Field(
        default="", description="Indicate No if the pet’s appetite is normal"
    )

    bad_breath_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has noticeably bad breath"
    )

    bad_breath_no: BooleanLike = Field(
        default="", description="Indicate No if the pet does not have bad breath"
    )

    behavioral_changes_yes: BooleanLike = Field(
        default="", description="Indicate Yes if there have been any behavioral changes"
    )

    behavioral_changes_no: BooleanLike = Field(
        default="", description="Indicate No if there are no behavioral changes"
    )

    heartworm_preventative_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet is on heartworm preventative"
    )

    heartworm_preventative_no: BooleanLike = Field(
        default="", description="Indicate No if the pet is not on heartworm preventative"
    )

    date_of_last_dose: str = Field(
        default="",
        description=(
            "Date the last heartworm preventative dose was given .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    eye_ear_nose_or_mouth_discharge_yes: BooleanLike = Field(
        default="",
        description="Indicate Yes if there is any discharge from eyes, ears, nose, or mouth",
    )

    eye_ear_nose_or_mouth_discharge_no: BooleanLike = Field(
        default="",
        description="Indicate No if there is no discharge from eyes, ears, nose, or mouth",
    )

    any_scooting_on_rear_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the pet has been scooting on its rear"
    )

    any_scooting_on_rear_no: BooleanLike = Field(
        default="", description="Indicate No if the pet has not been scooting on its rear"
    )


class Authorization(BaseModel):
    """Owner's signature and date of authorization"""

    owners_signature: str = Field(
        ...,
        description=(
            "Signature of the owner authorizing care; may be electronic using /Firstname "
            'Lastname/ .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class HealingPawsVeterinaryHospitalPatientDropoffMedicalInformation(BaseModel):
    """
        HEALING PAWS
    VETERINARY HOSPITAL

    PATIENT DROP-OFF MEDICAL INFORMATION

        Please fill out, print and bring this form in with you.
    """

    owner__patient_information: OwnerPatientInformation = Field(
        ..., description="Owner & Patient Information"
    )
    diet__feeding: DietFeeding = Field(..., description="Diet & Feeding")
    medical_history__symptoms: MedicalHistorySymptoms = Field(
        ..., description="Medical History & Symptoms"
    )
    authorization: Authorization = Field(..., description="Authorization")

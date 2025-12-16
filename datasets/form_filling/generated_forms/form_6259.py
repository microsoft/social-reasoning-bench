from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChildandSponsorInformation(BaseModel):
    """Basic identifying information for the child and sponsor"""

    childs_name_last_first_middle: str = Field(
        ...,
        description=(
            "Child’s full legal name in Last, First, Middle format .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    sex: str = Field(
        ...,
        description=(
            "Child’s sex as listed on official records .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    birthdate_mm_dd_yyyy: str = Field(
        ..., description="Child’s date of birth in MM/DD/YYYY format"
    )  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Child’s age in years")

    sponsors_name_last_first_middle: str = Field(
        ...,
        description=(
            "Sponsor’s full name in Last, First, Middle format .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartAIdentificationofChildYouthMedicalandorDietaryNeeds(BaseModel):
    """Information about the child’s medical needs, allergies, and dietary restrictions"""

    medical_needs_assistance_yes: BooleanLike = Field(
        ..., description="Check if the child has medical needs requiring assistance while in care"
    )

    medical_needs_assistance_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the child does not have medical needs requiring assistance while in care"
        ),
    )

    asthma: BooleanLike = Field(
        default="", description="Check if the child has asthma requiring assistance while in care"
    )

    diabetes: BooleanLike = Field(
        default="", description="Check if the child has diabetes requiring assistance while in care"
    )

    kidney_problems: BooleanLike = Field(
        default="",
        description="Check if the child has kidney problems requiring assistance while in care",
    )

    seizures: BooleanLike = Field(
        default="", description="Check if the child has seizures requiring assistance while in care"
    )

    heart_problems: BooleanLike = Field(
        default="",
        description="Check if the child has heart problems requiring assistance while in care",
    )

    other_chronic_medical_needs: BooleanLike = Field(
        default="", description="Check if the child has other chronic medical needs not listed"
    )

    physical_disability: BooleanLike = Field(
        default="", description="Check if the child has a physical disability"
    )

    epilepsy: BooleanLike = Field(default="", description="Check if the child has epilepsy")

    describe_chronic_medical_needs_or_physical_disability: str = Field(
        default="",
        description=(
            "Description of the child’s other chronic medical needs or physical disability "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    other_allergies_yes: BooleanLike = Field(
        default="", description="Check if the child has other allergies or allergic reactions"
    )

    other_allergies_no: BooleanLike = Field(
        default="",
        description="Check if the child does not have other allergies or allergic reactions",
    )

    list_other_allergies: str = Field(
        default="",
        description=(
            "List of other allergies or allergic reactions the child has .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    food_allergies_yes: BooleanLike = Field(
        default="", description="Check if the child has any food allergies"
    )

    food_allergies_no: BooleanLike = Field(
        default="", description="Check if the child does not have any food allergies"
    )

    list_food_allergies_and_reactions: str = Field(
        default="",
        description=(
            "List of food allergies and the reaction the child has to each food .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    epipen_required_yes: BooleanLike = Field(
        default="", description="Check if the child requires an EpiPen"
    )

    epipen_required_no: BooleanLike = Field(
        default="", description="Check if the child does not require an EpiPen"
    )

    describe_when_epipen_needed: str = Field(
        default="",
        description=(
            "Description of situations when the child might need an EpiPen .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    food_intolerances_yes: BooleanLike = Field(
        default="", description="Check if the child has food intolerances requiring substitutions"
    )

    food_intolerances_no: BooleanLike = Field(
        default="",
        description="Check if the child does not have food intolerances requiring substitutions",
    )

    describe_food_intolerances: str = Field(
        default="",
        description=(
            "Description of the child’s food intolerances and needed substitutions .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PartBIdentificationofMedicationNeeds(BaseModel):
    """Information about current medications and medications needed while in care"""

    currently_taking_medication_yes: BooleanLike = Field(
        default="", description="Check if the child is currently taking any medication"
    )

    currently_taking_medication_no: BooleanLike = Field(
        default="", description="Check if the child is not currently taking any medication"
    )

    list_current_medications_and_frequency: str = Field(
        default="",
        description=(
            "List of current medications and how often the child takes each .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    medication_needed_in_care_yes: BooleanLike = Field(
        default="", description="Check if the child will need to take medication while in CYP care"
    )

    medication_needed_in_care_no: BooleanLike = Field(
        default="",
        description="Check if the child will not need to take medication while in CYP care",
    )

    list_medications_needed_in_care: str = Field(
        default="",
        description=(
            "List of medications the child will need to take while in CYP care .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NavyChildAndYouthProgramHealthInformationForm170052(BaseModel):
    """
        NAVY CHILD AND YOUTH PROGRAM
    HEALTH INFORMATION FORM 1700/52

        ''
    """

    child_and_sponsor_information: ChildandSponsorInformation = Field(
        ..., description="Child and Sponsor Information"
    )
    part_a_identification_of_childyouth_medical_andor_dietary_needs: PartAIdentificationofChildYouthMedicalandorDietaryNeeds = Field(
        ..., description="Part A: Identification of Child/Youth Medical and/or Dietary Needs"
    )
    part_b_identification_of_medication_needs: PartBIdentificationofMedicationNeeds = Field(
        ..., description="Part B: Identification of Medication Needs"
    )

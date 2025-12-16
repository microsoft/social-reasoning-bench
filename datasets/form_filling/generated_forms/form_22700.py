from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WellnessPrograms(BaseModel):
    """Information about company wellness programs offered to employees"""

    does_your_company_offer_wellness_programs_for_your_employees_yes: BooleanLike = Field(
        default="", description="Select if the company offers wellness programs for employees."
    )

    does_your_company_offer_wellness_programs_for_your_employees_no: BooleanLike = Field(
        default="",
        description="Select if the company does not offer wellness programs for employees.",
    )

    drug_alcohol_screenings: BooleanLike = Field(
        default="",
        description="Check if drug or alcohol screenings are part of the wellness programs offered.",
    )

    on_site_flu_shots: BooleanLike = Field(
        default="",
        description="Check if on-site flu shots are part of the wellness programs offered.",
    )

    preventive_safety_classes: BooleanLike = Field(
        default="",
        description="Check if preventive safety classes are part of the wellness programs offered.",
    )

    blood_glucose_screenings: BooleanLike = Field(
        default="",
        description="Check if blood glucose screenings are part of the wellness programs offered.",
    )

    blood_pressure_checks: BooleanLike = Field(
        default="",
        description="Check if blood pressure checks are part of the wellness programs offered.",
    )

    smoking_cessation_programs: BooleanLike = Field(
        default="",
        description="Check if smoking cessation programs are part of the wellness programs offered.",
    )

    other: str = Field(
        default="",
        description=(
            "Describe any other wellness programs offered that are not listed. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CoordinationofCare(BaseModel):
    """Specialty providers and facilities requiring coordination of care"""

    providers_facilities_coordination_of_care_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if any prospective enrollees are being treated by specialty providers "
            "or facilities requiring coordination of care."
        ),
    )

    providers_facilities_coordination_of_care_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no prospective enrollees are being treated by specialty providers or "
            "facilities requiring coordination of care."
        ),
    )

    providers_facilities_requiring_coordination_of_care: str = Field(
        default="",
        description=(
            "List specialty providers and/or facilities that require coordination of care. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SpecialtyMedications(BaseModel):
    """Specialty medications that may require prior authorization"""

    specialty_medications_prior_auth_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if any specialty medications used by prospective enrollees would "
            "require prior authorization."
        ),
    )

    specialty_medications_prior_auth_no: BooleanLike = Field(
        default="",
        description=(
            "Select if you are not aware of any specialty medications requiring prior "
            "authorization."
        ),
    )

    specialty_medications_requiring_prior_authorization: str = Field(
        default="",
        description=(
            "List any specialty medications that would require prior authorization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class COBRACoverage(BaseModel):
    """Information about prospective enrollees on COBRA continuation coverage"""

    cobra_continuation_coverage_yes: BooleanLike = Field(
        default="",
        description="Select if there are prospective enrollees on COBRA continuation coverage.",
    )

    cobra_continuation_coverage_no: BooleanLike = Field(
        default="",
        description="Select if there are no prospective enrollees on COBRA continuation coverage.",
    )

    cobra_enrollees_count: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Enter the number of prospective enrollees on COBRA continuation coverage.",
    )


class FormCompletionDetails(BaseModel):
    """Information about the individual and company completing the form"""

    name_of_individual_completing_form: str = Field(
        ...,
        description=(
            "Full name of the person completing this form. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Job title or role of the individual completing the form. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the individual completing the form. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_company: str = Field(
        ...,
        description=(
            'Legal name of the company. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is completed.")  # YYYY-MM-DD format


class TransitionOfCareQuestionnaire(BaseModel):
    """
    Transition of Care Questionnaire

    Please answer each question, to the best of your knowledge to ensure a smooth transition of care for all prospective enrollees, including: owners, employees, spouses, dependent children, domestic partners and COBRA participants. This form is elective.
    """

    wellness_programs: WellnessPrograms = Field(..., description="Wellness Programs")
    coordination_of_care: CoordinationofCare = Field(..., description="Coordination of Care")
    specialty_medications: SpecialtyMedications = Field(..., description="Specialty Medications")
    cobra_coverage: COBRACoverage = Field(..., description="COBRA Coverage")
    form_completion_details: FormCompletionDetails = Field(
        ..., description="Form Completion Details"
    )

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ESRDDialysisRelatedUse(BaseModel):
    """Determination of whether the drug is being used for an ESRD/Dialysis-related condition"""

    esrd_dialysis_related_condition_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if the requested drug is being used to treat an ESRD/dialysis-related "
            "condition in a patient diagnosed with ESRD who currently requires dialysis."
        ),
    )

    esrd_dialysis_related_condition_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the requested drug is NOT being used to treat an "
            "ESRD/dialysis-related condition in a patient diagnosed with ESRD who currently "
            "requires dialysis."
        ),
    )


class PartDCoverageDeterminationCriteria(BaseModel):
    """Diagnosis and clinical criteria required for Medicare Part D coverage determination"""

    indicate_diagnosis: str = Field(
        ...,
        description=(
            "Primary diagnosis or condition for which the drug is being prescribed. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    icd_10_codes: str = Field(
        ...,
        description=(
            "ICD-10 diagnosis code or codes corresponding to the condition being treated. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    aranesp_tried_failed_epoetin: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether, for ARANESP requests, the patient has previously tried and "
            "failed or was intolerant to epoetin alfa (EPOGEN or PROCRIT)."
        ),
    )


class AdditionalClinicalInformation(BaseModel):
    """Other comments, diagnoses, symptoms, and pertinent information for review"""

    other_comments_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if there are additional comments, diagnoses, symptoms, medications "
            "tried/failed, or other pertinent information to provide."
        ),
    )

    other_comments_no: BooleanLike = Field(
        default="",
        description=(
            "Select if there are no additional comments, diagnoses, symptoms, medications "
            "tried/failed, or other pertinent information to provide."
        ),
    )

    other_comments_explain_line_1: str = Field(
        default="",
        description=(
            "First line of explanation for any additional comments, diagnoses, symptoms, "
            "medications tried/failed, or other pertinent information. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_comments_explain_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation for any additional comments, diagnoses, symptoms, "
            "medications tried/failed, or other pertinent information. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_comments_explain_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation for any additional comments, diagnoses, symptoms, "
            "medications tried/failed, or other pertinent information. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ExceptionRequests(BaseModel):
    """Requests to waive one or more prior authorization requirements"""

    exception_request_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the prescriber is requesting that one or more prior authorization "
            "requirements be waived."
        ),
    )

    exception_request_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the prescriber is NOT requesting that any prior authorization "
            "requirements be waived."
        ),
    )

    exception_medical_reason_statement: str = Field(
        default="",
        description=(
            "Narrative explanation of the medical reason why the requested exception to "
            "prior authorization requirements should be approved. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ClinicalJustificationforTherapyChoice(BaseModel):
    """Rationale for selecting this medication and risks of changing current regimen"""

    most_effective_option_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if this medication is believed to be the most effective option for the patient."
        ),
    )

    most_effective_option_no: BooleanLike = Field(
        default="",
        description=(
            "Select if this medication is NOT believed to be the most effective option for "
            "the patient."
        ),
    )

    most_effective_explain_line_1: str = Field(
        default="",
        description=(
            "First line of explanation for why this medication is likely the most effective "
            'option. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    most_effective_explain_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation for why this medication is likely the most "
            'effective option. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    most_effective_explain_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation for why this medication is likely the most effective "
            'option. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    regimen_change_adverse_effects_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if changing the current medication regimen is likely to result in "
            "adverse effects for the patient."
        ),
    )

    regimen_change_adverse_effects_no: BooleanLike = Field(
        default="",
        description=(
            "Select if changing the current medication regimen is NOT likely to result in "
            "adverse effects for the patient."
        ),
    )

    regimen_change_explain_line_1: str = Field(
        default="",
        description=(
            "First line of explanation for why changing the current regimen would likely "
            'result in adverse effects. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    regimen_change_explain_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation for why changing the current regimen would likely "
            'result in adverse effects. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    regimen_change_explain_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation for why changing the current regimen would likely "
            'result in adverse effects. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class BvdesrddialysisrelatedDrugs2018(BaseModel):
    """
    BvD_ESRD/Dialysis-Related Drugs_2018

    Anemia management: Drugs used to treat anemia in a patient diagnosed with ESRD who currently requires dialysis. This category includes epoetin alfa inj. (EPOGEN, PROCRIT) and darbepoetin alfa inj (ARANESP).
    Antiemetic; Anti-infective (including antibacterial and antifungal drugs); Antipruritic; Anxiolytic; Excess fluid management; Fluid and electrolyte management (including volume expanders) and Pain management: Drugs in these categories may be considered ESRD-related if they are prescribed for conditions that arise secondary to dialysis treatment.
    Part D Coverage Determination Criteria (required): The following requirements need to be met before this drug can be covered by the Part D plan. These requirements have been approved by the Centers for Medicare and Medicaid Services (CMS), but you may ask us for an exception if you believe one or more of these requirements should be waived.
    Please Note: This drug is only covered under Medicare Part D when it is used for a medically accepted indication. A medically accepted indication is a use of the drug that is either:
    Approved by the Food and Drug Administration (FDA) – that is, that the FDA has approved the drug for the diagnosis or condition for which it is being prescribed – or supported by any of the following reference books: American Hospital Formulary Service Drug Information, the DRUGDEX Information System, and/or the USPDI or its successor.
    This drug requires the following prior authorization criteria be met in order to be covered under the Part D plan: FOR ARANESP ONLY: Patient has tried and failed or was intolerant to: epoetin alfa (EPOGEN or PROCRIT).
    """

    esrddialysis_related_use: ESRDDialysisRelatedUse = Field(
        ..., description="ESRD/Dialysis-Related Use"
    )
    part_d_coverage_determination_criteria: PartDCoverageDeterminationCriteria = Field(
        ..., description="Part D Coverage Determination Criteria"
    )
    additional_clinical_information: AdditionalClinicalInformation = Field(
        ..., description="Additional Clinical Information"
    )
    exception_requests: ExceptionRequests = Field(..., description="Exception Requests")
    clinical_justification_for_therapy_choice: ClinicalJustificationforTherapyChoice = Field(
        ..., description="Clinical Justification for Therapy Choice"
    )

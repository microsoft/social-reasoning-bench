from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AdditionalInformation(BaseModel):
    """Mental health conditions and whether they are long-term, recent, or primary concerns"""

    more_than_6_months_ptsd_abuse_or_trauma: BooleanLike = Field(
        default="",
        description="Indicate if PTSD, abuse or trauma has been present for more than 6 months.",
    )

    last_6_months_ptsd_abuse_or_trauma: BooleanLike = Field(
        default="",
        description="Indicate if PTSD, abuse or trauma has been present in the last 6 months.",
    )

    primary_concern_ptsd_abuse_or_trauma: BooleanLike = Field(
        default="",
        description="Check if PTSD, abuse or trauma is the primary mental health concern.",
    )

    more_than_6_months_anxiety: BooleanLike = Field(
        default="", description="Indicate if anxiety has been present for more than 6 months."
    )

    last_6_months_anxiety: BooleanLike = Field(
        default="", description="Indicate if anxiety has been present in the last 6 months."
    )

    primary_concern_anxiety: BooleanLike = Field(
        default="", description="Check if anxiety is the primary mental health concern."
    )

    more_than_6_months_depression: BooleanLike = Field(
        default="", description="Indicate if depression has been present for more than 6 months."
    )

    last_6_months_depression: BooleanLike = Field(
        default="", description="Indicate if depression has been present in the last 6 months."
    )

    primary_concern_depression: BooleanLike = Field(
        default="", description="Check if depression is the primary mental health concern."
    )

    more_than_6_months_bipolar: BooleanLike = Field(
        default="",
        description="Indicate if bipolar disorder has been present for more than 6 months.",
    )

    last_6_months_bipolar: BooleanLike = Field(
        default="",
        description="Indicate if bipolar disorder has been present in the last 6 months.",
    )

    primary_concern_bipolar: BooleanLike = Field(
        default="", description="Check if bipolar disorder is the primary mental health concern."
    )

    more_than_6_months_addiction: BooleanLike = Field(
        default="", description="Indicate if addiction has been present for more than 6 months."
    )

    last_6_months_addiction: BooleanLike = Field(
        default="", description="Indicate if addiction has been present in the last 6 months."
    )

    primary_concern_addiction: BooleanLike = Field(
        default="", description="Check if addiction is the primary mental health concern."
    )

    more_than_6_months_chronic_pain: BooleanLike = Field(
        default="", description="Indicate if chronic pain has been present for more than 6 months."
    )

    last_6_months_chronic_pain: BooleanLike = Field(
        default="", description="Indicate if chronic pain has been present in the last 6 months."
    )

    primary_concern_chronic_pain: BooleanLike = Field(
        default="", description="Check if chronic pain is the primary concern."
    )

    more_than_6_months_cognitive_disorder: BooleanLike = Field(
        default="",
        description="Indicate if a cognitive disorder has been present for more than 6 months.",
    )

    last_6_months_cognitive_disorder: BooleanLike = Field(
        default="",
        description="Indicate if a cognitive disorder has been present in the last 6 months.",
    )

    primary_concern_cognitive_disorder: BooleanLike = Field(
        default="", description="Check if a cognitive disorder is the primary concern."
    )

    more_than_6_months_ocd: BooleanLike = Field(
        default="", description="Indicate if OCD has been present for more than 6 months."
    )

    last_6_months_ocd: BooleanLike = Field(
        default="", description="Indicate if OCD has been present in the last 6 months."
    )

    primary_concern_ocd: BooleanLike = Field(
        default="", description="Check if OCD is the primary concern."
    )

    more_than_6_months_personality_disorder: BooleanLike = Field(
        default="",
        description="Indicate if a personality disorder has been present for more than 6 months.",
    )

    last_6_months_personality_disorder: BooleanLike = Field(
        default="",
        description="Indicate if a personality disorder has been present in the last 6 months.",
    )

    primary_concern_personality_disorder: BooleanLike = Field(
        default="", description="Check if a personality disorder is the primary concern."
    )

    more_than_6_months_other_condition: BooleanLike = Field(
        default="",
        description=(
            "For any other condition, indicate if it has been present for more than 6 months."
        ),
    )

    last_6_months_other_condition: BooleanLike = Field(
        default="",
        description="For any other condition, indicate if it has been present in the last 6 months.",
    )

    primary_concern_other_condition: BooleanLike = Field(
        default="", description="For any other condition, check if it is the primary concern."
    )

    other_condition_description: str = Field(
        default="",
        description=(
            "Describe any other condition not listed. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CurrentRiskAssessment(BaseModel):
    """Current and historical risk factors related to self-harm or harm to others"""

    current_active_suicidal_thoughts: BooleanLike = Field(
        default="", description="Check if the client currently has active suicidal thoughts."
    )

    current_thoughts_of_harm_to_others: BooleanLike = Field(
        default="", description="Check if the client currently has thoughts of harming others."
    )

    current_passive_suicidal_thoughts: BooleanLike = Field(
        default="", description="Check if the client currently has passive suicidal thoughts."
    )

    history_of_violence_towards_self_self_harm: BooleanLike = Field(
        default="", description="Check if there is a history of self-harm or violence towards self."
    )

    history_of_suicide_attempts: BooleanLike = Field(
        default="", description="Check if there is a history of suicide attempts."
    )

    history_of_violence_toward_others: BooleanLike = Field(
        default="", description="Check if there is a history of violence toward others."
    )

    date_of_last_attempt: str = Field(
        default="",
        description="Enter the date of the client's most recent suicide attempt, if any.",
    )  # YYYY-MM-DD format

    additional_details_regarding_current_risk_assessment: str = Field(
        default="",
        description=(
            "Provide any additional information related to the current risk assessment. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class HistoryofAddictionSubstanceUse(BaseModel):
    """Substance use history and related details"""

    is_the_client_currently_free_of_substance_use_yes: BooleanLike = Field(
        ..., description="Select if the client is currently free of substance use."
    )

    is_the_client_currently_free_of_substance_use_no: BooleanLike = Field(
        ..., description="Select if the client is not currently free of substance use."
    )

    history_of_any_drug_or_alcohol_substance_use_yes: BooleanLike = Field(
        ..., description="Select if the client has any history of drug, alcohol, or substance use."
    )

    history_of_any_drug_or_alcohol_substance_use_no: BooleanLike = Field(
        ..., description="Select if the client has no history of drug, alcohol, or substance use."
    )

    if_yes_type_of_substance_length_of_use_and_treatment: str = Field(
        default="",
        description=(
            "If there is a history of substance use, describe the substances, duration of "
            'use, and any treatment received. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    does_the_client_use_medical_marijuana_yes: BooleanLike = Field(
        default="", description="Select if the client currently uses medical marijuana."
    )

    does_the_client_use_medical_marijuana_no: BooleanLike = Field(
        default="", description="Select if the client does not use medical marijuana."
    )

    does_the_client_use_prescribed_narcotics_yes: BooleanLike = Field(
        default="", description="Select if the client currently uses prescribed narcotics."
    )

    does_the_client_use_prescribed_narcotics_no: BooleanLike = Field(
        default="", description="Select if the client does not use prescribed narcotics."
    )


class RequiredDocuments(BaseModel):
    """Documents that must be attached with the referral"""

    funding_approval_confirmation_attached: BooleanLike = Field(
        ..., description="Check if funding approval confirmation is attached to the referral."
    )

    medical_background_documents_attached_including_diagnosis: BooleanLike = Field(
        ...,
        description="Check if medical and background documents, including diagnosis, are attached.",
    )

    current_medication_list_attached: BooleanLike = Field(
        ...,
        description=(
            "Check if a current medication list (name, dosage, frequency, reason) is attached."
        ),
    )

    other_required_document_description: str = Field(
        default="",
        description=(
            'Describe any other attached document. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class NotesandSignature(BaseModel):
    """Additional notes and referring provider authorization"""

    notes: str = Field(
        default="",
        description=(
            "Additional notes or comments regarding the referral. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referring_agency_or_care_provider_signature: str = Field(
        ...,
        description=(
            "Signature of the referring agency representative or care provider. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    referring_agency_or_care_provider_signature_date: str = Field(
        ...,
        description="Date the referral form was signed by the referring agency or care provider.",
    )  # YYYY-MM-DD format


class DiversifiedRehabilitationGroupMentalHealthProgramsReferralForm(BaseModel):
    """
        Diversified
    REHABILITATION GROUP

    Mental Health Programs Referral Form

        In order to be considered for our mental health programs, the client MUST be free of any substance use for a minimum of 30 days prior to admission (case by case basis).
    """

    additional_information: AdditionalInformation = Field(..., description="Additional Information")
    current_risk_assessment: CurrentRiskAssessment = Field(
        ..., description="Current Risk Assessment"
    )
    history_of_addictionsubstance_use: HistoryofAddictionSubstanceUse = Field(
        ..., description="History of Addiction/Substance Use"
    )
    required_documents: RequiredDocuments = Field(..., description="Required Documents")
    notes_and_signature: NotesandSignature = Field(..., description="Notes and Signature")

from pydantic import BaseModel, ConfigDict, Field


class OmniSeqCaresFinancialSupportApplication(BaseModel):
    """OmniSeq CARES – Financial Support Application

    Patients who have been invoiced by OmniSeq, Inc. submit this application to request
    financial support or reduced payment based on household income and financial circumstances.
    OmniSeq CARES program representatives review the patient and (if applicable) responsible
    party identifying details and financial information to determine eligibility and decide
    what assistance can be offered and how the account should be handled.
    """

    model_config = ConfigDict(extra="forbid")

    patient_info_account_number: str = Field(
        ...,
        description='Account # from statement. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_info_ordering_physician_practice: str = Field(
        ...,
        description='Ordering physician/practice. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    responsible_party_info_home_phone_number: str = Field(
        ...,
        description='Responsible party home phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    financial_info_total_earned_annual_gross_household_income: float | None = Field(
        ...,
        description="Total earned annual gross household income",
    )
    financial_info_unemployment_income: float | None = Field(
        ...,
        description="Unemployment income",
    )
    financial_info_additional_income_specify: str = Field(
        ...,
        description='Additional income description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    financial_info_other_health_care_expenses: str = Field(
        ...,
        description='Other health care expenses details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
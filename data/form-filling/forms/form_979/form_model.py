from pydantic import BaseModel, ConfigDict, Field


class IroIndependentReviewRequestForm(BaseModel):
    """Request Form - Request for a Review by an Independent Review Organization

    A patient, injured employee, provider, or authorized representative submits this form to the insurer/health plan or workers’ compensation carrier to request an Independent Review Organization (IRO) review of a denial of health care services (and certain prescription-related denials). The carrier and the IRO use the details here to identify the claim, determine the requester’s standing and the type/urgency of review (including court-ordered status), and to understand exactly what services were denied so the denial can be evaluated.
    """

    model_config = ConfigDict(extra="forbid")






    denied_services_description: str = Field(
        ...,
        description='Denied services description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    patient_claim_identification_number: str = Field(
        ...,
        description='Health plan or claim ID number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    patient_sex: str = Field(
        ...,
        description='Patient sex. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    patient_phone_number: str = Field(
        ...,
        description='Patient phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_fax_area_code: str = Field(
        ...,
        description='Patient fax area code. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_fax_number: str = Field(
        ...,
        description='Patient fax number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

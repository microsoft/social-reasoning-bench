from pydantic import BaseModel, ConfigDict, Field


class KrystexxaPegloticaseOrderForm(BaseModel):
    """KRYSTEXXA® (PEGLOTICASE) ORDER FORM

    Prescribing clinicians submit this referral/order form to the Allergy, Asthma & Immunology Center, P.C. Infusion Services team to start, renew, change, or discontinue KRYSTEXXA (pegloticase) IV infusion therapy. Infusion staff and benefits verification/pharmacy personnel use the patient/physician details, diagnosis, documentation checklist, and lab orders to determine scheduling readiness, protocol requirements, and insurance authorization/benefits verification actions.
    """

    model_config = ConfigDict(extra="forbid")


    patient_dob: str = Field(
        ...,
        description='Patient date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_address: str = Field(
        ...,
        description='Patient address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_phone: str = Field(
        ...,
        description='Patient phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    patient_allergies: str = Field(
        ...,
        description='Patient allergies. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    physician_fax: str = Field(
        ...,
        description='Physician fax. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    order_date: str = Field(
        ...,
        description='Order date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )





    notes_additional_comments: str = Field(
        ...,
        description='Notes/additional comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
